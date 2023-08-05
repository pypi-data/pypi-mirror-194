import numpy
from scipy.interpolate import interp1d
from SuPyMode.tools import plot_style

from MPSPlots.Render2D import Scene2D, Axis, Line


class AlphaProfile():
    """
    Class represent the fiber structure coupler z-profile.
    This particular class is set to a Gaussian profile.
    Translation table:
        - rho_w = radius_segment
        - rho_0 = initial_radius
        - l_w = heating_length_segment
        - x_0 = stretching_length
    """

    def __init__(self, initial_radius: float, symmetric: bool = False, name: str = 'profile'):
        self.taper_segment = []
        self.z_segment = []
        self.radius_segments = []
        self.heating_length_segment = []

        self.name = name
        self.initial_radius = initial_radius
        self.symmetric = symmetric

    def symmetrize_array(self, array: numpy.ndarray):
        return numpy.r_[array, array[::-1]]

    def symmetrize_distance(self, distance: numpy.ndarray):
        dz = abs(distance[0] - distance[1])
        return numpy.arange(2 * distance.size) * dz

    def add_constant_segment(self, length: float, n_point: int = 100):
        """
        Add the constant section following the last section which length is to be evaluated.

        :param      length:   Length of the constant section to be added
        :type       length:   float
        :param      n_point:  The number of point where wo which evaluate that segment
        :type       n_point:  int
        """
        return self.add_constant_custom_section(
            length=length,
            rho=self.last_radius,
            start_z=self.last_z,
            n_point=n_point
        )

    def add_end_of_taper_segment(self, length: float = None, n_point: int = 100) -> None:
        """
        Add the constant section which length equal the final length of the
        heating section.

        :param      n_point:  The number of point where wo which evaluate that segment
        :type       n_point:  int
        """
        if length is None:
            length = self.last_heating_length / 2

        return self.add_constant_custom_section(
            length=length,
            radius=self.last_radius,
            start_z=self.last_z,
            n_point=n_point
        )

    def add_constant_custom_section(self,
                                    length: float,
                                    radius: float,
                                    start_z: float = 0,
                                    n_point: int = 100) -> None:
        """
        Add the constant section which length, radius and start position is to be provided

        :param      length:   Length of the constant section to be added
        :type       length:   float
        :param      radius:   Radius of the constant section to be added
        :type       radius:   float
        :param      start_z:  Initial z-position of the constant section to be added
        :type       start_z:  float
        :param      n_point:  The number of point where wo which evaluate that segment
        :type       n_point:  int
        """
        z = numpy.linspace(0, length, n_point)

        radius = numpy.ones(n_point) * radius

        interpolation = interp1d(
            z + start_z,
            radius,
            bounds_error=False,
            fill_value=0
        )

        self.taper_segment.append(interpolation)
        self.z_segment.append(length + start_z)

    def evaluate_adiabatic_factor(self, itr: numpy.ndarray) -> numpy.ndarray:
        interpolation = interp1d(
            x=self._itr_list,
            y=self._adiabatic_factor,
            bounds_error=False,
            fill_value=numpy.nan
        )

        return interpolation(itr)

    def evaluate_distance_vs_itr(self, distance: numpy.ndarray) -> numpy.ndarray:

        interpolation = interp1d(
            x=self._itr_list,
            y=self._distance,
            bounds_error=True,
        )

        return interpolation(distance)

    def get_radius_from_segment(self,
                               alpha: float,
                               initial_heating_length: float,
                               stretching_length: float,
                               initial_radius: float,
                               distance: numpy.ndarray) -> tuple:
        """
        Gets the radius as a fonction of the distance for a specific segment.,

        :param      alpha:                  Alpha parameter which represent how the heating section changes in time
        :type       alpha:                  float
        :param      initial_heating_length: Initial length of the heating section
        :type       initial_heating_length: float
        :param      initial_radius:         The initial radius of the segment to be added
        :type       initial_radius:         float
        :param      stretching_length:      The total elongated lenght of the current segment to be added
        :type       stretching_length:      float
        :param      distance:               Array representing the z-distance.
        :type       distance:               numpy.ndarray
        """
        self.assert_conditions(
            alpha=alpha,
            stretching_length=stretching_length,
            initial_heating_length=initial_heating_length
        )

        term0 = 2 * alpha * distance
        term2 = (1 - alpha) * initial_heating_length
        term3 = -1 / (2 * alpha)

        radius = initial_radius * (1 + term0 / term2)**term3
        final_radius = initial_radius * (1 + alpha * stretching_length / initial_heating_length)**(-1 / (2 * alpha))
        final_heating_length = initial_heating_length + alpha * stretching_length

        assert not numpy.any(radius < 0), "Negative radius value are not physical"

        return radius, final_radius, final_heating_length

    def assert_conditions(self,
                          alpha: float,
                          stretching_length: float,
                          initial_heating_length: float) -> None:

        assert initial_heating_length > 0, "The initial heat lenght initial_heating_length cannot be negative!"

        if alpha < 0:
            assert stretching_length < initial_heating_length / abs(alpha), "Condition: x0 < initial_heating_length / |alpha| is not respected! see Birks article in the references!"

    def add_custom_segment(self, distance: numpy.ndarray, radius: numpy.ndarray):
        end_of_segment = distance[-1]
        final_radius_of_segment = radius[-1]

        interpolation = interp1d(
            distance,
            radius,
            bounds_error=False,
            fill_value=0
        )

        self.taper_segment.append(interpolation)
        self.z_segment.append(end_of_segment)
        self.radius_segments.append(final_radius_of_segment)

    def add_taper_custom_segment(self,
                                 alpha: float,
                                 initial_heating_length: float,
                                 initial_radius: float,
                                 stretching_length: float,
                                 start_z: float = 0,
                                 n_point: int = 100):
        """
        Add a tapered section for a given alpha, initial_heating_length, initial_radius, stretching_length and starting z position

        :param      alpha:                  Alpha parameter which represent how the heating section changes in time
        :type       alpha:                  float
        :param      initial_heating_length: Initial length of the heating section
        :type       initial_heating_length: float
        :param      initial_radius:         The initial radius of the segment to be added
        :type       initial_radius:         float
        :param      stretching_length:      The total elongated lenght of the current segment to be added
        :type       stretching_length:      float
        :param      n_point:                The number of point where wo which evaluate that segment
        :type       n_point:                int
        """
        alpha = 0.0001 if alpha == 0 else alpha

        z_0 = (1 - alpha) * stretching_length / 2
        end_of_segment = z_0 + start_z
        distance = numpy.linspace(0, z_0, n_point)

        assert distance[0] == 0, "Computation of taper section takes z as a reference and thus has to start with 0."

        radius, final_radius, final_heating_length = self.get_radius_from_segment(
            alpha=alpha,
            initial_heating_length=initial_heating_length,
            stretching_length=stretching_length,
            initial_radius=initial_radius,
            distance=distance
        )

        interpolation = interp1d(
            distance + start_z,
            radius,
            bounds_error=False,
            fill_value=0
        )

        self.taper_segment.append(interpolation)
        self.z_segment.append(end_of_segment)
        self.radius_segments.append(final_radius)
        self.heating_length_segment.append(final_heating_length)

    @property
    def distance(self):
        if self.symmetric:
            return self._symmetric_distance
        else:
            return self._distance

    @property
    def radius(self):
        if self.symmetric:
            return self._symmetric_radius
        else:
            return self._radius

    @property
    def itr_list(self):
        if self.symmetric:
            return self._symmetric_itr_list
        else:
            return self._itr_list

    @property
    def adiabatic(self):
        if self.symmetric:
            return self._symmetric_adiabatic_factor
        else:
            return self._adiabatic_factor

    @property
    def smallest_itr(self) -> float:
        return numpy.min(self.itr_list)

    @property
    def last_z(self):
        if len(self.z_segment) == 0:
            return 0
        else:
            return self.z_segment[-1]

    @property
    def last_radius(self):
        if len(self.radius_segments) == 0:
            return self.initial_radius
        else:
            return self.radius_segments[-1]

    @property
    def last_heating_length(self):
        return self.heating_length_segment[-1]

    def get_radius_from_segment_from_interpolation(self, z: numpy.ndarray):
        radius = numpy.zeros(z.size)

        for interpolation in self.taper_segment:
            radius += interpolation(z)

        return radius

    def add_taper_segment(self,
                          alpha: float,
                          initial_heating_length: float,
                          stretching_length: float,
                          initial_radius: float = None,
                          n_point: int = 100) -> None:
        """
        Add a tapered section following the previous one for a given alpha, initial_heating_length, stretching_length.

        :param      alpha:                  Alpha parameter which represent how the heating section changes in time
        :type       alpha:                  float
        :param      initial_heating_length: Initial length of the heating section
        :type       initial_heating_length: float
        :param      stretching_length:      The total elongated lenght of the current segment to be added
        :type       stretching_length:      float
        :param      n_point:                The number of point where wo which evaluate that segment
        :type       n_point:                int
        """
        if initial_radius is None:
            initial_radius = self.last_radius

        return self.add_taper_custom_segment(
            alpha=alpha,
            initial_heating_length=initial_heating_length,
            initial_radius=initial_radius,
            stretching_length=stretching_length,
            start_z=self.last_z,
            n_point=n_point
        )

    def initialize(self, n_point: int = 400) -> None:
        """
        Initialize all the computation including z, radius, distance, length, adiabatic criterion

        :param      n_point:  The number of point of the z-linespace to evaluate all the parameters.
        :type       n_point:  int
        """
        self._distance = numpy.linspace(0, self.last_z, n_point)
        self._radius = self.get_radius_from_segment_from_interpolation(self._distance)
        self._itr_list = self._radius / self.initial_radius
        self._adiabatic_factor = self.get_adiabatic_factor(radius=self._radius, distance=self._distance)

        self.symmetrize_parameters()
        self.length = self.distance[-1]

    def symmetrize_parameters(self):
        self._symmetric_distance = self.symmetrize_distance(self._distance)
        self._symmetric_radius = self.symmetrize_array(self._radius)
        self._symmetric_itr_list = self.symmetrize_array(self._itr_list)
        self._symmetric_adiabatic_factor = self.symmetrize_array(self._adiabatic_factor)

    def get_adiabatic_factor(self, radius: numpy.ndarray, distance: numpy.ndarray) -> numpy.ndarray:
        r"""
        Compute the adiabatic factor defined as:
        .. math::
          f_c = \frac{1}{\rho} \frac{d \rho}{d z}

        :returns:   The amplitudes as a function of the distance in the coupler
        :rtype:     numpy.ndarray
        """
        dz = numpy.gradient(distance, axis=0, edge_order=2)

        ditr = numpy.gradient(numpy.log(radius), axis=0, edge_order=2)

        return abs(ditr / dz)

    def _render_itr_vs_z_on_ax_(self, ax: Axis) -> None:
        """
        Add plot onto axis, the plots is ITR vs Z-distance

        :param      ax:   The axis on which to add the plot
        :type       ax:   Axis
        """
        ax.y_label = 'Inverse taper ratio'
        ax.x_label = 'z-distance'
        ax.y_scale = 'linear'

        artist = Line(x=self.distance, y=self.radius / self.initial_radius)

        ax.add_artist(artist)

    def _render_adiabatic_factor_vs_z_on_ax_(self, ax: Axis) -> None:
        """
        Add plot onto axis, the plots is adiabatic criterion vs Z-distance

        :param      ax:   The axis on which to add the plot
        :type       ax:   Axis
        """
        ax.y_scale = 'log'
        ax.y_label = 'Adiabatic criterion'
        ax.x_label = 'z-distance'

        artist = Line(x=self._distance, y=self._adiabatic_factor)

        ax.add_artist(artist)

    def _render_adiabatic_factor_vs_itr_on_ax_(self, ax: Axis) -> None:
        """
        Add plot onto axis, the plots is adiabatic criterion vs ITR

        :param      ax:   The axis on which to add the plot
        :type       ax:   Axis
        """
        ax.set_style(**plot_style.adiabatic)

        artist = Line(
            x=self.itr_list,
            y=self.adiabatic,
            line_style='--',
            color='k',
            label=self.name
        )

        ax.add_artist(artist)

    def plot(self) -> Scene2D:
        """
        Generate two plots: ITR vs z distance and adiabatic criterion vs ITR
        """

        itr = self._symmetric_radius / self.initial_radius
        figure = Scene2D(title=f'Minimum ITR: {itr.min():.4f}')

        ax0 = Axis(row=0, col=0, y_limits=[0, None])

        ax1 = Axis(row=1, col=0)

        figure.add_axes(ax0, ax1)

        self._render_itr_vs_z_on_ax_(ax0)

        self._render_adiabatic_factor_vs_itr_on_ax_(ax1)

        return figure

# -
