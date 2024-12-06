# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

"""Module containing types for the Stackup Service."""
try:
    import SherlockStackupService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockStackupService_pb2


class StackupProperties:
    """Stackup property values."""

    def __init__(self, properties: SherlockStackupService_pb2.GetStackupPropsResponse):
        """Initialize members from the properties."""
        self.board_dimension = properties.boardDimension
        self.board_thickness = properties.boardThickness
        self.density = properties.density
        self.conductor_layers_cnt = properties.conductorLayersCnt
        self.ctexy = properties.ctExy
        self.ctez = properties.ctEz
        self.exy = properties.exy
        self.ez = properties.ez
