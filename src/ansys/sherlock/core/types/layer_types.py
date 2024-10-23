# © 2023 ANSYS, Inc. All rights reserved.
"""Module containing types for the Layer Service."""


from typing import Union

from ansys.api.sherlock.v0 import SherlockLayerService_pb2
from pydantic import BaseModel, ValidationInfo, field_validator

from ansys.sherlock.core.types.common_types import basic_str_validator


class PolygonalShape(BaseModel):
    """Contains the properties for a polygonal shape."""

    points: list[tuple[float, float]]
    """points (length two tuples of the form (x, y)) : list[tuple[float, float]]"""
    rotation: float
    """rotation (in degrees) : float"""

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.PolygonalShape:
        grpc_polygonal_shape = SherlockLayerService_pb2.PolygonalShape()
        for x, y in self.points:
            p = grpc_polygonal_shape.points.add()
            p.x = x
            p.y = y
        grpc_polygonal_shape.rotation = self.rotation
        return grpc_polygonal_shape


class RectangularShape(BaseModel):
    """Contains the properties for a rectangular shape."""

    length: float
    """length : float"""
    width: float
    """width : float"""
    center_x: float
    """x coordinate of center : float"""
    center_y: float
    """y coordinate of center : float"""
    rotation: float
    """rotation (in degrees) : float"""

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.RectangularShape:
        grpc_rectangular_shape = SherlockLayerService_pb2.RectangularShape()
        grpc_rectangular_shape.length = self.length
        grpc_rectangular_shape.width = self.width
        grpc_rectangular_shape.centerX = self.center_x
        grpc_rectangular_shape.centerY = self.center_y
        grpc_rectangular_shape.rotation = self.rotation
        return grpc_rectangular_shape


class SlotShape(BaseModel):
    """Contains the properties for a slot shape."""

    length: float
    """length : float"""
    width: float
    """width : float"""
    node_count: int
    """node count : int"""
    center_x: float
    """x coordinate of center : float"""
    center_y: float
    """y coordinate of center : float"""
    rotation: float
    """rotation (in degrees) : float"""

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.SlotShape:
        grpc_slot_shape = SherlockLayerService_pb2.SlotShape

        grpc_slot_shape.length = self.length
        grpc_slot_shape.width = self.width
        grpc_slot_shape.nodeCount = self.node_count
        grpc_slot_shape.centerX = self.center_x
        grpc_slot_shape.centerY = self.center_y
        grpc_slot_shape.rotation = self.rotation

        return grpc_slot_shape


class CircularShape(BaseModel):
    """Contains the properties for a circular shape."""

    diameter: float
    """diameter : float"""
    node_count: int
    """node count : int"""
    center_x: float
    """x coordinate of center : float"""
    center_y: float
    """y coordinate of center : float"""
    rotation: float
    """rotation (in degrees) : float"""

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.CircularShape:
        grpc_circular_shape = SherlockLayerService_pb2.CircularShape()
        grpc_circular_shape.diameter = self.diameter
        grpc_circular_shape.nodeCount = self.node_count
        grpc_circular_shape.centerX = self.center_x
        grpc_circular_shape.centerY = self.center_y
        grpc_circular_shape.rotation = self.rotation
        return grpc_circular_shape


class PCBShape(BaseModel):
    """Contains the properties for a PCB shape."""

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.PCBShape:
        return SherlockLayerService_pb2.PCBShape()


class PottingRegionData(BaseModel):
    """Contains the properties of a Potting Region add or update request."""

    cca_name: str
    """The name of the CCA."""
    potting_id: str
    """The potting ID."""
    potting_side: str
    """The potting side, options are "TOP", "BOT", or "BOTTOM"."""
    potting_material: str
    """The potting material."""
    potting_units: str
    """The units to use for the potting region."""
    potting_thickness: float
    """The potting thickness."""
    potting_standoff: float
    """The potting standoff."""
    shape: Union[CircularShape, PCBShape, PolygonalShape, RectangularShape, SlotShape]
    """The shape of the potting region."""

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.PottingRegion:
        grpc_potting_region_data = SherlockLayerService_pb2.PottingRegion()

        grpc_potting_region_data.ccaName = self.cca_name
        grpc_potting_region_data.pottingID = self.potting_id
        grpc_potting_region_data.pottingSide = self.potting_side
        grpc_potting_region_data.pottingMaterial = self.potting_material
        grpc_potting_region_data.pottingUnits = self.potting_units
        grpc_potting_region_data.pottingThickness = self.potting_thickness
        grpc_potting_region_data.pottingStandoff = self.potting_standoff

        if isinstance(self.shape, CircularShape):
            grpc_potting_region_data.circularShape.CopyFrom(self.shape._convert_to_grpc())
        elif isinstance(self.shape, PCBShape):
            grpc_potting_region_data.pcbShape.CopyFrom(self.shape._convert_to_grpc())
        elif isinstance(self.shape, PolygonalShape):
            grpc_potting_region_data.polygonalShape.CopyFrom(self.shape._convert_to_grpc())
        elif isinstance(self.shape, RectangularShape):
            grpc_potting_region_data.rectangularShape.CopyFrom(self.shape._convert_to_grpc())
        elif isinstance(self.shape, SlotShape):
            grpc_potting_region_data.slotShape.CopyFrom(self.shape._convert_to_grpc())
        else:
            raise ValueError("Unsupported shape given '" + type(self.shape).__name__ + "'")

        return grpc_potting_region_data

    @field_validator("cca_name", "potting_id", "potting_side", "potting_material", "potting_units")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)


class PottingRegionUpdateData(BaseModel):
    """Contains the properties of a potting region update request."""

    potting_region_id_to_update: str
    potting_region: PottingRegionData

    def _convert_to_grpc(
        self,
    ) -> SherlockLayerService_pb2.UpdatePottingRegionRequest.PottingRegionUpdateData:

        grpc_potting_update_data = (
            SherlockLayerService_pb2.UpdatePottingRegionRequest.PottingRegionUpdateData()
        )

        grpc_potting_update_data.pottingRegionIDToUpdate = self.potting_region_id_to_update
        grpc_potting_update_data.pottingRegion.CopyFrom(self.potting_region._convert_to_grpc())
        return grpc_potting_update_data

    @field_validator("potting_region_id_to_update")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)
