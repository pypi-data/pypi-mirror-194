#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy
import matplotlib.pyplot as plt
import itertools


# 4th order accurate gradient function based on 2nd order version from http://projects.scipy.org/scipy/numpy/browser/trunk/numpy/lib/function_base.py
def gradientO4(f, *varargs):
    """Calculate the fourth-order-accurate gradient of an N-dimensional scalar function.
    Uses central differences on the interior and first differences on boundaries
    to give the same shape.
    Inputs:
      f -- An N-dimensional array giving samples of a scalar function
      varargs -- 0, 1, or N scalars giving the sample distances in each direction
    Outputs:
      N arrays of the same shape as f giving the derivative of f with respect
       to each dimension.
    """
    N = len(f.shape)  # number of dimensions
    n = len(varargs)
    dx = list(varargs)

    # use central differences on interior and first differences on endpoints

    outvals = []

    # create slice objects --- initially all are [:, :, ..., :]
    slice0 = [slice(None)] * N
    slice1 = [slice(None)] * N
    slice2 = [slice(None)] * N
    slice3 = [slice(None)] * N
    slice4 = [slice(None)] * N

    otype = f.dtype.char
    if otype not in ['f', 'd', 'F', 'D']:
        otype = 'd'

    for axis in range(N):
        # select out appropriate parts for this dimension
        out = numpy.zeros(f.shape, f.dtype.char)

        slice0[axis] = slice(2, -2)
        slice1[axis] = slice(None, -4)
        slice2[axis] = slice(1, -3)
        slice3[axis] = slice(3, -1)
        slice4[axis] = slice(4, None)
        # 1D equivalent -- out[2:-2] = (f[:4] - 8*f[1:-3] + 8*f[3:-1] - f[4:])/12.0
        out[tuple(slice0)] = (f[tuple(slice1)] - 8.0 * f[tuple(slice2)] + 8.0 * f[tuple(slice3)] - f[tuple(slice4)])/12.0

        slice0[axis] = slice(None, 2)
        slice1[axis] = slice(1, 3)
        slice2[axis] = slice(None, 2)
        # 1D equivalent -- out[0:2] = (f[1:3] - f[0:2])
        out[tuple(slice0)] = (f[tuple(slice1)] - f[tuple(slice2)])

        slice0[axis] = slice(-2, None)
        slice1[axis] = slice(-2, None)
        slice2[axis] = slice(-3, -1)
        # 1D equivalent -- out[-2:] = (f[-2:] - f[-3:-1])
        out[tuple(slice0)] = (f[tuple(slice1)] - f[tuple(slice2)])

        # divide by step size
        outvals.append(out / dx[axis])

        # reset the slice object in this dimension to ":"
        slice0[axis] = slice(None)
        slice1[axis] = slice(None)
        slice2[axis] = slice(None)
        slice3[axis] = slice(None)
        slice4[axis] = slice(None)

    if N == 1:
        return outvals[0]
    else:
        return outvals

def get_3_figures():

    fig = plt.figure(figsize=(8, 6))

    gs = fig.add_gridspec(2, 2,
                          width_ratios=(1, 1),
                          height_ratios=(1, 1),
                          left=0.1,
                          right=0.9,
                          bottom=0.1,
                          top=0.9,
                          wspace=0.5*2,
                          hspace=0.15)

    ax0 = fig.add_subplot(gs[0, 0:])
    ax1 = fig.add_subplot(gs[1, 0])
    ax2 = fig.add_subplot(gs[1, 1])

    ax1.tick_params(
        axis='both',
        which='both',
        top=False,
        bottom=False,
        right=False,
        left=False,
        labelleft=False,
        labelbottom=False,
        grid_alpha=0
    )
    ax2.tick_params(
        axis='both',
        which='both',
        top=False,
        bottom=False,
        right=False,
        left=False,
        labelleft=False,
        labelbottom=False,
        grid_alpha=0
    )

    ax1.set_aspect('equal')
    ax2.set_aspect('equal')

    return fig, ax0, ax1, ax2


def debug_get_mode_coupling_adiabatic(superset, geometry, plot=False):
    modes = superset.supermodes
    gradient = geometry.gradient
    couplings = []
    adiabatics = []
    combinations = list(itertools.combinations(modes, 2))

    for mode_0, mode_1 in combinations:
        k = 2 * numpy.pi / modes[0].wavelength

        delta_beta = (mode_0.beta._data - mode_1.beta._data)

        time_beta = k**2 / numpy.sqrt(mode_0.beta._data * mode_1.beta._data)

        integrand = mode_0.field._data * gradient * mode_1.field._data

        integral = numpy.trapz(numpy.trapz(integrand, axis=1), axis=1)

        coupling = - 1j / 2 * time_beta * (1 / delta_beta) * integral

        couplings.append(coupling)
        adiabatics.append(abs(delta_beta / coupling))

    couplings = numpy.asarray(couplings)
    adiabatics = numpy.asarray(adiabatics)

    if plot:
        figure, axe = plt.subplots(1, 1, figsize=(12, 5))
        for n, (mode_0, mode_1) in enumerate(combinations):
            cpp_adiabatic = mode_0.adiabatic.get_values(mode_1)

            im = axe.plot(
                superset.itr_list,
                cpp_adiabatic,
                linestyle='-',
                label=f'cpp: {mode_0.name}-{mode_1.name}'
            )

            axe.plot(
                superset.itr_list,
                adiabatics[n, :],
                marker='+',
                label=f'python: {mode_0.name}-{mode_1.name}',
                color=im[0].get_color()
            )

        plt.yscale('log')
        axe.legend()
        plt.show()

    return combinations, couplings, adiabatics

# -
