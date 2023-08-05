"""
1x1 Coupler
===========
"""

# %%
# Importing the package dependencies: FiberFusing, PyOptik [optional]
from FiberFusing import Geometry, Circle, BackGround
from SuPyMode.solver import SuPySolver
from PyOptik import ExpData

# %%
# Generating the fiber structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Here we make use of the FiberFusing to generate a fiber structure that we use
# as the cladding. The refractive index of the strcture is defined using PyOptik.
wavelength = 1.55e-6

index = ExpData('FusedSilica').GetRI(wavelength)

air = BackGround(index=1)

clad = Circle(position=(0, 0), radius=62.5e-6, index=index)

clad.plot().show()

# %%
# Creating the geometry rasterization
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The cladding being defined we create the cores that are distributed at
# each (virtual) center of the cladding.
# All the components: air -- cladding -- cores, are inputed into a geometry class
# that will generate the mesh which will be used in the finit-difference matrix.
cores = [Circle(position=clad.center, radius=4.1e-6, index=index + 0.005)]

geometry = Geometry(
    background=air,
    structures=[clad, *cores],
    x_bounds='centering-left',
    y_bounds='centering-top',
    n=40,
    index_scrambling=1e-6,
    gaussian_filter=None
)

_ = geometry.plot().show()

# %%
# We here create the solver class and generate the superset which
# will contains the supermodes to be computed.
solver = SuPySolver(
    geometry=geometry,
    tolerance=1e-8,
    max_iter=10000,
    show_iteration=False  # Put this to True to see the computing progression
)

solver.init_superset(
    wavelength=wavelength,
    n_step=500,
    itr_i=1.0,
    itr_f=0.05
)


# %%
# We now add supermodes for different type of attributes such as boundaries.
# By default the solver assume no boundaries in the system.
_ = solver.add_modes(
    boundaries={'right': 'symmetric', 'left': 'zero', 'top': 'zero', 'bottom': 'symmetric'},
    n_computed_mode=4,
    n_sorted_mode=2
)

_ = solver.add_modes(
    boundaries={'right': 'symmetric', 'left': 'zero', 'top': 'zero', 'bottom': 'anti-symmetric'},
    n_computed_mode=4,
    n_sorted_mode=2
)

# One important thing to understand here is as the probleme has a circular symmetry
# and no boundary condition are given to fix them the computed eigen vector
# which are supposed to represents the propgating modes are allowed to turn.
# This, in return ruin the field-sorting method that ensure a coherent distribution
# of the mode through the z-profile of the coupler.
# This 1x1 coupler case is a perfect show case for this problem.
# In order to fix this a break of symmetry is needed either fixing the boundary condition
# with symmetries or adding some asymmetrical structure.

# %%
# The modes are now computed [can take a few minutes], the modes are concatenated
# in a superset class that we can access with the get_set() function. This class
# can be used to analyse the data
superset = solver.get_set()

# %%
# Field computation: :math:`E_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(plot_type='field', itr_list=[1.0, 0.05]).show()

# %%
# After mode visualization we can name them for an easier further analyze.
# This step is, however, not mandatory.
_ = superset.name_supermodes('LP01', 'LP02', 'LP11_v', 'LP11_h')

# %%
# Effective index: :math:`n^{eff}_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(plot_type='index').show()

# %%
# Modal normalized coupling: :math:`C_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(plot_type='normalized-coupling').show()

# %%
# Adiabatic criterion: :math:`\tilde{C}_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(plot_type='adiabatic').show()
