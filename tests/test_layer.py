# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.

import copy
import os
import platform
import uuid

from ansys.api.sherlock.v0 import SherlockLayerService_pb2
import grpc
import pydantic
import pytest

from ansys.sherlock.core.errors import (
    SherlockAddModelingRegionError,
    SherlockAddPottingRegionError,
    SherlockCopyModelingRegionError,
    SherlockDeleteAllICTFixturesError,
    SherlockDeleteAllMountPointsError,
    SherlockDeleteAllTestPointsError,
    SherlockDeleteModelingRegionError,
    SherlockExportAllMountPoints,
    SherlockExportAllTestFixtures,
    SherlockExportAllTestPointsError,
    SherlockExportLayerImageError,
    SherlockListLayersError,
    SherlockUpdateModelingRegionError,
    SherlockUpdateMountPointsByFileError,
    SherlockUpdateTestFixturesByFileError,
    SherlockUpdateTestPointsByFileError,
)
from ansys.sherlock.core.layer import Layer
from ansys.sherlock.core.types.layer_types import (
    CircularShape,
    CopyPottingRegionRequest,
    DeletePottingRegionRequest,
    GetICTFixturesPropertiesRequest,
    GetTestPointPropertiesRequest,
    ICTFixtureProperties,
    PCBShape,
    PolygonalShape,
    PottingRegion,
    PottingRegionCopyData,
    PottingRegionDeleteData,
    PottingRegionUpdateData,
    RectangularShape,
    SlotShape,
    TestPointProperties,
    UpdateICTFixturesRequest,
    UpdatePottingRegionRequest,
    UpdateTestPointsRequest,
)
from ansys.sherlock.core.utils.version_check import SKIP_VERSION_CHECK
from tests.test_utils import assert_float_equals


def test_all():
    """Test all layer APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    layer = Layer(channel, SKIP_VERSION_CHECK)

    helper_test_add_potting_region(layer)
    helper_test_copy_potting_regions(layer)
    helper_test_export_all_mount_points(layer)
    helper_test_export_all_test_fixtures(layer)
    helper_test_export_all_test_points(layer)
    region_id = helper_test_add_modeling_region(layer)
    helper_test_list_layers(layer)
    helper_test_get_ict_fixtures_props(layer)
    helper_test_get_test_point_props(layer)
    helper_test_export_layer_image(layer)

    # Update APIs must be called after properties APIs so all pass
    helper_test_update_ict_fixtures(layer)
    helper_test_update_mount_points_by_file(layer)
    helper_test_update_potting_region(layer)
    helper_test_update_test_fixtures_by_file(layer)
    helper_test_update_test_points(layer)
    helper_test_update_test_points_by_file(layer)
    region_id = helper_test_update_modeling_region(layer, region_id)
    helper_test_copy_modeling_region(layer, region_id)

    # Delete APIs must be called last so that tests for update/properties APIs pass
    helper_test_delete_all_ict_fixtures(layer)
    helper_test_delete_all_mount_points(layer)
    helper_test_delete_all_test_points(layer)
    helper_test_delete_modeling_region(layer, region_id)
    helper_test_delete_potting_regions(layer)


def helper_test_add_potting_region(layer: Layer):
    """Test add_potting_region API."""
    try:
        shape = PCBShape()
        layer.add_potting_region(
            "",
            [
                {
                    "cca_name": "Main Board",
                    "potting_id": "Test Region",
                    "side": "TOP",
                    "material": "epoxyencapsulant",
                    "potting_units": "in",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": shape,
                },
            ],
        )
        pytest.fail("No exception thrown when using invalid project name.")
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Project name is invalid."

    try:
        layer.add_potting_region("Test", "")
        pytest.fail("No exception thrown when using invalid potting regions list.")
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Potting regions argument is invalid."

    try:
        layer.add_potting_region("Test", [])
        pytest.fail("No exception thrown when using empty potting regions list.")
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: One or more potting regions are required."

    try:
        layer.add_potting_region("Test", ["test"])
        pytest.fail("No exception thrown when using invalid element in potting regions list.")
    except SherlockAddPottingRegionError as e:
        assert (
            str(e) == "Add potting region error: "
            "Potting region argument is invalid for potting region 0."
        )

    try:
        shape = PCBShape()
        layer.add_potting_region(
            "Test",
            [
                {
                    "potting_id": "Test Region",
                    "side": "TOP",
                    "material": "epoxyencapsulant",
                    "potting_units": "in",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": shape,
                },
            ],
        )
        pytest.fail("No exception thrown when cca name missing.")
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: CCA name is missing for potting region 0."

    try:
        shape = PCBShape()
        layer.add_potting_region(
            "Test",
            [
                {
                    "cca_name": "",
                    "potting_id": "Test Region",
                    "side": "TOP",
                    "material": "epoxyencapsulant",
                    "potting_units": "in",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": shape,
                },
            ],
        )
        pytest.fail("No exception thrown when cca name is invalid.")
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: CCA name is invalid for potting region 0."

    try:
        layer.add_potting_region(
            "Test",
            [
                {
                    "cca_name": "Test Card",
                    "potting_id": "Test Region",
                    "side": "TOP",
                    "material": "epoxyencapsulant",
                    "potting_units": "in",
                    "thickness": 0.1,
                    "standoff": 0.2,
                },
            ],
        )
        pytest.fail("No exception thrown when shape missing.")
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Shape missing for potting region 0."

    try:
        layer.add_potting_region(
            "Test",
            [
                {
                    "cca_name": "Test Card",
                    "potting_id": "Test Region",
                    "side": "TOP",
                    "material": "epoxyencapsulant",
                    "potting_units": "in",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": "INVALID",
                },
            ],
        )
        pytest.fail("No exception thrown when shape is invalid.")
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Shape invalid for potting region 0."

    if not layer._is_connection_up():
        return

    try:
        potting_id = f"Test Region {uuid.uuid4()}"
        shape = PolygonalShape(points=[(1, 2), (4.4, 5.5), (1, 6)], rotation=123.4)
        layer.add_potting_region(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "potting_id": potting_id,
                    "side": "INVALID",
                    "material": "epoxyencapsulant",
                    "potting_units": "in",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": shape,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert type(e) == SherlockAddPottingRegionError

    try:
        potting_id = f"Test Region {uuid.uuid4()}"
        shape = PolygonalShape(points=[(1, 2), (4.4, 5.5), (1, 6)], rotation=123.4)
        result = layer.add_potting_region(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "potting_id": potting_id,
                    "side": "TOP",
                    "material": "epoxyencapsulant",
                    "potting_units": "mm",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": shape,
                },
            ],
        )
        assert result == 0
    except SherlockAddPottingRegionError as e:
        pytest.fail(str(e))


def helper_test_update_potting_region(layer: Layer):
    """Test update potting region API."""

    project = "Tutorial Project"
    # Add Potting region to update
    potting_id = f"Test Region update {uuid.uuid4()}"
    cca_name = "Main Board"
    potting_side = "TOP"
    potting_material = "epoxyencapsulant"
    potting_units = "mm"
    potting_thickness = 0.1
    potting_standoff = 0.2

    try:
        potting_region = PottingRegion(
            cca_name=cca_name,
            potting_id=potting_id,
            potting_side=potting_side,
            potting_material=potting_material,
            potting_units=potting_units,
            potting_thickness=potting_thickness,
            potting_standoff=potting_standoff,
            shape=PolygonalShape(points=[(0, 1), (5, 1), (5, 5), (1, 5)], rotation=45.0),
        )

        PottingRegionUpdateData(
            potting_region_id_to_update="",
            potting_region=potting_region,
        )
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            e.errors()[0]["msg"]
            == "Value error, potting_region_id_to_update is invalid because it is None or empty."
        )

    if layer._is_connection_up():

        potting_shape = PolygonalShape(points=[(1, 2), (4.4, 5.5), (1, 6)], rotation=0.0)

        layer.add_potting_region(
            project,
            [
                {
                    "cca_name": cca_name,
                    "potting_id": potting_id,
                    "side": potting_side,
                    "material": potting_material,
                    "potting_units": potting_units,
                    "thickness": potting_thickness,
                    "standoff": potting_standoff,
                    "shape": potting_shape,
                },
            ],
        )

        # Update potting region that was added above
        potting_regions = [
            PottingRegionUpdateData(
                potting_region_id_to_update=potting_id,
                potting_region=PottingRegion(
                    cca_name=cca_name,
                    potting_id=potting_id,
                    potting_side=potting_side,
                    potting_material=potting_material,
                    potting_units=potting_units,
                    potting_thickness=potting_thickness,
                    potting_standoff=potting_standoff,
                    shape=PolygonalShape(points=[(0, 1), (5, 1), (5, 5), (1, 5)], rotation=45.0),
                ),
            ),
            PottingRegionUpdateData(
                potting_region_id_to_update=potting_id,
                potting_region=PottingRegion(
                    cca_name=cca_name,
                    potting_id=potting_id,
                    potting_side=potting_side,
                    potting_material=potting_material,
                    potting_units=potting_units,
                    potting_thickness=potting_thickness,
                    potting_standoff=potting_standoff,
                    shape=PolygonalShape(points=[(0, 1), (5, 1), (5, 5), (1, 5)], rotation=0.0),
                ),
            ),
        ]

        request = UpdatePottingRegionRequest(
            project=project, update_potting_regions=potting_regions
        )

        responses = layer.update_potting_region(request)

        for return_code in responses:
            assert return_code.value == 0
            assert return_code.message == ""


def helper_test_copy_potting_regions(layer: Layer):

    project = "Tutorial Project"
    cca_name = "Main Board"
    potting_id = f"Test orig Region {uuid.uuid4()}"
    new_id = f"Test copy Region {uuid.uuid4()}"
    center_x = 0
    center_y = 0

    potting_side = "TOP"
    potting_material = "epoxyencapsulant"
    potting_units = "mm"
    potting_thickness = 0.1
    potting_standoff = 0.2

    try:
        PottingRegionCopyData(
            cca_name="",
            potting_id=potting_id,
            copy_potting_id=new_id,
            center_x=center_x,
            center_y=center_y,
        )
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)

    try:
        PottingRegionCopyData(
            cca_name=cca_name,
            potting_id="",
            copy_potting_id=new_id,
            center_x=center_x,
            center_y=center_y,
        )
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)

    try:
        PottingRegionCopyData(
            cca_name=cca_name,
            potting_id=potting_id,
            copy_potting_id="",
            center_x=center_x,
            center_y=center_y,
        )
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)

    try:
        PottingRegionCopyData(
            cca_name=cca_name,
            potting_id="same_id",
            copy_potting_id="same_id",
            center_x=center_x,
            center_y=center_y,
        )
        pytest.fail("Potting IDs were the same and should not be.")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)

    if layer._is_connection_up():
        potting_shape = PolygonalShape(points=[(1, 2), (4.4, 5.5), (1, 6)], rotation=0.0)

        layer.add_potting_region(
            project,
            [
                {
                    "cca_name": cca_name,
                    "potting_id": potting_id,
                    "side": potting_side,
                    "material": potting_material,
                    "potting_units": potting_units,
                    "thickness": potting_thickness,
                    "standoff": potting_standoff,
                    "shape": potting_shape,
                },
            ],
        )

        request = CopyPottingRegionRequest(
            project=project,
            potting_region_copy_data=[
                PottingRegionCopyData(
                    cca_name=cca_name,
                    potting_id=potting_id,
                    copy_potting_id=new_id,
                    center_x=center_x,
                    center_y=center_y,
                ),
                PottingRegionCopyData(
                    cca_name=cca_name,
                    potting_id=new_id,
                    copy_potting_id=new_id + "1",
                    center_x=center_x,
                    center_y=center_y,
                ),
            ],
        )

        responses = layer.copy_potting_region(request)

        for return_code in responses:
            assert return_code.value == 0
            assert return_code.message == ""


def helper_test_delete_potting_regions(layer: Layer):

    project = "Tutorial Project"
    cca_name = "Main Board"
    potting_id = f"Test Region {uuid.uuid4()}"
    potting_side = "TOP"
    potting_material = "epoxyencapsulant"
    potting_units = "mm"
    potting_thickness = 0.1
    potting_standoff = 0.2

    potting_shape = PolygonalShape(points=[(1, 2), (4.4, 5.5), (1, 6)], rotation=0.0)

    if layer._is_connection_up():
        layer.add_potting_region(
            project,
            [
                {
                    "cca_name": cca_name,
                    "potting_id": potting_id,
                    "side": potting_side,
                    "material": potting_material,
                    "potting_units": potting_units,
                    "thickness": potting_thickness,
                    "standoff": potting_standoff,
                    "shape": potting_shape,
                },
            ],
        )

        request = DeletePottingRegionRequest(
            project=project,
            potting_region_delete_data=[
                PottingRegionDeleteData(cca_name=cca_name, potting_id=potting_id)
            ],
        )
        responses = layer.delete_potting_region(request)

        for response in responses:
            assert response.value == 0


def helper_test_update_mount_points_by_file(layer):
    """Test update_mount_points_by_file API."""
    try:
        layer.update_mount_points_by_file(
            "",
            "Card",
            "MountPointImport.csv",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockUpdateMountPointsByFileError as e:
        assert e.str_itr()[0] == "Update mount points by file error: Project name is invalid."

    try:
        layer.update_mount_points_by_file(
            "Test",
            "",
            "MountPointImport.csv",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockUpdateMountPointsByFileError as e:
        assert e.str_itr()[0] == "Update mount points by file error: CCA name is invalid."

    try:
        layer.update_mount_points_by_file(
            "Test",
            "Card",
            "",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockUpdateMountPointsByFileError as e:
        assert e.str_itr()[0] == "Update mount points by file error: File path is required."

    if layer._is_connection_up():
        try:
            layer.update_mount_points_by_file(
                "Tutorial Project",
                "Invalid CCA",
                "MountPointImport.csv",
            )
            pytest.fail("No exception thrown when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdateMountPointsByFileError


def helper_test_delete_all_mount_points(layer: Layer):
    """Test delete_all_mount_points API."""
    try:
        layer.delete_all_mount_points(
            "",
            "CCA",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockDeleteAllMountPointsError as e:
        assert str(e) == "Delete mount points error: Project name is invalid."

    try:
        layer.delete_all_mount_points(
            "Tutorial Project",
            "",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockDeleteAllMountPointsError as e:
        assert str(e) == "Delete mount points error: CCA name is invalid."

    if layer._is_connection_up():
        try:
            layer.delete_all_mount_points(
                "Tutorial Project",
                "Invalid CCA",
            )
            pytest.fail("No exception thrown when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockDeleteAllMountPointsError

        try:
            result = layer.delete_all_mount_points(
                "Tutorial Project",
                "Main Board",
            )
            assert result == 0

        except SherlockDeleteAllMountPointsError as e:
            pytest.fail(e.message)


def helper_test_delete_all_ict_fixtures(layer: Layer):
    """Test delete_all_ict_fixtures API."""
    try:
        layer.delete_all_ict_fixtures(
            "",
            "CCA",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockDeleteAllICTFixturesError as e:
        assert str(e) == "Delete ict fixtures error: Project name is invalid."

    try:
        layer.delete_all_ict_fixtures(
            "Tutorial Project",
            "",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockDeleteAllICTFixturesError as e:
        assert str(e) == "Delete ict fixtures error: CCA name is invalid."

    if layer._is_connection_up():
        try:
            layer.delete_all_ict_fixtures(
                "Tutorial Project",
                "Invalid CCA",
            )
            pytest.fail("No exception thrown when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockDeleteAllICTFixturesError

        try:
            result = layer.delete_all_ict_fixtures(
                "Tutorial Project",
                "Main Board",
            )
            assert result == 0

        except SherlockDeleteAllICTFixturesError as e:
            pytest.fail(e.message)


def helper_test_delete_all_test_points(layer: Layer):
    """Test delete_all_test_points API."""
    try:
        layer.delete_all_test_points(
            "",
            "CCA",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockDeleteAllTestPointsError as e:
        assert str(e) == "Delete test points error: Project name is invalid."

    try:
        layer.delete_all_test_points(
            "Tutorial Project",
            "",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockDeleteAllTestPointsError as e:
        assert str(e) == "Delete test points error: CCA name is invalid."

    if layer._is_connection_up():
        try:
            layer.delete_all_test_points(
                "Tutorial Project",
                "Invalid CCA",
            )
            pytest.fail("No exception thrown when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockDeleteAllTestPointsError

        try:
            result = layer.delete_all_test_points(
                "Tutorial Project",
                "Main Board",
            )
            assert result == 0

        except SherlockDeleteAllTestPointsError as e:
            pytest.fail(e.message)


def helper_test_update_test_points_by_file(layer: Layer):
    """Test update_test_points_by_file API."""
    try:
        layer.update_test_points_by_file(
            "",
            "CCA",
            "TestPointImport.csv",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockUpdateTestPointsByFileError as e:
        assert e.str_itr()[0] == "Update test points by file error: Project name is invalid."

    try:
        layer.update_test_points_by_file(
            "Tutorial Project",
            "",
            "TestPointImport.csv",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockUpdateTestPointsByFileError as e:
        assert e.str_itr()[0] == "Update test points by file error: CCA name is invalid."

    try:
        layer.update_test_points_by_file(
            "Tutorial Project",
            "CCA",
            "",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockUpdateTestPointsByFileError as e:
        assert e.str_itr()[0] == "Update test points by file error: File path is required."

    if layer._is_connection_up():
        try:
            layer.update_test_points_by_file(
                "Tutorial Project",
                "Invalid CCA",
                "TestPointImport.csv",
            )
            pytest.fail("No exception thrown when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdateTestPointsByFileError


def helper_test_update_test_fixtures_by_file(layer: Layer):
    """Test update_test_fixtures_by_file API."""
    try:
        layer.update_test_fixtures_by_file(
            "",
            "CCA",
            "TestFixtureImport.csv",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockUpdateTestFixturesByFileError as e:
        assert e.str_itr()[0] == "Update test fixtures by file error: Project name is invalid."

    try:
        layer.update_test_fixtures_by_file(
            "Tutorial Project",
            "",
            "TestFixtureImport.csv",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockUpdateTestFixturesByFileError as e:
        assert e.str_itr()[0] == "Update test fixtures by file error: CCA name is invalid."

    try:
        layer.update_test_fixtures_by_file(
            "Tutorial Project",
            "CCA",
            "",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockUpdateTestFixturesByFileError as e:
        assert e.str_itr()[0] == "Update test fixtures by file error: File path is required."

    if layer._is_connection_up():
        try:
            layer.update_test_fixtures_by_file(
                "Tutorial Project",
                "Invalid CCA",
                "TestFixtureImport.csv",
            )
            pytest.fail("No exception thrown when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdateTestFixturesByFileError


def helper_test_export_all_test_points(layer: Layer):
    """Tests export_all_test_points API."""
    try:
        layer.export_all_test_points(
            "",
            "Main Board",
            "Test Points.csv",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportAllTestPointsError as e:
        assert str(e) == "Export test points error: Project name is invalid."

    try:
        layer.export_all_test_points(
            "Tutorial Project",
            "",
            "Test Points.csv",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportAllTestPointsError as e:
        assert str(e) == "Export test points error: CCA name is invalid."

    try:
        layer.export_all_test_points(
            "Tutorial Project",
            "Main Board",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportAllTestPointsError as e:
        assert str(e) == "Export test points error: File path is required."

    if layer._is_connection_up():
        if platform.system() == "Windows":
            temp_dir = os.environ.get("TEMP", "C:\\TEMP")
        else:
            temp_dir = os.environ.get("TEMP", "/tmp")
        test_points_file = os.path.join(temp_dir, "test_points.csv")

        try:
            layer.export_all_test_points(
                "Test Point Test Project",
                "Invalid CCA",
                test_points_file,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockExportAllTestPointsError

        try:
            result = layer.export_all_test_points(
                "Test Point Test Project",
                "Main Board",
                test_points_file,
            )

            assert os.path.exists(test_points_file)
            assert result == 0
        except SherlockExportAllTestPointsError as e:
            pytest.fail(str(e))


def helper_test_export_all_test_fixtures(layer: Layer):
    """Tests export_all_test_fixtures API."""
    try:
        layer.export_all_test_fixtures(
            "",
            "Main Board",
            "Test Fixtures.csv",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportAllTestFixtures as e:
        assert str(e) == "Export test fixtures error: Project name is invalid."

    try:
        layer.export_all_test_fixtures(
            "Tutorial Project",
            "",
            "Test Fixtures.csv",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportAllTestFixtures as e:
        assert str(e) == "Export test fixtures error: CCA name is invalid."

    try:
        layer.export_all_test_fixtures(
            "Tutorial Project",
            "Main Board",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportAllTestFixtures as e:
        assert str(e) == "Export test fixtures error: File path is required."

    if layer._is_connection_up():
        if platform.system() == "Windows":
            temp_dir = os.environ.get("TEMP", "C:\\TEMP")
        else:
            temp_dir = os.environ.get("TEMP", "/tmp")
        test_fixtures_file = os.path.join(temp_dir, "test_fixtures.csv")

        try:
            layer.export_all_test_fixtures(
                "Tutorial Project",
                "Invalid CCA",
                test_fixtures_file,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) is SherlockExportAllTestFixtures

        try:
            result = layer.export_all_test_fixtures(
                "Test Point Test Project",
                "Main Board",
                test_fixtures_file,
            )

            assert os.path.exists(test_fixtures_file)
            assert result == 0
        except SherlockExportAllTestFixtures as e:
            pytest.fail(str(e))


def helper_test_export_all_mount_points(layer: Layer):
    """Tests export_all_mount_points API."""
    try:
        layer.export_all_mount_points(
            "",
            "Main Board",
            "Mount Points.csv",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportAllMountPoints as e:
        assert str(e) == "Export mount points error: Project name is invalid."

    try:
        layer.export_all_mount_points(
            "Tutorial Project",
            "",
            "Mount Points.csv",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportAllMountPoints as e:
        assert str(e) == "Export mount points error: CCA name is invalid."

    try:
        layer.export_all_mount_points(
            "Tutorial Project",
            "Main Board",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportAllMountPoints as e:
        assert str(e) == "Export mount points error: File path is required."

    if layer._is_connection_up():
        if platform.system() == "Windows":
            temp_dir = os.environ.get("TEMP", "C:\\TEMP")
        else:
            temp_dir = os.environ.get("TEMP", "/tmp")
        mount_points_file = os.path.join(temp_dir, "mount_points.csv")

        try:
            layer.export_all_mount_points(
                "Tutorial Project",
                "Invalid CCA",
                mount_points_file,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockExportAllMountPoints

        try:
            result = layer.export_all_mount_points(
                "Test Point Test Project",
                "Main Board",
                mount_points_file,
            )

            assert os.path.exists(mount_points_file)
            assert result == 0
        except SherlockExportAllMountPoints as e:
            pytest.fail(e.message)


def helper_test_add_modeling_region(layer: Layer) -> str:
    modeling_region = [
        {
            "cca_name": "Card",
            "region_id": "Region001",
            "region_units": "mm",
            "model_mode": "Enabled",
            "shape": PolygonalShape(points=[(0, 0), (0, 6.35), (9.77, 0)], rotation=87.8),
            "pcb_model_props": {
                "export_model_type": "Sherlock",
                "elem_order": "First_Order",
                "max_mesh_size": 0.5,
                "max_mesh_size_units": "mm",
                "quads_preferred": True,
            },
            "trace_model_props": {
                "trace_model_type": "Enabled",
                "elem_order": "Second_Order",
                "trace_mesh_size": 0.3,
                "trace_mesh_size_units": "mm",
            },
        }
    ]

    # Invalid project name
    try:
        layer.add_modeling_region("", modeling_region)
        pytest.fail("No exception raised for invalid project name")
    except SherlockAddModelingRegionError as e:
        assert str(e.str_itr()) == "['Add modeling region error: Project name is invalid.']"

    # Empty modeling regions list
    try:
        layer.add_modeling_region("Tutorial Project", [])
        pytest.fail("No exception raised for empty modeling regions list")
    except SherlockAddModelingRegionError as e:
        assert str(e.str_itr()) == "['Add modeling region error: Modeling regions list is empty.']"

    # Invalid CCA name
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0]["cca_name"] = ""
    try:
        layer.add_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid CCA name")
    except SherlockAddModelingRegionError as e:
        assert str(e.str_itr()) == "['Add modeling region error: CCA name is invalid.']"

    # Invalid region ID
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0].pop("region_id")
    try:
        layer.add_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid region ID")
    except SherlockAddModelingRegionError as e:
        assert str(e.str_itr()) == "['Add modeling region error: Region ID is invalid.']"

    # Invalid region units
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0].pop("region_units")
    try:
        layer.add_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid region units")
    except SherlockAddModelingRegionError as e:
        assert str(e.str_itr()) == "['Add modeling region error: Region units are invalid.']"

    # Missing shape
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0].pop("shape")
    try:
        layer.add_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for missing shape")
    except SherlockAddModelingRegionError as e:
        assert str(e.str_itr()) == "['Add modeling region error: Shape is missing.']"

    # Invalid shape type
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0]["shape"] = "InvalidShapeType"
    try:
        layer.add_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid shape type")
    except SherlockAddModelingRegionError as e:
        assert str(e.str_itr()) == "['Add modeling region error: Shape is not of a valid type.']"

    # Invalid PCB model export type
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0]["pcb_model_props"]["export_model_type"] = ""
    try:
        layer.add_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid PCB model export type")
    except SherlockAddModelingRegionError as e:
        assert str(e.str_itr()) == (
            "['Add modeling region error: PCB model export type is invalid.']"
        )

    # Invalid PCB element order
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0]["pcb_model_props"]["elem_order"] = ""
    try:
        layer.add_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid PCB element order")
    except SherlockAddModelingRegionError as e:
        assert str(e.str_itr()) == "['Add modeling region error: PCB element order is invalid.']"

    # Invalid PCB max mesh size
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0]["pcb_model_props"]["max_mesh_size"] = "not_a_float"
    try:
        layer.add_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid PCB max mesh size")
    except SherlockAddModelingRegionError as e:
        assert str(e.str_itr()) == "['Add modeling region error: PCB max mesh size is invalid.']"

    # Invalid PCB quads preferred
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0]["pcb_model_props"]["quads_preferred"] = "not_a_bool"
    try:
        layer.add_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid PCB quads preferred")
    except SherlockAddModelingRegionError as e:
        assert str(e.str_itr()) == "['Add modeling region error: PCB quads preferred is invalid.']"

    # Invalid trace model type
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0]["trace_model_props"]["trace_model_type"] = ""
    try:
        layer.add_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid trace model type")
    except SherlockAddModelingRegionError as e:
        assert str(e.str_itr()) == "['Add modeling region error: Trace model type is invalid.']"

    if layer._is_connection_up():
        # Unhappy project name
        try:
            layer.add_modeling_region("Invalid Project", modeling_region)
            pytest.fail("No exception raised for invalid project name")
        except Exception as e:
            assert type(e) == SherlockAddModelingRegionError

        # Test for PolygonalShape
        valid_region_id = None
        valid_region = modeling_region
        valid_region[0]["cca_name"] = "Main Board"
        valid_region[0]["region_id"] = f"Region{uuid.uuid4()}"
        try:
            result = layer.add_modeling_region("Tutorial Project", valid_region)
            assert result == 0
            valid_region_id = valid_region[0]["region_id"]
        except SherlockAddModelingRegionError as e:
            pytest.fail(str(e.str_itr()))

        # Test for RectangularShape
        valid_region = copy.deepcopy(valid_region)
        rectangular_shape = RectangularShape(
            length=1.0, width=1.0, center_x=-5.0, center_y=5.0, rotation=15.0
        )
        valid_region[0]["shape"] = rectangular_shape
        valid_region[0]["region_id"] = f"Region{uuid.uuid4()}"
        try:
            result = layer.add_modeling_region("Tutorial Project", valid_region)
            assert result == 0
        except SherlockAddModelingRegionError as e:
            pytest.fail(str(e.str_itr()))

        # Test for SlotShape
        valid_region = copy.deepcopy(valid_region)
        slot_shape = SlotShape(
            length=1.0, width=2.0, node_count=6, center_x=-6.0, center_y=-5.0, rotation=-20.0
        )
        valid_region[0]["shape"] = slot_shape
        valid_region[0]["region_id"] = f"Region{uuid.uuid4()}"
        try:
            result = layer.add_modeling_region("Tutorial Project", valid_region)
            assert result == 0
        except SherlockAddModelingRegionError as e:
            pytest.fail(str(e.str_itr()))

        # Test for CircularShape
        valid_region = copy.deepcopy(valid_region)
        circular_shape = CircularShape(
            diameter=2.0, node_count=10, center_x=5.0, center_y=-5.0, rotation=30.0
        )
        valid_region[0]["shape"] = circular_shape
        valid_region[0]["region_id"] = f"Region{uuid.uuid4()}"
        try:
            result = layer.add_modeling_region("Tutorial Project", valid_region)
            assert result == 0
        except SherlockAddModelingRegionError as e:
            pytest.fail(str(e.str_itr()))

        return valid_region_id


def helper_test_update_modeling_region(layer: Layer, region_id: str) -> str:
    updated_region_id = f"UpdatedRegion{uuid.uuid4()}"
    modeling_region = [
        {
            "cca_name": "Card",
            "region_id": region_id,
            "region_units": "mm",
            "model_mode": "Enabled",
            "shape": PolygonalShape(points=[(0, 0), (0, 6.35), (9.77, 0)], rotation=87.8),
            "pcb_model_props": {
                "export_model_type": "Sherlock",
                "elem_order": "First_Order",
                "max_mesh_size": 0.5,
                "max_mesh_size_units": "mm",
                "quads_preferred": True,
            },
            "trace_model_props": {
                "trace_model_type": "Enabled",
                "elem_order": "Second_Order",
                "trace_mesh_size": 0.3,
                "trace_mesh_size_units": "mm",
            },
            "region_id_replacement": updated_region_id,
        }
    ]

    region_id = updated_region_id

    # Invalid project name
    try:
        layer.update_modeling_region("", modeling_region)
        pytest.fail("No exception raised for invalid project name")
    except SherlockUpdateModelingRegionError as e:
        assert str(e.str_itr()) == "['Update modeling region error: Project name is invalid.']"

    # Empty modeling regions list
    try:
        layer.update_modeling_region("Tutorial Project", [])
        pytest.fail("No exception raised for empty modeling regions list")
    except SherlockUpdateModelingRegionError as e:
        assert (
            str(e.str_itr()) == "['Update modeling region error: Modeling regions list is empty.']"
        )

    # Invalid CCA name
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0].pop("cca_name")
    try:
        layer.update_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid CCA name")
    except SherlockUpdateModelingRegionError as e:
        assert str(e.str_itr()) == "['Update modeling region error: CCA name is invalid.']"

    # Invalid region ID
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0].pop("region_id")
    try:
        layer.update_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid region ID")
    except SherlockUpdateModelingRegionError as e:
        assert str(e.str_itr()) == "['Update modeling region error: Region ID is invalid.']"

    # Invalid region units
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0].pop("region_units")
    try:
        layer.update_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid region units")
    except SherlockUpdateModelingRegionError as e:
        assert str(e.str_itr()) == "['Update modeling region error: Region units are invalid.']"

    # Missing shape
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0].pop("shape")
    try:
        layer.update_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for missing shape")
    except SherlockUpdateModelingRegionError as e:
        assert str(e.str_itr()) == "['Update modeling region error: Shape is missing.']"

    # Invalid PCB model export type
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0]["pcb_model_props"]["export_model_type"] = ""
    try:
        layer.update_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid PCB model export type")
    except SherlockUpdateModelingRegionError as e:
        assert str(e.str_itr()) == (
            "['Update modeling region error: PCB model export type is invalid.']"
        )

    # Invalid PCB element order
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0]["pcb_model_props"]["elem_order"] = ""
    try:
        layer.update_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid PCB element order")
    except SherlockUpdateModelingRegionError as e:
        assert str(e.str_itr()) == "['Update modeling region error: PCB element order is invalid.']"

    # Invalid PCB max mesh size
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0]["pcb_model_props"]["max_mesh_size"] = "not_a_float"
    try:
        layer.update_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid PCB max mesh size")
    except SherlockUpdateModelingRegionError as e:
        assert str(e.str_itr()) == "['Update modeling region error: PCB max mesh size is invalid.']"

    # Invalid PCB quads preferred
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0]["pcb_model_props"]["quads_preferred"] = "not_a_bool"
    try:
        layer.update_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid PCB quads preferred")
    except SherlockUpdateModelingRegionError as e:
        assert (
            str(e.str_itr()) == "['Update modeling region error: PCB quads preferred is invalid.']"
        )

    # Invalid trace model type
    invalid_region = copy.deepcopy(modeling_region)
    invalid_region[0]["trace_model_props"]["trace_model_type"] = ""
    try:
        layer.update_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid trace model type")
    except SherlockUpdateModelingRegionError as e:
        assert str(e.str_itr()) == "['Update modeling region error: Trace model type is invalid.']"

    if layer._is_connection_up():
        # Unhappy project name
        try:
            layer.update_modeling_region("Invalid Project", modeling_region)
            pytest.fail("No exception raised for invalid project name")
        except Exception as e:
            assert type(e) == SherlockUpdateModelingRegionError

        # Test for PolygonalShape
        valid_region = modeling_region
        valid_region[0]["cca_name"] = "Main Board"
        try:
            result = layer.update_modeling_region("Tutorial Project", valid_region)
            assert result == 0
        except SherlockUpdateModelingRegionError as e:
            pytest.fail(str(e))

        # Test for RectangularShape
        valid_region = copy.deepcopy(valid_region)
        rectangular_shape = RectangularShape(
            length=10.0, width=5.0, center_x=0.0, center_y=0.0, rotation=45.0
        )
        valid_region[0]["shape"] = rectangular_shape
        valid_region[0]["region_id"] = region_id
        region_id = f"UpdatedRegion{uuid.uuid4()}"
        valid_region[0]["region_id_replacement"] = region_id
        try:
            result = layer.update_modeling_region("Tutorial Project", valid_region)
            assert result == 0
        except SherlockUpdateModelingRegionError as e:
            pytest.fail(str(e))

        # Test for SlotShape
        valid_region = copy.deepcopy(valid_region)
        slot_shape = SlotShape(
            length=10.0, width=5.0, node_count=6, center_x=0.0, center_y=0.0, rotation=45.0
        )
        valid_region[0]["shape"] = slot_shape
        valid_region[0]["region_id"] = region_id
        region_id = f"UpdatedRegion{uuid.uuid4()}"
        valid_region[0]["region_id_replacement"] = region_id
        try:
            result = layer.update_modeling_region("Tutorial Project", valid_region)
            assert result == 0
        except SherlockUpdateModelingRegionError as e:
            pytest.fail(str(e))

        # Test for CircularShape
        circular_shape = CircularShape(
            diameter=10.0, node_count=8, center_x=0.0, center_y=0.0, rotation=0.0
        )
        valid_region[0]["shape"] = circular_shape
        valid_region[0]["region_id"] = region_id
        region_id = f"UpdatedRegion{uuid.uuid4()}"
        valid_region[0]["region_id_replacement"] = region_id
        try:
            result = layer.update_modeling_region("Tutorial Project", valid_region)
            assert result == 0
            return region_id
        except SherlockUpdateModelingRegionError as e:
            pytest.fail(str(e))


def helper_test_copy_modeling_region(layer: Layer, region_id: str):
    region_id_copy = f"RegionCopy{uuid.uuid4()}"
    copy_region_example = [
        {
            "cca_name": "Card",
            "region_id": region_id,
            "region_id_copy": region_id_copy,
            "center_x": 10.0,
            "center_y": 20.0,
        }
    ]

    # Invalid project name
    try:
        layer.copy_modeling_region("", copy_region_example)
        pytest.fail("No exception raised for invalid project name")
    except SherlockCopyModelingRegionError as e:
        assert str(e.str_itr()) == "['Copy modeling region error: Project name is invalid.']"

    # Empty copy regions list
    try:
        layer.copy_modeling_region("Tutorial Project", [])
        pytest.fail("No exception raised for empty copy regions list")
    except SherlockCopyModelingRegionError as e:
        assert str(e.str_itr()) == "['Copy modeling region error: Copy regions list is empty.']"

    # Invalid CCA name
    invalid_region = copy.deepcopy(copy_region_example)
    invalid_region[0]["cca_name"] = ""
    try:
        layer.copy_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid CCA name")
    except SherlockCopyModelingRegionError as e:
        assert str(e.str_itr()) == "['Copy modeling region error: CCA name is invalid.']"

    # Invalid region ID
    invalid_region = copy.deepcopy(copy_region_example)
    invalid_region[0]["region_id"] = ""
    try:
        layer.copy_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid region ID")
    except SherlockCopyModelingRegionError as e:
        assert str(e.str_itr()) == "['Copy modeling region error: Region ID is invalid.']"

    # Invalid region ID copy
    invalid_region = copy.deepcopy(copy_region_example)
    invalid_region[0]["region_id_copy"] = ""
    try:
        layer.copy_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid region ID copy")
    except SherlockCopyModelingRegionError as e:
        assert str(e.str_itr()) == "['Copy modeling region error: Region ID copy is invalid.']"

    # Invalid center X coordinate
    invalid_region = copy.deepcopy(copy_region_example)
    invalid_region[0]["center_x"] = "not_a_float"
    try:
        layer.copy_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid center X coordinate")
    except SherlockCopyModelingRegionError as e:
        assert str(e.str_itr()) == "['Copy modeling region error: Center X coordinate is invalid.']"

    # Invalid center Y coordinate
    invalid_region = copy.deepcopy(copy_region_example)
    invalid_region[0]["center_y"] = "not_a_float"
    try:
        layer.copy_modeling_region("Tutorial Project", invalid_region)
        pytest.fail("No exception raised for invalid center Y coordinate")
    except SherlockCopyModelingRegionError as e:
        assert str(e.str_itr()) == "['Copy modeling region error: Center Y coordinate is invalid.']"

    if layer._is_connection_up():
        # Unhappy project name
        try:
            layer.copy_modeling_region("Invalid Project", copy_region_example)
            pytest.fail("No exception raised for invalid project name")
        except Exception as e:
            assert type(e) == SherlockCopyModelingRegionError

        # Valid request
        try:
            valid_region = copy.deepcopy(copy_region_example)
            valid_region[0]["cca_name"] = "Main Board"
            result = layer.copy_modeling_region("Tutorial Project", valid_region)
            assert result == 0
        except SherlockCopyModelingRegionError as e:
            pytest.fail(e.str_itr())


def helper_test_delete_modeling_region(layer: Layer, region_id: str):

    # Invalid project name
    try:
        layer.delete_modeling_region("", [{"cca_name": "Main Board", "region_id": "12345"}])
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockDeleteModelingRegionError as e:
        assert str(e) == "Delete modeling region error: Project name is invalid."

    # Non-list delete regions
    try:
        layer.delete_modeling_region("Tutorial Project", "not_a_list")
        pytest.fail("No exception thrown when using a non-list delete regions")
    except SherlockDeleteModelingRegionError as e:
        assert str(e) == "Delete modeling region error: Delete regions should be a list."

    # Invalid modeling regions list
    try:
        layer.delete_modeling_region("Tutorial Project", [])
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockDeleteModelingRegionError as e:
        assert str(e) == "Delete modeling region error: Delete regions list is empty."

    # Non-dictionary delete region
    try:
        layer.delete_modeling_region("Tutorial Project", ["not_a_dict"])
        pytest.fail("No exception thrown when using a non-dictionary delete region")
    except SherlockDeleteModelingRegionError as e:
        assert str(e) == "Delete modeling region error: Each region should be a dictionary."

    # Invalid CCA name
    try:
        layer.delete_modeling_region("Tutorial Project", [{"cca_name": "", "region_id": "12345"}])
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockDeleteModelingRegionError as e:
        assert str(e) == "Delete modeling region error: CCA name is invalid."

    # Invalid region ID
    try:
        layer.delete_modeling_region(
            "Tutorial Project", [{"cca_name": "Main Board", "region_id": ""}]
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockDeleteModelingRegionError as e:
        assert str(e) == "Delete modeling region error: Region ID is invalid."

    if layer._is_connection_up():
        # Unhappy project name
        try:
            layer.delete_modeling_region(
                "Tutorial Project", [{"cca_name": "Main Board", "region_id": "InvalidID"}]
            )
            pytest.fail("No exception thrown when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockDeleteModelingRegionError

        # Valid request
        try:
            result = layer.delete_modeling_region(
                "Tutorial Project", [{"cca_name": "Main Board", "region_id": region_id}]
            )
            assert result == 0
        except Exception as e:
            pytest.fail(e.message)


def helper_test_list_layers(layer):
    """Test list_layers API"""

    try:
        layer.list_layers("Tutorial Project", "")
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockListLayersError as e:
        assert str(e) == "List layers error: CCA name is invalid."

    try:
        layer.list_layers("", "Main Board")
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockListLayersError as e:
        assert str(e) == "List layers error: Project name is invalid."

    if layer._is_connection_up():
        try:
            layer.list_layers("Invalid Project Name", "")
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockListLayersError

        try:
            response = layer.list_layers("Test Point Test Project", "Wrong Board Name")
        except Exception as e:
            assert str(e) == "List layers error: Cannot find CCA: Wrong Board Name"
            assert type(e) == SherlockListLayersError

        # Valid request
        try:
            response = layer.list_layers("Test Point Test Project", "Main Board")
            layer_count = 0
            for layer_info in response:
                layer_count += len(layer_info.layers)

            assert layer_count == 30
        except SherlockListLayersError as e:
            pytest.fail(e.message())


def helper_test_get_test_point_props(layer):
    """Test get_test_point_props API."""

    project = "Test Point Test Project"
    cca_name = "Main Board"
    test_point_ids = "TP1,TP2"

    good_bad_test_point_ids = "TP1,Bad1,Bad2,TP2"

    # Missing project name
    try:
        GetTestPointPropertiesRequest(
            project="",
            cca_name=cca_name,
            test_point_ids=test_point_ids,
        )
        pytest.fail("No exception raised when using an invalid project parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)

    # Missing CCA name
    try:
        GetTestPointPropertiesRequest(
            project=project,
            cca_name="",
            test_point_ids=test_point_ids,
        )
        pytest.fail("No exception raised when using an invalid cca_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)

    # test_point_ids is the empty string
    try:
        GetTestPointPropertiesRequest(
            project=project,
            cca_name=cca_name,
            test_point_ids="",
        )
        pytest.fail("No exception raised when using an invalid test_point_ids parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)

    if layer._is_connection_up():

        # Bad project name
        badProjectRequest = GetTestPointPropertiesRequest(
            project="Invalid Project Name",
            cca_name=cca_name,
            test_point_ids=test_point_ids,
        )

        badProjectResponses = layer.get_test_point_props(badProjectRequest)
        assert len(badProjectResponses) == 1
        assert badProjectResponses[0].returnCode.value == -1
        assert (
            badProjectResponses[0].returnCode.message == "Cannot find project: Invalid Project Name"
        )

        # Test request with valid test point ids.
        request = GetTestPointPropertiesRequest(
            project=project,
            cca_name=cca_name,
            test_point_ids=test_point_ids,
        )

        responses = layer.get_test_point_props(request)
        assert len(responses) == 2
        assert responses[0].testPointProperties.ID == "TP1"
        assert responses[0].testPointProperties.side == "TOP"
        assert responses[0].testPointProperties.units == "mm"
        assert_float_equals(53.09614010443865, responses[0].testPointProperties.centerX)
        assert_float_equals(10.578305680323764, responses[0].testPointProperties.centerY)
        assert responses[0].testPointProperties.radius == 1
        assert responses[0].testPointProperties.loadType == 0
        assert responses[0].testPointProperties.loadValue == 0.36
        assert responses[0].testPointProperties.loadUnits == "N"

        assert responses[1].testPointProperties.ID == "TP2"
        assert responses[1].testPointProperties.side == "TOP"
        assert responses[1].testPointProperties.units == "mm"
        assert_float_equals(71.21625140992168, responses[1].testPointProperties.centerX)
        assert_float_equals(10.718771659436035, responses[1].testPointProperties.centerY)
        assert responses[1].testPointProperties.radius == 1
        assert responses[1].testPointProperties.loadType == 0
        assert responses[1].testPointProperties.loadValue == 0.36
        assert responses[1].testPointProperties.loadUnits == "N"

        # Test a mix of valid test points and invalid ones.
        mixedRequest = GetTestPointPropertiesRequest(
            project=project,
            cca_name=cca_name,
            test_point_ids=good_bad_test_point_ids,
        )

        mixedResponses = layer.get_test_point_props(mixedRequest)
        # 2 good test points, 2 bad test points
        assert len(mixedResponses) == 4

        assert mixedResponses[0].returnCode.value == -1

        assert mixedResponses[1].returnCode.value == -1

        assert mixedResponses[2].testPointProperties.ID == "TP1"
        assert mixedResponses[2].testPointProperties.side == "TOP"
        assert mixedResponses[2].testPointProperties.units == "mm"
        assert_float_equals(53.09614010443865, mixedResponses[2].testPointProperties.centerX)
        assert_float_equals(10.578305680323764, mixedResponses[2].testPointProperties.centerY)
        assert mixedResponses[2].testPointProperties.radius == 1
        assert mixedResponses[2].testPointProperties.loadType == 0
        assert mixedResponses[2].testPointProperties.loadValue == 0.36
        assert mixedResponses[2].testPointProperties.loadUnits == "N"

        assert mixedResponses[3].testPointProperties.ID == "TP2"
        assert mixedResponses[3].testPointProperties.side == "TOP"
        assert mixedResponses[3].testPointProperties.units == "mm"
        assert_float_equals(71.21625140992168, mixedResponses[3].testPointProperties.centerX)
        assert_float_equals(10.718771659436035, mixedResponses[3].testPointProperties.centerY)
        assert mixedResponses[3].testPointProperties.radius == 1
        assert mixedResponses[3].testPointProperties.loadType == 0
        assert mixedResponses[3].testPointProperties.loadValue == 0.36
        assert mixedResponses[3].testPointProperties.loadUnits == "N"

        # Test that no test_point_ids param will return all of the test points in the project.
        allPointsRequest = GetTestPointPropertiesRequest(
            project=project,
            cca_name=cca_name,
        )

        allPointsResponses = layer.get_test_point_props(allPointsRequest)
        assert len(allPointsResponses) == 4

        assert allPointsResponses[0].testPointProperties.ID == "TP1"
        assert allPointsResponses[0].testPointProperties.side == "TOP"
        assert allPointsResponses[0].testPointProperties.units == "mm"
        assert_float_equals(53.09614010443865, allPointsResponses[0].testPointProperties.centerX)
        assert_float_equals(10.578305680323764, allPointsResponses[0].testPointProperties.centerY)
        assert allPointsResponses[0].testPointProperties.radius == 1
        assert allPointsResponses[0].testPointProperties.loadType == 0
        assert allPointsResponses[0].testPointProperties.loadValue == 0.36
        assert allPointsResponses[0].testPointProperties.loadUnits == "N"

        assert allPointsResponses[1].testPointProperties.side == "TOP"
        assert allPointsResponses[1].testPointProperties.units == "mm"
        assert_float_equals(71.21625140992168, allPointsResponses[1].testPointProperties.centerX)
        assert_float_equals(10.718771659436035, allPointsResponses[1].testPointProperties.centerY)
        assert allPointsResponses[1].testPointProperties.radius == 1
        assert allPointsResponses[1].testPointProperties.loadType == 0
        assert allPointsResponses[1].testPointProperties.loadValue == 0.36
        assert allPointsResponses[1].testPointProperties.loadUnits == "N"

        assert allPointsResponses[2].testPointProperties.ID == "TP3"
        assert allPointsResponses[2].testPointProperties.side == "TOP"
        assert allPointsResponses[2].testPointProperties.units == "mm"
        assert_float_equals(71.21625140992168, allPointsResponses[2].testPointProperties.centerX)
        assert_float_equals(-10.632057165629243, allPointsResponses[2].testPointProperties.centerY)
        assert allPointsResponses[2].testPointProperties.radius == 1
        assert allPointsResponses[2].testPointProperties.loadType == 0
        assert allPointsResponses[2].testPointProperties.loadValue == 0.36
        assert allPointsResponses[2].testPointProperties.loadUnits == "N"

        assert allPointsResponses[3].testPointProperties.ID == "TP4"
        assert allPointsResponses[3].testPointProperties.side == "TOP"
        assert allPointsResponses[3].testPointProperties.units == "mm"
        assert_float_equals(53.09614010443865, allPointsResponses[3].testPointProperties.centerX)
        assert_float_equals(-10.632057165629243, allPointsResponses[3].testPointProperties.centerY)
        assert allPointsResponses[3].testPointProperties.radius == 1
        assert allPointsResponses[3].testPointProperties.loadType == 0
        assert allPointsResponses[3].testPointProperties.loadValue == 0.36
        assert allPointsResponses[3].testPointProperties.loadUnits == "N"


def helper_test_get_ict_fixtures_props(layer):
    """Test get_ict_fixtures_props API"""

    project = "Tutorial Project"
    cca_name = "Main Board"

    # Missing project name
    try:
        GetICTFixturesPropertiesRequest(
            project="",
            cca_name=cca_name,
            ict_fixtures_ids="F1",
        )
        pytest.fail("No exception raised when using an invalid project parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)

    # Missing CCA name
    try:
        GetICTFixturesPropertiesRequest(
            project=project,
            cca_name="",
            ict_fixtures_ids="F1",
        )
        pytest.fail("No exception raised when using an invalid cca_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)

    # ict_fixtures_ids is the empty string
    try:
        GetICTFixturesPropertiesRequest(
            project=project,
            cca_name=cca_name,
            ict_fixtures_ids="",
        )
        pytest.fail("No exception raised when using an invalid ict_fixtures_ids parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)

    if layer._is_connection_up():

        # Bad project name
        bad_project_request = GetICTFixturesPropertiesRequest(
            project="Invalid Project Name",
            cca_name=cca_name,
            ict_fixtures_ids="F1, F1",
        )
        bad_project_response = layer.get_ict_fixtures_props(bad_project_request)
        assert bad_project_response.returnCode.value == -1
        assert (
            bad_project_response.returnCode.message == "Cannot find project: Invalid Project Name"
        )

        bad_project_request = GetICTFixturesPropertiesRequest(
            project=project,
            cca_name="Invalid CCA Name",
            ict_fixtures_ids="F1, F1",
        )
        bad_project_response = layer.get_ict_fixtures_props(bad_project_request)
        assert bad_project_response.returnCode.value == -1
        assert bad_project_response.returnCode.message == "Cannot find CCA: Invalid CCA Name"

        # Test request with valid ict fixture ids.
        request = GetICTFixturesPropertiesRequest(
            project=project,
            cca_name=cca_name,
            ict_fixtures_ids="F1, F1,",
        )

        response = layer.get_ict_fixtures_props(request)
        assert response.returnCode.value == 0
        assert len(response.ICTFixtureProperties) == 2

        # First requested ID of F1
        assert response.ICTFixtureProperties[0].ID == "F1"
        assert response.ICTFixtureProperties[0].type == "Mount Pad"
        assert response.ICTFixtureProperties[0].units == "mm"
        assert response.ICTFixtureProperties[0].side == "BOTTOM"
        assert_float_equals(-5.0, float(response.ICTFixtureProperties[0].height))
        assert response.ICTFixtureProperties[0].material == "ALLOY42"
        assert response.ICTFixtureProperties[0].state == "ENABLED"

        assert response.ICTFixtureProperties[0].shape == "Rectangular"
        assert_float_equals(-91.3029, float(response.ICTFixtureProperties[0].x))
        assert_float_equals(-0.1673, float(response.ICTFixtureProperties[0].y))
        assert_float_equals(7.0448, float(response.ICTFixtureProperties[0].length))
        assert_float_equals(74.6564, float(response.ICTFixtureProperties[0].width))
        assert_float_equals(7.0448, float(response.ICTFixtureProperties[0].diameter))
        assert_float_equals(4, int(response.ICTFixtureProperties[0].nodes))
        assert_float_equals(0.0, float(response.ICTFixtureProperties[0].rotation))

        assert response.ICTFixtureProperties[0].boundary == "Outline"
        assert (
            response.ICTFixtureProperties[0].constraints
            == "X-axis translation|Y-axis translation|Z-axis translation"
        )
        assert response.ICTFixtureProperties[0].polygon == ""
        assert response.ICTFixtureProperties[0].chassisMaterial == "ALUMINUM"

        # Second requested ID of F1
        assert response.ICTFixtureProperties[1].ID == "F1"
        assert response.ICTFixtureProperties[1].type == "Mount Pad"
        assert response.ICTFixtureProperties[1].units == "mm"
        assert response.ICTFixtureProperties[1].side == "BOTTOM"
        assert_float_equals(-5.0, float(response.ICTFixtureProperties[1].height))
        assert response.ICTFixtureProperties[1].material == "ALLOY42"
        assert response.ICTFixtureProperties[1].state == "ENABLED"

        assert response.ICTFixtureProperties[1].shape == "Rectangular"
        assert_float_equals(-91.3029, float(response.ICTFixtureProperties[1].x))
        assert_float_equals(-0.1673, float(response.ICTFixtureProperties[1].y))
        assert_float_equals(7.0448, float(response.ICTFixtureProperties[1].length))
        assert_float_equals(74.6564, float(response.ICTFixtureProperties[1].width))
        assert_float_equals(7.0448, float(response.ICTFixtureProperties[1].diameter))
        assert_float_equals(4, int(response.ICTFixtureProperties[1].nodes))
        assert_float_equals(0.0, float(response.ICTFixtureProperties[1].rotation))

        assert response.ICTFixtureProperties[1].boundary == "Outline"
        assert (
            response.ICTFixtureProperties[1].constraints
            == "X-axis translation|Y-axis translation|Z-axis translation"
        )
        assert response.ICTFixtureProperties[1].polygon == ""
        assert response.ICTFixtureProperties[1].chassisMaterial == "ALUMINUM"

        # Test request with a mix of valid and invalid ict fixture ids.
        mixed_request = GetICTFixturesPropertiesRequest(
            project=project,
            cca_name=cca_name,
            ict_fixtures_ids="invalid, F1, invalid",
        )

        mixed_response = layer.get_ict_fixtures_props(mixed_request)
        assert mixed_response.returnCode.value == -1
        assert len(mixed_response.ICTFixtureProperties) == 1

        assert response.ICTFixtureProperties[0].ID == "F1"
        assert response.ICTFixtureProperties[0].type == "Mount Pad"
        assert response.ICTFixtureProperties[0].units == "mm"
        assert response.ICTFixtureProperties[0].side == "BOTTOM"
        assert_float_equals(-5.0, float(response.ICTFixtureProperties[0].height))
        assert response.ICTFixtureProperties[0].material == "ALLOY42"
        assert response.ICTFixtureProperties[0].state == "ENABLED"

        assert response.ICTFixtureProperties[0].shape == "Rectangular"
        assert_float_equals(-91.3029, float(response.ICTFixtureProperties[0].x))
        assert_float_equals(-0.1673, float(response.ICTFixtureProperties[0].y))
        assert_float_equals(7.0448, float(response.ICTFixtureProperties[0].length))
        assert_float_equals(74.6564, float(response.ICTFixtureProperties[0].width))
        assert_float_equals(7.0448, float(response.ICTFixtureProperties[0].diameter))
        assert_float_equals(4, int(response.ICTFixtureProperties[0].nodes))
        assert_float_equals(0.0, float(response.ICTFixtureProperties[0].rotation))

        assert response.ICTFixtureProperties[0].boundary == "Outline"
        assert (
            response.ICTFixtureProperties[0].constraints
            == "X-axis translation|Y-axis translation|Z-axis translation"
        )
        assert response.ICTFixtureProperties[0].polygon == ""
        assert response.ICTFixtureProperties[0].chassisMaterial == "ALUMINUM"


def helper_test_update_test_points(layer):
    """Test update_test_points API"""

    project = "Tutorial Project"
    cca_name = "Main Board"

    test_point_1 = TestPointProperties(
        id="TP1",
        side="BOTTOM",
        units="in",
        center_x=1.0,
        center_y=0.5,
        radius=0.2,
        load_type=SherlockLayerService_pb2.TestPointProperties.LoadType.Force,
        load_value=3.0,
        load_units="ozf",
    )

    test_point_2 = TestPointProperties(
        id="",
        side="TOP",
        units="mm",
        center_x=-30,
        center_y=-10,
        radius=5,
        load_type=SherlockLayerService_pb2.TestPointProperties.LoadType.Displacement,
        load_value=0,
        load_units="in",
    )

    invalid_test_point = TestPointProperties(
        id="TP2",
        side="invalid",
        units="mm",
        center_x=60,
        center_y=-40,
        radius=4,
        load_type=SherlockLayerService_pb2.TestPointProperties.LoadType.Force,
        load_value=5,
        load_units="N",
    )

    # Missing Project Name
    try:
        UpdateTestPointsRequest(project="", cca_name=cca_name, update_test_points=[test_point_1])
        pytest.fail("No exception thrown when using an invalid parameter")
    except pydantic.ValidationError as e:
        assert isinstance(e, pydantic.ValidationError)

    # Missing CCA Name
    try:
        UpdateTestPointsRequest(project=project, cca_name="", update_test_points=[test_point_1])
        pytest.fail("No exception thrown when using an invalid parameter")
    except pydantic.ValidationError as e:
        assert isinstance(e, pydantic.ValidationError)

    if layer._is_connection_up():

        # Invalid test point test
        invalid_request = UpdateTestPointsRequest(
            project=project,
            cca_name=cca_name,
            update_test_points=[invalid_test_point],
        )
        invalid_response = layer.update_test_points(invalid_request)
        assert invalid_response.returnCode.value == -1

        # Successful test point test
        successful_request = UpdateTestPointsRequest(
            project=project,
            cca_name=cca_name,
            update_test_points=[test_point_1, test_point_2],
        )
        successful_response = layer.update_test_points(successful_request)
        assert successful_response.returnCode.value == 0

        properties_request = GetTestPointPropertiesRequest(
            project=project,
            cca_name=cca_name,
            test_point_ids="TP1, TP5",
        )
        properties_responses = layer.get_test_point_props(properties_request)

        # Tests updated properties for TP1
        assert properties_responses[0].testPointProperties.ID == "TP1"
        assert properties_responses[0].testPointProperties.side == "BOTTOM"
        assert properties_responses[0].testPointProperties.units == "in"
        assert_float_equals(1.0, properties_responses[0].testPointProperties.centerX)
        assert_float_equals(0.5, properties_responses[0].testPointProperties.centerY)
        assert properties_responses[0].testPointProperties.radius == 0.2
        assert properties_responses[0].testPointProperties.loadType == 0
        assert properties_responses[0].testPointProperties.loadValue == 3.0
        assert properties_responses[0].testPointProperties.loadUnits == "ozf"

        # Tests updated properties for TP5
        assert properties_responses[1].testPointProperties.ID == "TP5"
        assert properties_responses[1].testPointProperties.side == "TOP"
        assert properties_responses[1].testPointProperties.units == "mm"
        assert_float_equals(-30.0, properties_responses[1].testPointProperties.centerX)
        assert_float_equals(-10.0, properties_responses[1].testPointProperties.centerY)
        assert properties_responses[1].testPointProperties.radius == 5.0
        assert properties_responses[1].testPointProperties.loadType == 1
        assert properties_responses[1].testPointProperties.loadValue == 0.0
        assert properties_responses[1].testPointProperties.loadUnits == "in"


def helper_test_update_ict_fixtures(layer):
    """Test update_ict_fixtures API"""

    project = "Tutorial Project"
    cca_name = "Main Board"

    fixture_1 = ICTFixtureProperties(
        id="F1",
        type="Mount Hole",
        units="in",
        side="TOP",
        height="0.0",
        material="GOLD",
        state="DISABLED",
        shape="Slot",
        x="0.3",
        y="-0.4",
        length="1.0",
        width="0.2",
        diameter="0.0",
        nodes="10",
        rotation="15",
        polygon="",
        boundary="Outline",
        constraints="X-axis translation|Z-axis translation",
        chassis_material="SILVER",
    )

    fixture_2 = ICTFixtureProperties(
        id="",
        type="Standoff",
        units="mil",
        side="BOTTOM",
        height="10",
        material="FERRITE",
        state="ENABLED",
        shape="Circular",
        x="100",
        y="50",
        length="20",
        width="20",
        diameter="150",
        nodes="6",
        rotation="0",
        polygon="",
        boundary="Center",
        constraints="Y-axis translation",
        chassis_material="NYLON",
    )

    invalid_fixture = ICTFixtureProperties(
        id="F1",
        type="Mount Hole",
        units="in",
        side="TOP",
        height="0.0",
        material="GOLD",
        state="DISABLED",
        shape="Slot",
        x="invalid",
        y="-0.4",
        length="1.0",
        width="0.2",
        diameter="0.0",
        nodes="10",
        rotation="15",
        polygon="",
        boundary="Outline",
        constraints="X-axis translation|Z-axis translation",
        chassis_material="SILVER",
    )

    # Missing Project Name
    try:
        UpdateICTFixturesRequest(project="", cca_name=cca_name, update_fixtures=[fixture_1])
        pytest.fail("No exception thrown when using an invalid parameter")
    except pydantic.ValidationError as e:
        assert isinstance(e, pydantic.ValidationError)

    # Missing CCA Name
    try:
        UpdateICTFixturesRequest(project=project, cca_name="", update_fixtures=[fixture_1])
        pytest.fail("No exception thrown when using an invalid parameter")
    except pydantic.ValidationError as e:
        assert isinstance(e, pydantic.ValidationError)

    if layer._is_connection_up():
        # Invalid ict fixture test
        invalid_request = UpdateICTFixturesRequest(
            project=project,
            cca_name=cca_name,
            update_fixtures=[invalid_fixture],
        )
        invalid_response = layer.update_ict_fixtures(invalid_request)
        assert invalid_response.returnCode.value == -1

        # Successful ict fixture test
        successful_request = UpdateICTFixturesRequest(
            project=project,
            cca_name=cca_name,
            update_fixtures=[fixture_1, fixture_2],
        )
        successful_response = layer.update_ict_fixtures(successful_request)
        assert successful_response.returnCode.value == 0

        properties_request = GetICTFixturesPropertiesRequest(
            project=project,
            cca_name=cca_name,
            ict_fixtures_ids="F1, F2",
        )

        properties_response = layer.get_ict_fixtures_props(properties_request)

        # Tests updated properties for F1
        assert properties_response.ICTFixtureProperties[0].ID == "F1"
        assert properties_response.ICTFixtureProperties[0].type == "Mount Hole"
        assert properties_response.ICTFixtureProperties[0].units == "in"
        assert properties_response.ICTFixtureProperties[0].side == "TOP"
        assert properties_response.ICTFixtureProperties[0].material == "GOLD"
        assert properties_response.ICTFixtureProperties[0].state == "DISABLED"
        assert properties_response.ICTFixtureProperties[0].shape == "Slot"
        assert properties_response.ICTFixtureProperties[0].x == "0.3"
        assert properties_response.ICTFixtureProperties[0].y == "-0.4"
        assert properties_response.ICTFixtureProperties[0].length == "1"
        assert properties_response.ICTFixtureProperties[0].width == "0.2"
        assert properties_response.ICTFixtureProperties[0].nodes == "10"
        assert properties_response.ICTFixtureProperties[0].rotation == "15.0"
        assert properties_response.ICTFixtureProperties[0].boundary == "Outline"
        assert properties_response.ICTFixtureProperties[0].constraints == (
            "X-axis translation|" "Z-axis translation"
        )
        assert properties_response.ICTFixtureProperties[0].chassisMaterial == "SILVER"

        # Tests updated properties for F2
        assert properties_response.ICTFixtureProperties[1].ID == "F2"
        assert properties_response.ICTFixtureProperties[1].type == "Standoff"
        assert properties_response.ICTFixtureProperties[1].units == "mil"
        assert properties_response.ICTFixtureProperties[1].side == "BOTTOM"
        assert properties_response.ICTFixtureProperties[1].height == "-10.0"
        assert properties_response.ICTFixtureProperties[1].material == "FERRITE"
        assert properties_response.ICTFixtureProperties[1].state == "ENABLED"
        assert properties_response.ICTFixtureProperties[1].shape == "Circular"
        assert properties_response.ICTFixtureProperties[1].x == "100"
        assert properties_response.ICTFixtureProperties[1].y == "50"
        assert properties_response.ICTFixtureProperties[1].length == "150"
        assert properties_response.ICTFixtureProperties[1].width == "150"
        assert properties_response.ICTFixtureProperties[1].diameter == "150"
        assert properties_response.ICTFixtureProperties[1].nodes == "6"
        assert properties_response.ICTFixtureProperties[1].boundary == "Center"
        assert properties_response.ICTFixtureProperties[1].constraints == "Y-axis translation"
        assert properties_response.ICTFixtureProperties[1].chassisMaterial == "NYLON"


def helper_test_export_layer_image(layer):
    """Test export_layer_image API"""

    layer_infos = [
        {"layer_folder": "Components", "layers": ["comp-top"]},
        {"layer_folder": "Mechanical_Shock", "layers": ["SH Disp @ 5.2ms"]},
    ]
    export_layers = [
        {
            "grid_enabled": True,
            "layer_infos": layer_infos,
            "file_path": "C:\\Users\\user_id\\Downloads\\SH-image.jpg",
            "image_height": 600,
            "image_width": 800,
            "overwrite_existing_file": True,
        }
    ]

    try:
        layer.export_layer_image("Tutorial Project", "", export_layers)
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockExportLayerImageError as e:
        assert str(e) == "Export layer image error: CCA name is invalid."

    try:
        layer.export_layer_image("", "Main Board", export_layers)
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockExportLayerImageError as e:
        assert str(e) == "Export layer image error: Project name is invalid."

    try:
        layer.export_layer_image("Tutorial Project", "Main Board", export_layers)
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockExportLayerImageError as e:
        assert str(e) == "Export layer image error: Axes Enabled is invalid."

    export_layers = [
        {
            "axes_enabled": True,
            "layer_infos": layer_infos,
            "file_path": "C:\\Users\\user_id\\Downloads\\SH-image.jpg",
            "image_height": 600,
            "image_width": 800,
            "overwrite_existing_file": True,
        }
    ]

    try:
        layer.export_layer_image("Tutorial Project", "Main Board", export_layers)
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockExportLayerImageError as e:
        assert str(e) == "Export layer image error: Grid Enabled is invalid."

    export_layers = [
        {
            "axes_enabled": True,
            "grid_enabled": True,
            "layer_infos": [],
            "file_path": "C:\\Users\\user_id\\Downloads\\SH-image.jpg",
            "image_height": 600,
            "image_width": 800,
            "overwrite_existing_file": True,
        }
    ]

    try:
        layer.export_layer_image("Tutorial Project", "Main Board", export_layers)
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockExportLayerImageError as e:
        assert str(e) == "Export layer image error: Layer info is invalid."

    export_layers = [
        {
            "axes_enabled": True,
            "grid_enabled": True,
            "layer_infos": layer_infos,
            "image_height": 600,
            "image_width": 800,
            "overwrite_existing_file": True,
        }
    ]

    try:
        layer.export_layer_image("Tutorial Project", "Main Board", export_layers)
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockExportLayerImageError as e:
        assert str(e) == "Export layer image error: File Path is invalid."

    export_layers = [
        {
            "axes_enabled": True,
            "grid_enabled": True,
            "layer_infos": layer_infos,
            "file_path": "C:\\Users\\user_id\\Downloads\\SH-image.jpg",
            "image_width": 800,
            "overwrite_existing_file": True,
        }
    ]

    try:
        layer.export_layer_image("Tutorial Project", "Main Board", export_layers)
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockExportLayerImageError as e:
        assert str(e) == "Export layer image error: Image Height is invalid."

    export_layers = [
        {
            "axes_enabled": True,
            "grid_enabled": True,
            "layer_infos": layer_infos,
            "file_path": "C:\\Users\\user_id\\Downloads\\SH-image.jpg",
            "image_height": 800,
            "overwrite_existing_file": True,
        }
    ]

    try:
        layer.export_layer_image("Tutorial Project", "Main Board", export_layers)
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockExportLayerImageError as e:
        assert str(e) == "Export layer image error: Image Width is invalid."

    export_layers = [
        {
            "axes_enabled": True,
            "grid_enabled": True,
            "layer_infos": layer_infos,
            "file_path": "C:\\Users\\user_id\\Downloads\\SH-image.jpg",
            "image_height": 800,
            "image_width": 800,
        }
    ]

    try:
        layer.export_layer_image("Tutorial Project", "Main Board", export_layers)
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockExportLayerImageError as e:
        assert str(e) == "Export layer image error: Overwrite Existing File is invalid."

    test_file_path = "C:\\temp\\SH-image.jpg"
    export_layers = [
        {
            "components_enabled": True,
            "labels_enabled": True,
            "leads_enabled": True,
            "axes_enabled": True,
            "grid_enabled": True,
            "layer_infos": layer_infos,
            "file_path": test_file_path,
            "image_height": 800,
            "image_width": 800,
            "overwrite_existing_file": True,
        }
    ]

    if layer._is_connection_up():
        try:
            layer.export_layer_image("Invalid Project Name", "", export_layers)
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockExportLayerImageError

        try:
            results = layer.export_layer_image(
                "Tutorial Project", "Wrong Board Name", export_layers
            )
            for result in results:
                assert result.returnCode.value == -1
        except Exception as e:
            assert type(e) == SherlockExportLayerImageError

        try:
            results = layer.export_layer_image("Tutorial Project", "Main Board", export_layers)
            for result in results:
                assert result.returnCode.value == 0
        except Exception as e:
            pytest.fail(str(e))

        layer_infos = [
            {"layer_folder": "Components", "layers": ["comp-top"]},
            {"layer_folder": "Mechanical_Shock", "layers": ["SH Disp @ 5.2ms"]},
            {"layer_folder": "Mechanical_Shock", "layers": ["SH Strain Bot @ 5.2ms"]},
            {"layer_folder": "Random_Vibe", "layers": ["RV Strain RMS Bot"]},
        ]

        export_layers = [
            {
                "components_enabled": True,
                "labels_enabled": True,
                "leads_enabled": True,
                "axes_enabled": True,
                "grid_enabled": True,
                "layer_infos": layer_infos,
                "file_path": test_file_path,
                "image_height": 800,
                "image_width": 800,
                "overwrite_existing_file": True,
            }
        ]

        try:
            results = layer.export_layer_image("Tutorial Project", "Main Board", export_layers)
            for result in results:
                assert result.returnCode.value == 0
        except Exception as e:
            pytest.fail(str(e))

        if os.path.exists(test_file_path):
            os.remove(test_file_path)


if __name__ == "__main__":
    test_all()
