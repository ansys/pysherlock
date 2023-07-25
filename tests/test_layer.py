# © 2023 ANSYS, Inc. All rights reserved
import uuid

import grpc
import pytest

from ansys.sherlock.core.errors import (
    SherlockAddPottingRegionError,
    SherlockUpdateMountPointsByFileError,
)
from ansys.sherlock.core.layer import Layer


def test_all():
    """Test all layer APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    layer = Layer(channel)

    helper_test_update_mount_points_by_file(layer)
    helper_test_add_potting_region(layer)


def helper_test_add_potting_region(layer):
    """Test add_potting_region API."""
    try:
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
                    "shape": {"shape_type": "pcb"},
                },
            ],
        )
        assert False
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Project name is invalid."

    try:
        layer.add_potting_region("Test", "")
        assert False
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Potting regions argument is invalid."

    try:
        layer.add_potting_region("Test", [])
        assert False
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: One or more potting regions are required."

    try:
        layer.add_potting_region("Test", ["test"])
        assert False
    except SherlockAddPottingRegionError as e:
        assert (
            str(e) == "Add potting region error: "
            "Potting region argument is invalid for potting region 0."
        )

    try:
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
                    "shape": {"shape_type": "pcb"},
                },
            ],
        )
        assert False
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: CCA name is missing for potting region 0."

    try:
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
                    "shape": {"shape_type": "pcb"},
                },
            ],
        )
        assert False
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
        assert False
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
        assert False
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Shape invalid for potting region 0."

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
                    "shape": {},
                },
            ],
        )
        assert False
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Shape type missing for potting region 0."

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
                    "shape": {"shape_type": "INVALID"},
                },
            ],
        )
        assert False
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Shape type invalid for potting region 0."

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
                    "shape": {"shape_type": "POLYGONAL", "points": "INVALID"},
                },
            ],
        )
        assert False
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Invalid points argument for potting region 0."

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
                    "shape": {"shape_type": "POLYGONAL", "points": [(1, 2), (4.4, 5.5), "INVALID"]},
                },
            ],
        )
        assert False
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Point 2 invalid for potting region 0."

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
                    "shape": {
                        "shape_type": "POLYGONAL",
                        "points": [(1, 2), (4.4, 5.5, 9.9), (4.4, 5.5)],
                    },
                },
            ],
        )
        assert False
    except SherlockAddPottingRegionError as e:
        assert str(e) == "Add potting region error: Point 1 invalid for potting region 0."

    if not layer._is_connection_up():
        return

    potting_id1 = f"Test Region {uuid.uuid4()}"
    try:
        layer.add_potting_region(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "potting_id": potting_id1,
                    "side": "INVALID",
                    "material": "epoxyencapsulant",
                    "potting_units": "in",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": {
                        "shape_type": "POLYGONAL",
                        "points": [(1, 2), (4.4, 5.5), (10, 5.5)],
                        "rotation": 16.7,
                    },
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert type(e) == SherlockAddPottingRegionError

    potting_id2 = f"Test Region {uuid.uuid4()}"
    try:
        layer.add_potting_region(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "potting_id": potting_id2,
                    "side": "BOT",
                    "material": "epoxyencapsulant",
                    "potting_units": "invalid",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": {
                        "shape_type": "rectangular",
                        "length": 10,
                        "width": 44.4,
                        "center_x": 55.5,
                        "center_y": 12.3,
                        "rotation": 55.5,
                    },
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert type(e) == SherlockAddPottingRegionError

    potting_id3 = f"Test Region {uuid.uuid4()}"
    try:
        layer.add_potting_region(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "potting_id": potting_id3,
                    "side": "BOT",
                    "material": "epoxyencapsulant",
                    "potting_units": "invalid",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": {
                        "shape_type": "slot",
                        "length": 10,
                        "width": 25.5,
                        "node_count": 11,
                        "center_x": 55.5,
                        "center_y": 12.3,
                        "rotation": 55.5,
                    },
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert type(e) == SherlockAddPottingRegionError

    potting_id4 = f"Test Region {uuid.uuid4()}"
    try:
        layer.add_potting_region(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "potting_id": potting_id4,
                    "side": "BOT",
                    "material": "epoxyencapsulant",
                    "potting_units": "invalid",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": {
                        "shape_type": "circular",
                        "diameter": 10,
                        "node_count": 11,
                        "center_x": 55.5,
                        "center_y": 12.3,
                        "rotation": 55.5,
                    },
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert type(e) == SherlockAddPottingRegionError

    potting_id5 = f"Test Region {uuid.uuid4()}"
    try:
        layer.add_potting_region(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "potting_id": potting_id5,
                    "side": "BOT",
                    "material": "epoxyencapsulant",
                    "potting_units": "invalid",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": {
                        "shape_type": "PCB",
                    },
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert type(e) == SherlockAddPottingRegionError

    potting_id6 = f"Test Region {uuid.uuid4()}"
    try:
        result = layer.add_potting_region(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "potting_id": potting_id6,
                    "side": "TOP",
                    "material": "epoxyencapsulant",
                    "potting_units": "in",
                    "thickness": 0.1,
                    "standoff": 0.2,
                    "shape": {
                        "shape_type": "POLYGONAL",
                        "points": [(1, 2), (4.4, 5.5), (10, 5.5)],
                        "rotation": 16.7,
                    },
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


if __name__ == "__main__":
    test_all()
