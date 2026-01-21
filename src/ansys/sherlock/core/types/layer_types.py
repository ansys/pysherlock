# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# © 2023 ANSYS, Inc. All rights reserved.

"""Module containing types for the Layer Service."""


from typing import Optional, Union

from ansys.api.sherlock.v0 import SherlockLayerService_pb2
from pydantic import BaseModel, ValidationInfo, field_validator, model_validator
from typing_extensions import Self

from ansys.sherlock.core.types.common_types import basic_str_validator, optional_str_validator


class PolygonalShape(BaseModel):
    """Contains the properties for a polygonal shape."""

    points: list[tuple[float, float]]
    """Points (length two tuples of the form (x, y)) : list[tuple[float, float]]"""
    rotation: float
    """Rotation (in degrees) : float"""

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
    """Length : float"""
    width: float
    """Width : float"""
    center_x: float
    """X coordinate of center : float"""
    center_y: float
    """Y coordinate of center : float"""
    rotation: float
    """Rotation (in degrees) : float"""

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
    """Length : float"""
    width: float
    """Width : float"""
    node_count: int
    """Node count : int"""
    center_x: float
    """X coordinate of center : float"""
    center_y: float
    """Y coordinate of center : float"""
    rotation: float
    """Rotation (in degrees) : float"""

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
    """Diameter : float"""
    node_count: int
    """Node count : int"""
    center_x: float
    """X coordinate of center : float"""
    center_y: float
    """Y coordinate of center : float"""
    rotation: float
    """Rotation (in degrees) : float"""

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
    """ID of the potting region to update."""
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
    """ID to assign to the new potting region."""
    copy_potting_id: str
    """ID of the potting region to copy."""
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


class GetTestPointPropertiesRequest(BaseModel):
    """Return the properties for each test point given a comma-separated list of test point ids."""

    project: str
    """Name of the project."""
    cca_name: str
    """Name of the CCA containing the test point properties to return."""
    test_point_ids: Optional[str] = None
    """Optional Param: Comma-separated list of test point ids representing one or more test points.
        If this parameter is not included, then the entire list of test points for a given CCA will
        have their properties returned.
    """

    @field_validator("project", "cca_name", "test_point_ids")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @field_validator("test_point_ids")
    @classmethod
    def optional_str_validation(cls, value: Optional[str], info):
        """Allow the test_point_ids to not be set, i.e., None."""
        return optional_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.GetTestPointPropertiesRequest:
        request = SherlockLayerService_pb2.GetTestPointPropertiesRequest()
        request.project = self.project
        request.ccaName = self.cca_name
        if self.test_point_ids is not None:
            request.testPointIDs = self.test_point_ids
        return request


class GetICTFixturesPropertiesRequest(BaseModel):
    """Return the properties for each ICT fixture given a comma-separated list of fixture ids."""

    project: str
    """Name of the project."""
    cca_name: str
    """Name of the CCA containing the ict fixture properties to return."""
    ict_fixtures_ids: Optional[str] = None
    """Optional Param: Comma-separated list of ict fixture ids representing one or more ict
        fixtures.   If this parameter is not included, then the entire list of ict fixtures
        for a given CCA will have their properties returned.
    """

    @field_validator("project", "cca_name", "ict_fixtures_ids")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @field_validator("ict_fixtures_ids")
    @classmethod
    def optional_str_validation(cls, value: Optional[str], info):
        """Allow the ict_fixtures_ids to not be set, i.e., None."""
        return optional_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.GetICTFixturesPropertiesRequest:
        request = SherlockLayerService_pb2.GetICTFixturesPropertiesRequest()
        request.project = self.project
        request.ccaName = self.cca_name
        if self.ict_fixtures_ids is not None:
            request.ICTFixtureIDs = self.ict_fixtures_ids
        return request


class TestPointProperties(BaseModel):
    """Contains the properties of a test point."""

    __test__ = False  # This line is to notify pytest that this is not a test class.

    id: str
    """ID"""
    side: str
    """Side"""
    units: str
    """Units"""
    center_x: float
    """Center x-value"""
    center_y: float
    """Center y-value"""
    radius: float
    """Radius"""
    load_type: SherlockLayerService_pb2.TestPointProperties.LoadType.ValueType
    """Load type"""
    load_value: float
    """Load value"""
    load_units: str
    """Load units"""

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.TestPointProperties:
        grpc_test_point_data = SherlockLayerService_pb2.TestPointProperties()

        grpc_test_point_data.ID = self.id
        grpc_test_point_data.side = self.side
        grpc_test_point_data.units = self.units
        grpc_test_point_data.centerX = self.center_x
        grpc_test_point_data.centerY = self.center_y
        grpc_test_point_data.radius = self.radius
        grpc_test_point_data.loadType = self.load_type
        grpc_test_point_data.loadValue = self.load_value
        grpc_test_point_data.loadUnits = self.load_units

        return grpc_test_point_data

    @field_validator("side", "units", "load_type")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)


class UpdateTestPointsRequest(BaseModel):
    """Contains the properties of a test points update per project."""

    project: str
    """Name of the Sherlock project."""
    cca_name: str
    """Name of the Sherlock CCA."""
    update_test_points: list[TestPointProperties]
    """List of test points with their properties to update"""

    @field_validator("project", "cca_name")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.UpdateTestPointsRequest:
        request = SherlockLayerService_pb2.UpdateTestPointsRequest()
        request.project = self.project
        request.ccaName = self.cca_name
        if self.update_test_points is not None:
            for update_test_point in self.update_test_points:
                request.testPointProperties.append(update_test_point._convert_to_grpc())
        return request


class ICTFixtureProperties(BaseModel):
    """Contains the properties of an ict fixture."""

    id: str
    """ID"""
    type: str
    """Type"""
    units: str
    """Units"""
    side: str
    """Side"""
    height: str
    """Height"""
    material: str
    """Material"""
    state: str
    """State"""
    shape: str
    """Shape type"""
    x: str
    """Center X"""
    y: str
    """Center Y"""
    length: str
    """Length"""
    width: str
    """Width"""
    diameter: str
    """Diameter"""
    nodes: str
    """Number of nodes"""
    rotation: str
    """Degrees of rotation"""
    polygon: str
    """Coordinates of points"""
    boundary: str
    """Boundary point(s)"""
    constraints: str
    """FEA constraints"""
    chassis_material: str
    """Chassis material"""

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.ICTFixtureProperties:
        grpc_fixture_data = SherlockLayerService_pb2.ICTFixtureProperties()

        grpc_fixture_data.ID = self.id
        grpc_fixture_data.type = self.type
        grpc_fixture_data.units = self.units
        grpc_fixture_data.side = self.side
        grpc_fixture_data.height = self.height
        grpc_fixture_data.material = self.material
        grpc_fixture_data.state = self.state
        grpc_fixture_data.shape = self.shape
        grpc_fixture_data.x = self.x
        grpc_fixture_data.y = self.y
        grpc_fixture_data.length = self.length
        grpc_fixture_data.width = self.width
        grpc_fixture_data.diameter = self.diameter
        grpc_fixture_data.nodes = self.nodes
        grpc_fixture_data.rotation = self.rotation
        grpc_fixture_data.polygon = self.polygon
        grpc_fixture_data.boundary = self.boundary
        grpc_fixture_data.constraints = self.constraints
        grpc_fixture_data.chassisMaterial = self.chassis_material

        return grpc_fixture_data

    @field_validator("type", "units", "side", "state", "shape")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)


class UpdateICTFixturesRequest(BaseModel):
    """Contains the properties of an ict fixtures update per project."""

    project: str
    """Name of the Sherlock project."""
    cca_name: str
    """Name of the Sherlock CCA."""
    update_fixtures: list[ICTFixtureProperties]
    """List of ict fixtures with their properties to update"""

    @field_validator("project", "cca_name")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.UpdateICTFixturesRequest:
        request = SherlockLayerService_pb2.UpdateICTFixturesRequest()
        request.project = self.project
        request.ccaName = self.cca_name
        if self.update_fixtures is not None:
            for update_fixture in self.update_fixtures:
                request.ICTFixtureProperties.append(update_fixture._convert_to_grpc())
        return request


class MountPointProperties(BaseModel):
    """Contains the properties of a mount point."""

    id: str
    """ID"""
    type: str
    """Type"""
    shape: str
    """Shape type"""
    units: str
    """Units"""
    x: float
    """Center X"""
    y: float
    """Center Y"""
    length: float
    """Length"""
    width: float
    """Width"""
    diameter: float
    """Diameter"""
    nodes: str
    """Number of nodes"""
    rotation: float
    """Degrees of rotation"""
    side: str
    """Side"""
    height: float
    """Height"""
    material: str
    """Material"""
    boundary: str
    """Boundary point(s)"""
    constraints: str
    """FEA constraints"""
    polygon: str
    """Coordinates of points"""
    state: str
    """State"""
    chassis_material: str
    """Chassis material"""

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.MountPointProperties:
        grpc_mount_point_data = SherlockLayerService_pb2.MountPointProperties()

        grpc_mount_point_data.ID = self.id
        grpc_mount_point_data.type = self.type
        grpc_mount_point_data.shape = self.shape
        grpc_mount_point_data.units = self.units
        grpc_mount_point_data.x = str(self.x)
        grpc_mount_point_data.y = str(self.y)
        grpc_mount_point_data.length = str(self.length)
        grpc_mount_point_data.width = str(self.width)
        grpc_mount_point_data.diameter = str(self.diameter)
        grpc_mount_point_data.nodes = self.nodes
        grpc_mount_point_data.rotation = str(self.rotation)
        grpc_mount_point_data.side = self.side
        grpc_mount_point_data.height = str(self.height)
        grpc_mount_point_data.material = self.material
        grpc_mount_point_data.boundary = self.boundary
        grpc_mount_point_data.constraints = self.constraints
        grpc_mount_point_data.polygon = self.polygon
        grpc_mount_point_data.state = self.state
        grpc_mount_point_data.chassisMaterial = self.chassis_material

        return grpc_mount_point_data

    @field_validator("type", "shape", "units", "side", "state")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)


class GetMountPointsPropertiesRequest(BaseModel):
    """Return the properties for each mount point given a comma-separated list of mount point ids."""  # noqa: E501

    project: str
    """Name of the project."""
    cca_name: str
    """Name of the CCA containing the mount point properties to return."""
    mount_point_ids: Optional[str] = None
    """Optional Param: Comma-separated list of mount point ids representing one or more mount
        points. If this parameter is not included, then the entire list of mount points
        for a given CCA will have their properties returned.
    """

    @field_validator("project", "cca_name", "mount_point_ids")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @field_validator("mount_point_ids")
    @classmethod
    def optional_str_validation(cls, value: Optional[str], info):
        """Allow the mount_point_ids to not be set, i.e., None."""
        return optional_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.GetMountPointsPropertiesRequest:
        request = SherlockLayerService_pb2.GetMountPointsPropertiesRequest()
        request.project = self.project
        request.ccaName = self.cca_name
        if self.mount_point_ids is not None:
            request.mountPointIDs = self.mount_point_ids
        return request


class UpdateMountPointsRequest(BaseModel):
    """Contains the properties of a mount point update per project."""

    project: str
    """Name of the Sherlock project."""
    cca_name: str
    """Name of the Sherlock CCA."""
    mount_points: list[MountPointProperties]
    """List of mount points with their properties to update"""

    @field_validator("project", "cca_name")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    @field_validator("mount_points")
    @classmethod
    def list_validation(cls, value: list, info: ValidationInfo):
        """Validate that mount_points is not empty."""
        if not value:
            raise ValueError(f"{info.field_name} must contain at least one item.")
        return value

    def _convert_to_grpc(self) -> SherlockLayerService_pb2.UpdateMountPointsRequest:
        request = SherlockLayerService_pb2.UpdateMountPointsRequest()
        request.project = self.project
        request.ccaName = self.cca_name
        if self.mount_points is not None:
            for mount_point in self.mount_points:
                request.mountPointsProperties.append(mount_point._convert_to_grpc())
        else:
            raise ValueError("mount_points is invalid because it is None or empty.")

        return request
