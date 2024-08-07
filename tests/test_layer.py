# © 2023-2024 ANSYS, Inc. All rights reserved
import os
import platform
import uuid

import grpc
import pytest

from ansys.sherlock.core.errors import (
    SherlockAddPottingRegionError,
    SherlockDeleteAllICTFixturesError,
    SherlockDeleteAllMountPointsError,
    SherlockDeleteAllTestPointsError,
    SherlockExportAllMountPoints,
    SherlockExportAllTestFixtures,
    SherlockExportAllTestPoints,
    SherlockUpdateMountPointsByFileError,
    SherlockUpdateTestFixturesByFileError,
    SherlockUpdateTestPointsByFileError,
)
from ansys.sherlock.core.layer import Layer
from ansys.sherlock.core.types.layer_types import PCBShape, PolygonalShape


def test_all():
    """Test all layer APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    layer = Layer(channel)

    helper_test_update_mount_points_by_file(layer)
    helper_test_delete_all_ict_fixtures(layer)
    helper_test_delete_all_mount_points(layer)
    helper_test_delete_all_test_points(layer)
    helper_test_add_potting_region(layer)
    helper_test_update_test_fixtures_by_file(layer)
    helper_test_update_test_points_by_file(layer)
    helper_test_export_all_mount_points(layer)
    helper_test_export_all_test_fixtures(layer)
    helper_test_export_all_test_points(layer)


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

    try:
        shape = PolygonalShape(points="INVALID", rotation=123.4)
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
                    "shape": shape,
                },
            ],
        )
        pytest.fail("No exception thrown when polygonal points list is invalid.")
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Invalid points argument for potting region 0."

    try:
        invalid_point = "INVALID"
        shape = PolygonalShape(points=[(1, 2), (4.4, 5.5), invalid_point], rotation=123.4)
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
                    "shape": shape,
                },
            ],
        )
        pytest.fail("No exception thrown when polygonal points list element is incorrect type.")
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Point 2 invalid for potting region 0."

    try:
        invalid_point = (4.4, 5.5, 10)
        shape = PolygonalShape(points=[(1, 2), invalid_point, (1, 6)], rotation=123.4)
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
                    "shape": shape,
                },
            ],
        )
        pytest.fail("No exception thrown when polygonal points list element is incorrect length.")
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Point 1 invalid for potting region 0."

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
                    "potting_units": "in",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": shape,
                },
            ],
        )
        assert result == 0
    except SherlockAddPottingRegionError as e:
        pytest.fail(str(e))


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

        except Exception as e:
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

        except Exception as e:
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

        except Exception as e:
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
    except SherlockExportAllTestPoints as e:
        assert e.str_itr()[0] == "Export test points error: Project name is invalid."

    try:
        layer.export_all_test_points(
            "Tutorial Project",
            "",
            "Test Points.csv",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportAllTestPoints as e:
        assert e.str_itr()[0] == "Export test points error: CCA name is invalid."

    try:
        layer.export_all_test_points(
            "Tutorial Project",
            "Main Board",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportAllTestPoints as e:
        assert e.str_itr()[0] == "Export test points error: File path is required."

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
            assert type(e) == SherlockExportAllTestPoints

        try:
            result = layer.export_all_test_points(
                "Test Point Test Project",
                "Main Board",
                test_points_file,
            )

            assert os.path.exists(test_points_file)
            assert result == 0
        except SherlockExportAllTestPoints as e:
            pytest.fail(str(e.str_itr()))


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
                "Tutorial Project",
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
            result = layer.export_all_mount_points(
                "Tutorial Project",
                "Main Board",
                mount_points_file,
            )

            assert os.path.exists(mount_points_file)
            assert result == 0
        except Exception as e:
            pytest.fail(e.message)

        try:
            layer.export_all_mount_points(
                "Tutorial Project",
                "Invalid CCA",
                mount_points_file,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockExportAllMountPoints


if __name__ == "__main__":
    test_all()
