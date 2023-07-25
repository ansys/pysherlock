# © 2023 ANSYS, Inc. All rights reserved

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

    if not layer._is_connection_up():
        return

    # layer.add_potting_region(
    #     "Tutorial Project",
    #     [{
    #         'cca_name': 'Main Board',
    #         'potting_id': 'Test Region',
    #         'side': 'TOP',
    #         'material': 'epoxyencapsulant',
    #         'potting_units': 'in',
    #         'thickness': 0.1,
    #         'standoff': 0.2,
    #         'shape': {
    #             'shape_type': 'pcb'
    #         }
    #     },
    #     ]
    # )


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
