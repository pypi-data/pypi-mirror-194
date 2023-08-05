"""
Validation: 1 with Xavier Daxhelet program
==========================================
"""

from MPSPlots.Render2D import Scene2D, Axis, Line
from FiberFusing import Geometry, Fused2, BackGround
from SuPyMode.solver import SuPySolver
from SuPyMode.fibers import CustomFiber, get_silica_index

# ---------------- SuPyMode data ________________________________
wavelength = 1.55e-6

air = BackGround(index=1)

clad = Fused2(
    fiber_radius=62.5e-6,
    fusion_degree=0.9,
    index=get_silica_index(wavelength=wavelength)
)

fiber_0 = CustomFiber(  # V_2 = 4.0
    wavelength=wavelength,
    position=clad.fiber[0].core,
    name_list=['outer-clad', 'inner-clad', 'core'],
    na_list=[1.04172, 0.05, 0.113],
    radius_list=[62.5e-6, 20.0e-6, 3.8e-6]
)

fiber_1 = CustomFiber(  # V_2 = 4.0
    wavelength=wavelength,
    position=clad.fiber[1].core,
    name_list=['outer-clad', 'inner-clad', 'core'],
    na_list=[1.04172, 0.05, 0.113],
    radius_list=[62.5e-6, 20.0e-6, 3.8e-6]
)


cores = [
    *fiber_0.structures,
    *fiber_1.structures
]

geometry = Geometry(
    background=air,
    structures=[clad, *cores],
    x_bounds='auto-left',
    y_bounds='auto-bottom',
    n=80,  # 200 gives the same results
    index_scrambling=0
)

_ = geometry.plot().show()

solver = SuPySolver(
    geometry=geometry,
    tolerance=1e-10,
    max_iter=10000,
    show_iteration=False,
    accuracy=2
)

_ = solver.init_superset(
    wavelength=wavelength,
    n_step=500,
    itr_i=1.0,
    itr_f=0.05
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

_ = solver.superset.plot(plot_type='field').show()

figure = Scene2D(unit_size=(8, 5), title='SBB figure 4.16-(b)')

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

    ax.add_artist(artist)


# ---------------- Figure data ________________________________-
# data_directory = [
#     (f"{validation_data_path}/SBB_figure_4_16_a/LP01-LP02.csv", 'blue'),
#     (f"{validation_data_path}/SBB_figure_4_16_a/LP01-LP21.csv", 'red'),
#     (f"{validation_data_path}/SBB_figure_4_16_a/LP01-LP41.csv", 'orange'),
#     (f"{validation_data_path}/SBB_figure_4_16_a/LP11-LP31.csv", 'purple'),
#     (f"{validation_data_path}/SBB_figure_4_16_a/LP11-LP12.csv", 'green'),
#     (f"{validation_data_path}/SBB_figure_4_16_a/LP11-LP51.csv", 'turquoise')
# ]


# for data_dir, color in data_directory:
#     data = genfromtxt(data_dir, delimiter=',').T
#     artist = Line(x=data[0], y=data[1], line_style="--", color=color)
#     ax.add_artist(artist)

figure.show()


# -
