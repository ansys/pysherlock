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
        )
        assert False
    except SherlockGenStackupError as e:
        assert str(e) == "Generate stackup error: Invalid project name"
    """TODO: Write test case."""
    pass
