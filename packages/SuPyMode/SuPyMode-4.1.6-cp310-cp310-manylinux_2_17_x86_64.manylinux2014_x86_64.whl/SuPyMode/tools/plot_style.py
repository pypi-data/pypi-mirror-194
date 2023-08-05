#!/usr/bin/env python
# -*- coding: utf-8 -*-

beta = {
    "show_legend": True,
    "x_label": 'ITR',
    "y_label": 'Propagation constant [rad/M]',
    "y_scale": "linear"
}

index = {
    "show_legend": True,
    "x_label": 'ITR',
    "y_label": 'Effective refraction index',
    "y_scale": "linear"
}

eigen_value = {
    "show_legend": True,
    "x_label": 'ITR',
    "y_label": 'Mode eigen values',
    "y_scale": "linear"
}

field = {
    "show_legend": False,
    "x_label": r'X-Direction [$\mu m$]',
    "y_label": r'Y-direction [$\mu m$]',
    "equal": True
}

adiabatic = {
    "show_legend": True,
    "x_label": 'ITR',
    "y_label": r'Adiabatic criterion [$\mu$m$^{-1}$]',
    "y_scale": 'log',
    "y_scale_factor": 1e-6,
    "y_limits": [1e-5, 1]
}

normalized_coupling = {
    "show_legend": True,
    "x_label": 'ITR',
    "y_label": 'Mode coupling',
    "y_scale": "linear"
}

overlap = {
    "show_legend": True,
    "x_label": 'ITR',
    "y_label": 'Mode overlap intergral',
    "y_scale": "linear"
}

beating_length = {
    "show_legend": True,
    "x_label": 'ITR',
    "y_label": 'Beating length [m]',
    "y_scale": "log"
}


# -
