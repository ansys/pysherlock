# © 2023 ANSYS, Inc. All rights reserved.

"""Module containing types for the Layer Service."""


class PolygonalShape:
    """Contains the properties for a polygonal shape."""

    def __init__(self, points, rotation):
        """Initialize the shape properties."""
        self.points = points
        self.rotation = rotation


class RectangularShape:
    """Contains the properties for a rectangular shape."""

    def __init__(self, length, width, center_x, center_y, rotation):
        """Initialize the shape properties."""
        self.length = length
        self.width = width
        self.center_x = center_x
        self.center_y = center_y
        self.rotation = rotation


class SlotShape:
    """Contains the properties for a slot shape."""

    def __init__(self, length, width, node_count, center_x, center_y, rotation):
        """Initialize the shape properties."""
        self.length = length
        self.width = width
        self.node_count = node_count
        self.center_x = center_x
        self.center_y = center_y
        self.rotation = rotation


class CircularShape:
    """Contains the properties for a circular shape."""

    def __init__(self, diameter, node_count, center_x, center_y, rotation):
        """Initialize the shape properties."""
        self.diameter = diameter
        self.node_count = node_count
        self.center_x = center_x
        self.center_y = center_y
        self.rotation = rotation


class PCBShape:
    """Contains the properties for a PCB shape."""
