import grpc

from ansys.sherlock.core.errors import SherlockAddThermalEventError
from ansys.sherlock.core.lifecycle import Lifecycle


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    lifecycle = Lifecycle(channel)
    test_add_thermal_event(lifecycle)


def test_add_thermal_event(lifecycle):
    """Test add_thermal_event API"""

    try:
        lifecycle.add_thermal_event(
            "",
            "",
            "",
            1,
            "PER SEC",
            "STORAGE",
        )
        assert False
    except SherlockAddThermalEventError as e:
        assert e.strItr()[0] == "Add thermal event error: Invalid Project Name"

    try:
        lifecycle.add_thermal_event(
            "Test",
            "",
            "",
            1,
            "PER SEC",
            "STORAGE",
        )
        assert False
    except SherlockAddThermalEventError as e:
        assert e.strItr()[0] == "Add thermal event error: Invalid Phase Name"

    try:
        lifecycle.add_thermal_event(
            "Test",
            "Example",
            "",
            1,
            "PER SEC",
            "STORAGE",
        )
        assert False
    except SherlockAddThermalEventError as e:
        assert e.strItr()[0] == "Add thermal event error: Invalid Event Name"

    try:
        lifecycle.add_thermal_event(
            "Test",
            "Example",
            "Event1",
            -1,
            "PER SEC",
            "STORAGE",
        )
        assert False
    except SherlockAddThermalEventError as e:
        assert e.strItr()[0] == "Add thermal event error: Number of Cycles Must Be Greater Than 0"

    try:
        lifecycle.add_thermal_event(
            "Test",
            "Example",
            "Event1",
            -1,
            "PER 0.5MIN",
            "STORAGE",
        )
        assert False
    except SherlockAddThermalEventError as e:
        assert e.strItr()[0] == "Add thermal event error: Invalid Cycle Type"

    try:
        lifecycle.add_thermal_event(
            "Test",
            "Example",
            "Event1",
            1,
            "PER SEC",
            "Invalid",
        )
        assert False
    except SherlockAddThermalEventError as e:
        assert e.strItr()[0] == "Add thermal event error: Invalid Cycle State"

    # Below are the grpc-reliant tests

    # try:
    #     lifecycle.add_thermal_event(
    #         "Test", "Example", "Event1", 1, "COUNT", "STORAGE",
    #     )
    #     assert True
    # except SherlockAddThermalEventError:
    #     assert False


if __name__ == "__main__":
    test_all()
