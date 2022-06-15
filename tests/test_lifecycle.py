import grpc

from ansys.sherlock.core.errors import SherlockCreateLifePhaseError
from ansys.sherlock.core.lifecycle import Lifecycle


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    lifecycle = Lifecycle(channel)
    helper_test_create_life_phase(lifecycle)


def helper_test_create_life_phase(lifecycle):
    """Test create_life_phase API"""

    try:
        lifecycle.create_life_phase("", "", 1, "sec", 1, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.strItr()[0] == "Create life phase error: Invalid Project Name"

    try:
        lifecycle.create_life_phase("Test", "", 1, "sec", 1, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.strItr()[0] == "Create life phase error: Invalid Phase Name"

    try:
        lifecycle.create_life_phase("Test", "Example", 0, "sec", 1, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.strItr()[0] == "Create life phase error: Duration Must Be Greater Than 0"

    try:
        lifecycle.create_life_phase(
            "Test", "Example", 0, "invalid", 1, "PER SEC", description="Test1"
        )
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.strItr()[0] == "Create life phase error: Invalid Duration Unit Specified"

    try:
        lifecycle.create_life_phase("Test", "Example", 5, "sec", 0, "invalid", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.strItr()[0] == "Create life phase error: Invalid Cycle Type"

    try:
        lifecycle.create_life_phase("Test", "Example", 5, "sec", 0, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.strItr()[0] == "Create life phase error: Number of Cycles Must Be Greater Than 0"


if __name__ == "__main__":
    test_all()
