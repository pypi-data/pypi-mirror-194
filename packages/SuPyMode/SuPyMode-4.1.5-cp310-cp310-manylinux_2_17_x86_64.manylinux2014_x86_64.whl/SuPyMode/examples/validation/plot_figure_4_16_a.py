"""
Validation: 0 with Xavier Daxhelet program
==========================================
"""


from numpy import genfromtxt
from MPSPlots.Render2D import Scene2D, Axis, Line
from FiberFusing import Geometry, Fused2, BackGround
from SuPyMode.solver import SuPySolver
from SuPyMode.fibers import SMF28, get_silica_index
from SuPyMode.tools.directories import validation_data_path

# ---------------- SuPyMode data ________________________________
wavelength = 1.55e-6

air = BackGround(index=1)

clad = Fused2(
    fiber_radius=62.5e-6,
    fusion_degree=0.9,
    index=get_silica_index(wavelength=wavelength)
)

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
    n=200,
    index_scrambling=0,
    gaussian_filter=None
)

geometry.plot().show()

solver = SuPySolver(
    geometry=geometry,
    tolerance=1e-10,
    max_iter=10000,
    show_iteration=False,
    accuracy=2,
    extrapolation_order=1
)

solver.init_superset(
    wavelength=wavelength,
    n_step=500,
    itr_i=1.0,
    itr_f=0.03
)

solver.add_modes(
    n_computed_mode=5,
    n_sorted_mode=4,
    boundaries={
        'right': 'symmetric',
        'left': 'zero',
        'top': 'symmetric',
        'bottom': 'zero'
    }
)

solver.add_modes(
    n_computed_mode=5,
    n_sorted_mode=4,
    boundaries={
        'right': 'symmetric',
        'left': 'zero',
        'top': 'anti-symmetric',
        'bottom': 'zero'
    }
)

solver.superset.name_supermodes(
    'LP01',
    'LP21',
    'LP02',
    'LP41',
    'LP11',
    'LP31',
    'LP12',
    'LP51'
)

solver.superset.plot('field').show()

solver.superset.save_instance("figure4_16")

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

figure.add_axes(ax)

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

    ax.add_artist(artist)


# ---------------- Figure data ________________________________
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

    ax.add_artist(artist)

figure.show()


# -
