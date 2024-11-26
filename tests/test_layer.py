# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.
import copy
import os
import platform
import uuid

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
    PCBShape,
    PolygonalShape,
    PottingRegion,
    PottingRegionCopyData,
    PottingRegionDeleteData,
    PottingRegionUpdateData,
    RectangularShape,
    SlotShape,
    UpdatePottingRegionRequest,
)
from ansys.sherlock.core.utils.version_check import SKIP_VERSION_CHECK


def test_all():
    """Test all layer APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    layer = Layer(channel, SKIP_VERSION_CHECK)

    helper_test_update_mount_points_by_file(layer)
    helper_test_delete_all_ict_fixtures(layer)
    helper_test_delete_all_mount_points(layer)
    helper_test_delete_all_test_points(layer)
    helper_test_add_potting_region(layer)
    helper_test_update_potting_region(layer)
    helper_test_copy_potting_regions(layer)
    helper_test_delete_potting_regions(layer)
    helper_test_update_test_fixtures_by_file(layer)
    helper_test_update_test_points_by_file(layer)
    helper_test_export_all_mount_points(layer)
    helper_test_export_all_test_fixtures(layer)
    helper_test_export_all_test_points(layer)
    region_id = helper_test_add_modeling_region(layer)
    region_id = helper_test_update_modeling_region(layer, region_id)
    helper_test_copy_modeling_region(layer, region_id)
    helper_test_delete_modeling_region(layer, region_id)
    helper_test_list_layers(layer)


def helper_test_add_potting_region(layer):
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


def helper_test_update_potting_region(layer):
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


def helper_test_copy_potting_regions(layer):

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


def helper_test_delete_potting_regions(layer):

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


def helper_test_delete_all_mount_points(layer):
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


def helper_test_delete_all_ict_fixtures(layer):
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


def helper_test_delete_all_test_points(layer):
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


def helper_test_update_test_points_by_file(layer):
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


def helper_test_update_test_fixtures_by_file(layer):
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


def helper_test_export_all_test_points(layer):
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


def helper_test_export_all_test_fixtures(layer):
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


def helper_test_export_all_mount_points(layer):
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


def helper_test_add_modeling_region(layer):
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


def helper_test_update_modeling_region(layer, region_id):
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


def helper_test_copy_modeling_region(layer, region_id):
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


def helper_test_delete_modeling_region(layer, region_id):

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
        assert str(e) == "CCA name is invalid."

    try:
        layer.list_layers("", "Main Board")
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockListLayersError as e:
        assert str(e) == "Project name is invalid."

    if layer._is_connection_up():
        try:
            layer.list_layers("Invalid Project Name", "")
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockListLayersError

        try:
            layer.list_layers("Tutorial Project", "Wrong Board Name")
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockListLayersError

if __name__ == "__main__":
    test_all()
