import grpc

from ansys.sherlock.core.errors import SherlockGenStackupError
from ansys.sherlock.core.stackup import Stackup


def test_all():
    """Test all stackup APIs."""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    stackup = Stackup(channel)

    helper_test_gen_stackup(stackup)


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


if __name__ == "__main__":
    test_all()
