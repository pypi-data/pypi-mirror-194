#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy
from FiberFusing import Circle
from PyOptik import ExpData
import pprint
pp = pprint.PrettyPrinter(indent=4, sort_dicts=False, compact=True, width=1)

__all__ = ['DCF1300S_20',
           'DCF1300S_33',
           'NewA',
           'NewB',
           'NewC',
           'NewD',
           'F2028M24',
           'F2028M21',
           'F2028M12',
           'F2058G1',
           'F2058L1',
           'SMF28',
           'HP630',
           'CustomFiber',
           'get_silica_index']


def get_silica_index(wavelength: float):
    return ExpData('FusedSilica').GetRI(wavelength)[0]


micro = 1e-6


class GenericFiber():
    def __init__(self, wavelength: float, position: tuple = (0, 0)):
        self._structures = {}
        self.wavelength = wavelength
        self.position = position

        self.post_init()

    @property
    def silica_index(self):
        return ExpData('FusedSilica').GetRI(self.wavelength)[0]

    def NA_to_core_index(self, NA: float, index_clad: float):
        return numpy.sqrt(NA**2 + index_clad**2)

    def core_index_to_NA(self, interior_index: float, exterior_index: float):
        return numpy.sqrt(interior_index**2 - exterior_index**2)

    @property
    def polygones(self):
        if not self._polygones:
            self.initialize_polygones()
        return self._polygones

    @property
    def structures(self):
        return [struc['polygon'] for name, struc in self._structures.items() if name not in ['air', 'outer-clad']]

    def __repr__(self):
        pp.pprint(self._structures)
        return ""

    def add_air(self):
        self._structures['air'] = {
            "na": None,
            "radius": None,
            "index": 1,
            "V": None,
            "polygon": None
        }

    def add_next_structure(self,
                           name: str,
                           na: float,
                           radius: float):

        previous_structure_name = [*self._structures.keys()][-1]

        exterior_index = self._structures[previous_structure_name]['index']

        structure_index = self.NA_to_core_index(na, exterior_index)

        V = 2 * numpy.pi / self.wavelength * numpy.sqrt(structure_index**2 - exterior_index**2) * radius

        self._structures[name] = {
            "na": na,
            "radius": radius,
            "index": structure_index,
            "V": V,
            "polygon": Circle(position=self.position, radius=radius, index=structure_index)
        }


class CustomFiber(GenericFiber):
    def __init__(self, wavelength: float, na_list: list, radius_list: list, name_list: list = None, position: tuple = (0, 0)):
        self._structures = {}
        self.wavelength = wavelength
        self.position = position

        if name_list is None:
            name_list = [f'layer_{n}' for n in range(len(na_list))]

        self.add_air()

        for n, (na, radius) in enumerate(zip(na_list, radius_list)):
            self.add_next_structure(
                name=name_list[n],
                na=na,
                radius=radius,
            )


class DCF1300S_20(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='inner-clad',
            na=0.11,
            radius=19.9 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.12,
            radius=9.2 / 2 * micro
        )


class DCF1300S_33(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='inner-clad',
            na=0.11,
            radius=33.0 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.125,
            radius=9.0 / 2 * micro
        )


class NewA(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='inner-clad',
            na=0.11,
            radius=33.0 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.13,
            radius=9.0 / 2 * micro
        )


class NewB(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='inner-clad',
            na=0.11,
            radius=33.0 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.115,
            radius=9.0 / 2 * micro
        )


class F2028M24(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='inner-clad',
            na=0.19,
            radius=14.1 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.11,
            radius=2.3/ 2 * micro
        )


class F2028M21(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='inner-clad',
            na=0.19,
            radius=17.6 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.11,
            radius=2.8 / 2 * micro
        )


class NewC(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='inner-clad',
            na=0.11,
            radius=30.0 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.115,
            radius=9.1 / 2 * micro
        )


class NewD(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='inner-clad',
            na=0.11,
            radius=28.0 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.13,
            radius=9.3 / 2 * micro
        )


class F2058L1(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='inner-clad',
            na=0.117,
            radius=19.6 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.13,
            radius=9.0 / 2 * micro
        )


class F2058G1(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='inner-clad',
            na=0.115,
            radius=32.3 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.124,
            radius=9.0 / 2 * micro
        )


class F2028M12(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='inner-clad',
            na=0.19,
            radius=25.8 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.11,
            radius=4.1 / 2 * micro
        )


class SMF28(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.12,
            radius=8.2 / 2 * micro
        )


class HP630(GenericFiber):
    def post_init(self):
        self.add_air()

        self.add_next_structure(
            name='outer-clad',
            na=1.0417297132615746,
            radius=125 / 2 * micro
        )

        self.add_next_structure(
            name='core',
            na=0.13,
            radius=3.5 / 2 * micro
        )

# -
