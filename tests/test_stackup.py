# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

import grpc

from ansys.sherlock.core.errors import (
    SherlockGenStackupError,
    SherlockGetLayerCountError,
    SherlockGetStackupPropsError,
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
    helper_test_get_stackup_props(stackup)

    helper_test_get_layer_count(stackup)


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
        assert False
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
        assert False
    except SherlockGenStackupError as e:
        assert str(e) == "Generate stackup error: CCA name is invalid."

    try:
        stackup.gen_stackup(
            "Test",
            "Card",
            -5,
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
        assert False
    except SherlockGenStackupError as e:
        assert str(e) == "Generate stackup error: Board thickness is invalid."

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
        assert False
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
        assert False
    except SherlockGenStackupError as e:
        assert str(e) == "Generate stackup error: Conductor thickness is invalid."

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
            0.5,
            "oz",
            -10,
            "mil",
            False,
            1.0,
            "mil",
        )
        assert False
    except SherlockGenStackupError as e:
        assert str(e) == "Generate stackup error: Laminate thickness is invalid."

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
            0.5,
            "oz",
            1.0,
            "mil",
            False,
            -1,
            "mil",
        )
        assert False
    except SherlockGenStackupError as e:
        assert str(e) == "Generate stackup error: Power thickness is invalid."

    if stackup._is_connection_up():
        try:
            stackup.gen_stackup(
                "Test",
                "Card",
                82.6,
                "Invalid",
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
            assert False
        except SherlockGenStackupError as e:
            assert str(e) == "Generate stackup error: Board thickness units are invalid."

        try:
            stackup.gen_stackup(
                "Test",
                "Card",
                82.6,
                "mil",
                "Invalid",
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
            assert False
        except SherlockGenStackupError as e:
            assert str(e) == "Generate stackup error: Laminate manufacturer is invalid."

        try:
            stackup.gen_stackup(
                "Test",
                "Card",
                82.6,
                "mil",
                "Generic",
                "Invalid",
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
            assert False
        except SherlockGenStackupError as e:
            assert str(e) == "Generate stackup error: Laminate grade is invalid."

        try:
            stackup.gen_stackup(
                "Test",
                "Card",
                82.6,
                "mil",
                "Generic",
                "FR-4",
                "Invalid",
                6,
                0.5,
                "oz",
                1.0,
                "mil",
                False,
                1.0,
                "mil",
            )
            assert False
        except SherlockGenStackupError as e:
            assert str(e) == "Generate stackup error: Laminate material is invalid."

        try:
            stackup.gen_stackup(
                "Test",
                "Card",
                82.6,
                "mil",
                "Hitachi",
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
            assert False
        except SherlockGenStackupError as e:
            assert str(e) == "Generate stackup error: Laminate material is invalid."

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
                0.5,
                "Invalid",
                1.0,
                "mil",
                False,
                1.0,
                "mil",
            )
            assert False
        except SherlockGenStackupError as e:
            assert str(e) == "Generate stackup error: Conductor thickness units are invalid."

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
                0.5,
                "oz",
                1.0,
                "Invalid",
                False,
                1.0,
                "mil",
            )
            assert False
        except SherlockGenStackupError as e:
            assert str(e) == "Generate stackup error: Laminate thickness units are invalid."

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
                0.5,
                "oz",
                1.0,
                "mil",
                False,
                1.0,
                "Invalid",
            )
            assert False
        except SherlockGenStackupError as e:
            assert str(e) == "Generate stackup error: Power thickness units are invalid."


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
        assert False
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
        assert False
    except SherlockUpdateConductorLayerError as e:
        assert str(e) == "Update conductor layer error: CCA name is invalid."

    try:
        stackup.update_conductor_layer(
            "Test",
            "Card",
            "",
            "POWER",
            "COPPER",
            1.0,
            "oz",
            "94.2",
            "Generic FR-4 Generic FR-4",
        )
        assert False
    except SherlockUpdateConductorLayerError as e:
        assert str(e) == "Update conductor layer error: Layer ID conductor is missing."

    try:
        stackup.update_conductor_layer(
            "Test",
            "Card",
            "-4",
            "POWER",
            "COPPER",
            1.0,
            "oz",
            "94.2",
            "Generic FR-4 Generic FR-4",
        )
        assert False
    except SherlockUpdateConductorLayerError as e:
        assert str(e) == (
            "Update conductor layer error: "
            "Layer ID is invalid. It must be an integer greater than 0."
        )

    try:
        stackup.update_conductor_layer(
            "Test",
            "Card",
            "Invalid",
            "POWER",
            "COPPER",
            1.0,
            "oz",
            "94.2",
            "Generic FR-4 Generic FR-4",
        )
        assert False
    except SherlockUpdateConductorLayerError as e:
        assert (
            str(e) == "Update conductor layer error: Layer ID is invalid. "
            "It must be an integer greater than 0."
        )

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
        assert False
    except SherlockUpdateConductorLayerError as e:
        assert str(e) == (
            "Update conductor layer error: "
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
            assert False
        except SherlockUpdateConductorLayerError as e:
            assert str(e) == "Update conductor layer error: Conductor material is invalid."

    try:
        stackup.update_conductor_layer(
            "Test",
            "Card",
            "3",
            "POWER",
            "COPPER",
            -4,
            "oz",
            "94.2",
            "Generic FR-4 Generic FR-4",
        )
        assert False
    except SherlockUpdateConductorLayerError as e:
        assert str(e) == "Update conductor layer error: Conductor thickness is invalid."

    if stackup._is_connection_up():
        try:
            stackup.update_conductor_layer(
                "Test",
                "Card",
                "3",
                "POWER",
                "COPPER",
                1.0,
                "Invalid",
                "94.2",
                "Generic FR-4 Generic FR-4",
            )
            assert False
        except SherlockUpdateConductorLayerError as e:
            assert (
                str(e) == "Update conductor layer error: Conductor thickness units are invalid."
            )

    try:
        stackup.update_conductor_layer(
            "Test",
            "Card",
            "3",
            "POWER",
            "COPPER",
            0,
            "oz",
            "105",
            "Generic FR-4 Generic FR-4",
        )
        assert False
    except SherlockUpdateConductorLayerError as e:
        assert str(e) == (
            "Update conductor layer error: "
            "Conductor percent is invalid. It must be between 0 and 100."
        )

    try:
        stackup.update_conductor_layer(
            "Test",
            "Card",
            "3",
            "POWER",
            "COPPER",
            1.0,
            "oz",
            "Invalid",
            "Generic FR-4 Generic FR-4",
        )
        assert False
    except SherlockUpdateConductorLayerError as e:
        assert (
            str(e) == "Update conductor layer error: Conductor percent is invalid. "
            "It must be between 0 and 100."
        )


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
        assert False
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
        assert False
    except SherlockUpdateLaminateLayerError as e:
        assert str(e) == "Update laminate layer error: CCA name is invalid."

    try:
        stackup.update_laminate_layer(
            "Test",
            "Card",
            "",
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
        assert False
    except SherlockUpdateLaminateLayerError as e:
        assert str(e) == "Update laminate layer error: Layer ID laminate is missing."

    try:
        stackup.update_laminate_layer(
            "Test",
            "Card",
            "-2",
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
        assert False
    except SherlockUpdateLaminateLayerError as e:
        assert str(e) == (
            "Update laminate layer error: Layer ID is invalid. "
            "It must be an integer greater than 0."
        )

    try:
        stackup.update_laminate_layer(
            "Test",
            "Card",
            "Invalid",
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
        assert False
    except SherlockUpdateLaminateLayerError as e:
        assert (
            str(e) == "Update laminate layer error: Layer ID is invalid. "
            "It must be an integer greater than 0."
        )

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
            assert False
        except SherlockUpdateLaminateLayerError as e:
            assert str(e) == "Update laminate layer error: Laminate manufacturer is invalid."

    if stackup._is_connection_up():
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
            assert False
        except SherlockUpdateLaminateLayerError as e:
            assert str(e) == "Update laminate layer error: Laminate grade is invalid."

    if stackup._is_connection_up():
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
            assert False
        except SherlockUpdateLaminateLayerError as e:
            assert str(e) == "Update laminate layer error: Laminate material is invalid."

    try:
        stackup.update_laminate_layer(
            "Test",
            "Card",
            "2",
            "Generic",
            "FR-4",
            "Generic FR-4",
            -0.015,
            "in",
            "106",
            [("106", 68.0, 0.015, "in")],
            "E-GLASS",
            "COPPER",
            "0.0",
        )
        assert False
    except SherlockUpdateLaminateLayerError as e:
        assert str(e) == "Update laminate layer error: Laminate thickness is invalid."

    if stackup._is_connection_up():
        try:
            stackup.update_laminate_layer(
                "Test",
                "Card",
                "2",
                "Generic",
                "FR-4",
                "Generic FR-4",
                0.015,
                "Invalid",
                "106",
                [("106", 68.0, 0.015, "in")],
                "E-GLASS",
                "COPPER",
                "0.0",
            )
            assert False
        except SherlockUpdateLaminateLayerError as e:
            assert str(e) == "Update laminate layer error: Laminate thickness units are invalid."

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
            "Invalid",
            "E-GLASS",
            "COPPER",
            "0.0",
        )
        assert False
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
        assert False
    except SherlockUpdateLaminateLayerError as e:
        assert (
            str(e) == "Update laminate layer error: Invalid layer 0: Number of arguments "
            "is wrong."
        )

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
            [("106", 68.0, -0.015, "in")],
            "E-GLASS",
            "COPPER",
            "0.0",
        )
        assert False
    except SherlockUpdateLaminateLayerError as e:
        assert str(e) == "Update laminate layer error: Invalid layer 0: Thickness is invalid."

    if stackup._is_connection_up():
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
                [("106", 68.0, 0.015, "Invalid")],
                "E-GLASS",
                "COPPER",
                "0.0",
            )
            assert False
        except SherlockUpdateLaminateLayerError as e:
            assert (
                str(e)
                == "Update laminate layer error: Invalid layer 0: Thickness units are invalid."
            )

    if stackup._is_connection_up():
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
                [("106", 68.0, 0.015, "in")],
                "Invalid",
                "COPPER",
                "0.0",
            )
            assert False
        except SherlockUpdateLaminateLayerError as e:
            assert str(e) == "Update laminate layer error: Fiber material is invalid."

    if stackup._is_connection_up():
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
                [("106", 68.0, 0.015, "in")],
                "E-GLASS",
                "Invalid",
                "0.0",
            )
            assert False
        except SherlockUpdateLaminateLayerError as e:
            assert str(e) == "Update laminate layer error: Conductor material is invalid."

    try:
        stackup.update_laminate_layer(
            "Test",
            "Card",
            "2",
            "",
            "FR-4",
            "Generic FR-4",
            0,
            "Invalid",
            "106",
            [("106", 68.0, 0.015, "in")],
            "",
            "",
            "101",
        )
        assert False
    except SherlockUpdateLaminateLayerError as e:
        assert str(e) == (
            "Update laminate layer error: Conductor percent is invalid."
            " It must be between 0 and 100."
        )


def helper_test_list_conductor_layers(stackup):
    """Test list_conductor_layers API"""
    try:
        stackup.list_conductor_layers("")
        assert False
    except SherlockListConductorLayersError as e:
        assert str(e) == "List conductor layer error: Project name is invalid."


def helper_test_list_laminate_layers(stackup):
    """Test list_laminate_layers API"""
    try:
        stackup.list_laminate_layers("")
        assert False
    except SherlockListLaminateLayersError as e:
        assert str(e) == "List laminate layer error: Project name is invalid."


def helper_test_get_stackup_props(stackup):
    """Test get_stackup_props API"""
    try:
        stackup.get_stackup_props(
            "",
            "Card",
        )
        assert False
    except SherlockGetStackupPropsError as e:
        assert str(e) == "Get stackup prop error: Project name is invalid."
    try:
        stackup.get_stackup_props(
            "Test",
            "",
        )
        assert False
    except SherlockGetStackupPropsError as e:
        assert str(e) == "Get stackup prop error: CCA name is invalid."


def helper_test_get_layer_count(stackup):
    """Test get_layer_count API"""
    try:
        stackup.get_layer_count(project="", cca_name="Card")
        assert False
    except SherlockGetLayerCountError as e:
        assert str(e) == "Get layer count error: Project name is invalid."

    try:
        stackup.get_layer_count(project="Test", cca_name="")
        assert False
    except SherlockGetLayerCountError as e:
        assert str(e) == "Get layer count error: CCA name is invalid."

    """Test get_layer_count API"""
    try:
        stackup.get_layer_count(
            "",
            "Card",
        )
        assert False
    except SherlockGetLayerCountError as e:
        assert str(e) == "Get layer count error: Project name is invalid."

    try:
        stackup.get_layer_count(
            "Test",
            "",
        )
        assert False
    except SherlockGetLayerCountError as e:
        assert str(e) == "Get layer count error: CCA name is invalid."


if __name__ == "__main__":
    test_all()
