"""
Validation: 0 with Xavier Daxhelet program
==========================================
"""


# %%
# Importing the package dependencies
from numpy import genfromtxt
from MPSPlots.Render2D import Scene2D, Axis, Line
from FiberFusing import Geometry, Fused2, BackGround
from SuPyMode.solver import SuPySolver
from SuPyMode.fibers import SMF28, get_silica_index
from SuPyMode.tools.directories import validation_data_path

# %%
# Generating the fiber structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Here we make use of the FiberFusing to generate a fiber structure that we use
# as the cladding.
_ = wavelength = 1.55e-6

air = BackGround(index=1)

clad = Fused2(
    fiber_radius=62.5e-6,
    fusion_degree=0.9,
    index=get_silica_index(wavelength=wavelength)
)

_ = clad.plot().show()

# %%
# Creating the geometry rasterization
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The cladding being defined we create the cores that are distributed at
# each (virtual) center of the cladding.
# All the components: air -- cladding -- cores, are inputed into a geometry class
# that will generate the mesh which will be used in the finit-difference matrix.
fiber_0 = SMF28(wavelength=1.55e-6, position=clad.fiber[0].core)
fiber_1 = SMF28(wavelength=1.55e-6, position=clad.fiber[1].core)


cores = [
    *fiber_0.structures,
    *fiber_1.structures
]

geometry = Geometry(
    background=air,
    structures=[clad, *cores],
    x_bounds='centering-left',
    y_bounds='centering-bottom',
    n=80,  # 200 gives the same results
    index_scrambling=0,
    gaussian_filter=None
)

_ = geometry.plot().show()

# %%
# We here create the solver class and generate the superset which
# will contains the supermodes to be computed.
solver = SuPySolver(
    geometry=geometry,
    tolerance=1e-10,
    max_iter=10000,
    show_iteration=False,  # Put this to True to see the computing progression
    accuracy=2,
    extrapolation_order=1
)

_ = solver.init_superset(
    wavelength=wavelength,
    n_step=500,
    itr_i=1.0,
    itr_f=0.03
)

_ = solver.add_modes(
    n_computed_mode=5,
    n_sorted_mode=4,
    boundaries={
        'right': 'symmetric',
        'left': 'zero',
        'top': 'symmetric',
        'bottom': 'zero'
    }
)

# %%
# We now add supermodes for different type of attributes such as boundaries.
# By default the solver assume no boundaries in the system.
_ = solver.add_modes(
    n_computed_mode=5,
    n_sorted_mode=4,
    boundaries={
        'right': 'symmetric',
        'left': 'zero',
        'top': 'anti-symmetric',
        'bottom': 'zero'
    }
)

# %%
# We now name the supermode for and easier evaluation of the outputed graphs
_ = solver.superset.name_supermodes(
    'LP01',
    'LP21',
    'LP02',
    'LP41',
    'LP11',
    'LP31',
    'LP12',
    'LP51'
)

# %%
# Field plotting
_ = solver.superset.plot('field').show()

_ = solver.superset.save_instance("figure4_16")

figure = Scene2D(unit_size=(8, 5), title='SBB figure 4.16')

ax = Axis(
    row=0,
    col=0,
    y_scale='log',
    x_label='ITR',
    y_label='Adiabatic criterion',
    show_legend=True,
    y_limits=[1e-4, 1]
)

_ = figure.add_axes(ax)

coupling_list = [
    (solver.superset.LP01, solver.superset.LP02, '-', 'blue'),
    (solver.superset.LP01, solver.superset.LP21, '-', 'red'),
    (solver.superset.LP01, solver.superset.LP41, '-', 'orange'),
    (solver.superset.LP11, solver.superset.LP31, '-', 'purple'),
    (solver.superset.LP11, solver.superset.LP12, '-', 'green'),
    (solver.superset.LP11, solver.superset.LP51, '-', 'turquoise')
]

for mode_0, mode_1, line_style, color in coupling_list:
    adiabatic = mode_0.adiabatic.get_values(mode_1)

    artist = Line(
        x=mode_0.itr_list,
        y=adiabatic * 1e-6,
        label=f'{mode_0.stylized_name}-{mode_1.stylized_name}',
        line_style=line_style,
        color=color
    )

    _ = ax.add_artist(artist)


# %%
# Comparisons with the other datas.
data_directory = [
    (f"{validation_data_path}/SBB_figure_4_16_a/LP01-LP02.csv", 'blue'),
    (f"{validation_data_path}/SBB_figure_4_16_a/LP01-LP21.csv", 'red'),
    (f"{validation_data_path}/SBB_figure_4_16_a/LP01-LP41.csv", 'orange'),
    (f"{validation_data_path}/SBB_figure_4_16_a/LP11-LP31.csv", 'purple'),
    (f"{validation_data_path}/SBB_figure_4_16_a/LP11-LP12.csv", 'green'),
    (f"{validation_data_path}/SBB_figure_4_16_a/LP11-LP51.csv", 'turquoise')
]


for data_dir, color in data_directory:
    data = genfromtxt(data_dir, delimiter=',').T

    artist = Line(
        x=data[0],
        y=data[1],
        line_style="--",
        color=color,
        label='experiment'
    )

    _ = ax.add_artist(artist)

_ = figure.show()


# -
