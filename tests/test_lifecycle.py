import grpc

from ansys.sherlock.core.errors import (
    SherlockAddHarmonicEventError,
    SherlockAddRandomVibeEventError,
    SherlockAddRandomVibeProfileError,
    SherlockAddThermalEventError,
    SherlockAddThermalProfileError,
    SherlockCreateLifePhaseError,
)
from ansys.sherlock.core.lifecycle import Lifecycle


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    lifecycle = Lifecycle(channel)

    helper_test_create_life_phase(lifecycle)
    helper_test_add_random_vibe_event(lifecycle)
    helper_test_add_random_vibe_profile(lifecycle)
    helper_test_add_thermal_event(lifecycle)
    helper_test_add_thermal_profile(lifecycle)
    helper_test_add_harmonic_event(lifecycle)


def helper_test_add_random_vibe_event(lifecycle):
    """Test add_random_vibe_event API"""

    try:
        lifecycle.add_random_vibe_event(
            "", "", "", 1, "sec", 1, "PER SEC", "45,45", "Uniaxial", "1,2,3", description="Test1"
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.str_itr()[0] == "Add random vibe event error: Invalid Project Name"

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "",
            "",
            1,
            "sec",
            1,
            "PER SEC",
            "45,45",
            "Uniaxial",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.str_itr()[0] == "Add random vibe event error: Invalid Phase Name"

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "",
            1,
            "sec",
            1,
            "PER SEC",
            "45,45",
            "Uniaxial",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.str_itr()[0] == "Add random vibe event error: Invalid Event Name"

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            0,
            "sec",
            1,
            "PER SEC",
            "45,45",
            "Uniaxial",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.str_itr()[0] == "Add random vibe event error: Duration Must Be Greater Than 0"

    if lifecycle._is_connection_up():
        try:
            lifecycle.add_random_vibe_event(
                "Test",
                "Example",
                "Event1",
                0,
                "invalid",
                1,
                "PER SEC",
                "45,45",
                "Uniaxial",
                "1,2,3",
                description="Test1",
            )
            assert False
        except SherlockAddRandomVibeEventError as e:
            assert e.str_itr()[0] == "Add random vibe event error: Invalid Duration Unit Specified"

        try:
            lifecycle.add_random_vibe_event(
                "Test",
                "Example",
                "Event1",
                5,
                "sec",
                0,
                "invalid",
                "45,45",
                "Uniaxial",
                "1,2,3",
                description="Test1",
            )
            assert False
        except SherlockAddRandomVibeEventError as e:
            assert e.str_itr()[0] == "Add random vibe event error: Invalid Cycle Type"

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            5,
            "sec",
            0,
            "PER SEC",
            "45,45",
            "Uniaxial",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert (
            e.str_itr()[0] == "Add random vibe event error: Number of Cycles Must Be Greater Than 0"
        )

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            5,
            "sec",
            4,
            "PER SEC",
            "45,x",
            "Uniaxial",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.str_itr()[0] == "Add random vibe event error: Invalid elevation value"

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            5,
            "sec",
            4,
            "PER MIN",
            "45,45",
            "Uniaxial",
            "0,0,0",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert (
            e.str_itr()[0]
            == "Add random vibe event error: At least one direction coordinate must be non-zero"
        )

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            5,
            "sec",
            4,
            "PER MIN",
            "4545",
            "Uniaxial",
            "0,1,0",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert (
            e.str_itr()[0] == "Add random vibe event error: Invalid number of spherical coordinates"
        )


def helper_test_create_life_phase(lifecycle):
    """Test create_life_phase API"""

    try:
        lifecycle.create_life_phase("", "", 1, "sec", 1, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.str_itr()[0] == "Create life phase error: Invalid Project Name"

    try:
        lifecycle.create_life_phase("Test", "", 1, "sec", 1, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.str_itr()[0] == "Create life phase error: Invalid Phase Name"

    try:
        lifecycle.create_life_phase("Test", "Example", 0, "sec", 1, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.str_itr()[0] == "Create life phase error: Duration Must Be Greater Than 0"

    if lifecycle._is_connection_up():
        try:
            lifecycle.create_life_phase(
                "Test", "Example", 0, "invalid", 1, "PER SEC", description="Test1"
            )
            assert False
        except SherlockCreateLifePhaseError as e:
            assert e.str_itr()[0] == "Create life phase error: Invalid Duration Unit Specified"

        try:
            lifecycle.create_life_phase(
                "Test", "Example", 5, "sec", 0, "invalid", description="Test1"
            )
            assert False
        except SherlockCreateLifePhaseError as e:
            assert e.str_itr()[0] == "Create life phase error: Invalid Cycle Type"

    try:
        lifecycle.create_life_phase("Test", "Example", 5, "sec", 0, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.str_itr()[0] == "Create life phase error: Number of Cycles Must Be Greater Than 0"


def helper_test_add_random_vibe_profile(lifecycle):
    """Test the add_random_vibe_profile API"""

    try:
        lifecycle.add_random_vibe_profile(
            "Test",
            "Example",
            "Event1",
            "",
            "HZ",
            "G2/Hz",
            [(1, 2), (3, 4), (5, 6)],
        )
        assert False
    except SherlockAddRandomVibeProfileError as e:
        assert e.str_itr()[0] == "Add random vibe profile error: Invalid Profile Name"

    if lifecycle._is_connection_up():
        try:
            lifecycle.add_random_vibe_profile(
                "Test",
                "Example",
                "Event1",
                "Profile1",
                "per sec",
                "G2/Hz",
                [(1, 2), (3, 4), (5, 6)],
            )
            assert False
        except SherlockAddRandomVibeProfileError as e:
            assert e.str_itr()[0] == "Add random vibe profile error: Invalid Frequency Unit"

        try:
            lifecycle.add_random_vibe_profile(
                "Test",
                "Example",
                "Event1",
                "Profile1",
                "HZ",
                "G2/sec",
                [(1, 2), (3, 4), (5, 6)],
            )
            assert False
        except SherlockAddRandomVibeProfileError as e:
            assert e.str_itr()[0] == "Add random vibe profile error: Invalid Amplitude Type"

    try:
        lifecycle.add_random_vibe_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "HZ",
            "G2/Hz",
            [(12,), (3, 4), (5, 6)],
        )
        assert False
    except SherlockAddRandomVibeProfileError as e:
        assert (
            e.str_itr()[0] == "Add random vibe profile error: Invalid entry 0: Wrong number of args"
        )

    try:
        lifecycle.add_random_vibe_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "HZ",
            "G2/Hz",
            [(12, 4), (3, "x"), (5, 6)],
        )
        assert False
    except SherlockAddRandomVibeProfileError as e:
        assert e.str_itr()[0] == "Add random vibe profile error: Invalid entry 1: Invalid freq/ampl"

    try:
        lifecycle.add_random_vibe_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "HZ",
            "G2/Hz",
            [(12, 4), (3, 4), (-5, 6)],
        )
        assert False
    except SherlockAddRandomVibeProfileError as e:
        assert (
            e.str_itr()[0]
            == "Add random vibe profile error: Invalid entry 2: Frequencies must be greater than 0"
        )


def helper_test_add_thermal_event(lifecycle):
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
        assert e.str_itr()[0] == "Add thermal event error: Invalid Project Name"

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
        assert e.str_itr()[0] == "Add thermal event error: Invalid Phase Name"

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
        assert e.str_itr()[0] == "Add thermal event error: Invalid Event Name"

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
        assert e.str_itr()[0] == "Add thermal event error: Number of Cycles Must Be Greater Than 0"

    if lifecycle._is_connection_up():
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
            assert e.str_itr()[0] == "Add thermal event error: Invalid Cycle Type"

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
            assert e.str_itr()[0] == "Add thermal event error: Invalid Cycle State"


def helper_test_add_thermal_profile(lifecycle):
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
        assert e.str_itr()[0] == "Add thermal profile error: Invalid Profile Name"

    if lifecycle._is_connection_up():
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
            assert e.str_itr()[0] == "Add thermal profile error: Invalid Time Unit"

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
            assert e.str_itr()[0] == "Add thermal profile error: Invalid Temperature Unit"

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
        assert e.str_itr()[0] == "Add thermal profile error: Invalid entry 0: Wrong number of args"

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
        assert e.str_itr()[0] == "Add thermal profile error: Invalid entry 1: Invalid step name"

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
        assert e.str_itr()[0] == "Add thermal profile error: Invalid entry 2: Invalid step type"

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
            e.str_itr()[0]
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
        assert e.str_itr()[0] == "Add thermal profile error: Invalid entry 1: Invalid time"

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
        assert e.str_itr()[0] == "Add thermal profile error: Invalid entry 0: Invalid temp"


def helper_test_add_harmonic_event(lifecycle):
    """Test add_harmonic_event API"""

    try:
        lifecycle.add_harmonic_event(
            "",
            "Example",
            "Event1",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            5,
            "45,45",
            "Uniaxial",
            "2,4,5",
        )
        assert False
    except SherlockAddHarmonicEventError as e:
        assert e.str_itr()[0] == "Add harmonic event error: Invalid Project Name"

    try:
        lifecycle.add_harmonic_event(
            "Test",
            "",
            "Event1",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            5,
            "45,45",
            "Uniaxial",
            "2,4,5",
        )
        assert False
    except SherlockAddHarmonicEventError as e:
        assert e.str_itr()[0] == "Add harmonic event error: Invalid Phase Name"

    try:
        lifecycle.add_harmonic_event(
            "Test",
            "Example",
            "",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            5,
            "45,45",
            "Uniaxial",
            "2,4,5",
        )
        assert False
    except SherlockAddHarmonicEventError as e:
        assert e.str_itr()[0] == "Add harmonic event error: Invalid Event Name"

    try:
        lifecycle.add_harmonic_event(
            "Test",
            "Example",
            "Event1",
            0,
            "sec",
            4.0,
            "PER MIN",
            5,
            "45,45",
            "Uniaxial",
            "2,4,5",
        )
        assert False
    except SherlockAddHarmonicEventError as e:
        assert e.str_itr()[0] == "Add harmonic event error: Duration Must Be Greater Than 0"

    if lifecycle._is_connection_up():
        try:
            lifecycle.add_harmonic_event(
                "Test",
                "Example",
                "Event1",
                1.5,
                "Invalid",
                4.0,
                "PER MIN",
                5,
                "45,45",
                "Uniaxial",
                "2,4,5",
            )
            assert False
        except SherlockAddHarmonicEventError as e:
            assert e.str_itr()[0] == "Add harmonic event error: Invalid Duration Unit Specified"

        try:
            lifecycle.add_harmonic_event(
                "Test",
                "Example",
                "Event1",
                1.5,
                "sec",
                4.0,
                "Invalid",
                5,
                "45,45",
                "Uniaxial",
                "2,4,5",
            )
            assert False
        except SherlockAddHarmonicEventError as e:
            assert e.str_itr()[0] == "Add harmonic event error: Invalid Cycle Type"

    try:
        lifecycle.add_harmonic_event(
            "Test",
            "Example",
            "Event1",
            1.5,
            "sec",
            0,
            "PER MIN",
            5,
            "45,45",
            "Uniaxial",
            "2,4,5",
        )
        assert False
    except SherlockAddHarmonicEventError as e:
        assert e.str_itr()[0] == "Add harmonic event error: Number of Cycles Must Be Greater Than 0"

    try:
        lifecycle.add_harmonic_event(
            "Test",
            "Example",
            "Event1",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            0,
            "45,45",
            "Uniaxial",
            "2,4,5",
        )
        assert False
    except SherlockAddHarmonicEventError as e:
        assert e.str_itr()[0] == "Add harmonic event error: Sweep Rate Must Be Greater Than 0"

    try:
        lifecycle.add_harmonic_event(
            "Test",
            "Example",
            "Event1",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            5,
            "x,45",
            "Uniaxial",
            "2,4,5",
        )
        assert False
    except SherlockAddHarmonicEventError as e:
        assert e.str_itr()[0] == "Add harmonic event error: Invalid azimuth value"

    try:
        lifecycle.add_harmonic_event(
            "Test",
            "Example",
            "Event1",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            5,
            "45,45",
            "Uniaxial",
            "0,0,0",
        )
        assert False
    except SherlockAddHarmonicEventError as e:
        assert (
            e.str_itr()[0]
            == "Add harmonic event error: At least one direction coordinate must be non-zero"
        )

    try:
        lifecycle.add_harmonic_event(
            "Test",
            "Example",
            "Event1",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            5,
            "4545",
            "Uniaxial",
            "2,4,5",
        )
        assert False
    except SherlockAddHarmonicEventError as e:
        assert e.str_itr()[0] == "Add harmonic event error: Invalid number of spherical coordinates"


if __name__ == "__main__":
    test_all()
