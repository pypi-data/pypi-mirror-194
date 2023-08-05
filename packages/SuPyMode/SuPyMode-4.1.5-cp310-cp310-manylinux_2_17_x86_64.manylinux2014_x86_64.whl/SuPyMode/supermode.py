# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

# Built-in imports
import numpy
from dataclasses import dataclass

# Local imports
from SuPyMode import representations


class InheritFromSuperSet():
    """
    Property class for inherited attribute from SuperSet.

    """
    @property
    def geometry(self) -> object:
        return self.parent_set.geometry

    @property
    def axes(self) -> object:
        return self.parent_set.axes


@dataclass
class SuperMode(InheritFromSuperSet):
    """
    .. note::
        This class is a representation of the fiber optic structures SuperModes.
        Those mode belongs to a SuperSet class and are constructed with the SuPySolver.
        It links to c++ SuperMode class.
    """
    parent_set: None
    """SuperSet to which is associated the computed this mode"""
    binded_supermode: None
    """C++ binded sueprmode"""
    solver_number: int
    """Number which bind this mode to a specific python solver"""
    mode_number: int
    """Unique number associated to this mode in a particular symmetry set"""
    wavelength: float
    """UWavelength of the simulated modes"""
    boundaries: dict
    """Boundary conditions"""
    itr_list: numpy.ndarray
    """List of itr value corresponding to the slices where fields and propagation constant are computed"""
    name: str = None
    """Name to give to the mode"""

    def __post_init__(self):
        self.ID = [self.solver_number, self.binding_number]
        self.field = representations.Field(parent_supermode=self)
        self.index = representations.Index(parent_supermode=self)
        self.beta = representations.Beta(parent_supermode=self)
        self.normalized_coupling = representations.NormalizedCoupling(parent_supermode=self)
        self.overlap = representations.Overlap(parent_supermode=self)
        self.adiabatic = representations.Adiabatic(parent_supermode=self)
        self.eigen_value = representations.EigenValue(parent_supermode=self)
        self.beating_length = representations.BeatingLength(parent_supermode=self)

    @property
    def binding_number(self):
        """ Returns the mode number specific to one CppSolver """
        return self.binded_supermode.binding_number

    @property
    def mesh_gradient(self) -> numpy.ndarray:
        return self.binded_supermode.mesh_gradient

    @property
    def nx(self) -> int:
        return self.binded_supermode.nx

    @property
    def ny(self) -> int:
        return self.binded_supermode.ny

    @property
    def stylized_name(self):
        if self.name is None:
            return f"Mode: {self.ID}"
        else:
            return f"${self.name}$"

    def is_computation_compatible(self, other: 'SuperMode') -> bool:
        """
        Determines whether the specified other supermode is compatible
        for computation of the modal coupling and adiabatic criterion.
        It, basically return False only if the mode is the same or if the
        boundaries symmetries differ in some way.

        :param      other:  The other SuperMode to compare with
        :type       other:  SuperMode

        :returns:   True if the specified other is computation compatible, False otherwise.
        :rtype:     bool
        """
        if self.ID != other.ID and self.is_symmetry_compatible(other):
            return True
        else:
            return False

    def is_symmetry_compatible(self, other: 'SuperMode'):
        return self.boundaries == other.boundaries

# -
