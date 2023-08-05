"""
4x4 Coupler
===========
"""

# %%
# Importing the package dependencies: FiberFusing, PyOptik [optional]
from FiberFusing import Geometry, Fused4, Circle, BackGround
from SuPyMode.solver import SuPySolver

# %%
# Generating the fiber structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Here we make use of the FiberFusing to generate a fiber structure that we use
# as the cladding. The refractive index of the strcture is defined using PyOptik.
wavelength = 1.55e-6

index = 1.4444

air = BackGround(index=1)

clad = Fused4(fiber_radius=62.5e-6, fusion_degree=0.9, index=index)

clad.plot().show()

# %%
# Creating the geometry rasterization
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The cladding being defined we create the cores that are distributed at
# each (virtual) center of the cladding.
# All the components: air -- cladding -- cores, are inputed into a geometry class
# that will generate the mesh which will be used in the finit-difference matrix.
cores = [Circle(position=fiber.core, radius=4.1e-6, index=index + 0.005) for fiber in clad.fiber_list]

geometry = Geometry(
    background=air,
    structures=[clad, *cores],
    x_bounds='centering-left',
    y_bounds='centering-bottom',
    n=40,
    index_scrambling=0,
    gaussian_filter=None
)

_ = geometry.plot().show()

# %%
# We here create the solver class and generate the superset which
# will contains the supermodes to be computed.
Sol = SuPySolver(
    geometry=geometry,
    tolerance=1e-8,
    max_iter=10000,
    show_iteration=False  # Put this to True to see the computing progression
)

Sol.init_superset(
    wavelength=wavelength,
    n_step=500,
    itr_i=1.0,
    itr_f=0.05
)


# %%
# We now add supermodes for different type of attributes such as boundaries.
# In this current case we use the left-right and top-bottom symmetry to compute the
# associated symmetric and anti-symmetric modes.
_ = Sol.add_modes(
    boundaries={'right': 'symmetric', 'left': 'zero', 'top': 'symmetric', 'bottom': 'zero'},
    n_computed_mode=3,
    n_sorted_mode=2
)

_ = Sol.add_modes(
    boundaries={'right': 'anti-symmetric', 'left': 'zero', 'top': 'symmetric', 'bottom': 'zero'},
    n_computed_mode=2,
    n_sorted_mode=1
)

_ = Sol.add_modes(
    boundaries={'right': 'symmetric', 'left': 'zero', 'top': 'anti-symmetric', 'bottom': 'zero'},
    n_computed_mode=2,
    n_sorted_mode=1
)

# %%
# The modes are now computed [can take a few minutes], the modes are concatenated
# in a superset class that we can access with the get_set() function. This class
# can be used to analyse the data
Set = Sol.get_set()

# %%
# Field computation: :math:`E_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = Set.plot(plot_type='field', itr_list=[1.0, 0.05]).show()

# %%
# After mode visualization we can name them for an easier further analyze.
# This step is, however, not mandatory.
_ = Set.name_supermodes('LP01', 'LP21', 'LP11_v', 'LP11_h')

# %%
# Effective index: :math:`n^{eff}_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = Set.plot(plot_type='index').show()

# %%
# Modal coupling: :math:`C_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = Set.plot(plot_type='normalized-coupling').show()

# %%
# Adiabatic criterion: :math:`\tilde{C}_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = Set.plot(plot_type='adiabatic').show()
