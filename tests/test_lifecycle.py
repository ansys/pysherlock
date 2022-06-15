import grpc

from ansys.sherlock.core.errors import SherlockAddThermalProfileError
from ansys.sherlock.core.lifecycle import Lifecycle


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    lifecycle = Lifecycle(channel)
    test_add_thermal_profile(lifecycle)


def test_add_thermal_profile(lifecycle):
    """Test add_thermal_profile API."""

    try:
        lifecycle.add_thermal_profile(
            "Test",
            "Example",
            "Event1",
            "",
            "sec",
            "F",
            [
                ("Initial", "HOLD", 40, 40),
                ("Up", "RAMP", 20, 20),
                ("Back", "RAMP", 20, 40),
            ],
        )
        assert False
    except SherlockAddThermalProfileError as e:
        assert e.strItr()[0] == "Add thermal profile error: Invalid Profile Name"

    try:
        lifecycle.add_thermal_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "Sec",
            "F",
            [
                ("Initial", "HOLD", 40, 40),
                ("Up", "RAMP", 20, 20),
                ("Back", "RAMP", 20, 40),
            ],
        )
        assert False
    except SherlockAddThermalProfileError as e:
        assert e.strItr()[0] == "Add thermal profile error: Invalid Time Unit"

    try:
        lifecycle.add_thermal_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "sec",
            "IDK",
            [
                ("Initial", "HOLD", 40, 40),
                ("Up", "RAMP", 20, 20),
                ("Back", "RAMP", 20, 40),
            ],
        )
        assert False
    except SherlockAddThermalProfileError as e:
        assert e.strItr()[0] == "Add thermal profile error: Invalid Temperature Unit"

    try:
        lifecycle.add_thermal_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "sec",
            "F",
            [
                ("HOLD", 40, 40),
                ("Up", "RAMP", 20, 20),
                ("Back", "RAMP", 20, 40),
            ],
        )
        assert False
    except SherlockAddThermalProfileError as e:
        assert e.strItr()[0] == "Add thermal profile error: Invalid entry 0: Wrong number of args"

    try:
        lifecycle.add_thermal_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "sec",
            "F",
            [
                ("Initial", "HOLD", 40, 40),
                (0, "RAMP", 20, 20),
                ("Back", "RAMP", 20, 40),
            ],
        )
        assert False
    except SherlockAddThermalProfileError as e:
        assert e.strItr()[0] == "Add thermal profile error: Invalid entry 1: Invalid step name"

    try:
        lifecycle.add_thermal_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "sec",
            "F",
            [
                ("Initial", "HOLD", 40, 40),
                ("Up", "RAMP", 20, 20),
                ("Back", "INVALID", 20, 40),
            ],
        )
        assert False
    except SherlockAddThermalProfileError as e:
        assert e.strItr()[0] == "Add thermal profile error: Invalid entry 2: Invalid step type"

    try:
        lifecycle.add_thermal_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "sec",
            "F",
            [
                ("Initial", "HOLD", 40, 40),
                ("Up", "RAMP", 0, 20),
                ("Back", "RAMP", 20, 40),
            ],
        )
        assert False
    except SherlockAddThermalProfileError as e:
        assert (
            e.strItr()[0]
            == "Add thermal profile error: Invalid entry 1: Time must be greater than 0"
        )

    try:
        lifecycle.add_thermal_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "sec",
            "F",
            [
                ("Initial", "HOLD", 40, 40),
                ("Up", "RAMP", "Invalid", 20),
                ("Back", "RAMP", 20, 40),
            ],
        )
        assert False
    except SherlockAddThermalProfileError as e:
        print(e.strItr()[0])
        assert e.strItr()[0] == "Add thermal profile error: Invalid entry 1: Invalid time"

    try:
        lifecycle.add_thermal_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "sec",
            "F",
            [
                ("Initial", "HOLD", 40, "40"),
                ("Up", "RAMP", 20, 20),
                ("Back", "RAMP", 20, 40),
            ],
        )
        assert False
    except SherlockAddThermalProfileError as e:
        assert e.strItr()[0] == "Add thermal profile error: Invalid entry 0: Invalid temp"

    # Below are the grpc-reliant testcases

    # try:
    #     lifecycle.add_thermal_profile(
    #         "Test",
    #         "Example",
    #         "Event1",
    #         "Profile5",
    #         "sec",
    #         "F",
    #         [
    #             ("Initial", "HOLD", 40, 40),
    #             ("Up", "RAMP", 20, 20),
    #             ("Back", "RAMP", 20, 40),
    #         ],
    #     )
    #     assert True
    # except SherlockAddThermalProfileError:
    #     assert False


if __name__ == "__main__":
    test_all()
