# © 2023 ANSYS, Inc. All rights reserved.

"""Module containing types for the Stackup Service."""


class StackupProperties:
    """Stackup property values."""

    def __init__(self, properties):
        """Initialize members from the properties."""
        self.board_dimension = properties.boardDimension
        self.board_thickness = properties.boardThickness
        self.density = properties.density
        self.conductor_layers_cnt = properties.conductorLayersCnt
        self.ctexy = properties.ctExy
        self.ctez = properties.ctEz
        self.exy = properties.exy
        self.ez = properties.ez
