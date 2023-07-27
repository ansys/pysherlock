# © 2023 ANSYS, Inc. All rights reserved.

"""Module containing types for the Layer Service."""


class PolygonalShape:
    """Contains the properties for a polygonal shape."""

    def __init__(self, points, rotation):
        """Initialize the shape properties."""
        self.points = points
        """points (length two tuples of the form (x, y)) : list[tuple[float, float]]"""
        self.rotation = rotation
        """rotation (in degrees) : float"""


class RectangularShape:
    """Contains the properties for a rectangular shape."""

    def __init__(self, length, width, center_x, center_y, rotation):
        """Initialize the shape properties."""
        self.length = length
        """length : float"""
        self.width = width
        """width : float"""
        self.center_x = center_x
        """x coordinate of center : float"""
        self.center_y = center_y
        """y coordinate of center : float"""
        self.rotation = rotation
        """rotation (in degrees) : float"""


class SlotShape:
    """Contains the properties for a slot shape."""

    def __init__(self, length, width, node_count, center_x, center_y, rotation):
        """Initialize the shape properties."""
        self.length = length
        """length : float"""
        self.width = width
        """width : float"""
        self.node_count = node_count
        """node count : int"""
        self.center_x = center_x
        """x coordinate of center : float"""
        self.center_y = center_y
        """y coordinate of center : float"""
        self.rotation = rotation
        """rotation (in degrees) : float"""


class CircularShape:
    """Contains the properties for a circular shape."""

    def __init__(self, diameter, node_count, center_x, center_y, rotation):
        """Initialize the shape properties."""
        self.diameter = diameter
        """diameter : float"""
        self.node_count = node_count
        """node count : int"""
        self.center_x = center_x
        """x coordinate of center : float"""
        self.center_y = center_y
        """y coordinate of center : float"""
        self.rotation = rotation
        """rotation (in degrees) : float"""


class PCBShape:
    """Contains the properties for a PCB shape."""
