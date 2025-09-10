# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.

import uuid

import grpc
import pydantic
import pytest

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
from ansys.sherlock.core.types.lifecycle_types import (
    ImportThermalSignalRequest,
    ThermalSignalFileProperties,
)
from ansys.sherlock.core.utils.version_check import SKIP_VERSION_CHECK


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    lifecycle = Lifecycle(channel, SKIP_VERSION_CHECK)

    phase_name = helper_test_create_life_phase(lifecycle)
    random_vibe_event_name = helper_test_add_random_vibe_event(lifecycle, phase_name)
    helper_test_add_random_vibe_profiles(lifecycle, random_vibe_event_name, phase_name)
    thermal_event_name = helper_test_add_thermal_event(lifecycle, phase_name)
    helper_test_add_thermal_profiles(lifecycle, phase_name, thermal_event_name)
    harmonic_vibe_event_name = helper_test_add_harmonic_event(lifecycle, phase_name)
    helper_test_add_harmonic_vibe_profile(lifecycle, phase_name, harmonic_vibe_event_name)
    shock_event_name = helper_test_add_shock_event(lifecycle, phase_name)
    helper_test_add_shock_profile(lifecycle, phase_name, shock_event_name)
    helper_test_load_random_vibe_profile(lifecycle)
    helper_test_load_thermal_profile(lifecycle)
    helper_test_load_harmonic_profile(lifecycle)
    helper_test_load_shock_profile_dataset(lifecycle)
    helper_test_load_shock_profile_pulses(lifecycle)
    helper_test_import_thermal_signal(lifecycle)


def helper_test_create_life_phase(lifecycle: Lifecycle):
    """Test create_life_phase API"""

    try:
        lifecycle.create_life_phase("", "", 1, "sec", 1, "PER SEC", description="Test1")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockCreateLifePhaseError as e:
        assert str(e.str_itr()) == "['Create life phase error: Project name is invalid.']"

    try:
        lifecycle.create_life_phase("Test", "", 1, "sec", 1, "PER SEC", description="Test1")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockCreateLifePhaseError as e:
        assert str(e.str_itr()) == "['Create life phase error: Phase name is invalid.']"

    try:
        lifecycle.create_life_phase("Test", "Example", 0, "sec", 1, "PER SEC", description="Test1")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockCreateLifePhaseError as e:
        assert str(e.str_itr()) == "['Create life phase error: Duration must be greater than 0.']"

    if lifecycle._is_connection_up():
        try:
            lifecycle.create_life_phase(
                "Test", "Example", 5, "sec", 0, "invalid", description="Test1"
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockCreateLifePhaseError as e:
            assert str(e.str_itr()) == "['Create life phase error: Cycle type is invalid.']"

    try:
        lifecycle.create_life_phase("Test", "Example", 5, "sec", 0, "PER SEC", description="Test1")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockCreateLifePhaseError as e:
        assert (
            str(e.str_itr())
            == "['Create life phase error: Number of cycles must be greater than 0.']"
        )

    if lifecycle._is_connection_up():
        phase_name = "Phase " + str(uuid.uuid4())
        try:
            lifecycle.create_life_phase(
                "Invalid Project",
                phase_name,
                duration=8400,
                duration_units="sec",
                num_of_cycles=4,
                cycle_type="COUNT",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockCreateLifePhaseError

        try:
            result = lifecycle.create_life_phase(
                "Tutorial Project",
                phase_name,
                duration=8400,
                duration_units="sec",
                num_of_cycles=4,
                cycle_type="COUNT",
            )
            assert result == 0
        except SherlockCreateLifePhaseError as e:
            pytest.fail(str(e.str_itr()))

        return phase_name


def helper_test_add_random_vibe_event(lifecycle: Lifecycle, phase_name: str) -> str:
    """Test add_random_vibe_event API"""

    try:
        lifecycle.add_random_vibe_event(
            "", "", "", 1, "sec", 1, "PER SEC", "45,45", "Uniaxial", "1,2,3", description="Test1"
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeEventError as e:
        assert str(e.str_itr()) == "['Add random vibe event error: Project name is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeEventError as e:
        assert str(e.str_itr()) == "['Add random vibe event error: Phase name is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeEventError as e:
        assert str(e.str_itr()) == "['Add random vibe event error: Event name is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeEventError as e:
        assert (
            str(e.str_itr()) == "['Add random vibe event error: Duration must be greater than 0.']"
        )

    if lifecycle._is_connection_up():
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
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockAddRandomVibeEventError as e:
            assert str(e.str_itr()) == "['Add random vibe event error: Cycle type is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeEventError as e:
        assert (
            str(e.str_itr())
            == "['Add random vibe event error: Number of cycles must be greater than 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeEventError as e:
        assert str(e.str_itr()) == "['Add random vibe event error: Elevation value is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeEventError as e:
        assert (
            str(e.str_itr()) == "['Add random vibe event error: "
            "At least one direction coordinate must be non-zero.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeEventError as e:
        assert (
            str(e.str_itr())
            == "['Add random vibe event error: Number of spherical coordinates is invalid.']"
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

        try:
            lifecycle.add_random_vibe_event(
                "Missing Project",
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
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockAddRandomVibeEventError

        return event_name


def helper_test_add_random_vibe_profiles(lifecycle: Lifecycle, event_name: str, phase_name: str):
    """Test the add_random_vibe_profiles API"""

    try:
        lifecycle.add_random_vibe_profiles(
            "",
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeProfilesError as e:
        assert str(e.str_itr()) == "['Add random vibe profiles error: " "Project name is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add random vibe profiles error: "
            "Profile name is invalid for random vibe profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add random vibe profiles error: "
            "Invalid entry 0: "
            "Number of elements is wrong for random vibe profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add random vibe profiles error:"
            " Invalid entry 1:"
            " Frequency or amplitude is invalid for random vibe profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddRandomVibeProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add random vibe profiles error:"
            " Invalid entry 2:"
            " Frequencies must be greater than 0 for random vibe profile 0.']"
        )

    if lifecycle._is_connection_up():
        try:
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
        except SherlockAddRandomVibeProfilesError as e:
            pytest.fail(str(e.str_itr()))

        try:
            lifecycle.add_random_vibe_profiles(
                "Missing Project",
                [
                    (
                        "Example",
                        "Event1",
                        "Profile1",
                        "HZ",
                        "G2/Hz",
                        [(1, 2), (3, 4)],
                    )
                ],
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockAddRandomVibeProfilesError


def helper_test_add_thermal_event(lifecycle: Lifecycle, phase_name: str) -> str:
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddThermalEventError as e:
        assert str(e.str_itr()) == "['Add thermal event error: Project name is invalid.']"

    try:
        lifecycle.add_thermal_event(
            "Test",
            "",
            "",
            1,
            "PER SEC",
            "STORAGE",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddThermalEventError as e:
        assert str(e.str_itr()) == "['Add thermal event error: Phase name is invalid.']"

    try:
        lifecycle.add_thermal_event(
            "Test",
            "Example",
            "",
            1,
            "PER SEC",
            "STORAGE",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddThermalEventError as e:
        assert str(e.str_itr()) == "['Add thermal event error: Event name is invalid.']"

    try:
        lifecycle.add_thermal_event(
            "Test",
            "Example",
            "Event1",
            -1,
            "PER SEC",
            "STORAGE",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddThermalEventError as e:
        assert (
            str(e.str_itr()) == "['Add thermal event error: "
            "Number of cycles must be greater than 0.']"
        )

    if lifecycle._is_connection_up():
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

        try:
            lifecycle.add_thermal_event(
                "Missing Project",
                phase_name,
                event_name,
                num_of_cycles=1,
                cycle_type="COUNT",
                cycle_state="OPERATING",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockAddThermalEventError

        return event_name


def helper_test_add_thermal_profiles(lifecycle: Lifecycle, phase_name: str, event_name: str):
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddThermalProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add thermal profiles error: "
            "Profile name is invalid for thermal profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddThermalProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add thermal profiles error: "
            "Invalid entry 0: "
            "Number of elements is wrong for thermal profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddThermalProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add thermal profiles error: "
            "Invalid entry 1: "
            "Step name is invalid for thermal profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddThermalProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add thermal profiles error: "
            "Invalid entry 2: "
            "Step type is invalid for thermal profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddThermalProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add thermal profiles error: "
            "Invalid entry 1: "
            "Time must be greater than 0 for thermal profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddThermalProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add thermal profiles error: "
            "Invalid entry 1: "
            "Time is invalid for thermal profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddThermalProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add thermal profiles error: "
            "Invalid entry 0: Temperature is invalid for thermal profile 0.']"
        )

    if lifecycle._is_connection_up():
        profile = str(uuid.uuid4())
        try:
            lifecycle.add_thermal_profiles(
                "Missing Project",
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
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockAddThermalProfilesError

        try:
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
        except SherlockAddThermalProfilesError as e:
            pytest.fail(str(e.str_itr()))


def helper_test_add_harmonic_event(lifecycle: Lifecycle, phase_name: str) -> str:
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicEventError as e:
        assert str(e.str_itr()) == "['Add harmonic event error: Project name is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicEventError as e:
        assert str(e.str_itr()) == "['Add harmonic event error: Phase name is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicEventError as e:
        assert str(e.str_itr()) == "['Add harmonic event error: Event name is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicEventError as e:
        assert str(e.str_itr()) == "['Add harmonic event error: Duration must be greater than 0.']"

    if lifecycle._is_connection_up():
        try:
            lifecycle.add_harmonic_event(
                "Test",
                "Example",
                "Event1",
                1.5,
                "sec",
                4.0,
                "Invalid Cycle Type",
                5,
                "45,45",
                "Uniaxial",
                "2,4,5",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockAddHarmonicEventError as e:
            assert str(e.str_itr()) == "['Add harmonic event error: Cycle type is invalid.']"

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
                "Invalid Profile Type",
                "2,4,5",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockAddHarmonicEventError as e:
            assert str(e.str_itr()) == "['Add harmonic event error: Profile type is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicEventError as e:
        assert (
            str(e.str_itr()) == "['Add harmonic event error: "
            "Number of cycles must be greater than 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicEventError as e:
        assert (
            str(e.str_itr()) == "['Add harmonic event error: "
            "Sweep rate must be greater than 0.']"
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
            "x,45",
            "Uniaxial",
            "2,4,5",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicEventError as e:
        assert str(e.str_itr()) == "['Add harmonic event error: Azimuth value is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicEventError as e:
        assert (
            str(e.str_itr()) == "['Add harmonic event error: "
            "At least one direction coordinate must be non-zero.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicEventError as e:
        assert (
            str(e.str_itr()) == "['Add harmonic event error: "
            "Number of spherical coordinates is invalid.']"
        )
    if lifecycle._is_connection_up():
        event_name = "Harmonic Vibe Event " + str(uuid.uuid4())
        try:
            lifecycle.add_harmonic_event(
                "Invalid Project",
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
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockAddHarmonicEventError

        try:
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
        except SherlockAddHarmonicEventError as e:
            raise (str(e.str_itr()))

        return event_name


def helper_test_add_harmonic_vibe_profile(
    lifecycle: Lifecycle, phase_name: str, harmonic_vibe_event_name: str
):
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicVibeProfilesError as e:
        assert str(e.str_itr()) == "['Add harmonic vibe profiles error: Project name is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicVibeProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add harmonic vibe profiles error:"
            " Phase name is invalid for harmonic vibe profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicVibeProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add harmonic vibe profiles error:"
            " Event name is invalid for harmonic vibe profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicVibeProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add harmonic vibe profiles error:"
            " Profile name is invalid for harmonic vibe profile 0.']"
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
                        "HZ",
                        "InvalidLoadUnits",
                        [
                            (10, 1),
                            (1000, 1),
                        ],
                        "",
                    )
                ],
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockAddHarmonicVibeProfilesError as e:
            assert (
                str(e.str_itr()) == "['Add harmonic vibe profiles error: "
                "Load units InvalidLoadUnits are invalid for harmonic vibe profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicVibeProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add harmonic vibe profiles error:"
            " Invalid entry 0: Number of elements is wrong for harmonic vibe profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicVibeProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add harmonic vibe profiles error: "
            "Invalid entry 1: Frequency or load is invalid for harmonic vibe profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddHarmonicVibeProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add harmonic vibe profiles error:"
            " Invalid entry 0: Load must be greater than 0 for harmonic vibe profile 0.']"
        )
    if lifecycle._is_connection_up():
        profile = str(uuid.uuid4())
        try:
            lifecycle.add_harmonic_vibe_profiles(
                "Invalid Project",
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
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockAddHarmonicVibeProfilesError

        try:
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
        except SherlockAddHarmonicVibeProfilesError as e:
            pytest.fail(str(e.str_itr()))


def helper_test_add_shock_event(lifecycle: Lifecycle, phase_name: str) -> str:
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockEventError as e:
        assert str(e.str_itr()) == "['Add shock event error: Project name is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockEventError as e:
        assert str(e.str_itr()) == "['Add shock event error: Phase name is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockEventError as e:
        assert str(e.str_itr()) == "['Add shock event error: Event name is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockEventError as e:
        assert str(e.str_itr()) == "['Add shock event error: Duration must be greater than 0.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockEventError as e:
        assert (
            str(e.str_itr()) == "['Add shock event error: "
            "Number of cycles must be greater than 0.']"
        )

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockEventError as e:
        assert str(e.str_itr()) == "['Add shock event error: Elevation value is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockEventError as e:
        assert (
            str(e.str_itr()) == "['Add shock event error: "
            "At least one direction coordinate must be non-zero.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockEventError as e:
        assert (
            str(e.str_itr()) == "['Add shock event error: "
            "Number of spherical coordinates is invalid.']"
        )

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
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockAddShockEventError

        try:
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
        except SherlockAddShockEventError as e:
            pytest.fail(str(e.str_itr()))

        return event_name


def helper_test_add_shock_profile(lifecycle: Lifecycle, phase_name: str, shock_event_name: str):
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockProfilesError as e:
        assert str(e.str_itr()) == "['Add shock profiles error: Project name is invalid.']"

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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add shock profiles error: Phase name is invalid for "
            "shock profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add shock profiles error: Event name is invalid for "
            "shock profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add shock profiles error:"
            " Profile name is invalid for shock profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add shock profiles error:"
            " Duration must be greater than 0 for shock profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add shock profiles error:"
            " Duration must be greater than 0 for shock profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add shock profiles error:"
            " Sample rate must be greater than 0 for shock profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add shock profiles error:"
            " Invalid entry 0: Number of elements is wrong for shock"
            " profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add shock profiles error:"
            " Invalid entry 0: Load must be "
            "greater than 0 for shock profile 0.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddShockProfilesError as e:
        assert (
            str(e.str_itr()) == "['Add shock profiles error:"
            " Invalid entry 0: Decay must be non-negative for "
            "shock profile 0.']"
        )

    if lifecycle._is_connection_up():
        profile = str(uuid.uuid4())
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
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockAddShockProfilesError

        try:
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
        except SherlockAddShockProfilesError as e:
            pytest.fail(str(e.str_itr()))


def helper_test_load_random_vibe_profile(lifecycle: Lifecycle):
    """Test load_random_vibe_profile."""

    try:
        lifecycle.load_random_vibe_profile(
            "",
            "Phase 1",
            "Random Event",
            "TestProfile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadRandomVibeProfileError as e:
        assert str(e.str_itr()) == "['Load random vibe profile error: Project name is invalid.']"

    try:
        lifecycle.load_random_vibe_profile(
            "Test",
            "",
            "Random Event",
            "TestProfile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadRandomVibeProfileError as e:
        assert str(e.str_itr()) == "['Load random vibe profile error: Phase name is invalid.']"

    try:
        lifecycle.load_random_vibe_profile(
            "Test",
            "Phase 1",
            "",
            "TestProfile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadRandomVibeProfileError as e:
        assert str(e.str_itr()) == "['Load random vibe profile error: Event name is invalid.']"

    try:
        lifecycle.load_random_vibe_profile(
            "Test",
            "Phase 1",
            "Random Event",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadRandomVibeProfileError as e:
        assert str(e.str_itr()) == "['Load random vibe profile error: File path is invalid.']"

    if lifecycle._is_connection_up():
        # happy path test missing because needs valid file
        try:
            lifecycle.load_random_vibe_profile(
                "Invalid Project",
                "Phase 1",
                "Random Event",
                "TestProfile.dat",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockLoadRandomVibeProfileError


def helper_test_load_harmonic_profile(lifecycle: Lifecycle):
    """Test load_harmonic_profile API."""

    try:
        lifecycle.load_harmonic_profile("", "Phase 1", "Harmonic Event", "Test_Profile.dat")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadHarmonicProfileError as e:
        assert str(e.str_itr()) == "['Load harmonic profile error: Project name is invalid.']"

    try:
        lifecycle.load_harmonic_profile("Test", "", "Harmonic Event", "Test_Profile.dat")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadHarmonicProfileError as e:
        assert str(e.str_itr()) == "['Load harmonic profile error: Phase name is invalid.']"

    try:
        lifecycle.load_harmonic_profile("Test", "Phase 1", "", "Test_Profile.dat")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadHarmonicProfileError as e:
        assert str(e.str_itr()) == "['Load harmonic profile error: Event name is invalid.']"

    try:
        lifecycle.load_harmonic_profile("Test", "Phase 1", "Harmonic Event", "")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadHarmonicProfileError as e:
        assert str(e.str_itr()) == "['Load harmonic profile error: File name is invalid.']"

    if lifecycle._is_connection_up():
        # happy path test missing because needs valid file
        try:
            lifecycle.load_harmonic_profile(
                "Invalid Project",
                "Phase 1",
                "Harmonic Event",
                "Test_Profile.dat",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockLoadHarmonicProfileError


def helper_test_load_thermal_profile(lifecycle: Lifecycle):
    """Test load_thermal_profile API"""

    try:
        lifecycle.load_thermal_profile(
            "",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadThermalProfileError as e:
        assert str(e.str_itr()) == "['Load thermal profile error: Project name is invalid.']"

    try:
        lifecycle.load_thermal_profile(
            "Test",
            "",
            "Thermal Event",
            "Tutorial_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadThermalProfileError as e:
        assert str(e.str_itr()) == "['Load thermal profile error: Phase name is invalid.']"

    try:
        lifecycle.load_thermal_profile(
            "Test",
            "Phase 1",
            "",
            "Tutorial_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadThermalProfileError as e:
        assert str(e.str_itr()) == "['Load thermal profile error: Event name is invalid.']"

    try:
        lifecycle.load_thermal_profile(
            "Test",
            "Phase 1",
            "Thermal Event",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadThermalProfileError as e:
        assert str(e.str_itr()) == "['Load thermal profile error: File path is invalid.']"

    if lifecycle._is_connection_up():
        # happy path test missing because needs valid file
        try:
            lifecycle.load_thermal_profile(
                "Test Project",
                "Phase 1",
                "Thermal Event",
                "Tutorial_Profile.dat",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockLoadThermalProfileError


def helper_test_load_shock_profile_dataset(lifecycle: Lifecycle):
    """Test load_shock_profile_dataset API"""

    try:
        lifecycle.load_shock_profile_dataset(
            "",
            "Phase 1",
            "Shock Event",
            "Test_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfileDatasetError as e:
        assert str(e.str_itr()) == "['Load shock profile dataset error: Project name is invalid.']"

    try:
        lifecycle.load_shock_profile_dataset(
            "Test",
            "",
            "Shock Event",
            "Test_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfileDatasetError as e:
        assert str(e.str_itr()) == "['Load shock profile dataset error: Phase name is invalid.']"

    try:
        lifecycle.load_shock_profile_dataset(
            "Test",
            "Phase 1",
            "",
            "Test_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfileDatasetError as e:
        assert str(e.str_itr()) == "['Load shock profile dataset error: Event name is invalid.']"

    try:
        lifecycle.load_shock_profile_dataset(
            "Test",
            "Phase 1",
            "Shock Event",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfileDatasetError as e:
        assert str(e.str_itr()) == "['Load shock profile dataset error: File path is invalid.']"

    if lifecycle._is_connection_up():
        # happy path test missing because needs valid file
        try:
            lifecycle.load_shock_profile_dataset(
                "Tutorial Project",
                "Phase 1",
                "Shock Event",
                "Test_Profile.dat",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockLoadShockProfileDatasetError


def helper_test_load_shock_profile_pulses(lifecycle: Lifecycle):
    """Test load_shock_profile_pulses API"""
    try:
        lifecycle.load_shock_profile_pulses(
            "",
            "Phase 1",
            "Shock Event",
            "Test_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfilePulsesError as e:
        assert str(e.str_itr()) == "['Load shock profile pulses error: Project name is invalid.']"

    try:
        lifecycle.load_shock_profile_pulses(
            "Test",
            "",
            "Shock Event",
            "Test_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfilePulsesError as e:
        assert str(e.str_itr()) == "['Load shock profile pulses error: Phase name is invalid.']"

    try:
        lifecycle.load_shock_profile_pulses(
            "Test",
            "Phase 1",
            "",
            "Test_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfilePulsesError as e:
        assert str(e.str_itr()) == "['Load shock profile pulses error: Event name is invalid.']"

    try:
        lifecycle.load_shock_profile_pulses(
            "Test",
            "Phase 1",
            "Shock Event",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfilePulsesError as e:
        assert str(e.str_itr()) == "['Load shock profile pulses error: File path is invalid.']"

    if lifecycle._is_connection_up():
        # happy path test missing because needs valid file
        try:
            lifecycle.load_shock_profile_pulses(
                "Tutorial Project",
                "Phase 1",
                "Shock Event",
                "Test_Profile.dat",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockLoadShockProfilePulsesError


def helper_test_import_thermal_signal(lifecycle: Lifecycle):
    try:
        lifecycle.import_thermal_signal(
            ImportThermalSignalRequest(
                file_name="",
                project="Tutorial Project",
                thermal_signal_file_properties=ThermalSignalFileProperties(
                    header_row_count=0,
                    numeric_format="English",
                    column_delimiter=",",
                    time_column="Time",
                    time_units="sec",
                    temperature_column="Temperature",
                    temperature_units="C",
                ),
                phase_name="Environmental",
                time_removal=False,
                load_range_percentage=0.25,
                number_of_range_bins=0,
                number_of_mean_bins=0,
                number_of_dwell_bins=0,
                temperature_range_filtering_limit=0.0,
                time_filtering_limit=72.0,
                time_filtering_limit_units="hr",
                generated_cycles_label="Generated Cycles from pySherlock",
            )
        )
        pytest.fail("No exception raised when using a missing file_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, file_name is invalid because it is None or empty."
        )

    try:
        lifecycle.import_thermal_signal(
            ImportThermalSignalRequest(
                file_name="C:/Temp/ThermalSignalMissing.csv",
                project="",
                thermal_signal_file_properties=ThermalSignalFileProperties(
                    header_row_count=0,
                    numeric_format="English",
                    column_delimiter=",",
                    time_column="Time",
                    time_units="sec",
                    temperature_column="Temperature",
                    temperature_units="C",
                ),
                phase_name="Environmental",
                time_removal=False,
                load_range_percentage=0.25,
                number_of_range_bins=0,
                number_of_mean_bins=0,
                number_of_dwell_bins=0,
                temperature_range_filtering_limit=0.0,
                time_filtering_limit=72.0,
                time_filtering_limit_units="hr",
                generated_cycles_label="Generated Cycles from pySherlock",
            )
        )
        pytest.fail("No exception raised when using a missing project parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, project is invalid because it is None or empty."
        )

    try:
        lifecycle.import_thermal_signal(
            ImportThermalSignalRequest(
                file_name="C:/Temp/ThermalSignalMissing.csv",
                project="Tutorial Project",
                thermal_signal_file_properties=ThermalSignalFileProperties(
                    header_row_count=0,
                    numeric_format="English",
                    column_delimiter=",",
                    time_column="Time",
                    time_units="sec",
                    temperature_column="Temperature",
                    temperature_units="C",
                ),
                phase_name="",
                time_removal=False,
                load_range_percentage=0.25,
                number_of_range_bins=0,
                number_of_mean_bins=0,
                number_of_dwell_bins=0,
                temperature_range_filtering_limit=0.0,
                time_filtering_limit=72.0,
                time_filtering_limit_units="hr",
                generated_cycles_label="Generated Cycles from pySherlock",
            )
        )
        pytest.fail("No exception raised when using a missing phase_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, phase_name is invalid because it is None or empty."
        )

    try:
        lifecycle.import_thermal_signal(
            ImportThermalSignalRequest(
                file_name="C:/Temp/ThermalSignalMissing.csv",
                project="Tutorial Project",
                thermal_signal_file_properties=ThermalSignalFileProperties(
                    header_row_count=0,
                    numeric_format="English",
                    column_delimiter=",",
                    time_column="Time",
                    time_units="sec",
                    temperature_column="Temperature",
                    temperature_units="C",
                ),
                phase_name="Environmental",
                time_removal=False,
                load_range_percentage=0.25,
                number_of_range_bins=-1,
                number_of_mean_bins=0,
                number_of_dwell_bins=0,
                temperature_range_filtering_limit=0.0,
                time_filtering_limit=72.0,
                time_filtering_limit_units="hr",
                generated_cycles_label="Generated Cycles from pySherlock",
            )
        )
        pytest.fail("No exception raised when using invalid number_of_range_bins parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, number_of_range_bins must be greater than or equal to 0."
        )

    try:
        lifecycle.import_thermal_signal(
            ImportThermalSignalRequest(
                file_name="C:/Temp/ThermalSignalMissing.csv",
                project="Tutorial Project",
                thermal_signal_file_properties=ThermalSignalFileProperties(
                    header_row_count=0,
                    numeric_format="English",
                    column_delimiter=",",
                    time_column="Time",
                    time_units="sec",
                    temperature_column="Temperature",
                    temperature_units="C",
                ),
                phase_name="Environmental",
                time_removal=False,
                load_range_percentage=0.25,
                number_of_range_bins=0,
                number_of_mean_bins=-1,
                number_of_dwell_bins=0,
                temperature_range_filtering_limit=0.0,
                time_filtering_limit=72.0,
                time_filtering_limit_units="hr",
                generated_cycles_label="Generated Cycles from pySherlock",
            )
        )
        pytest.fail("No exception raised when using invalid number_of_mean_bins parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, number_of_mean_bins must be greater than or equal to 0."
        )

    try:
        lifecycle.import_thermal_signal(
            ImportThermalSignalRequest(
                file_name="C:/Temp/ThermalSignalMissing.csv",
                project="Tutorial Project",
                thermal_signal_file_properties=ThermalSignalFileProperties(
                    header_row_count=0,
                    numeric_format="English",
                    column_delimiter=",",
                    time_column="Time",
                    time_units="sec",
                    temperature_column="Temperature",
                    temperature_units="C",
                ),
                phase_name="Environmental",
                time_removal=False,
                load_range_percentage=0.25,
                number_of_range_bins=0,
                number_of_mean_bins=0,
                number_of_dwell_bins=-1,
                temperature_range_filtering_limit=0.0,
                time_filtering_limit=72.0,
                time_filtering_limit_units="hr",
                generated_cycles_label="Generated Cycles from pySherlock",
            )
        )
        pytest.fail("No exception raised when using invalid number_of_dwell_bins parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, number_of_dwell_bins must be greater than or equal to 0."
        )

    try:
        lifecycle.import_thermal_signal(
            ImportThermalSignalRequest(
                file_name="C:/Temp/ThermalSignalMissing.csv",
                project="Tutorial Project",
                thermal_signal_file_properties=ThermalSignalFileProperties(
                    header_row_count=0,
                    numeric_format="English",
                    column_delimiter=",",
                    time_column="Time",
                    time_units="sec",
                    temperature_column="Temperature",
                    temperature_units="C",
                ),
                phase_name="Environmental",
                time_removal=False,
                load_range_percentage=0.25,
                number_of_range_bins=0,
                number_of_mean_bins=0,
                number_of_dwell_bins=0,
                temperature_range_filtering_limit=0.0,
                time_filtering_limit=72.0,
                time_filtering_limit_units="",
                generated_cycles_label="Generated Cycles from pySherlock",
            )
        )
        pytest.fail("No exception raised when using a missing time_filtering_limit_units parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, time_filtering_limit_units is invalid because it is None or empty."
        )

    try:
        lifecycle.import_thermal_signal(
            ImportThermalSignalRequest(
                file_name="C:/Temp/ThermalSignalMissing.csv",
                project="Tutorial Project",
                thermal_signal_file_properties=ThermalSignalFileProperties(
                    header_row_count=0,
                    numeric_format="English",
                    column_delimiter=",",
                    time_column="Time",
                    time_units="sec",
                    temperature_column="Temperature",
                    temperature_units="C",
                ),
                phase_name="Environmental",
                time_removal=False,
                load_range_percentage=0.25,
                number_of_range_bins=0,
                number_of_mean_bins=0,
                number_of_dwell_bins=0,
                temperature_range_filtering_limit=0.0,
                time_filtering_limit=72.0,
                time_filtering_limit_units="hr",
                generated_cycles_label="",
            )
        )
        pytest.fail("No exception raised when using a missing generated_cycles_label parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, generated_cycles_label is invalid because it is None or empty."
        )


if __name__ == "__main__":
    test_all()
