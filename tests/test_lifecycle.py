# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

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
    SherlockLoadShockProfileDatasetError,
    SherlockLoadRandomVibeProfileError,
    SherlockLoadShockProfileDatasetError,
    SherlockLoadThermalProfileError,
    SherlockLoadShockProfileDatasetError,
    SherlockLoadHarmonicProfileError,
)
from ansys.sherlock.core.lifecycle import Lifecycle


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    lifecycle = Lifecycle(channel)

    helper_test_create_life_phase(lifecycle)
    helper_test_add_random_vibe_event(lifecycle)
    helper_test_add_random_vibe_profiles(lifecycle)
    helper_test_add_thermal_event(lifecycle)
    helper_test_add_thermal_profiles(lifecycle)
    helper_test_add_harmonic_event(lifecycle)
    helper_test_add_harmonic_vibe_profiles(lifecycle)
    helper_test_add_shock_event(lifecycle)
    helper_test_add_shock_profiles(lifecycle)
    helper_test_load_random_vibe_profile(lifecycle)
    helper_test_load_thermal_profile(lifecycle)
    helper_test_load_shock_profile_dataset(lifecycle)


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


def helper_test_add_random_vibe_event(lifecycle):
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


def helper_test_add_random_vibe_profiles(lifecycle):
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

    if lifecycle._is_connection_up():
        try:
            lifecycle.add_random_vibe_profiles(
                "Test",
                [
                    (
                        "Example",
                        "Event1",
                        "Profile1",
                        "per sec",
                        "G2/Hz",
                        [(1, 2), (3, 4), (5, 6)],
                    )
                ],
            )
            assert False
        except SherlockAddRandomVibeProfilesError as e:
            assert (
                e.str_itr()[0] == "Add random vibe profiles error: "
                "Frequency units of seconds are invalid for random vibe "
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
                        "G2/sec",
                        [(1, 2), (3, 4), (5, 6)],
                    )
                ],
            )
            assert False
        except SherlockAddRandomVibeProfilesError as e:
            assert (
                e.str_itr()[0] == "Add random vibe profiles error: "
                "Amplitude type G2/sec is invalid for random vibe profile 0."
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
                "Test",
                "Example",
                "Event1",
                -1,
                "PER 0.5MIN",
                "STORAGE",
            )
            assert False
        except SherlockAddThermalEventError as e:
            assert e.str_itr()[0] == "Add thermal event error: Cycle type is invalid."

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
            assert e.str_itr()[0] == "Add thermal event error: Cycle state is invalid."


def helper_test_add_thermal_profiles(lifecycle):
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
            assert False
        except SherlockAddThermalProfilesError as e:
            assert (
                e.str_itr()[0] == "Add thermal profiles error: Time unit of seconds is invalid for "
                "thermal profile 0."
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
                        "IDK",
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
                == "Add thermal profiles error: Temperature unit of IDK is invalid for "
                "thermal profile 0."
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
            assert False
        except SherlockAddHarmonicEventError as e:
            assert e.str_itr()[0] == "Add harmonic event error: Duration unit is invalid."

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
            assert False
        except SherlockAddHarmonicEventError as e:
            assert e.str_itr()[0] == "Add harmonic event error: Profile type is invalid."

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


def helper_test_add_harmonic_vibe_profiles(lifecycle):
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
            assert False
        except SherlockAddHarmonicVibeProfilesError as e:
            assert (
                e.str_itr()[0] == "Add harmonic vibe profiles error:"
                "Frequency units badUnits are invalid for harmonic "
                "vibe profile 0."
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
                        "badUnits",
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
                " Load units badUnits are invalid for harmonic vibe profile 0."
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


def helper_test_add_shock_event(lifecycle):
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

    if lifecycle._is_connection_up():
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
        except SherlockAddShockEventError as e:
            assert e.str_itr()[0] == "Add shock event error: IDuration unit is invalid."

        try:
            lifecycle.add_shock_event(
                "Test",
                "Example",
                "Event1",
                1.5,
                "sec",
                4.0,
                "Invalid",
                "45,45",
                "2,4,5",
            )
            assert False
        except SherlockAddShockEventError as e:
            assert e.str_itr()[0] == "Add shock event error: Cycle type is invalid."

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


def helper_test_add_shock_profiles(lifecycle):
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

    if lifecycle._is_connection_up():
        try:
            lifecycle.add_shock_profiles(
                "Test",
                [
                    (
                        "Example",
                        "Event1",
                        "Profile1",
                        10.0,
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
                " Duration units unitsInvalid are invalid for shock profile 0."
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
                        "unitsInvalid",
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
                " Sample rate units unitsInvalid are invalid for "
                "shock profile 0."
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
                        "unitInvalid",
                        "HZ",
                        [("HalfSine", 100.0, 100.0, 0)],
                    )
                ],
            )
            assert False
        except SherlockAddShockProfilesError as e:
            assert (
                e.str_itr()[0] == "Add shock profiles error:"
                " Load units unitInvalid are invalid for shock profile 0."
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
                        "badFreq",
                        [("HalfSine", 100.0, 100.0, 0)],
                    )
                ],
            )
            assert False
        except SherlockAddShockProfilesError as e:
            assert (
                e.str_itr()[0] == "Add shock profiles error:"
                " Frequency units badFreq are invalid for shock profile 0."
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

    if lifecycle._is_connection_up():
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
                        [("badShapType", 100.0, 100.0, 0)],
                    )
                ],
            )
            assert False
        except SherlockAddShockProfilesError as e:
            assert (
                e.str_itr()[0] == "Add shock profiles error:"
                " Invalid entry 0: Shape type is invalid for shock profile 0."
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


def helper_test_load_harmonic_profile(lifcycle):
    """Test load_harmonic_profile API."""

    try:
        lifcycle.load_harmonic_profile("", "Phase 1", "Harmonic Event", "Test_Profile.dat")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert "Load Harmonic profile error: Project name is invalid."

    try:
        lifcycle.load_harmonic_profile("Test", "", "Harmonic Event", "Test_Profile.dat")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert "Load Harmonic profile error: Phase name is invalid."

    try:
        lifcycle.load_harmonic_profile("Test", "Phase 1", "", "Test_Profile.dat")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert "Load Harmonic profile error: Event name is invalid."

    try:
        lifcycle.load_harmonic_profile("Test", "Phase 1", "Harmonic Event", "")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert "Load Harmonic profile error: File name is invalid."


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


def helper_test_load_harmonic_profile(lifcycle):
    """Test load_harmonic_profile API."""

    try:
        lifcycle.load_harmonic_profile("", "Phase 1", "Harmonic Event", "Test_Profile.dat")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert "Load Harmonic profile error: Project name is invalid."

    try:
        lifcycle.load_harmonic_profile("Test", "", "Harmonic Event", "Test_Profile.dat")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert "Load Harmonic profile error: Phase name is invalid."

    try:
        lifcycle.load_harmonic_profile("Test", "Phase 1", "", "Test_Profile.dat")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert "Load Harmonic profile error: Event name is invalid."

    try:
        lifcycle.load_harmonic_profile("Test", "Phase 1", "Harmonic Event", "")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert "Load Harmonic profile error: File name is invalid."


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


def helper_test_load_harmonic_profile(lifcycle):
    """Test load_harmonic_profile API."""

    try:
        lifcycle.load_harmonic_profile("", "Phase 1", "Harmonic Event", "Test_Profile.dat")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert "Load Harmonic profile error: Project name is invalid."

    try:
        lifcycle.load_harmonic_profile("Test", "", "Harmonic Event", "Test_Profile.dat")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert "Load Harmonic profile error: Phase name is invalid."

    try:
        lifcycle.load_harmonic_profile("Test", "Phase 1", "", "Test_Profile.dat")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert "Load Harmonic profile error: Event name is invalid."

    try:
        lifcycle.load_harmonic_profile("Test", "Phase 1", "Harmonic Event", "")
        assert False
    except SherlockLoadHarmonicProfileError as e:
        assert "Load Harmonic profile error: File name is invalid."


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


if __name__ == "__main__":
    test_all()
