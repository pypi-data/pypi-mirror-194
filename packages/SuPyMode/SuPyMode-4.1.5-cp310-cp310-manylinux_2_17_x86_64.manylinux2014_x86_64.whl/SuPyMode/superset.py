#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import pickle
import numpy
import os
import logging
from dataclasses import dataclass
from itertools import combinations

# Third-party imports
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp

# Local imports
from SuPyMode.supermode import SuperMode
from SuPyMode.tools import plot_style
from SuPyMode.tools import directories
from MPSPlots.Render2D import Scene2D, Axis, Multipage, Line, ColorBar, Mesh
from MPSPlots import CMAP


@dataclass
class SuperSet(object):
    """
    Solver to which is associated the computed SuperSet Modes

    .. note::
        This class is a representation of the fiber optic structures set of supermodes, hence the name.
        This class has not ling to c++ codes, it is pure Python.
        The items of this class are the supermodes generated from within the SuPySolver

    """

    standard_name = ['LP01', "LP11_a", "LP11_b", "LP21_a", "LP21_b", "LP02", "LP31_a", "LP31_b"]
    parent_solver: object
    wavelength: float

    def __post_init__(self):
        self.wavenumber = 2 * numpy.pi / self.wavelength
        self._transmission_matrix = None
        self.supermodes = []
        self._itr_to_slice = interp1d(self.itr_list, numpy.arange(self.itr_list.size))

    def __getitem__(self, idx: int):
        return self.supermodes[idx]

    def __setitem__(self, idx: int, value):
        self.supermodes[idx] = value

    @property
    def geometry(self):
        """
        Return geometry of the coupler structure
        """

        return self.parent_solver.geometry

    @property
    def itr_list(self):
        """
        Return list of itr value that are used to compute the supermodes
        """

        return self.parent_solver.itr_list

    @property
    def axes(self):
        """
        Return axes object of the geometry
        """
        return self.parent_solver.geometry.axes

    @property
    def transmission_matrix(self) -> numpy.ndarray:
        """Return supermode transfert matrix"""
        if self._transmission_matrix is None:
            self.compute_transmission_matrix()

        return self._transmission_matrix

    def itr_to_slice(self, itr_list: list[int], floor_down: bool = True) -> list[int]:
        """
        Return slice number associated to itr value

        :param      itr_list:      Inverse taper ration value to evaluate the slice.
        :type       itr_list:      { type_description }

        :returns:   List of itr values,
        :rtype:     list[float]
        """
        itr_list = numpy.asarray(itr_list)
        itr_i = self.itr_list[0]
        itr_f = self.itr_list[-1]

        assert numpy.all((itr_list >= itr_f) & (itr_i >= itr_list)), \
            f"ITR evaluation: {itr_list} is outside the boundaries!"

        if floor_down:
            return numpy.floor(self._itr_to_slice(itr_list)).astype(int)

        else:
            return numpy.ceil(self._itr_to_slice(itr_list)).astype(int)

    def slice_to_itr(self, slice_list: list[int]) -> list[float]:
        """
        Return slice number associated to itr value

        :param      slice_list:      Value of the slice to which evaluate the itr.
        :type       slice_list:      list[int]

        :returns:   List of itr values,
        :rtype:     list[float]
        """
        return [self.itr_list[i] for i in slice_list]

    def name_supermodes(self, *name_list, auto=False) -> None:
        if auto:
            name_list = self.standard_name[:len(self.supermodes)]

        for n, name in enumerate(name_list):
            self[n].name = name
            setattr(self, name, self[n])

        return [getattr(self, name) for name in name_list]

    def swap_supermode_order(self, idx0: int, idx1: int) -> "SuperSet":
        """
        Swap two supermodes.
        it doesn't change any of their characteristic, it only changes the order on whihc they will
        appear, notably for the plots.

        :param      idx0:            Index of the first mode to swap
        :type       idx0:            int
        :param      idx1:            Index of the second mode to swap
        :type       idx1:            int
        """
        self.supermodes[idx0], self.supermodes[idx1] = self.supermodes[idx1], self.supermodes[idx0]

        return self

    def compute_transmission_matrix(self) -> None:
        """
        Calculates the transmission matrix with only the propagation constant included.

        :returns:   The transmission matrix.
        :rtype:     numpy.ndarray
        """
        shape = [
            len(self.supermodes),
            len(self.supermodes),
            len(self.itr_list)
        ]

        self._transmission_matrix = numpy.zeros(shape)

        for mode in self.supermodes:
            self._transmission_matrix[mode.mode_number, mode.mode_number, :] = mode.beta._data

    def add_coupling_to_t_matrix(self, t_matrix: numpy.ndarray, coupling_factor: numpy.ndarray) -> numpy.ndarray:
        """
        Add the coupling coefficients to the transmission matrix.

        :returns:   The transmission matrix.
        :rtype:     numpy.ndarray
        """

        size = t_matrix.shape[-1]

        t_matrix = t_matrix.astype(complex)
        for mode_0, mode_1 in combinations(self.supermodes, 2):
            coupling = mode_0.coupling.get_values(mode_1)[:size] * coupling_factor

            t_matrix[mode_0.mode_number, mode_1.mode_number, :] = - coupling
            t_matrix[mode_1.mode_number, mode_0.mode_number, :] = + coupling

        return t_matrix

    def compute_coupling_factor(self, coupler_length: float) -> numpy.ndarray:
        r"""
        Compute the coupling factor defined as:
        .. math::
          f_c = \frac{1}{\rho} \frac{d \rho}{d z}

        :param      coupler_length:     The length of the coupler
        :type       coupler_length:     float

        :returns:   The amplitudes as a function of the distance in the coupler
        :rtype:     numpy.ndarray
        """

        dx = coupler_length / (self.itr_list.size)

        ditr = numpy.gradient(numpy.log(self.itr_list), axis=0)

        return ditr / dx

    def get_transmision_matrix_from_profile(self, profile, with_coupling: bool = True, coupling_factor: float = 1):
        """
        Gets the transmision matrix from profile.

        :param      profile:          The z-profile of the coupler
        :type       profile:          object
        :param      with_coupling:    Adding the mode coupling or not to the propagation problem
        :type       with_coupling:    bool
        :param      coupling_factor:  Factor to be mutliplied to the coupling coefficients
        :type       coupling_factor:  float
        """
        final_slice = self.itr_to_slice(itr_list=profile.smallest_itr, floor_down=False)

        sub_t_matrix = self.transmission_matrix[..., :final_slice]

        sub_itr_vector = self.itr_list[: final_slice]

        array_coupling_factor = profile.evaluate_adiabatic_factor(itr=sub_itr_vector)

        if with_coupling:
            sub_t_matrix = self.add_coupling_to_t_matrix(
                t_matrix=sub_t_matrix,
                coupling_factor=array_coupling_factor * coupling_factor
            )

        sub_distance = profile.evaluate_distance_vs_itr(sub_itr_vector)

        return sub_distance, sub_itr_vector, sub_t_matrix

    def propagate(self,
            profile,
            initial_amplitude: list,
            max_step: float = None,
            with_coupling: bool = True,
            coupling_factor: float = 1,
            method: str = 'RK45',
            **kwargs) -> numpy.ndarray:
        """
        Returns the amplitudes value of the supermodes in the coupler.

        :param      initial_amplitude:  The initial amplitude
        :type       initial_amplitude:  list
        :param      profile:            The z-profile of the coupler
        :type       profile:            object
        :param      max_step:           The maximum stride to use in the solver
        :type       max_step:           float
        :param      with_coupling:      Adding the mode coupling or not to the propagation problem
        :type       with_coupling:      bool
        :param      kwargs:             The keywords arguments to be passed to the solver
        :type       kwargs:             dictionary

        :returns:   The amplitudes as a function of the distance in the coupler
        :rtype:     numpy.ndarray
        """
        # from numba import jit
        initial_amplitude = numpy.asarray(initial_amplitude).astype(complex)

        if max_step is None:
            max_step = self.parent_solver.wavelength / 50

        sub_distance, sub_itr_vector, sub_t_matrix = self.get_transmision_matrix_from_profile(
            profile=profile,
            with_coupling=with_coupling,
            coupling_factor=coupling_factor
        )

        z_to_itr = interp1d(
            profile.distance,
            profile.itr_list,
            bounds_error=False,
            fill_value='extrapolate',
            axis=-1
        )

        itr_to_t_matrix = interp1d(
            sub_itr_vector,
            sub_t_matrix,
            bounds_error=False,
            fill_value='extrapolate',
            axis=-1
        )

        # @jit
        def model(z, y):
            itr = z_to_itr(z)
            return 1j * itr_to_t_matrix(itr).dot(y)

        sol = solve_ivp(
            model,
            y0=initial_amplitude,
            t_span=[0, profile.length],
            vectorized=True,
            max_step=max_step,
            method=method,
            **kwargs
        )

        return sol.t, sol.y

    def get_mix_field(self, distance: numpy.ndarray, amplitudes: numpy.ndarray, under_sampling: int = 1):
        distance = distance[::under_sampling]

        slice_list = (distance / distance[-1] * (self.itr_list.size - 1)).astype(int)

        field_mix = \
            amplitudes[0, slice_list, numpy.newaxis, numpy.newaxis] * self[0].field._data[slice_list, ...] + \
            amplitudes[1, slice_list, numpy.newaxis, numpy.newaxis] * self[1].field._data[slice_list, ...]

        return distance, field_mix

    def get_propagation_field(self,
                              initial_amplitude: list,
                              coupler_length: float = 1000,
                              max_step: float = 0.05,
                              under_sampling: int = 10,
                              **kwargs) -> None:
        """
        Generates a gif video of the mode propagation.

        :param      initial_amplitude:  The initial amplitude
        :type       initial_amplitude:  list
        :param      coupler_length:     The length of the coupler
        :type       coupler_length:     float
        :param      max_step:           The maximum stride to use in the solver
        :type       max_step:           float
        :param      under_sampling:     Propagation undersampling factor for the video production
        :type       under_sampling:     int
        :param      kwargs:             The keywords arguments
        :type       kwargs:             dictionary
        """
        import pyvista as pv

        z, amplitudes = self.propagate(
            initial_amplitude=initial_amplitude,
            coupler_length=coupler_length,
            max_step=max_step,
            **kwargs
        )

        distance, all_field = self.get_mix_field(distance=z, amplitudes=numpy.abs(amplitudes), under_sampling=2)

        x = self.axes.x.mesh / 200
        y = self.axes.y.mesh / 200

        grid = pv.StructuredGrid(x, y, all_field[0])

        plotter = pv.Plotter(notebook=False, off_screen=True)

        plotter.add_mesh(
            grid,
            scalars=all_field[0],
            lighting=False,
            show_edges=True,
        )

        plotter.open_gif("wave_test.gif", fps=20)

        pts = grid.points.copy()

        for z, field in zip(distance, all_field.real):
            pts[:, -1] = field.ravel()
            plotter.update_coordinates(pts, render=False)
            plotter.update_scalars(field.ravel(), render=False)

            plotter.write_frame()

        plotter.close()

    def append_supermode(self, **kwargs) -> None:
        """
        Add a supermode to the SuperSet list of supermodes.
        """
        superMode = SuperMode(parent_set=self, **kwargs)

        self.supermodes.append(superMode)

    def _sorting_modes_(self, *ordering_list) -> None:
        """
        Generic mode sorting method

        :param      ordering_parameters:  The ordering list to sort the supermodes
        :type       ordering_parameters:  list
        """
        order = numpy.lexsort(ordering_list)

        supermodes = [self.supermodes[idx] for idx in order]

        for n, supermode in enumerate(supermodes):
            supermode.mode_number = n

        return supermodes

    def sorting_modes_beta(self) -> None:
        """
        Re-order modes to sort them in descending value of propagation constant.
        """
        return self._sorting_modes_([-mode.beta[-1] for mode in self.supermodes])

    def sorting_modes(self, sorting_method: str = "beta", keep_only: int = None) -> None:
        """
        Re-order modes according to a sorting method, either "beta" or "symmetry+beta".
        The final mode selection will also be filter to keep only a certain number of modes
        """
        assert sorting_method.lower() in ["beta", "symmetry+beta"], \
            f"Unrecognized sortingmethod: {sorting_method}, accepted values are ['beta', 'symmetry+beta']"

        match sorting_method.lower():
            case "beta":
                supermodes = self.sorting_modes_beta()
            case "symmetry+beta":
                supermodes = self.sorting_modes_solver_beta()

        self.all_supermodes = supermodes

        self.supermodes = supermodes[:keep_only]

    def sorting_modes_solver_beta(self):
        """
        Re-order modes to sort them in with two parameters:
        ascending cpp_solver number and descending value of propagation constant.
        """
        return self._sorting_modes_(
            [-mode.beta[-1] for mode in self.supermodes],
            [mode.solver_number for mode in self.supermodes],
        )

    def _interpret_itr_slice_list_(self, slice_list: list, itr_list: list):
        slice_list = [*slice_list, *self.itr_to_slice(itr_list)]

        if len(slice_list) == 0:
            slice_list = [0, -1]

        itr_list = self.slice_to_itr(slice_list)

        itr_list = numpy.sort(itr_list)[::-1]

        return self.itr_to_slice(itr_list), itr_list

    @staticmethod
    def single_plot(plot_function):
        def wrapper(self, *args, **kwargs):
            figure = Scene2D(unit_size=(10, 4))
            ax = Axis(row=0, col=0)
            figure.add_axes(ax)
            plot_function(self, ax=ax, *args, **kwargs)

            return figure

        return wrapper

    @single_plot
    def plot_index(self, ax: Axis) -> Scene2D:
        """
         Plot effective index for each mode as a function of itr

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.index)

        for mode in self.supermodes:
            y = mode.index.get_values()
            artist = Line(x=self.itr_list, y=y, label=f'{mode.stylized_name}')
            ax.add_artist(artist)

    @single_plot
    def plot_beta(self, ax: Axis) -> Scene2D:
        """
         Plot propagation constant for each mode as a function of itr

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.beta)

        for mode in self.supermodes:
            y = mode.beta.get_values()
            artist = Line(x=self.itr_list, y=y, label=f'{mode.stylized_name}')
            ax.add_artist(artist)

    @single_plot
    def plot_eigen_value(self, ax: Axis) -> Scene2D:
        """
         Plot propagation constant for each mode as a function of itr

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.eigen_value)

        for mode in self.supermodes:
            y = mode.eigen_value.get_values()
            artist = Line(x=self.itr_list, y=y, label=f'{mode.stylized_name}')
            ax.add_artist(artist)

    @single_plot
    def plot_normalized_coupling(self, ax: Axis, mode_of_interest: list = [], mode_selection='all') -> Scene2D:
        """
         Plot coupling value for each mode as a function of itr

        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.normalized_coupling)

        combination = self.interpret_combinations(
            mode_of_interest=mode_of_interest,
            mode_selection=mode_selection
        )

        for mode_0, mode_1 in combination:
            if mode_0.is_computation_compatible(mode_1):
                y = numpy.abs(mode_0.normalized_coupling.get_values(other_supermode=mode_1))
                artist = Line(x=self.itr_list, y=y, label=f'{mode_0.stylized_name} - {mode_1.stylized_name}')
                ax.add_artist(artist)

    @single_plot
    def plot_overlap(self, ax: Axis, mode_of_interest: list = [], mode_selection='all') -> Scene2D:
        """
         Plot overlap value for each mode as a function of itr

        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.overlap)

        combination = self.interpret_combinations(
            mode_of_interest=mode_of_interest,
            mode_selection=mode_selection
        )

        for mode_0, mode_1 in combination:
            if mode_0.is_computation_compatible(mode_1):
                y = mode_0.overlap.get_values(other_supermode=mode_1)
                artist = Line(x=self.itr_list, y=y, label=f'{mode_0.stylized_name} - {mode_1.stylized_name}')
                ax.add_artist(artist)

    @single_plot
    def plot_beating_length(self, ax: Axis, mode_of_interest: list = [], mode_selection='all') -> Scene2D:
        """
         Plot coupling value for each mode as a function of itr

        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.beating_length)

        combination = self.interpret_combinations(
            mode_of_interest=mode_of_interest,
            mode_selection=mode_selection
        )

        for mode_0, mode_1 in combination:
            if mode_0.is_computation_compatible(mode_1):
                y = mode_0.beating_length.get_values(other_supermode=mode_1)
                artist = Line(x=self.itr_list, y=y, label=f'{mode_0.stylized_name} - {mode_1.stylized_name}')
                ax.add_artist(artist)

    @single_plot
    def plot_adiabatic(self, ax: Axis, mode_of_interest: list = [], mode_selection: str = 'all', add_profile=[]) -> Scene2D:
        """
         Plot adiabatic criterion for each mode as a function of itr

        :param      pair_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       pair_of_interest:  list
        :param      mode_selection:    The type of combination to be plotted, either 'specific/all/pairs'
        :type       mode_selection:    str

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.adiabatic)

        combination = self.interpret_combinations(
            mode_of_interest=mode_of_interest,
            mode_selection=mode_selection
        )

        for mode_0, mode_1 in combination:
            if mode_0.is_computation_compatible(mode_1):
                y = mode_0.adiabatic.get_values(other_supermode=mode_1)
                artist = Line(x=self.itr_list, y=y, label=f'{mode_0.stylized_name} - {mode_1.stylized_name}')
                ax.add_artist(artist)

        for profile in add_profile:
            profile._render_adiabatic_factor_vs_itr_on_ax_(ax)

    @single_plot
    def plot_normalized_adiabatic(self, ax: Axis, mode_of_interest: list = [], mode_selection: str = 'all', add_profile=[]) -> Scene2D:
        """
         Plot adiabatic criterion for each mode as a function of itr

        :param      pair_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       pair_of_interest:  list
        :param      mode_selection:    The type of combination to be plotted, either 'specific/all/pairs'
        :type       mode_selection:    str

        :returns:   figure instance, to plot the show() method.
        :rtype:     Scene2D
        """
        ax.set_style(**plot_style.adiabatic)

        combination = self.interpret_combinations(
            mode_of_interest=mode_of_interest,
            mode_selection=mode_selection
        )

        for mode_0, mode_1 in combination:
            if mode_0.is_computation_compatible(mode_1):
                n0 = mode_0.index._data
                n1 = mode_1.index._data
                beating_length = mode_0.wavelength / abs(n0 - n1)
                y = mode_0.adiabatic.get_values(other_supermode=mode_1) * beating_length

                artist = Line(x=self.itr_list, y=y, label=f'{mode_0.stylized_name} - {mode_1.stylized_name}')
                ax.add_artist(artist)

    def interpret_combinations(self, mode_of_interest: list, mode_selection: str):
        assert mode_selection in ['all', 'pairs', 'specific'], f"mode_selection: {mode_selection} not recoginized, argument have to be in ['all', 'pairs', 'specific']"
        match mode_selection:
            case 'all':
                combination = combinations(self.supermodes, 2)
            case 'pairs':
                combination = self.interpret_pair_of_interest(mode_of_interest)
            case 'specific':
                combination = self.interpret_mode_of_interest(mode_of_interest)

        return combination

    def interpret_pair_of_interest(self, mode_of_interest: list):
        """
        Interpret the argument mode_of_interest to isolate the
        only the pairs containing both of the mode of interests.

        :param      mode_of_interest:  The mode of interest
        :type       mode_of_interest:  list
        """
        combination = []
        for mode_0, mode_1 in combinations(mode_of_interest, 2):
            if mode_0.is_computation_compatible(mode_1):
                combination.append((mode_0, mode_1))

        return self.remove_duplicate_in_combination(combination)

    def interpret_mode_of_interest(self, mode_of_interest: list):
        """
        Interpret the argument mode_of_interest to isolate the
        only combinations that contains the modes of interests.

        :param      mode_of_interest:  The mode of interest
        :type       mode_of_interest:  list
        """
        combination = []
        for mode_0 in mode_of_interest:
            for mode_1 in self.supermodes:
                if mode_0.is_computation_compatible(mode_1):
                    combination.append((mode_0, mode_1))

        return self.remove_duplicate_in_combination(combination)

    def remove_duplicate_in_combination(self, combination: list):
        """
        Removes a duplicate tuple of modes pair in combination.

        :param      combination:  The cleaned combination
        :type       combination:  list
        """
        new_combination = []
        for mode_0, mode_1 in combination:
            couple = mode_0, mode_1
            if (mode_0, mode_1) not in new_combination and (mode_1, mode_0) not in new_combination:
                new_combination.append(couple)

        return new_combination

    def plot_field(self, itr_list: list[float] = [], slice_list: list[int] = []) -> Scene2D:
        """
        Plot each of the mode field for different itr value or slice number.

        :param      itr_list:    List of itr value to evaluate the mode field
        :type       itr_list:    list
        :param      slice_list:  List of integer reprenting the slice where the mode field is evaluated
        :type       slice_list:  list

        :returns:   The figure
        :rtype:     Scene2D
        """
        figure = Scene2D(unit_size=(3, 3))

        slice_list, itr_list = self._interpret_itr_slice_list_(slice_list, itr_list)

        for m, mode in enumerate(self.supermodes):
            for n, (itr, slice) in enumerate(zip(itr_list, slice_list)):
                ax = Axis(row=n, col=m, title=f'{mode.stylized_name}\n[slice: {slice}  ITR: {itr:.4f}]')
                ax.colorbar = ColorBar(symmetric=True, position='right')

                x, y, field = mode.field.get_field_with_boundaries(slice=slice)

                artist = Mesh(x=x, y=y, scalar=field, colormap=CMAP.BKR)

                ax.add_artist(artist)

                ax.set_style(**plot_style.field)
                figure.add_axes(ax)

        return figure

    def plot(self, plot_type: str, **kwargs) -> Scene2D:
        """
        Generic plot function.

        Args:
            type: Plot type ['index', 'beta', 'adiabatic', 'normalized-adiabatic', 'overlap', 'coupling', 'field', 'beating-length']
        """
        match plot_type.lower():
            case 'index':
                return self.plot_index(**kwargs)
            case 'beta':
                return self.plot_beta(**kwargs)
            case 'eigen-value':
                return self.plot_eigen_value(**kwargs)
            case 'normalized-coupling':
                return self.plot_normalized_coupling(**kwargs)
            case 'overlap':
                return self.plot_overlap(**kwargs)
            case 'adiabatic':
                return self.plot_adiabatic(**kwargs)
            case 'field':
                return self.plot_field(**kwargs)
            case 'beating-length':
                return self.plot_beating_length(**kwargs)
            case 'normalized-adiabatic':
                return self.plot_normalized_adiabatic(**kwargs)

        plot_type_list = [
            'index',
            'beta',
            'eigen_value',
            'adiabatic',
            'overlap'
            'normalized-adiabatic',
            'normalized-coupling',
            'field',
            'beating-length'
        ]

        raise ValueError(f"plot type: {plot_type} not recognized, accepted values are: {plot_type_list}")

    def generate_report(self,
                        filename: str = "report",
                        itr_list: list[float] = [],
                        slice_list: list[int] = [],
                        dpi: int = 200,
                        mode_of_interest: list = None) -> None:
        """
        Generate a full report of the coupler properties as a .pdf file

        :param      filename:          Name of the Report file to be outputed.
        :type       filename:          str
        :param      itr_list:          List of itr value to evaluate the mode field.
        :type       itr_list:          Array
        :param      slice_list:        List of slice value to evaluate the mode field.
        :type       slice_list:        Array
        :param      dpi:               Pixel density for the image included in the report.
        :type       dpi:               int
        :param      mode_of_interest:  List of the mode that are to be considered in the adiabatic criterion plotting.
        :type       mode_of_interest:  list

        :returns:   { description_of_the_return_value }
        :rtype:     None
        """
        figures = []
        figures.append(self.geometry.plot()._render_())

        figures.append(self.plot_field(itr_list=itr_list, slice_list=slice_list)._render_())

        figures.append(self.plot_index()._render_())

        figures.append(self.plot_beta()._render_())

        figures.append(self.plot_normalized_coupling(mode_of_interest=mode_of_interest)._render_())

        figures.append(self.plot_adiabatic(mode_of_interest=mode_of_interest)._render_())

        # directory = os.path.join(Directories.ReportPath, filename) + '.pdf'

        directory = f"{os.getcwd()}/{filename}.pdf"

        logging.info(f'Saving report to {directory}')

        Multipage(directory, figs=figures, dpi=dpi)

        for figure in figures:
            figure.close()

    def save_instance(self, filename: str, directory: str = '.'):
        """
        Saves the superset instance as a serialized pickle file.

        :param      filename:  The directory where to save the file, 'auto' options means the superset_instance folder
        :type       filename:  str
        :param      filename:  The filename
        :type       filename:  str
        """
        if directory == 'auto':
            directory = directories.instance_directory

        filename = directory + filename + ".instance.pickle"
        logging.info(f"Saving pickled superset into: {filename}")

        with open(f"{filename}", 'wb') as output_file:
            pickle.dump(self, output_file, pickle.HIGHEST_PROTOCOL)

# -
