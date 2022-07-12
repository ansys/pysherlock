import grpc

from ansys.sherlock.core.errors import SherlockGenStackupError, SherlockUpdateConductorLayerError
from ansys.sherlock.core.stackup import Stackup


def test_all():
    """Test all stackup APIs."""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    stackup = Stackup(channel)

    helper_test_gen_stackup(stackup)
    helper_test_update_conductor_layer(stackup)


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
        assert str(e) == "Generate stackup error: Invalid project name"

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
        assert str(e) == "Generate stackup error: Invalid cca name"

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
        assert str(e) == "Generate stackup error: Invalid board thickness provided"

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
            str(e)
            == "Generate stackup error: The number of conductor layers must be greater than 1"
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
        assert str(e) == "Generate stackup error: Invalid conductor thickness provided"

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
        assert str(e) == "Generate stackup error: Invalid laminate thickness provided"

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
        assert str(e) == "Generate stackup error: Invalid power thickness provided"

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
            assert str(e) == "Generate stackup error: Invalid board thickness unit provided"

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
            assert str(e) == "Generate stackup error: Invalid laminate manufacturer provided"

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
            assert str(e) == "Generate stackup error: Invalid laminate grade provided"

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
            assert str(e) == "Generate stackup error: Invalid laminate material provided"

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
            assert str(e) == "Generate stackup error: Invalid laminate material provided"

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
            assert str(e) == "Generate stackup error: Invalid conductor thickness unit provided"

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
            assert str(e) == "Generate stackup error: Invalid laminate thickness unit provided"

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
            assert str(e) == "Generate stackup error: Invalid power thickness unit provided"


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
        assert str(e) == "Update conductor layer error: Invalid project name"

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
        assert str(e) == "Update conductor layer error: Invalid cca name"

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
        assert str(e) == "Update conductor layer error: Missing conductor layer ID"

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
            "Invalid layer ID provided, it must be an integer greater than 0"
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
        assert str(e) == "Update conductor layer error: Invalid layer ID, layer ID must be numeric"

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
            'Invalid conductor type provided. Valid values are "SIGNAL", "POWER", or "SUBSTRATE".'
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
            assert str(e) == "Update conductor layer error: Invalid conductor material provided"

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
        assert str(e) == "Update conductor layer error: Invalid board thickness provided"

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
            assert str(e) == "Update conductor layer error: Invalid thickness unit provided"

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
            "Invalid conductor percent provided. It must be between 0 and 100"
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
        assert str(e) == "Update conductor layer error: Invalid percent, percent must be numeric"


if __name__ == "__main__":
    test_all()
