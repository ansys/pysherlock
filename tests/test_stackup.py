# © 2023 ANSYS, Inc. All rights reserved

import time

import grpc
import pytest

from ansys.sherlock.core.errors import (
    SherlockGenStackupError,
    SherlockGetLayerCountError,
    SherlockGetStackupPropsError,
    SherlockGetTotalConductorThicknessError,
    SherlockListConductorLayersError,
    SherlockListLaminateLayersError,
    SherlockUpdateConductorLayerError,
    SherlockUpdateLaminateLayerError,
)
from ansys.sherlock.core.stackup import Stackup


def test_all():
    """Test all stackup APIs."""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    stackup = Stackup(channel)
    helper_test_gen_stackup(stackup)
    helper_test_update_conductor_layer(stackup)
    helper_test_update_laminate_layer(stackup)
    helper_test_list_conductor_layers(stackup)
    helper_test_list_laminate_layers(stackup)
    helper_test_get_layer_count(stackup)
    helper_test_get_stackup_props(stackup)
    helper_test_get_total_conductor_thickness(stackup)


def helper_test_gen_stackup(stackup):
    """Test gen_stackup API."""
    try:
        stackup.gen_stackup(
            "",
            "Card",
            82.6,
            "mil",
            "Generic",
            "FR-4",
            "Generic FR-4",
            6,
            0.5,
            "oz",
            1.0,
            "mil",
            False,
            1.0,
            "mil",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGenStackupError as e:
        assert str(e) == "Generate stackup error: Project name is invalid."

    try:
        stackup.gen_stackup(
            "Test",
            "",
            82.6,
            "mil",
            "Generic",
            "FR-4",
            "Generic FR-4",
            6,
            0.5,
            "oz",
            1.0,
            "mil",
            False,
            1.0,
            "mil",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGenStackupError as e:
        assert str(e) == "Generate stackup error: CCA name is invalid."

    try:
        stackup.gen_stackup(
            "Test",
            "Card",
            82.6,
            "mil",
            "Generic",
            "FR-4",
            "Generic FR-4",
            1,
            0.5,
            "oz",
            1.0,
            "mil",
            False,
            1.0,
            "mil",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGenStackupError as e:
        assert (
            str(e) == "Generate stackup error: Number of conductor layers must be greater than 1."
        )

    try:
        stackup.gen_stackup(
            "Test",
            "Card",
            82.6,
            "mil",
            "Generic",
            "FR-4",
            "Generic FR-4",
            6,
            -4,
            "oz",
            1.0,
            "mil",
            False,
            1.0,
            "mil",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGenStackupError as e:
        assert str(e) == "Generate stackup error: Conductor thickness is invalid."

    if stackup._is_connection_up():
        try:
            stackup.gen_stackup(
                "Invalid Project",
                "Card",
                82.6,
                "mil",
                "Generic",
                "FR-4",
                "Generic FR-4",
                6,
                0.5,
                "oz",
                1.0,
                "mil",
                False,
                1.0,
                "mil",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockGenStackupError

        try:
            result = stackup.gen_stackup(
                "Tutorial Project",
                "Main Board",
                82.6,
                "mil",
                "Generic",
                "FR-4",
                "Generic FR-4",
                6,
                0.5,
                "oz",
                1.0,
                "mil",
                False,
                1.0,
                "mil",
            )
            assert result == 0
            # wait for the process to finish to allow tests that modify a layer to succeed
            time.sleep(2)
        except SherlockGenStackupError as e:
            pytest.fail(str(e))


def helper_test_update_conductor_layer(stackup):
    """Test update_conductor_layer API."""
    try:
        stackup.update_conductor_layer(
            "",
            "Card",
            "3",
            "POWER",
            "COPPER",
            1.0,
            "oz",
            "94.2",
            "Generic FR-4 Generic FR-4",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateConductorLayerError as e:
        assert str(e) == "Update conductor layer error: Project name is invalid."

    try:
        stackup.update_conductor_layer(
            "Test",
            "",
            "3",
            "POWER",
            "COPPER",
            1.0,
            "oz",
            "94.2",
            "Generic FR-4 Generic FR-4",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateConductorLayerError as e:
        assert str(e) == "Update conductor layer error: CCA name is invalid."

    try:
        stackup.update_conductor_layer(
            "Test",
            "Card",
            "3",
            "Invalid",
            "COPPER",
            1.0,
            "oz",
            "94.2",
            "Generic FR-4 Generic FR-4",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateConductorLayerError as e:
        assert (
            str(e) == "Update conductor layer error: "
            'Conductor type is invalid. Options are "SIGNAL", "POWER", and "SUBSTRATE".'
        )

    if stackup._is_connection_up():
        try:
            stackup.update_conductor_layer(
                "Test",
                "Card",
                "3",
                "",
                "Invalid",
                1.0,
                "oz",
                "94.2",
                "Generic FR-4 Generic FR-4",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockUpdateConductorLayerError as e:
            assert str(e) == "Update conductor layer error: Conductor material is invalid."

    if stackup._is_connection_up():
        try:
            stackup.update_conductor_layer(
                "Invalid Project",
                "Main Board",
                "3",
                "POWER",
                "COPPER",
                2.0,
                "oz",
                "94.2",
                "Generic FR-4 Generic FR-4",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdateConductorLayerError

        try:
            # NOTE: Don't modify the thickness because that changes
            # the result of get_total_conductor_thickness.
            result = stackup.update_conductor_layer(
                "Tutorial Project",
                "Main Board",
                "3",
                "POWER",
                "ALUMINA",
                # thickness=0.5,
                # thickness_unit="oz",
                conductor_percent="94.2",
                resin_material="Generic FR-4 Generic FR-4",
            )
            assert result == 0
            time.sleep(1)
        except SherlockUpdateConductorLayerError as e:
            pytest.fail(str(e))


def helper_test_update_laminate_layer(stackup):
    """Test update_laminate_layer API."""

    try:
        stackup.update_laminate_layer(
            "",
            "Card",
            "2",
            "Generic",
            "FR-4",
            "Generic FR-4",
            0.015,
            "in",
            "106",
            [("106", 68.0, 0.015, "in")],
            "E-GLASS",
            "COPPER",
            "0.0",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateLaminateLayerError as e:
        assert str(e) == "Update laminate layer error: Project name is invalid."

    try:
        stackup.update_laminate_layer(
            "Test",
            "",
            "2",
            "Generic",
            "FR-4",
            "Generic FR-4",
            0.015,
            "in",
            "106",
            [("106", 68.0, 0.015, "in")],
            "E-GLASS",
            "COPPER",
            "0.0",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateLaminateLayerError as e:
        assert str(e) == "Update laminate layer error: CCA name is invalid."

    if stackup._is_connection_up():
        try:
            stackup.update_laminate_layer(
                "Test",
                "Card",
                "2",
                "Invalid",
                "FR-4",
                "Generic FR-4",
                0.015,
                "in",
                "106",
                [("106", 68.0, 0.015, "in")],
                "E-GLASS",
                "COPPER",
                "0.0",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockUpdateLaminateLayerError as e:
            assert str(e) == "Update laminate layer error: Laminate manufacturer is invalid."

        try:
            stackup.update_laminate_layer(
                "Test",
                "Card",
                "2",
                "Generic",
                "Invalid",
                "Generic FR-4",
                0.015,
                "in",
                "106",
                [("106", 68.0, 0.015, "in")],
                "E-GLASS",
                "COPPER",
                "0.0",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockUpdateLaminateLayerError as e:
            assert str(e) == "Update laminate layer error: Laminate grade is invalid."

        try:
            stackup.update_laminate_layer(
                "Test",
                "Card",
                "2",
                "Generic",
                "FR-4",
                "Invalid",
                0.015,
                "in",
                "106",
                [("106", 68.0, 0.015, "in")],
                "E-GLASS",
                "COPPER",
                "0.0",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockUpdateLaminateLayerError as e:
            assert str(e) == "Update laminate layer error: Laminate material is invalid."

    try:
        stackup.update_laminate_layer(
            "Tutorial Project",
            "Main Board",
            "2",
            "Generic",
            "FR-4",
            "Generic FR-4",
            0.015,
            "in",
            "106",
            "Invalid",
            "E-GLASS",
            "COPPER",
            "0.0",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateLaminateLayerError as e:
        assert str(e) == "Update laminate layer error: glass_construction argument is invalid."

    try:
        stackup.update_laminate_layer(
            "Test",
            "Card",
            "2",
            "Generic",
            "FR-4",
            "Generic FR-4",
            0.015,
            "in",
            "106",
            [("106", 0.015, "in")],
            "E-GLASS",
            "COPPER",
            "0.0",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateLaminateLayerError as e:
        assert (
            str(e) == "Update laminate layer error: "
            "Invalid layer 0: Number of elements is wrong."
        )

    if stackup._is_connection_up():
        try:
            stackup.update_laminate_layer(
                "Invalid Project",
                "Card",
                "2",
                "Generic",
                "FR-4",
                "Generic FR-4",
                0.015,
                "in",
                "106",
                [("106", 68.0, 0.015, "in")],
                "E-GLASS",
                "COPPER",
                "0.0",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdateLaminateLayerError

        try:
            result = stackup.update_laminate_layer(
                "Tutorial Project",
                "Main Board",
                "2",
                "Generic",
                "FR-4",
                "Generic FR-4",
                15.4,
                "mil",
                "106",
                [("106", 68.0, 0.0154, "in")],
                "E-GLASS",
                "COPPER",
                "0.0",
            )
            assert result == 0
            time.sleep(1)
        except SherlockUpdateLaminateLayerError as e:
            pytest.fail(str(e))


def helper_test_list_conductor_layers(stackup):
    """Test list_conductor_layers API"""
    try:
        stackup.list_conductor_layers("")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockListConductorLayersError as e:
        assert str(e) == "List conductor layer error: Project name is invalid."

    if stackup._is_connection_up():
        try:
            stackup.list_conductor_layers("Invalid Project")
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockListConductorLayersError

        try:
            layer_properties_per_board = stackup.list_conductor_layers("Tutorial Project")
            assert len(layer_properties_per_board) == 1
            layer_properties_of_board = layer_properties_per_board[0]
            assert layer_properties_of_board.ccaName == "Main Board"
            layer_properties_per_layer = layer_properties_of_board.conductorLayerProps
            assert len(layer_properties_per_layer) == 6, "Incorrect number of conductor layers"
            layer_properties = layer_properties_per_layer[0]
            assert layer_properties.layer == "1"
            assert layer_properties.type == "SIGNAL"
        except SherlockListConductorLayersError as e:
            pytest.fail(str(e))


def helper_test_list_laminate_layers(stackup):
    """Test list_laminate_layers API"""
    try:
        stackup.list_laminate_layers("")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockListLaminateLayersError as e:
        assert str(e) == "List laminate layer error: Project name is invalid."

    if stackup._is_connection_up():
        try:
            stackup.list_laminate_layers("Invalid Project")
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockListLaminateLayersError

        try:
            layer_properties_per_board = stackup.list_laminate_layers("Tutorial Project")
            assert len(layer_properties_per_board) == 1
            layer_properties_of_board = layer_properties_per_board[0]
            assert layer_properties_of_board.ccaName == "Main Board"
            layer_properties_per_layer = layer_properties_of_board.laminateProps
            assert len(layer_properties_per_layer) == 5, "Incorrect number of laminate layers"
            layer_properties = layer_properties_per_layer[0]
            assert layer_properties.layer == "2"
        except SherlockListLaminateLayersError as e:
            pytest.fail(str(e))


def helper_test_get_layer_count(stackup):
    """Test get_layer_count API"""
    try:
        stackup.get_layer_count(project="", cca_name="Card")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetLayerCountError as e:
        assert str(e) == "Get layer count error: Project name is invalid."

    try:
        stackup.get_layer_count(project="Test", cca_name="")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetLayerCountError as e:
        assert str(e) == "Get layer count error: CCA name is invalid."

    """Test get_layer_count API"""
    try:
        stackup.get_layer_count(
            "",
            "Card",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetLayerCountError as e:
        assert str(e) == "Get layer count error: Project name is invalid."

    try:
        stackup.get_layer_count(
            "Test",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetLayerCountError as e:
        assert str(e) == "Get layer count error: CCA name is invalid."

    if stackup._is_connection_up():
        try:
            stackup.get_layer_count(
                "Tutorial Project",
                "Invalid CCA",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockGetLayerCountError

        try:
            layer_count = stackup.get_layer_count(
                "Tutorial Project",
                "Main Board",
            )
            assert layer_count == 11
        except SherlockGetLayerCountError as e:
            pytest.fail(str(e))


def helper_test_get_stackup_props(stackup):
    """Test get_stackup_props API"""
    try:
        stackup.get_stackup_props(
            "",
            "Card",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetStackupPropsError as e:
        assert str(e) == "Get stackup prop error: Project name is invalid."
    try:
        stackup.get_stackup_props(
            "Test",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetStackupPropsError as e:
        assert str(e) == "Get stackup prop error: CCA name is invalid."

    if stackup._is_connection_up():
        try:
            stackup.get_stackup_props(
                "Tutorial Project",
                "Invalid CCA",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockGetLayerCountError

        try:
            stackup_properties = stackup.get_stackup_props(
                "Tutorial Project",
                "Main Board",
            )
            assert stackup_properties.conductorLayersCnt == "6"
        except SherlockGetLayerCountError as e:
            pytest.fail(str(e))


def helper_test_get_total_conductor_thickness(stackup):
    try:
        stackup.get_total_conductor_thickness(project="", cca_name="Card", thickness_unit="oz")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetTotalConductorThicknessError as e:
        assert str(e) == "Get total conductor thickness error: Invalid project name"

    try:
        stackup.get_total_conductor_thickness(project="Test", cca_name="", thickness_unit="oz")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetTotalConductorThicknessError as e:
        assert str(e) == "Get total conductor thickness error: Invalid CCA name"

    try:
        stackup.get_total_conductor_thickness(project="Test", cca_name="Card", thickness_unit="")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetTotalConductorThicknessError as e:
        assert str(e) == "Get total conductor thickness error: Invalid thickness unit"

    if stackup._is_connection_up():
        try:
            stackup.get_total_conductor_thickness(
                "Tutorial Project",
                "Invalid CCA",
                "mm",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockGetTotalConductorThicknessError

        try:
            thickness = stackup.get_total_conductor_thickness(
                "Tutorial Project",
                "Main Board",
                "oz",
            )
            assert thickness == 3
        except SherlockGetTotalConductorThicknessError as e:
            pytest.fail(str(e))


if __name__ == "__main__":
    test_all()
