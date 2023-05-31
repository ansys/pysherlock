# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.
import uuid

import grpc

from ansys.sherlock.core.errors import (
    SherlockAddHarmonicEventError,
    SherlockAddHarmonicVibeProfilesError,
    SherlockAddRandomVibeEventError,
    SherlockAddRandomVibeProfilesError,
    SherlockAddShockEventError,
    SherlockAddShockProfilesError,
    SherlockAddThermalEventError,
    SherlockAddThermalProfilesError,
    SherlockCreateLifePhaseError,
    SherlockLoadHarmonicProfileError,
    SherlockLoadRandomVibeProfileError,
    SherlockLoadShockProfileDatasetError,
    SherlockLoadShockProfilePulsesError,
    SherlockLoadThermalProfileError,
)
from ansys.sherlock.core.lifecycle import Lifecycle


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    lifecycle = Lifecycle(channel)

    phase_name = helper_test_create_life_phase(lifecycle)
    random_vibe_event_name = helper_test_add_random_vibe_event(lifecycle, phase_name)
    helper_test_add_random_vibe_profile(lifecycle, random_vibe_event_name, phase_name)
    thermal_event_name = helper_test_add_thermal_event(lifecycle, phase_name)
    helper_test_add_thermal_profile(lifecycle, phase_name, thermal_event_name)
    harmonic_vibe_event_name = helper_test_add_harmonic_event(lifecycle, phase_name)
    helper_test_add_harmonic_vibe_profile(lifecycle, phase_name, harmonic_vibe_event_name)
    shock_event_name = helper_test_add_shock_event(lifecycle, phase_name)
    helper_test_add_shock_profile(lifecycle, phase_name, shock_event_name)
    helper_test_load_random_vibe_profile(lifecycle)
    helper_test_load_thermal_profile(lifecycle)
    helper_test_load_harmonic_profile(lifecycle)
    helper_test_load_shock_profile_dataset(lifecycle)
    helper_test_load_shock_profile_pulses(lifecycle)


def helper_test_create_life_phase(lifecycle):
    """Test create_life_phase API"""

    try:
        lifecycle.create_life_phase("", "", 1, "sec", 1, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.str_itr()[0] == "Create life phase error: Project name is invalid."

    try:
        lifecycle.create_life_phase("Test", "", 1, "sec", 1, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.str_itr()[0] == "Create life phase error: Phase name is invalid."

    try:
        lifecycle.create_life_phase("Test", "Example", 0, "sec", 1, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.str_itr()[0] == "Create life phase error: Duration must be greater than 0."

    if lifecycle._is_connection_up():
        try:
            lifecycle.create_life_phase(
                "Test", "Example", 0, "invalid", 1, "PER SEC", description="Test1"
            )
            assert False
        except SherlockCreateLifePhaseError as e:
            assert e.str_itr()[0] == "Create life phase error: Duration unit is invalid."

        try:
            lifecycle.create_life_phase(
                "Test", "Example", 5, "sec", 0, "invalid", description="Test1"
            )
            assert False
        except SherlockCreateLifePhaseError as e:
            assert e.str_itr()[0] == "Create life phase error: Cycle type is invalid."

    try:
        lifecycle.create_life_phase("Test", "Example", 5, "sec", 0, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.str_itr()[0] == "Create life phase error: Number of cycles must be greater than 0."

    if lifecycle._is_connection_up():
        phase_name = "Phase " + str(uuid.uuid4())
        result = lifecycle.create_life_phase(
            "Tutorial Project",
            phase_name,
            duration=8400,
            duration_units="sec",
            num_of_cycles=4,
            cycle_type="COUNT",
        )
        assert result == 0
        return phase_name


def helper_test_add_random_vibe_event(lifecycle, phase_name):
    """Test add_random_vibe_event API"""

    try:
        lifecycle.add_random_vibe_event(
            "", "", "", 1, "sec", 1, "PER SEC", "45,45", "Uniaxial", "1,2,3", description="Test1"
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.str_itr()[0] == "Add random vibe event error: Project name is invalid."

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
        assert e.str_itr()[0] == "Add random vibe event error: Phase name is invalid."

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
        assert e.str_itr()[0] == "Add random vibe event error: Event name is invalid."

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
        assert e.str_itr()[0] == "Add random vibe event error: Duration must be greater than 0."

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
            assert e.str_itr()[0] == "Add random vibe event error: Duration unit is invalid."

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
            assert e.str_itr()[0] == "Add random vibe event error: Cycle type is invalid."

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
            e.str_itr()[0] == "Add random vibe event error: "
            "Number of cycles must be greater than 0."
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
        assert e.str_itr()[0] == "Add random vibe event error: Elevation value is invalid."

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
            == "Add random vibe event error: At least one direction coordinate must be "
            "non-zero."
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
            e.str_itr()[0] == "Add random vibe event error: "
            "Number of spherical coordinates is invalid."
        )

    if lifecycle._is_connection_up():
        event_name = "Random Vibe Event " + str(uuid.uuid4())
        result = lifecycle.add_random_vibe_event(
            "Tutorial Project",
            phase_name,
            event_name,
            1,
            "sec",
            4.0,
            "PER MIN",
            "45,45",
            "Uniaxial",
            "2,4,5",
        )

        assert result == 0

        return event_name


def helper_test_add_random_vibe_profile(lifecycle, event_name, phase_name):
    """Test the add_random_vibe_profiles API"""

    try:
        lifecycle.add_random_vibe_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "",
                    "HZ",
                    "G2/Hz",
                    [(1, 2), (3, 4), (5, 6)],
                )
            ],
        )
        assert False
    except SherlockAddRandomVibeProfilesError as e:
        assert (
            e.str_itr()[0] == "Add random vibe profiles error: "
            "Profile name is invalid for random vibe profile 0."
        )

    try:
        lifecycle.add_random_vibe_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    "HZ",
                    "G2/Hz",
                    [(12,), (3, 4), (5, 6)],
                )
            ],
        )
        assert False
    except SherlockAddRandomVibeProfilesError as e:
        assert (
            e.str_itr()[0] == "Add random vibe profiles error: "
            "Invalid entry 0: "
            "Number of elements is wrong for random vibe "
            "profile 0."
        )

    try:
        lifecycle.add_random_vibe_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    "HZ",
                    "G2/Hz",
                    [(12, 4), (3, "x"), (5, 6)],
                )
            ],
        )
        assert False
    except SherlockAddRandomVibeProfilesError as e:
        assert (
            e.str_itr()[0] == "Add random vibe profiles error:"
            " Invalid entry 1:"
            " Frequency or amplitude is invalid for random vibe profile 0."
        )

    try:
        lifecycle.add_random_vibe_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    "HZ",
                    "G2/Hz",
                    [(12, 4), (3, 4), (-5, 6)],
                )
            ],
        )
        assert False
    except SherlockAddRandomVibeProfilesError as e:
        assert (
            e.str_itr()[0] == "Add random vibe profiles error:"
            " Invalid entry 2:"
            " Frequencies must be greater than 0 for random vibe profile 0."
        )

    if lifecycle._is_connection_up():
        result = lifecycle.add_random_vibe_profiles(
            "Tutorial Project",
            [
                (
                    phase_name,
                    event_name,
                    "Profile1",
                    "HZ",
                    "G2/Hz",
                    [(1, 2), (3, 4)],
                )
            ],
        )
        assert result == 0

        try:
            lifecycle.add_random_vibe_profiles(
                "Tutorial Project",
                [
                    (
                        "Example",
                        "Event1",
                        "Profile1",
                        "per sec",
                        "G2/Hz",
                        [(1, 2), (3, 4)],
                    )
                ],
            )
            assert False
        except Exception as e:
            assert type(e) == SherlockAddRandomVibeProfilesError


def helper_test_add_thermal_event(lifecycle, phase_name):
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
        assert e.str_itr()[0] == "Add thermal event error: Project name is invalid."

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
        assert e.str_itr()[0] == "Add thermal event error: Phase name is invalid."

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
        assert e.str_itr()[0] == "Add thermal event error: Event name is invalid."

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
        assert e.str_itr()[0] == "Add thermal event error: Number of cycles must be greater than 0."

    if lifecycle._is_connection_up():
        try:
            lifecycle.add_thermal_event(
                "Tutorial Project",
                "Example",
                "Event 1",
                -1,
                "PER 0.5MIN",
                "STORAGE",
            )
        except Exception as e:
            assert type(e) == SherlockAddThermalEventError

        event_name = "Thermal Event " + str(uuid.uuid4())
        result = lifecycle.add_thermal_event(
            "Tutorial Project",
            phase_name,
            event_name,
            num_of_cycles=1,
            cycle_type="COUNT",
            cycle_state="OPERATING",
        )
        assert result == 0

        return event_name


def helper_test_add_thermal_profile(lifecycle, phase_name, event_name):
    """Test add_thermal_profiles API."""

    try:
        lifecycle.add_thermal_profiles(
            "Test",
            [
                (
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
            ],
        )
        assert False
    except SherlockAddThermalProfilesError as e:
        assert (
            e.str_itr()[0]
            == "Add thermal profiles error: Profile name is invalid for thermal profile 0."
        )

    if lifecycle._is_connection_up():
        try:
            lifecycle.add_thermal_profiles(
                "Test",
                [
                    (
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
                ],
            )
        except SherlockAddThermalProfilesError as e:
            print(str(e.str_itr()[0]))
            assert True

        try:
            lifecycle.add_thermal_profiles(
                "Test",
                [
                    (
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
                ],
            )

        except SherlockAddThermalProfilesError as e:
            print(str(e.str_itr()[0]))
            assert True

    try:
        lifecycle.add_thermal_profiles(
            "Test",
            [
                (
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
            ],
        )
        assert False
    except SherlockAddThermalProfilesError as e:
        assert (
            e.str_itr()[0] == "Add thermal profiles error: Invalid entry 0: "
            "Number of elements is wrong for thermal profile 0."
        )

    try:
        lifecycle.add_thermal_profiles(
            "Test",
            [
                (
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
            ],
        )
        assert False
    except SherlockAddThermalProfilesError as e:
        assert (
            e.str_itr()[0] == "Add thermal profiles error: Invalid entry 1: "
            "Step name is invalid for thermal profile 0."
        )

    try:
        lifecycle.add_thermal_profiles(
            "Test",
            [
                (
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
            ],
        )
        assert False
    except SherlockAddThermalProfilesError as e:
        assert (
            e.str_itr()[0] == "Add thermal profiles error: Invalid entry 2: "
            "Step type is invalid for thermal profile 0."
        )

    try:
        lifecycle.add_thermal_profiles(
            "Test",
            [
                (
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
            ],
        )
        assert False
    except SherlockAddThermalProfilesError as e:
        assert (
            e.str_itr()[0] == "Add thermal profiles error: Invalid entry 1: "
            "Time must be greater than 0 for thermal profile 0."
        )

    try:
        lifecycle.add_thermal_profiles(
            "Test",
            [
                (
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
            ],
        )
        assert False
    except SherlockAddThermalProfilesError as e:
        assert (
            e.str_itr()[0]
            == "Add thermal profiles error: Invalid entry 1: Time is invalid for thermal profile 0."
        )

    try:
        lifecycle.add_thermal_profiles(
            "Test",
            [
                (
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
            ],
        )
        assert False
    except SherlockAddThermalProfilesError as e:
        assert (
            e.str_itr()[0]
            == "Add thermal profiles error: Invalid entry 0: Temperature is invalid for thermal "
            "profile 0."
        )
    if lifecycle._is_connection_up():
        profile = str(uuid.uuid4())
        result = lifecycle.add_thermal_profiles(
            "Tutorial Project",
            [
                (
                    phase_name,
                    event_name,
                    profile,
                    "sec",
                    "F",
                    [
                        ("Steady1", "HOLD", 40, 40),
                        ("Steady", "HOLD", 20, 20),
                        ("Back", "RAMP", 20, 40),
                    ],
                )
            ],
        )
        assert result == 0


def helper_test_add_harmonic_event(lifecycle, phase_name):
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
        assert e.str_itr()[0] == "Add harmonic event error: Project name is invalid."

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
        assert e.str_itr()[0] == "Add harmonic event error: Phase name is invalid."

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
        assert e.str_itr()[0] == "Add harmonic event error: Event name is invalid."

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
        assert e.str_itr()[0] == "Add harmonic event error: Duration must be greater than 0."

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
        except SherlockAddHarmonicEventError as e:
            print(str(e.str_itr()[0]))
            assert True

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
            assert e.str_itr()[0] == "Add harmonic event error: Cycle type is invalid."

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
                "Invalid",
                "2,4,5",
            )
        except SherlockAddHarmonicEventError as e:
            print(str(e.str_itr()[0]))
            assert True

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
        assert (
            e.str_itr()[0] == "Add harmonic event error: Number of cycles must be "
            "greater than 0."
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
            0,
            "45,45",
            "Uniaxial",
            "2,4,5",
        )
        assert False
    except SherlockAddHarmonicEventError as e:
        assert e.str_itr()[0] == "Add harmonic event error: Sweep rate must be greater than 0."

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
        assert e.str_itr()[0] == "Add harmonic event error: Azimuth value is invalid."

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
            == "Add harmonic event error: At least one direction coordinate must be non-zero."
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
        assert (
            e.str_itr()[0] == "Add harmonic event error: Number of spherical coordinates "
            "is invalid."
        )
    if lifecycle._is_connection_up():
        event_name = "Harmonic Vibe Event " + str(uuid.uuid4())
        result = lifecycle.add_harmonic_event(
            "Tutorial Project",
            phase_name,
            event_name,
            1.0,
            "sec",
            4.0,
            "PER MIN",
            5.0,
            "45,45",
            "Triaxial",
            "2,4,5",
        )
        assert result == 0

        return event_name


def helper_test_add_harmonic_vibe_profile(lifecycle, phase_name, harmonic_vibe_event_name):
    """Test add_harmonic_profiles API."""

    try:
        lifecycle.add_harmonic_vibe_profiles(
            "",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    "Hz",
                    "G",
                    [
                        (10, 1),
                        (1000, 1),
                    ],
                    "",
                )
            ],
        )
        assert False
    except SherlockAddHarmonicVibeProfilesError as e:
        assert e.str_itr()[0] == "Add harmonic vibe profiles error: Project name is invalid."

    try:
        lifecycle.add_harmonic_vibe_profiles(
            "Test",
            [
                (
                    "",
                    "Event1",
                    "Profile1",
                    "Hz",
                    "G",
                    [
                        (10, 1),
                        (1000, 1),
                    ],
                    "",
                )
            ],
        )
        assert False
    except SherlockAddHarmonicVibeProfilesError as e:
        assert (
            e.str_itr()[0] == "Add harmonic vibe profiles error:"
            " Phase name is invalid for harmonic vibe profile 0."
        )

    try:
        lifecycle.add_harmonic_vibe_profiles(
            "Test",
            [
                (
                    "Example",
                    "",
                    "Profile1",
                    "Hz",
                    "G",
                    [
                        (10, 1),
                        (1000, 1),
                    ],
                    "",
                )
            ],
        )
        assert False
    except SherlockAddHarmonicVibeProfilesError as e:
        assert (
            e.str_itr()[0] == "Add harmonic vibe profiles error:"
            " Event name is invalid for harmonic vibe profile 0."
        )

    try:
        lifecycle.add_harmonic_vibe_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "",
                    "Hz",
                    "G",
                    [
                        (10, 1),
                        (1000, 1),
                    ],
                    "",
                )
            ],
        )
        assert False
    except SherlockAddHarmonicVibeProfilesError as e:
        assert (
            e.str_itr()[0] == "Add harmonic vibe profiles error:"
            " Profile name is invalid for harmonic vibe profile 0."
        )

    if lifecycle._is_connection_up():
        try:
            lifecycle.add_harmonic_vibe_profiles(
                "Test",
                [
                    (
                        "Example",
                        "Event1",
                        "Profile1",
                        "badUnits",
                        "G",
                        [
                            (10, 1),
                            (1000, 1),
                        ],
                        "",
                    )
                ],
            )
        except SherlockAddHarmonicVibeProfilesError as e:
            print(str(e.str_itr()[0]))
            assert True

        try:
            lifecycle.add_harmonic_vibe_profiles(
                "Test",
                [
                    (
                        "Example",
                        "Event1",
                        "Profile1",
                        "HZ",
                        "badUnits",
                        [
                            (10, 1),
                            (1000, 1),
                        ],
                        "",
                    )
                ],
            )
        except SherlockAddHarmonicVibeProfilesError as e:
            print(str(e.str_itr()[0]))
            assert True

    try:
        lifecycle.add_harmonic_vibe_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    "HZ",
                    "G",
                    [
                        (10,),
                        (1000, 1),
                    ],
                    "",
                )
            ],
        )
        assert False
    except SherlockAddHarmonicVibeProfilesError as e:
        assert (
            e.str_itr()[0] == "Add harmonic vibe profiles error:"
            " Invalid entry 0:"
            " Number of elements is wrong for harmonic vibe profile 0."
        )

    try:
        lifecycle.add_harmonic_vibe_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    "HZ",
                    "G",
                    [
                        (10, 1),
                        (1000, "Invalid"),
                    ],
                    "",
                )
            ],
        )
        assert False
    except SherlockAddHarmonicVibeProfilesError as e:
        assert (
            e.str_itr()[0] == "Add harmonic vibe profiles error: "
            "Invalid entry 1: Frequency or load is invalid for "
            "harmonic vibe profile 0."
        )

    try:
        lifecycle.add_harmonic_vibe_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    "HZ",
                    "G",
                    [
                        (10, -5),
                        (1000, 1),
                    ],
                    "",
                )
            ],
        )
        assert False
    except SherlockAddHarmonicVibeProfilesError as e:
        assert (
            e.str_itr()[0] == "Add harmonic vibe profiles error:"
            " Invalid entry 0:"
            " Load must be greater than 0 for harmonic vibe profile 0."
        )
    if lifecycle._is_connection_up():
        profile = str(uuid.uuid4())
        result = lifecycle.add_harmonic_vibe_profiles(
            "Tutorial Project",
            [
                (
                    phase_name,
                    harmonic_vibe_event_name,
                    profile,
                    "HZ",
                    "G",
                    [
                        (10, 1),
                        (1000, 1),
                    ],
                    "z",
                )
            ],
        )
        assert result == 0


def helper_test_add_shock_event(lifecycle, phase_name):
    """Test add_shock_event API."""

    try:
        lifecycle.add_shock_event(
            "",
            "Example",
            "Event1",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            "45,45",
            "2,4,5",
        )
        assert False
    except SherlockAddShockEventError as e:
        assert e.str_itr()[0] == "Add shock event error: Project name is invalid."

    try:
        lifecycle.add_shock_event(
            "Test",
            "",
            "Event1",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            "45,45",
            "2,4,5",
        )
        assert False
    except SherlockAddShockEventError as e:
        assert e.str_itr()[0] == "Add shock event error: Phase name is invalid."

    try:
        lifecycle.add_shock_event(
            "Test",
            "Example",
            "",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            "45,45",
            "2,4,5",
        )
        assert False
    except SherlockAddShockEventError as e:
        assert e.str_itr()[0] == "Add shock event error: Event name is invalid."

    try:
        lifecycle.add_shock_event(
            "Test",
            "Example",
            "Event1",
            0,
            "sec",
            4.0,
            "PER MIN",
            "45,45",
            "2,4,5",
        )
        assert False
    except SherlockAddShockEventError as e:
        assert e.str_itr()[0] == "Add shock event error: Duration must be greater than 0."

    try:
        lifecycle.add_shock_event(
            "Test",
            "Example",
            "Event1",
            1.5,
            "sec",
            0,
            "PER MIN",
            "45,45",
            "2,4,5",
        )
        assert False
    except SherlockAddShockEventError as e:
        assert e.str_itr()[0] == "Add shock event error: Number of cycles must be greater than 0."

    try:
        lifecycle.add_shock_event(
            "Test",
            "Example",
            "Event1",
            5,
            "sec",
            4,
            "PER SEC",
            "45,x",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddShockEventError as e:
        assert e.str_itr()[0] == "Add shock event error: Elevation value is invalid."

    try:
        lifecycle.add_shock_event(
            "Test",
            "Example",
            "Event1",
            5,
            "sec",
            4,
            "PER MIN",
            "45,45",
            "0,0,0",
            description="Test1",
        )
        assert False
    except SherlockAddShockEventError as e:
        assert (
            e.str_itr()[0] == "Add shock event error: At least one direction coordinate must be "
            "non-zero."
        )

    try:
        lifecycle.add_shock_event(
            "Test",
            "Example",
            "Event1",
            5,
            "sec",
            4,
            "PER MIN",
            "4545",
            "0,1,0",
            description="Test1",
        )
        assert False
    except SherlockAddShockEventError as e:
        assert (
            e.str_itr()[0] == "Add shock event error: Number of spherical coordinates "
            "is invalid."
        )

    if lifecycle._is_connection_up():
        event_name = "Shock Event " + str(uuid.uuid4())
        result = lifecycle.add_shock_event(
            "Tutorial Project",
            phase_name,
            event_name,
            1.0,
            "sec",
            4.0,
            "PER MIN",
            "45,45",
            "2,4,5",
        )
        assert result == 0

        try:
            lifecycle.add_shock_event(
                "Test",
                "Example",
                "Event1",
                1.5,
                "Invalid",
                4.0,
                "PER MIN",
                "45,45",
                "2,4,5",
            )
            assert False
        except Exception as e:
            assert type(e) == SherlockAddShockEventError

        return event_name


def helper_test_add_shock_profile(lifecycle, phase_name, shock_event_name):
    """Test add_shock_profiles API."""

    try:
        lifecycle.add_shock_profiles(
            "",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    10.0,
                    "ms",
                    0.1,
                    "ms",
                    "G",
                    "HZ",
                    [("HalfSine", 100.0, 100.0, 0)],
                )
            ],
        )
        assert False
    except SherlockAddShockProfilesError as e:
        assert e.str_itr()[0] == "Add shock profiles error: Project name is invalid."

    try:
        lifecycle.add_shock_profiles(
            "Test",
            [
                (
                    "",
                    "Event1",
                    "Profile1",
                    10.0,
                    "ms",
                    0.1,
                    "ms",
                    "G",
                    "HZ",
                    [("HalfSine", 100.0, 100.0, 0)],
                )
            ],
        )
        assert False
    except SherlockAddShockProfilesError as e:
        assert (
            e.str_itr()[0] == "Add shock profiles error: Phase name is invalid for "
            "shock profile 0."
        )

    try:
        lifecycle.add_shock_profiles(
            "Test",
            [
                (
                    "Example",
                    "",
                    "Profile1",
                    10.0,
                    "ms",
                    0.1,
                    "ms",
                    "G",
                    "HZ",
                    [("HalfSine", 100.0, 100.0, 0)],
                )
            ],
        )
        assert False
    except SherlockAddShockProfilesError as e:
        assert (
            e.str_itr()[0] == "Add shock profiles error: Event name is invalid for "
            "shock profile 0."
        )

    try:
        lifecycle.add_shock_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "",
                    10.0,
                    "ms",
                    0.1,
                    "ms",
                    "G",
                    "HZ",
                    [("HalfSine", 100.0, 100.0, 0)],
                )
            ],
        )
        assert False
    except SherlockAddShockProfilesError as e:
        assert (
            e.str_itr()[0] == "Add shock profiles error:"
            " Profile name is invalid for shock profile 0."
        )

    try:
        lifecycle.add_shock_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    0,
                    "ms",
                    0.1,
                    "ms",
                    "G",
                    "HZ",
                    [("HalfSine", 100.0, 100.0, 0)],
                )
            ],
        )
        assert False
    except SherlockAddShockProfilesError as e:
        assert (
            e.str_itr()[0] == "Add shock profiles error:"
            " Duration must be greater than 0 for shock profile 0."
        )

    try:
        lifecycle.add_shock_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    0,
                    "unitsInvalid",
                    0.1,
                    "ms",
                    "G",
                    "HZ",
                    [("HalfSine", 100.0, 100.0, 0)],
                )
            ],
        )
        assert False
    except SherlockAddShockProfilesError as e:
        assert (
            e.str_itr()[0] == "Add shock profiles error:"
            " Duration must be greater than 0 for shock profile 0."
        )

    try:
        lifecycle.add_shock_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    10.0,
                    "ms",
                    0,
                    "ms",
                    "G",
                    "HZ",
                    [("HalfSine", 100.0, 100.0, 0)],
                )
            ],
        )
        assert False
    except SherlockAddShockProfilesError as e:
        assert (
            e.str_itr()[0] == "Add shock profiles error:"
            " Sample rate must be greater than 0 for shock profile 0."
        )

    try:
        lifecycle.add_shock_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    10.0,
                    "ms",
                    0.1,
                    "ms",
                    "G",
                    "HZ",
                    [(100.0, 100.0, 0)],
                )
            ],
        )
        assert False
    except SherlockAddShockProfilesError as e:
        assert (
            e.str_itr()[0] == "Add shock profiles error:"
            " Invalid entry 0: Number of elements is wrong for shock"
            " profile 0."
        )

    try:
        lifecycle.add_shock_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    10.0,
                    "ms",
                    0.1,
                    "ms",
                    "G",
                    "HZ",
                    [("HalfSine", 0, 100.0, 0)],
                )
            ],
        )
        assert False
    except SherlockAddShockProfilesError as e:
        assert (
            e.str_itr()[0] == "Add shock profiles error:"
            " Invalid entry 0: Load must be "
            "greater than 0 for shock profile 0."
        )

    try:
        lifecycle.add_shock_profiles(
            "Test",
            [
                (
                    "Example",
                    "Event1",
                    "Profile1",
                    10.0,
                    "ms",
                    0.1,
                    "ms",
                    "G",
                    "HZ",
                    [("HalfSine", 100.0, 100.0, -5)],
                )
            ],
        )
        assert False
    except SherlockAddShockProfilesError as e:
        assert (
            e.str_itr()[0] == "Add shock profiles error:"
            " Invalid entry 0: Decay must be non-negative for "
            "shock profile 0."
        )

    if lifecycle._is_connection_up():
        profile = str(uuid.uuid4())
        result = lifecycle.add_shock_profiles(
            "Tutorial Project",
            [
                (
                    phase_name,
                    shock_event_name,
                    profile,
                    10.0,
                    "ms",
                    0.1,
                    "ms",
                    "G",
                    "HZ",
                    [("HalfSine", 100.0, 100.0, 0)],
                )
            ],
        )
        assert result == 0

        try:
            lifecycle.add_shock_profiles(
                "Test",
                [
                    (
                        "Example",
                        "Event1",
                        "Profile1",
                        10.0,
                        "ms",
                        0.1,
                        "unitsInvalid",
                        "G",
                        "HZ",
                        [("HalfSine", 100.0, 100.0, 0)],
                    )
                ],
            )
            assert False
        except Exception as e:
            assert type(e) == SherlockAddShockProfilesError


def helper_test_load_random_vibe_profile(lifecycle):
    """Test load_random_vibe_profile."""

    try:
        lifecycle.load_random_vibe_profile(
            "",
            "Phase 1",
            "Random Event",
            "TestProfile.dat",
        )
        assert False
    except SherlockLoadRandomVibeProfileError as e:
        assert str(e) == "Load random vibe profile error: Project name is invalid."
    try:
        lifecycle.load_random_vibe_profile(
            "Test",
            "",
            "Random Event",
            "TestProfile.dat",
        )
        assert False
    except SherlockLoadRandomVibeProfileError as e:
        assert str(e) == "Load random vibe profile error: Phase name is invalid."
    try:
        lifecycle.load_random_vibe_profile(
            "Test",
            "Phase 1",
            "",
            "TestProfile.dat",
        )
        assert False
    except SherlockLoadRandomVibeProfileError as e:
        assert str(e) == "Load random vibe profile error: Event name is invalid."

    try:
        lifecycle.load_random_vibe_profile(
            "Test",
            "Phase 1",
            "Random Event",
            "",
        )
        assert False
    except SherlockLoadRandomVibeProfileError as e:
        assert str(e) == "Load random vibe profile error: File path is invalid."

    if lifecycle._is_connection_up():
        loaded = lifecycle.load_random_vibe_profile(
            "Test Project",
            "Phase 1",
            "Random Event",
            "TestProfile.dat",
        )
        try:
            return loaded
        except Exception as e:
            print(str(e))


def helper_test_load_harmonic_profile(lifecycle):
    """Test load_harmonic_profile API."""

    try:
        lifecycle.load_harmonic_profile("", "Phase 1", "Harmonic Event", "Test_Profile.dat")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert str(e) == "Load Harmonic profile error: Project name is invalid."

    try:
        lifecycle.load_harmonic_profile("Test", "", "Harmonic Event", "Test_Profile.dat")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert str(e) == "Load Harmonic profile error: Phase name is invalid."

    try:
        lifecycle.load_harmonic_profile("Test", "Phase 1", "", "Test_Profile.dat")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert str(e) == "Load Harmonic profile error: Event name is invalid."

    try:
        lifecycle.load_harmonic_profile("Test", "Phase 1", "Harmonic Event", "")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert str(e) == "Load Harmonic profile error: File name is invalid."
    if lifecycle._is_connection_up():
        loaded = lifecycle.load_harmonic_profile(
            "Test Project",
            "Phase 1",
            "Harmonic Event",
            "Test_Profile.dat",
        )
        try:
            return loaded
        except Exception as e:
            print(str(e))


def helper_test_load_thermal_profile(lifecycle):
    """Test load_thermal_profile API"""

    try:
        lifecycle.load_thermal_profile(
            "",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.dat",
        )
        assert False
    except SherlockLoadThermalProfileError as e:
        assert str(e) == "Load thermal profile error: Project name is invalid."

    try:
        lifecycle.load_thermal_profile(
            "Test",
            "",
            "Thermal Event",
            "Tutorial_Profile.dat",
        )
        assert False
    except SherlockLoadThermalProfileError as e:
        assert str(e) == "Load thermal profile error: Phase name is invalid."

    try:
        lifecycle.load_thermal_profile(
            "Test",
            "Phase 1",
            "",
            "Tutorial_Profile.dat",
        )
        assert False
    except SherlockLoadThermalProfileError as e:
        assert str(e) == "Load thermal profile error: Event name is invalid."

    try:
        lifecycle.load_thermal_profile(
            "Test",
            "Phase 1",
            "Thermal Event",
            "",
        )
        assert False
    except SherlockLoadThermalProfileError as e:
        assert str(e) == "Load thermal profile error: File path is invalid."

    if lifecycle._is_connection_up():
        loaded = lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.dat",
        )
        try:
            return loaded
        except Exception as e:
            print(str(e))


def helper_test_load_shock_profile_dataset(lifecycle):
    """Test load_shock_profile_dataset API"""

    try:
        lifecycle.load_shock_profile_dataset(
            "",
            "Phase 1",
            "Shock Event",
            "Test_Profile.dat",
        )
        assert False
    except SherlockLoadShockProfileDatasetError as e:
        assert str(e) == "Load shock profile dataset error: Project name is invalid."

    try:
        lifecycle.load_shock_profile_dataset(
            "Test",
            "",
            "Shock Event",
            "Test_Profile.dat",
        )
        assert False
    except SherlockLoadShockProfileDatasetError as e:
        assert str(e) == "Load shock profile dataset error: Phase name is invalid."

    try:
        lifecycle.load_shock_profile_dataset(
            "Test",
            "Phase 1",
            "",
            "Test_Profile.dat",
        )
        assert False
    except SherlockLoadShockProfileDatasetError as e:
        assert str(e) == "Load shock profile dataset error: Event name is invalid."

    try:
        lifecycle.load_shock_profile_dataset(
            "Test",
            "Phase 1",
            "Shock Event",
            "",
        )
        assert False
    except SherlockLoadShockProfileDatasetError as e:
        assert str(e) == "Load shock profile dataset error: File path is invalid."

    if lifecycle._is_connection_up():
        loaded = lifecycle.load_shock_profile_dataset(
            "Tutorial Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.dat",
        )
        try:
            return loaded
        except Exception as e:
            print(str(e))


def helper_test_load_shock_profile_pulses(lifecycle):
    """Test load_shock_profile_pulses API"""
    try:
        lifecycle.load_shock_profile_pulses(
            "",
            "Phase 1",
            "Shock Event",
            "Test_Profile.dat",
        )
    except SherlockLoadShockProfilePulsesError as e:
        assert str(e) == "Load shock profile pulses error: Project name is invalid."

    try:
        lifecycle.load_shock_profile_pulses(
            "Test",
            "",
            "Shock Event",
            "Test_Profile.dat",
        )
    except SherlockLoadShockProfilePulsesError as e:
        assert str(e) == "Load shock profile pulses error: Phase name is invalid."

    try:
        lifecycle.load_shock_profile_pulses(
            "Test",
            "Phase 1",
            "",
            "Test_Profile.dat",
        )
    except SherlockLoadShockProfilePulsesError as e:
        assert str(e) == "Load shock profile pulses error: Event name is invalid."

    try:
        lifecycle.load_shock_profile_pulses(
            "Test",
            "Phase 1",
            "Shock Event",
            "",
        )
    except SherlockLoadShockProfilePulsesError as e:
        assert str(e) == "Load shock profile pulses error: File path is invalid."
    if lifecycle._is_connection_up():
        loaded = lifecycle.load_shock_profile_pulses(
            "Tutorial Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.dat",
        )
        try:
            return loaded
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    test_all()
