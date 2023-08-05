# coding: utf-8
"""Skylight Parameters with instructions for generating skylights."""
from __future__ import division
import math

from honeybee.typing import float_in_range, float_positive
from honeybee.altnumber import autocalculate
from honeybee.aperture import Aperture
from honeybee.door import Door

from ladybug_geometry.geometry2d.pointvector import Point2D, Vector2D
from ladybug_geometry.geometry2d.polygon import Polygon2D
from ladybug_geometry.geometry3d.pointvector import Vector3D, Point3D
from ladybug_geometry.geometry3d.face import Face3D

import sys
if (sys.version_info < (3, 0)):  # python 2
    from itertools import izip as zip  # python 2


class _SkylightParameterBase(object):
    """Base object for all Skylight parameters.

    This object records the minimum number of the methods that must be overwritten
    on a skylight parameter object for it to be successfully be applied in
    dragonfly workflows.
    """
    __slots__ = ()

    def __init__(self):
        pass

    def area_from_face(self, face):
        """Get the skylight area generated by these parameters from a Room2D Face3D."""
        return 0

    def add_skylight_to_face(self, face, tolerance=0.01):
        """Add Apertures to a Honeybee Roof Face using these Skylight Parameters."""
        pass

    def scale(self, factor):
        """Get a scaled version of these SkylightParameters.

        This method is called within the scale methods of the Room2D.

        Args:
            factor: A number representing how much the object should be scaled.
        """
        return self

    @classmethod
    def from_dict(cls, data):
        """Create SkylightParameterBase from a dictionary.

        .. code-block:: python

            {
            "type": "SkylightParameterBase"
            }
        """
        assert data['type'] == 'SkylightParameterBase', \
            'Expected SkylightParameterBase dictionary. Got {}.'.format(data['type'])
        return cls()

    def to_dict(self):
        """Get SkylightParameterBase as a dictionary."""
        return {'type': 'SkylightParameterBase'}

    def duplicate(self):
        """Get a copy of this object."""
        return self.__copy__()

    def ToString(self):
        return self.__repr__()

    def __copy__(self):
        return _SkylightParameterBase()

    def __repr__(self):
        return 'SkylightParameterBase'


class GriddedSkylightRatio(_SkylightParameterBase):
    """Instructions for gridded skylights derived from an area ratio with the roof.

    Args:
        skylight_ratio: A number between 0 and 0.75 for the ratio between the skylight
            area and the total Roof face area.
        spacing: A number for the spacing between the centers of each grid cell.
            This should be less than a third of the dimension of the Roof geometry
            if multiple, evenly-spaced skylights are desired. If None or Autocalculate,
            a spacing of one third the smaller dimension of the parent Roof will
            be automatically assumed. (Default: Autocalculate).

    Properties:
        * skylight_ratio
        * spacing
    """
    __slots__ = ('_skylight_ratio', '_spacing')

    def __init__(self, skylight_ratio, spacing=autocalculate):
        """Initialize GriddedSkylightRatio."""
        self._skylight_ratio = float_in_range(skylight_ratio, 0, 0.75, 'skylight ratio')
        if spacing == autocalculate:
            spacing = None
        elif spacing is not None:
            spacing = float_positive(spacing, 'skylight spacing')
            assert spacing > 0, 'GriddedSkylightRatio spacing must be greater than zero.'
        self._spacing = spacing

    @property
    def skylight_ratio(self):
        """Get a number between 0 and 0.75 for the skylight ratio."""
        return self._skylight_ratio

    @property
    def spacing(self):
        """Get a number or the spacing between the skylights.

        None indicates that the spacing will always be one third of the smaller
        dimension of the parent Roof.
        """
        return self._spacing

    def area_from_segment(self, face):
        """Get the skylight area generated by these parameters from a Room2D Face3D.

        Args:
            face: A Roof Face3D to which these parameters are applied.
        """
        return face.area * self._skylight_ratio

    def add_skylight_to_face(self, face, tolerance=0.01):
        """Add Apertures to a Honeybee Roof Face using these Skylight Parameters.

        Args:
            face: A honeybee-core Face object.
            tolerance: The maximum difference between point values for them to be
                considered distinct. (Default: 0.01, suitable for objects in meters).
        """
        if self._skylight_ratio == 0:
            return None
        spacing = self.spacing
        if self.spacing is None:
            min_pt, max_pt = face.min, face.max
            min_dim = min(max_pt.x - min_pt.x, max_pt.y - min_pt.y)
            spacing = (min_dim / 3) - tolerance
        face.apertures_by_ratio_gridded(
            self.skylight_ratio, spacing, tolerance=tolerance)

    def scale(self, factor):
        """Get a scaled version of these SkylightParameters.

        This method is called within the scale methods of the Room2D.

        Args:
            factor: A number representing how much the object should be scaled.
        """
        spc = self.spacing * factor if self.spacing is not None else None
        return GriddedSkylightRatio(self.skylight_ratio, spc)

    @classmethod
    def from_dict(cls, data):
        """Create GriddedSkylightRatio from a dictionary.

        .. code-block:: python

            {
            "type": "GriddedSkylightRatio",
            "skylight_ratio": 0.05,
            "spacing": 2
            }
        """
        assert data['type'] == 'GriddedSkylightRatio', \
            'Expected GriddedSkylightRatio dictionary. Got {}.'.format(data['type'])
        spc = data['spacing'] if 'spacing' in data and \
            data['spacing'] != autocalculate.to_dict() else None
        return cls(data['skylight_ratio'], spc)

    def to_dict(self):
        """Get GriddedSkylightRatio as a dictionary."""
        base = {'type': 'GriddedSkylightRatio', 'skylight_ratio': self.skylight_ratio}
        if self.spacing is not None:
            base['spacing'] = self.spacing
        return base

    def __copy__(self):
        return GriddedSkylightRatio(
            self.skylight_ratio, self.spacing)

    def __key(self):
        """A tuple based on the object properties, useful for hashing."""
        return (self.skylight_ratio, self.spacing)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, GriddedSkylightRatio) and self.__key() == other.__key()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'GriddedSkylightRatio: [ratio: {}]'.format(self.skylight_ratio)


class DetailedSkylights(_SkylightParameterBase):
    """Instructions for detailed skylights, defined by 2D Polygons (lists of 2D vertices).

    Note that these parameters are intended to represent skylights that are specific
    to a particular Room2D and, unlike the other SkylightsParameters, this class
    performs no automatic checks to ensure that the skylights lie within the
    boundary of the Roof that they are assigned to.

    Args:
        polygons: An array of ladybug_geometry Polygon2D objects in world XY
            coordinates with one polygon for each skylight. These coordinate
            values should lie within the Room2D's Polygon2D.
        are_doors: An array of booleans that align with the polygons and note whether
            each of the polygons represents an overhead door (True) or a skylight
            (False). If None, it will be assumed that all polygons represent skylights
            and they will be translated to Apertures in any resulting Honeybee
            model. (Default: None).

    Properties:
        * polygons
        * are_doors
    """
    __slots__ = ('_polygons', '_are_doors')

    def __init__(self, polygons, are_doors=None):
        """Initialize DetailedSkylights."""
        if not isinstance(polygons, tuple):
            polygons = tuple(polygons)
        for polygon in polygons:
            assert isinstance(polygon, Polygon2D), \
                'Expected Polygon2D for skylight polygon. Got {}'.format(type(polygon))
        assert len(polygons) != 0, \
            'There must be at least one polygon to use DetailedSkylights.'
        self._polygons = polygons
        if are_doors is None:
            self._are_doors = (False,) * len(polygons)
        else:
            if not isinstance(are_doors, tuple):
                are_doors = tuple(are_doors)
            for is_dr in are_doors:
                assert isinstance(is_dr, bool), 'Expected booleans for ' \
                    'DetailedSkylights.are_doors. Got {}'.format(type(is_dr))
            assert len(are_doors) == len(polygons), \
                'Length of DetailedSkylights.are_doors ({}) does not match the length ' \
                'of DetailedSkylights.polygons ({}).'.format(
                    len(are_doors), len(polygons))
            self._are_doors = are_doors

    @property
    def polygons(self):
        """Get an array of Polygon2Ds with one polygon for each skylight."""
        return self._polygons

    @property
    def are_doors(self):
        """Get an array of booleans that note whether each polygon is a door."""
        return self._are_doors

    def area_from_segment(self, face):
        """Get the skylight area generated by these parameters from a Room2D Face3D.

        Args:
            face: A Roof Face3D to which these parameters are applied.
        """
        return sum(polygon.area for polygon in self._polygons)

    def check_valid_for_face(self, face):
        """Check that these skylight parameters are valid for a given Face3D.

        Args:
            face: A Roof Face3D to which these parameters are applied.

        Returns:
            A string with the message. Will be an empty string if valid.
        """
        # first check that the total skylight area isn't larger than the roof
        total_area = face.area
        win_area = self.area_from_segment(face)
        if win_area >= total_area:
            return 'Total area of skylights [{}] is greater than the area of the ' \
                'parent roof [{}].'.format(win_area, total_area)
        # next, check to be sure that no skylight is out of the roof boundary
        msg_template = 'Skylight polygon {} is outside the range allowed ' \
            'by the parent roof.'
        verts2d = tuple(Point2D(pt.x, pt.y) for pt in face.boundary)
        parent_poly, parent_holes = Polygon2D(verts2d), None
        if face.has_holes:
            parent_holes = tuple(
                tuple(Point2D(pt.x, pt.y) for pt in hole)
                for hole in face.holes
            )
        for i, p_gon in enumerate(self.polygons):
            if not self._is_sub_polygon(p_gon, parent_poly, parent_holes):
                return msg_template.format(i)
        return ''

    def add_skylight_to_face(self, face, tolerance=0.01):
        """Add Apertures to a Honeybee Roof Face using these Skylight Parameters.

        Args:
            face: A honeybee-core Face object.
            tolerance: The maximum difference between point values for them to be
                considered distinct. (Default: 0.01, suitable for objects in meters).
        """
        # get the polygons that represent the roof face
        verts2d = tuple(Point2D(pt.x, pt.y) for pt in face.geometry.boundary)
        parent_poly, parent_holes = Polygon2D(verts2d), None
        if face.geometry.has_holes:
            parent_holes = tuple(
                tuple(Point2D(pt.x, pt.y) for pt in hole)
                for hole in face.geometry.holes
            )
        # loop through each polygon and create its geometry
        p_dir = Vector3D(0, 0, 1)
        for i, (polygon, isd) in enumerate(zip(self.polygons, self.are_doors)):
            if not self._is_sub_polygon(polygon, parent_poly, parent_holes):
                continue
            pt3d = tuple(
                face.geometry.plane.project_point(Point3D(p.x, p.y, 0), p_dir)
                for p in polygon)
            s_geo = Face3D(pt3d)
            if isd:
                sub_f = Door('{}_Door{}'.format(face.identifier, i + 1), s_geo)
                face.add_door(sub_f)
            else:
                sub_f = Aperture('{}_Glz{}'.format(face.identifier, i + 1), s_geo)
                face.add_aperture(sub_f)

    def move(self, moving_vec):
        """Get this DetailedSkylights moved along a vector.

        Args:
            moving_vec: A Vector3D with the direction and distance to move the polygon.
        """
        vec2 = Vector2D(moving_vec.x, moving_vec.y)
        return DetailedSkylights(
            tuple(polygon.move(vec2) for polygon in self.polygons),
            self.are_doors)

    def scale(self, factor, origin=None):
        """Get a scaled version of these DetailedSkylights.

        This method is called within the scale methods of the Room2D.

        Args:
            factor: A number representing how much the object should be scaled.
            origin: A ladybug_geometry Point3D representing the origin from which
                to scale. If None, it will be scaled from the World origin (0, 0, 0).
        """
        ori = Point2D(origin.x, origin.y) if origin is not None else None
        return DetailedSkylights(
            tuple(polygon.scale(factor, ori) for polygon in self.polygons),
            self.are_doors)

    def rotate(self, angle, origin):
        """Get these DetailedSkylights rotated counterclockwise in the XY plane.

        Args:
            angle: An angle in degrees.
            origin: A ladybug_geometry Point3D for the origin around which the
                object will be rotated.
        """
        ori, ang = Point2D(origin.x, origin.y), math.radians(angle)
        return DetailedSkylights(
            tuple(polygon.rotate(ang, ori) for polygon in self.polygons),
            self.are_doors)

    def reflect(self, plane):
        """Get a reflected version of these DetailedSkylights across a plane.

        Args:
            plane: A ladybug_geometry Plane across which the object will be reflected.
        """
        # get the plane normal and origin in 2D space
        normal = Vector2D(plane.n.x, plane.n.y)
        origin = Point2D(plane.o.x, plane.o.y)
        # loop through the polygons and reflect them across the plane
        new_polygons = []
        for polygon in self.polygons:
            new_verts = tuple(pt.reflect(normal, origin) for pt in polygon.vertices)
            new_polygons.append(Polygon2D(tuple(reversed(new_verts))))
        return DetailedSkylights(new_polygons, self.are_doors)

    @classmethod
    def from_dict(cls, data):
        """Create DetailedSkylights from a dictionary.

        Args:
            data: A dictionary in the format below.

        .. code-block:: python

            {
            "type": "DetailedSkylights",
            "polygons": [((0.5, 0.5), (2, 0.5), (2, 2), (0.5, 2)),
                         ((3, 1), (4, 1), (4, 2))],
            "are_doors": [False]
            }
        """
        assert data['type'] == 'DetailedSkylights', \
            'Expected DetailedSkylights dictionary. Got {}.'.format(data['type'])
        are_doors = data['are_doors'] if 'are_doors' in data else None
        return cls(
            tuple(Polygon2D(tuple(Point2D.from_array(pt) for pt in poly))
                  for poly in data['polygons']),
            are_doors
        )

    def to_dict(self):
        """Get DetailedSkylights as a dictionary."""
        return {
            'type': 'DetailedSkylights',
            'polygons': [[pt.to_array() for pt in poly] for poly in self.polygons],
            'are_doors': self.are_doors
        }

    @staticmethod
    def _is_sub_polygon(sub_poly, parent_poly, parent_holes=None):
        """Check if a sub-polygon is valid for a given assumed parent polygon.

        Args:
            sub_poly: A sub-Polygon2D for which sub-face equivalency will be tested.
            parent_poly: A parent Polygon2D.
            parent_holes: An optional list of Polygon2D for any holes that may
                exist in the parent polygon. (Default: None).
        """
        if parent_holes is None:
            return parent_poly.is_polygon_inside(sub_poly)
        else:
            if not parent_poly.is_polygon_inside(sub_poly):
                return False
            for hole_poly in parent_holes:
                if not hole_poly.is_polygon_outside(sub_poly):
                    return False
            return True

    def __copy__(self):
        return DetailedSkylights(self._polygons, self._are_doors)

    def __key(self):
        """A tuple based on the object properties, useful for hashing."""
        return tuple(hash(polygon) for polygon in self._polygons) + self.are_doors

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return isinstance(other, DetailedSkylights) and \
            len(self._polygons) == len(other._polygons)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return 'DetailedSkylights: [{} windows]'.format(len(self._polygons))
