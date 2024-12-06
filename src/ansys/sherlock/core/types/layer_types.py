# © 2023 ANSYS, Inc. All rights reserved.
"""Module containing types for the Layer Service."""


from typing import Union

from ansys.api.sherlock.v0 import SherlockLayerService_pb2
from pydantic import BaseModel, ValidationInfo, field_validator, model_validator
from typing_extensions import Self

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
        grpc_slot_shape = SherlockLayerService_pb2.SlotShape()

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

    @staticmethod
    def _convert_to_grpc() -> SherlockLayerService_pb2.PCBShape:
        return SherlockLayerService_pb2.PCBShape()


class PottingRegion(BaseModel):
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
            grpc_potting_region_data.pCBShape.CopyFrom(self.shape._convert_to_grpc())
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
    """Id of the potting region to update."""
    potting_region: PottingRegion
    """Potting region data used to update the potting region."""

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


class UpdatePottingRegionRequest(BaseModel):
    """Contains the properties of a potting region update per project."""

    project: str
    """Name of the Sherlock project."""
    update_potting_regions: list[PottingRegionUpdateData]
    """List of potting region data to update."""

    @field_validator("project")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(
        self,
    ) -> SherlockLayerService_pb2.UpdatePottingRegionRequest:
        request = SherlockLayerService_pb2.UpdatePottingRegionRequest()
        request.project = self.project
        for update_potting_region in self.update_potting_regions:
            request.updatePottingRegions.append(update_potting_region._convert_to_grpc())
        return request


class PottingRegionCopyData(BaseModel):
    """Data identifying which potting regions to copy."""

    cca_name: str
    """Name of the cca."""
    potting_id: str
    """Id to assign to the new potting region."""
    copy_potting_id: str
    """Id of the potting region to copy."""
    center_x: float
    """X coordinate for the center of the new potting region."""
    center_y: float
    """Y coordinate for the center of the new potting region."""

    @field_validator("cca_name", "potting_id", "copy_potting_id")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @model_validator(mode="after")
    def validate_ids(self) -> Self:
        """Validate that the potting IDs are not the same between the original and copy."""
        if self.potting_id == self.copy_potting_id:
            raise ValueError("potting_id must be different than copy_potting_id")
        return self

    def _convert_to_grpc(
        self,
    ) -> SherlockLayerService_pb2.CopyPottingRegionRequest.PottingRegionCopyData:

        grpc_potting_copy_data = (
            SherlockLayerService_pb2.CopyPottingRegionRequest.PottingRegionCopyData()
        )

        grpc_potting_copy_data.ccaName = self.cca_name
        grpc_potting_copy_data.pottingID = self.potting_id
        grpc_potting_copy_data.copyPottingID = self.copy_potting_id
        grpc_potting_copy_data.centerX = self.center_x
        grpc_potting_copy_data.centerY = self.center_y

        return grpc_potting_copy_data


class CopyPottingRegionRequest(BaseModel):
    """Request to delete 1 or more potting regions."""

    project: str
    """Name of the project containing the potting region(s) to be copied."""
    potting_region_copy_data: list[PottingRegionCopyData]
    """Data identifying which potting regions to copy and what potting regions to copy from."""

    @field_validator("project")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(
        self,
    ) -> SherlockLayerService_pb2.CopyPottingRegionRequest:

        grpc_potting_copy_request = SherlockLayerService_pb2.CopyPottingRegionRequest()
        grpc_potting_copy_request.project = self.project
        for copy_data in self.potting_region_copy_data:
            grpc_potting_copy_request.pottingRegionCopyData.append(copy_data._convert_to_grpc())

        return grpc_potting_copy_request


class PottingRegionDeleteData(BaseModel):
    """Data specifying potting regions to delete."""

    cca_name: str
    """Name of the CCA containing the potting region(s) to delete."""
    potting_id: str
    """Id of the potting region(s) to delete."""

    @field_validator("cca_name", "potting_id")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(
        self,
    ) -> SherlockLayerService_pb2.DeletePottingRegionRequest.PottingRegionDeleteData:
        delete_data = SherlockLayerService_pb2.DeletePottingRegionRequest.PottingRegionDeleteData()

        delete_data.ccaName = self.cca_name
        delete_data.pottingID = self.potting_id
        return delete_data


class DeletePottingRegionRequest(BaseModel):
    """Request to delete 1 or more potting regions."""

    project: str
    """Name of the project containing the potting regions to delete."""
    potting_region_delete_data: list[PottingRegionDeleteData]
    """Data identifying which potting regions should be deleted."""

    @field_validator("project")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.DeletePottingRegionRequest:
        request = SherlockLayerService_pb2.DeletePottingRegionRequest()
        request.project = self.project
        for delete_data in self.potting_region_delete_data:
            request.pottingRegionDeleteData.append(delete_data._convert_to_grpc())
        return request
