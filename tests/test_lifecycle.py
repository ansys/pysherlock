# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
    SherlockDeleteError,
    SherlockLoadHarmonicProfileError,
    SherlockLoadRandomVibeProfileError,
    SherlockLoadShockProfileDatasetError,
    SherlockLoadShockProfilePulsesError,
    SherlockLoadThermalProfileError,
    SherlockSaveLifeCycleError,
    SherlockSaveProfileError,
    SherlockUpdateLifePhaseError,
)
from ansys.sherlock.core.lifecycle import Lifecycle
from ansys.sherlock.core.types.lifecycle_types import (
    DeleteEventRequest,
    DeletePhaseRequest,
    HarmonicVibeProfileCsvFileProperties,
    ImportThermalSignalRequest,
    RandomVibeProfileCsvFileProperties,
    SaveHarmonicProfileRequest,
    SaveLifeCycleRequest,
    SaveRandomVibeProfileRequest,
    SaveShockPulseProfileRequest,
    SaveThermalProfileRequest,
    ShockProfileDatasetCsvFileProperties,
    ShockProfilePulsesCsvFileProperties,
    ThermalProfileCsvFileProperties,
    ThermalSignalFileProperties,
    UpdateLifeCycleRequest,
    UpdateLifePhaseRequest,
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

    helper_test_save_harmonic_profile(lifecycle)
    helper_test_save_random_vibe_profile(lifecycle)
    helper_test_save_shock_pulse_profile(lifecycle)
    helper_test_save_thermal_profile(lifecycle)

    helper_test_delete_event(lifecycle, shock_event_name, phase_name)
    helper_test_delete_phase(lifecycle, phase_name)
    helper_test_update_life_phase(lifecycle)

    helper_test_update_life_cycle(lifecycle)
    helper_test_save_life_cycle(lifecycle)


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


def helper_test_update_life_cycle(lifecycle: Lifecycle):
    """Test update_life_cycle API"""

    if lifecycle._is_connection_up():
        project = "Tutorial Project"
        new_name = "new name"
        new_description = "new description"
        new_reliability_metric = 20

        # Unit options:
        # "Reliability (%)", "Prob. of Failure (%)", "MTBF (years)",
        # "MTBF (hours)", "FITs (1E6 hrs)", "FITs (1E9 hrs)"
        new_reliability_metric_units = "invalid_unit"

        new_service_life = 5

        # Unit options:
        # "year","day","hr", "min","sec"
        new_service_life_units = "year"

        result_archive_file_name = "filename"

        # Test invalid reliability unit
        return_code = lifecycle.update_life_cycle(
            UpdateLifeCycleRequest(
                project=project,
                new_name=new_name,
                new_description=new_description,
                new_reliability_metric=new_reliability_metric,
                new_reliability_metric_units=new_reliability_metric_units,
                new_service_life=new_service_life,
                new_service_life_units=new_service_life_units,
                result_archive_file_name=result_archive_file_name,
            )
        )

        expected_err = "Unsupported unit type '" + new_reliability_metric_units
        assert return_code.message.startswith(expected_err)
        new_reliability_metric_units = "Prob. of Failure (%)"

        # Test invalid service life unit
        new_service_life_units = "invalid_unit"

        return_code = lifecycle.update_life_cycle(
            UpdateLifeCycleRequest(
                project=project,
                new_name=new_name,
                new_description=new_description,
                new_reliability_metric=new_reliability_metric,
                new_reliability_metric_units=new_reliability_metric_units,
                new_service_life=new_service_life,
                new_service_life_units=new_service_life_units,
                result_archive_file_name=result_archive_file_name,
            )
        )

        expected_err = "Unsupported unit type '" + new_service_life_units + "' Valid options are: "
        assert return_code.message.startswith(expected_err)
        new_service_life_units = "year"

        # Test invalid file name
        result_archive_file_name = "file/name"

        return_code = lifecycle.update_life_cycle(
            UpdateLifeCycleRequest(
                project=project,
                new_name=new_name,
                new_description=new_description,
                new_reliability_metric=new_reliability_metric,
                new_reliability_metric_units=new_reliability_metric_units,
                new_service_life=new_service_life,
                new_service_life_units=new_service_life_units,
                result_archive_file_name=result_archive_file_name,
            )
        )

        assert (
            return_code.message
            == "Invalid Archive Name: The archive name contains invalid characters"
        )
        result_archive_file_name = "filename"

        # Test success
        return_code = lifecycle.update_life_cycle(
            UpdateLifeCycleRequest(
                project=project,
                new_name=new_name,
                new_description=new_description,
                new_reliability_metric=new_reliability_metric,
                new_reliability_metric_units=new_reliability_metric_units,
                new_service_life=new_service_life,
                new_service_life_units=new_service_life_units,
                result_archive_file_name=result_archive_file_name,
            )
        )

        assert return_code.message == ""


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
        assert str(e.message) == "Project name is invalid."

    try:
        lifecycle.load_random_vibe_profile(
            "Test Project",
            "",
            "Random Event",
            "TestProfile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadRandomVibeProfileError as e:
        assert str(e.message) == "Phase name is invalid."

    try:
        lifecycle.load_random_vibe_profile(
            "Test Project",
            "Phase 1",
            "",
            "TestProfile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadRandomVibeProfileError as e:
        assert str(e.message) == "Event name is invalid."

    try:
        lifecycle.load_random_vibe_profile(
            "Test Project",
            "Phase 1",
            "Random Event",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadRandomVibeProfileError as e:
        assert str(e.message) == "File path is invalid."

    try:
        lifecycle.load_random_vibe_profile(
            "Test Project",
            "Phase 1",
            "Random Event",
            "RandomProfile.csv",
        )
        pytest.fail("No exception raised when using missing CSV properties")
    except SherlockLoadRandomVibeProfileError as e:
        assert (
            str(e.message)
            == "CSV file properties must be provided for CSV random vibe profile files."
        )

    try:
        lifecycle.load_random_vibe_profile(
            "Test Project",
            "Phase 1",
            "Random Event",
            "RandomProfile.csv",
            csv_file_properties=RandomVibeProfileCsvFileProperties(
                profile_name="",
                header_row_count=0,
                column_delimiter=",",
                frequency_column="Frequency",
                frequency_units="Hz",
                amplitude_column="Amplitude",
                amplitude_units="G2/Hz",
            ),
        )
        pytest.fail("No exception raised when using missing profile name")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, profile_name is invalid because it is None or empty."
        )

    try:
        lifecycle.load_random_vibe_profile(
            "Test Project",
            "Phase 1",
            "Random Event",
            "RandomProfile.csv",
            csv_file_properties=RandomVibeProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                frequency_column="",
                frequency_units="Hz",
                amplitude_column="Amplitude",
                amplitude_units="G2/Hz",
            ),
        )
        pytest.fail("No exception raised when using missing frequency column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, frequency_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_random_vibe_profile(
            "Test Project",
            "Phase 1",
            "Random Event",
            "RandomProfile.csv",
            csv_file_properties=RandomVibeProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                frequency_column="Frequency",
                frequency_units="",
                amplitude_column="Amplitude",
                amplitude_units="G2/Hz",
            ),
        )
        pytest.fail("No exception raised when using missing frequency units")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, frequency_units is invalid because it is None or empty."
        )

    try:
        lifecycle.load_random_vibe_profile(
            "Test Project",
            "Phase 1",
            "Random Event",
            "RandomProfile.csv",
            csv_file_properties=RandomVibeProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                frequency_column="Frequency",
                frequency_units="Hz",
                amplitude_column="",
                amplitude_units="G2/Hz",
            ),
        )
        pytest.fail("No exception raised when using missing amplitude column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, amplitude_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_random_vibe_profile(
            "Test Project",
            "Phase 1",
            "Random Event",
            "RandomProfile.csv",
            csv_file_properties=RandomVibeProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                frequency_column="Frequency",
                frequency_units="Hz",
                amplitude_column="Amplitude",
                amplitude_units="",
            ),
        )
        pytest.fail("No exception raised when using missing amplitude units")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, amplitude_units is invalid because it is None or empty."
        )

    try:
        lifecycle.load_random_vibe_profile(
            "Test Project",
            "Phase 1",
            "Random Event",
            "RandomProfile.csv",
            csv_file_properties=RandomVibeProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=-1,
                column_delimiter=",",
                frequency_column="Frequency",
                frequency_units="Hz",
                amplitude_column="Amplitude",
                amplitude_units="G2/Hz",
            ),
        )
        pytest.fail("No exception raised when using negative header row count")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, header_row_count must be greater than or equal to 0."
        )

    try:
        lifecycle.load_random_vibe_profile(
            "Test Project",
            "Phase 1",
            "Random Event",
            "RandomProfile.dat",
            csv_file_properties=RandomVibeProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                frequency_column="Frequency",
                frequency_units="Hz",
                amplitude_column="Amplitude",
                amplitude_units="G2/Hz",
            ),
        )
        pytest.fail("No exception raised when using csv_file_properties for non-CSV file")
    except SherlockLoadRandomVibeProfileError as e:
        assert (
            str(e.message)
            == "CSV file properties are not used for non-CSV random vibe profile files."
        )

    if lifecycle._is_connection_up():
        # happy path test missing because needs valid file
        try:
            lifecycle.load_random_vibe_profile(
                "Test Project",
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
        lifecycle.load_harmonic_profile("", "Phase 1", "Harmonic Event", "Test_Profile.dat", "X")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadHarmonicProfileError as e:
        assert str(e.message) == "Project name is invalid."

    try:
        lifecycle.load_harmonic_profile(
            "Test Project", "", "Harmonic Event", "Test_Profile.dat", "X"
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadHarmonicProfileError as e:
        assert str(e.message) == "Phase name is invalid."

    try:
        lifecycle.load_harmonic_profile("Test Project", "Phase 1", "", "Test_Profile.dat", "X")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadHarmonicProfileError as e:
        assert str(e.message) == "Event name is invalid."

    try:
        lifecycle.load_harmonic_profile("Test Project", "Phase 1", "Harmonic Event", "", "X")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadHarmonicProfileError as e:
        assert str(e.message) == "File name is invalid."

    try:
        lifecycle.load_harmonic_profile(
            "Test Project",
            "Phase 1",
            "Harmonic Event",
            "Harmonic_Profile.csv",
            "X",
        )
        pytest.fail("No exception raised when using missing CSV properties")
    except SherlockLoadHarmonicProfileError as e:
        assert (
            str(e.message) == "CSV file properties must be provided for CSV harmonic profile files."
        )

    try:
        lifecycle.load_harmonic_profile(
            "Test Project",
            "Phase 1",
            "Harmonic Event",
            "Harmonic_Profile.csv",
            "X",
            csv_file_properties=HarmonicVibeProfileCsvFileProperties(
                profile_name="",
                header_row_count=0,
                column_delimiter=",",
                frequency_column="Frequency",
                frequency_units="Hz",
                load_column="Load",
                load_units="G",
            ),
        )
        pytest.fail("No exception raised when using missing profile name")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, profile_name is invalid because it is None or empty."
        )

    try:
        lifecycle.load_harmonic_profile(
            "Test Project",
            "Phase 1",
            "Harmonic Event",
            "Harmonic_Profile.csv",
            "X",
            csv_file_properties=HarmonicVibeProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                frequency_column="",
                frequency_units="Hz",
                load_column="Load",
                load_units="G",
            ),
        )
        pytest.fail("No exception raised when using missing frequency column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, frequency_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_harmonic_profile(
            "Test Project",
            "Phase 1",
            "Harmonic Event",
            "Harmonic_Profile.csv",
            "X",
            csv_file_properties=HarmonicVibeProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                frequency_column="Frequency",
                frequency_units="",
                load_column="Load",
                load_units="G",
            ),
        )
        pytest.fail("No exception raised when using missing frequency units")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, frequency_units is invalid because it is None or empty."
        )

    try:
        lifecycle.load_harmonic_profile(
            "Test Project",
            "Phase 1",
            "Harmonic Event",
            "Harmonic_Profile.csv",
            "X",
            csv_file_properties=HarmonicVibeProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                frequency_column="Frequency",
                frequency_units="Hz",
                load_column="",
                load_units="G",
            ),
        )
        pytest.fail("No exception raised when using missing load column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, load_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_harmonic_profile(
            "Test Project",
            "Phase 1",
            "Harmonic Event",
            "Harmonic_Profile.csv",
            "X",
            csv_file_properties=HarmonicVibeProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                frequency_column="Frequency",
                frequency_units="Hz",
                load_column="Load",
                load_units="",
            ),
        )
        pytest.fail("No exception raised when using missing load units")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, load_units is invalid because it is None or empty."
        )

    try:
        lifecycle.load_harmonic_profile(
            "Test Project",
            "Phase 1",
            "Harmonic Event",
            "Harmonic_Profile.csv",
            "X",
            csv_file_properties=HarmonicVibeProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=-1,
                column_delimiter=",",
                frequency_column="Frequency",
                frequency_units="Hz",
                load_column="Load",
                load_units="G",
            ),
        )
        pytest.fail("No exception raised when using negative header row count")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, header_row_count must be greater than or equal to 0."
        )

    try:
        lifecycle.load_harmonic_profile(
            "Test Project",
            "Phase 1",
            "Harmonic Event",
            "Harmonic_Profile.dat",
            "X",
            csv_file_properties=HarmonicVibeProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                frequency_column="Frequency",
                frequency_units="Hz",
                load_column="Load",
                load_units="G",
            ),
        )
        pytest.fail("No exception raised when using csv_file_properties for non-CSV file")
    except SherlockLoadHarmonicProfileError as e:
        assert (
            str(e.message) == "CSV file properties are not used for non-CSV harmonic profile files."
        )

    if lifecycle._is_connection_up():
        # happy path test missing because needs valid file
        try:
            lifecycle.load_harmonic_profile(
                "Test Project",
                "Phase 1",
                "Harmonic Event",
                "Test_Profile.dat",
                "x",
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
        assert str(e.message) == "Project name is invalid."

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "",
            "Thermal Event",
            "Tutorial_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadThermalProfileError as e:
        assert str(e.message) == "Phase name is invalid."

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "",
            "Tutorial_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadThermalProfileError as e:
        assert str(e.message) == "Event name is invalid."

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "Thermal Event",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadThermalProfileError as e:
        assert str(e.message) == "File path is invalid."

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.csv",
        )
        pytest.fail("No exception raised when using missing CSV properties")
    except SherlockLoadThermalProfileError as e:
        assert (
            str(e.message) == "CSV file properties must be provided for CSV thermal profile files."
        )

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.csv",
            csv_file_properties=ThermalProfileCsvFileProperties(
                profile_name="",
                header_row_count=0,
                column_delimiter=",",
                step_column="Step",
                type_column="Type",
                time_column="Time",
                time_units="min",
                temperature_column="Temp",
                temperature_units="C",
            ),
        )
        pytest.fail("No exception raised when using missing profile name")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, profile_name is invalid because it is None or empty."
        )

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.csv",
            csv_file_properties=ThermalProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                step_column="",
                type_column="Type",
                time_column="Time",
                time_units="min",
                temperature_column="Temp",
                temperature_units="C",
            ),
        )
        pytest.fail("No exception raised when using missing step column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, step_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.csv",
            csv_file_properties=ThermalProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                step_column="Step",
                type_column="",
                time_column="Time",
                time_units="min",
                temperature_column="Temp",
                temperature_units="C",
            ),
        )
        pytest.fail("No exception raised when using missing type column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, type_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.csv",
            csv_file_properties=ThermalProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                step_column="Step",
                type_column="Type",
                time_column="",
                time_units="min",
                temperature_column="Temp",
                temperature_units="C",
            ),
        )
        pytest.fail("No exception raised when using missing time column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, time_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.csv",
            csv_file_properties=ThermalProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                step_column="Step",
                type_column="Type",
                time_column="Time",
                time_units="",
                temperature_column="Temp",
                temperature_units="C",
            ),
        )
        pytest.fail("No exception raised when using missing time units")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, time_units is invalid because it is None or empty."
        )

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.csv",
            csv_file_properties=ThermalProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                step_column="Step",
                type_column="Type",
                time_column="Time",
                time_units="min",
                temperature_column="",
                temperature_units="C",
            ),
        )
        pytest.fail("No exception raised when using missing temperature column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, temperature_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.csv",
            csv_file_properties=ThermalProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                step_column="Step",
                type_column="Type",
                time_column="Time",
                time_units="min",
                temperature_column="Temp",
                temperature_units="",
            ),
        )
        pytest.fail("No exception raised when using missing temperature units")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, temperature_units is invalid because it is None or empty."
        )

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.csv",
            csv_file_properties=ThermalProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=-1,
                column_delimiter=",",
                step_column="Step",
                type_column="Type",
                time_column="Time",
                time_units="min",
                temperature_column="Temp",
                temperature_units="C",
            ),
        )
        pytest.fail("No exception raised when using invalid header_row_count")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, header_row_count must be greater than or equal to 0."
        )

    try:
        lifecycle.load_thermal_profile(
            "Test Project",
            "Phase 1",
            "Thermal Event",
            "Tutorial_Profile.dat",
            csv_file_properties=ThermalProfileCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                step_column="Step",
                type_column="Type",
                time_column="Time",
                time_units="min",
                temperature_column="Temp",
                temperature_units="C",
            ),
        )
        pytest.fail("No exception raised when using csv_file_properties for non-CSV file")
    except SherlockLoadThermalProfileError as e:
        assert (
            str(e.message) == "CSV file properties are not used for non-CSV thermal profile files."
        )

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
        assert str(e.message) == "Project name is invalid."

    try:
        lifecycle.load_shock_profile_dataset(
            "Test Project",
            "",
            "Shock Event",
            "Test_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfileDatasetError as e:
        assert str(e.message) == "Phase name is invalid."

    try:
        lifecycle.load_shock_profile_dataset(
            "Test Project",
            "Phase 1",
            "",
            "Test_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfileDatasetError as e:
        assert str(e.message) == "Event name is invalid."

    try:
        lifecycle.load_shock_profile_dataset(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfileDatasetError as e:
        assert str(e.message) == "File path is invalid."

    try:
        lifecycle.load_shock_profile_dataset(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
        )
        pytest.fail("No exception raised when using missing CSV properties")
    except SherlockLoadShockProfileDatasetError as e:
        assert (
            str(e.message)
            == "CSV file properties must be provided for CSV shock profile dataset files."
        )

    try:
        lifecycle.load_shock_profile_dataset(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfileDatasetCsvFileProperties(
                profile_name="",
                header_row_count=0,
                column_delimiter=",",
                time_column="Time",
                time_units="ms",
                load_column="Load",
                load_units="G",
            ),
        )
        pytest.fail("No exception raised when using missing profile name")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, profile_name is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_dataset(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfileDatasetCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                time_column="",
                time_units="ms",
                load_column="Load",
                load_units="G",
            ),
        )
        pytest.fail("No exception raised when using missing time column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, time_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_dataset(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfileDatasetCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                time_column="Time",
                time_units="",
                load_column="Load",
                load_units="G",
            ),
        )
        pytest.fail("No exception raised when using missing time units")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, time_units is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_dataset(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfileDatasetCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                time_column="Time",
                time_units="ms",
                load_column="",
                load_units="G",
            ),
        )
        pytest.fail("No exception raised when using missing load column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, load_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_dataset(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfileDatasetCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                time_column="Time",
                time_units="ms",
                load_column="Load",
                load_units="",
            ),
        )
        pytest.fail("No exception raised when using missing load units")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, load_units is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_dataset(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfileDatasetCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=-1,
                column_delimiter=",",
                time_column="Time",
                time_units="ms",
                load_column="Load",
                load_units="G",
            ),
        )
        pytest.fail("No exception raised when using invalid header_row_count")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, header_row_count must be greater than or equal to 0."
        )

    try:
        lifecycle.load_shock_profile_dataset(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.dat",
            csv_file_properties=ShockProfileDatasetCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                column_delimiter=",",
                time_column="Time",
                time_units="ms",
                load_column="Load",
                load_units="G",
            ),
        )
        pytest.fail("No exception raised when using csv_file_properties for non-CSV file")
    except SherlockLoadShockProfileDatasetError as e:
        assert (
            str(e.message)
            == "CSV file properties are not used for non-CSV shock profile dataset files."
        )

    if lifecycle._is_connection_up():
        # happy path test missing because needs valid file
        try:
            lifecycle.load_shock_profile_dataset(
                "Test Project",
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
        assert str(e.message) == "Project name is invalid."

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "",
            "Shock Event",
            "Test_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfilePulsesError as e:
        assert str(e.message) == "Phase name is invalid."

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "",
            "Test_Profile.dat",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfilePulsesError as e:
        assert str(e.message) == "Event name is invalid."

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockLoadShockProfilePulsesError as e:
        assert str(e.message) == "File path is invalid."

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
        )
        pytest.fail("No exception raised when using missing CSV properties")
    except SherlockLoadShockProfilePulsesError as e:
        assert (
            str(e.message)
            == "CSV file properties must be provided for CSV shock profile pulses files."
        )

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="",
                header_row_count=0,
                numeric_format="English",
                column_delimiter=",",
                duration=25,
                duration_units="ms",
                sample_rate=0.1,
                sample_rate_units="ms",
                shape_column="Shape",
                load_column="Load",
                load_units="G",
                frequency_column="Frequency",
                frequency_units="HZ",
                decay_column="Decay",
            ),
        )
        pytest.fail("No exception raised when using missing profile name")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, profile_name is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                numeric_format="English",
                column_delimiter=",",
                duration=25,
                duration_units="ms",
                sample_rate=0.1,
                sample_rate_units="ms",
                shape_column="",
                load_column="Load",
                load_units="G",
                frequency_column="Frequency",
                frequency_units="HZ",
                decay_column="Decay",
            ),
        )
        pytest.fail("No exception raised when using missing shape column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, shape_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                numeric_format="English",
                column_delimiter=",",
                duration=25,
                duration_units="ms",
                sample_rate=0.1,
                sample_rate_units="ms",
                shape_column="Shape",
                load_column="",
                load_units="G",
                frequency_column="Frequency",
                frequency_units="HZ",
                decay_column="Decay",
            ),
        )
        pytest.fail("No exception raised when using missing load column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, load_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                numeric_format="English",
                column_delimiter=",",
                duration=25,
                duration_units="ms",
                sample_rate=0.1,
                sample_rate_units="ms",
                shape_column="Shape",
                load_column="Load",
                load_units="",
                frequency_column="Frequency",
                frequency_units="HZ",
                decay_column="Decay",
            ),
        )
        pytest.fail("No exception raised when using missing load units")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, load_units is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                numeric_format="English",
                column_delimiter=",",
                duration=25,
                duration_units="ms",
                sample_rate=0.1,
                sample_rate_units="ms",
                shape_column="Shape",
                load_column="Load",
                load_units="G",
                frequency_column="",
                frequency_units="HZ",
                decay_column="Decay",
            ),
        )
        pytest.fail("No exception raised when using missing frequency column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, frequency_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                numeric_format="English",
                column_delimiter=",",
                duration=25,
                duration_units="ms",
                sample_rate=0.1,
                sample_rate_units="ms",
                shape_column="Shape",
                load_column="Load",
                load_units="G",
                frequency_column="Frequency",
                frequency_units="",
                decay_column="Decay",
            ),
        )
        pytest.fail("No exception raised when using missing frequency units")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, frequency_units is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                numeric_format="English",
                column_delimiter=",",
                duration=25,
                duration_units="ms",
                sample_rate=0.1,
                sample_rate_units="ms",
                shape_column="Shape",
                load_column="Load",
                load_units="G",
                frequency_column="Frequency",
                frequency_units="HZ",
                decay_column="",
            ),
        )
        pytest.fail("No exception raised when using missing decay column")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, decay_column is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                numeric_format="English",
                column_delimiter=",",
                duration=25,
                duration_units="",
                sample_rate=0.1,
                sample_rate_units="ms",
                shape_column="Shape",
                load_column="Load",
                load_units="G",
                frequency_column="Frequency",
                frequency_units="HZ",
                decay_column="Decay",
            ),
        )
        pytest.fail("No exception raised when using missing duration units")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, duration_units is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                numeric_format="English",
                column_delimiter=",",
                duration=25,
                duration_units="ms",
                sample_rate=0.1,
                sample_rate_units="",
                shape_column="Shape",
                load_column="Load",
                load_units="G",
                frequency_column="Frequency",
                frequency_units="HZ",
                decay_column="Decay",
            ),
        )
        pytest.fail("No exception raised when using missing sample rate units")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, sample_rate_units is invalid because it is None or empty."
        )

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                numeric_format="English",
                column_delimiter=",",
                duration=-25,
                duration_units="ms",
                sample_rate=0.1,
                sample_rate_units="ms",
                shape_column="Shape",
                load_column="Load",
                load_units="G",
                frequency_column="Frequency",
                frequency_units="HZ",
                decay_column="Decay",
            ),
        )
        pytest.fail("No exception raised when using negative duration")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == "Value error, duration must be greater than 0."

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                numeric_format="English",
                column_delimiter=",",
                duration=25,
                duration_units="ms",
                sample_rate=-0.1,
                sample_rate_units="ms",
                shape_column="Shape",
                load_column="Load",
                load_units="G",
                frequency_column="Frequency",
                frequency_units="HZ",
                decay_column="Decay",
            ),
        )
        pytest.fail("No exception raised when using negative sample rate")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == "Value error, sample_rate must be greater than 0."

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.csv",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=-1,
                numeric_format="English",
                column_delimiter=",",
                duration=25,
                duration_units="ms",
                sample_rate=0.1,
                sample_rate_units="ms",
                shape_column="Shape",
                load_column="Load",
                load_units="G",
                frequency_column="Frequency",
                frequency_units="HZ",
                decay_column="Decay",
            ),
        )
        pytest.fail("No exception raised when using invalid header_row_count")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            str(e.errors()[0]["msg"])
            == "Value error, header_row_count must be greater than or equal to 0."
        )

    try:
        lifecycle.load_shock_profile_pulses(
            "Test Project",
            "Phase 1",
            "Shock Event",
            "Test_Profile.dat",
            csv_file_properties=ShockProfilePulsesCsvFileProperties(
                profile_name="Test Profile",
                header_row_count=0,
                numeric_format="English",
                column_delimiter=",",
                duration=25,
                duration_units="ms",
                sample_rate=0.1,
                sample_rate_units="ms",
                shape_column="Shape",
                load_column="Load",
                load_units="G",
                frequency_column="Frequency",
                frequency_units="HZ",
                decay_column="Decay",
            ),
        )
        pytest.fail("No exception raised when using csv_file_properties for non-CSV file")
    except SherlockLoadShockProfilePulsesError as e:
        assert (
            str(e.message)
            == "CSV file properties are not used for non-CSV shock profile pulses files."
        )

    if lifecycle._is_connection_up():
        # happy path test missing because needs valid file
        try:
            lifecycle.load_shock_profile_pulses(
                "Test Project",
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


def helper_test_save_harmonic_profile(lifecycle: Lifecycle):
    # project missing
    try:
        lifecycle.save_harmonic_profile(
            SaveHarmonicProfileRequest(
                project="",
                phase_name="On The Road",
                event_name="5 - Harmonic Event",
                triaxial_axis="x",
                file_path="C:/Temp/Harmonic.dat",
            )
        )
        pytest.fail("No exception raised when using a missing project parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, project is invalid because it is None or empty."
        )

    # phase_name missing
    try:
        lifecycle.save_harmonic_profile(
            SaveHarmonicProfileRequest(
                project="Tutorial Project",
                phase_name="",
                event_name="5 - Harmonic Event",
                triaxial_axis="x",
                file_path="C:/Temp/Harmonic.dat",
            )
        )
        pytest.fail("No exception raised when using a missing phase_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, phase_name is invalid because it is None or empty."
        )

    # event_name missing
    try:
        lifecycle.save_harmonic_profile(
            SaveHarmonicProfileRequest(
                project="Tutorial Project",
                phase_name="On The Road",
                event_name="",
                triaxial_axis="x",
                file_path="C:/Temp/Harmonic.dat",
            )
        )
        pytest.fail("No exception raised when using a missing event_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, event_name is invalid because it is None or empty."
        )

    if lifecycle._is_connection_up():

        # invalid triaxial_axis
        try:
            lifecycle.save_harmonic_profile(
                SaveHarmonicProfileRequest(
                    project="Tutorial Project",
                    phase_name="On The Road",
                    event_name="5 - Harmonic Event",
                    triaxial_axis="a",
                    file_path="C:/Temp/Harmonic.dat",
                )
            )
            pytest.fail("No exception raised when using a missing triaxial_axis parameter")
        except Exception as e:
            assert type(e) == SherlockSaveProfileError


def helper_test_save_random_vibe_profile(lifecycle: Lifecycle):
    # project missing
    try:
        lifecycle.save_random_vibe_profile(
            SaveRandomVibeProfileRequest(
                project="",
                phase_name="On The Road",
                event_name="RV_Event_01",
                file_path="C:/Temp/RV_Event_01.dat",
            )
        )
        pytest.fail("No exception raised when using a missing project parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, project is invalid because it is None or empty."
        )

    # phase_name missing
    try:
        lifecycle.save_random_vibe_profile(
            SaveRandomVibeProfileRequest(
                project="Tutorial Project",
                phase_name="",
                event_name="1 - Vibration",
                file_path="C:/Temp/1 - Vibration.dat",
            )
        )
        pytest.fail("No exception raised when using a missing phase_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, phase_name is invalid because it is None or empty."
        )

    # event_name missing
    try:
        lifecycle.save_random_vibe_profile(
            SaveRandomVibeProfileRequest(
                project="Tutorial Project",
                phase_name="On The Road",
                event_name="",
                file_path="C:/Temp/1 - Vibration.dat",
            )
        )
        pytest.fail("No exception raised when using a missing event_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, event_name is invalid because it is None or empty."
        )

    if lifecycle._is_connection_up():

        # invalid file_path
        try:
            lifecycle.save_random_vibe_profile(
                SaveRandomVibeProfileRequest(
                    project="Tutorial Project",
                    phase_name="On The Road",
                    event_name="1 - Vibration",
                    file_path="C:/Temp/RV_Event_01.txt",
                )
            )
            pytest.fail("No exception raised when using an invalid file_path parameter")
        except Exception as e:
            assert type(e) == SherlockSaveProfileError


def helper_test_save_shock_pulse_profile(lifecycle: Lifecycle):
    # project missing
    try:
        lifecycle.save_shock_pulse_profile(
            SaveShockPulseProfileRequest(
                project="",
                phase_name="On The Road",
                event_name="3 - Collision",
                file_path="C:/Temp/3 - Collision.dat",
            )
        )
        pytest.fail("No exception raised when using a missing project parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, project is invalid because it is None or empty."
        )

    # phase_name missing
    try:
        lifecycle.save_shock_pulse_profile(
            SaveShockPulseProfileRequest(
                project="Tutorial Project",
                phase_name="",
                event_name="3 - Collision",
                file_path="C:/Temp/3 - Collision.dat",
            )
        )
        pytest.fail("No exception raised when using a missing phase_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, phase_name is invalid because it is None or empty."
        )

    # event_name missing
    try:
        lifecycle.save_shock_pulse_profile(
            SaveShockPulseProfileRequest(
                project="Tutorial Project",
                phase_name="On The Road",
                event_name="",
                file_path="C:/Temp/3 - Collision.dat",
            )
        )
        pytest.fail("No exception raised when using a missing event_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, event_name is invalid because it is None or empty."
        )

    if lifecycle._is_connection_up():

        # invalid file_path
        try:
            lifecycle.save_shock_pulse_profile(
                SaveShockPulseProfileRequest(
                    project="Tutorial Project",
                    phase_name="On The Road",
                    event_name="3 - Collision",
                    file_path="C:/Temp/3 - Collision.txt",
                )
            )
            pytest.fail("No exception raised when using an invalid file_path parameter")
        except Exception as e:
            assert type(e) == SherlockSaveProfileError


def helper_test_save_thermal_profile(lifecycle: Lifecycle):
    # project missing
    try:
        lifecycle.save_thermal_profile(
            SaveThermalProfileRequest(
                project="",
                phase_name="On The Road",
                event_name="ThermalCycle_A",
                file_path="C:/Temp/ThermalCycle_A.dat",
            )
        )
        pytest.fail("No exception raised when using a missing project parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, project is invalid because it is None or empty."
        )

    # phase_name missing
    try:
        lifecycle.save_thermal_profile(
            SaveThermalProfileRequest(
                project="Tutorial Project",
                phase_name="",
                event_name="ThermalCycle_A",
                file_path="C:/Temp/ThermalCycle_A.dat",
            )
        )
        pytest.fail("No exception raised when using a missing phase_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, phase_name is invalid because it is None or empty."
        )

    # event_name missing
    try:
        lifecycle.save_thermal_profile(
            SaveThermalProfileRequest(
                project="Tutorial Project",
                phase_name="On The Road",
                event_name="",
                file_path="C:/Temp/ThermalCycle_A.dat",
            )
        )
        pytest.fail("No exception raised when using a missing event_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, event_name is invalid because it is None or empty."
        )

    if lifecycle._is_connection_up():

        # invalid file_path
        try:
            lifecycle.save_thermal_profile(
                SaveThermalProfileRequest(
                    project="Tutorial Project",
                    phase_name="On The Road",
                    event_name="ThermalCycle_A",
                    file_path="C:/Temp/ThermalCycle_A.txt",
                )
            )
            pytest.fail("No exception raised when using an invalid file_path parameter")
        except Exception as e:
            assert type(e) == SherlockSaveProfileError


def helper_test_delete_event(lifecycle: Lifecycle, event_name: str, phase_name: str):
    # project missing
    try:
        lifecycle.delete_event(
            DeleteEventRequest(
                project="",
                phase_name="On The Road",
                event_name="ThermalCycle_A",
            )
        )
        pytest.fail("No exception raised when using a missing project parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, project is invalid because it is None or empty."
        )

    # phase_name missing
    try:
        lifecycle.delete_event(
            DeleteEventRequest(
                project="Tutorial Project",
                phase_name="",
                event_name="ThermalCycle_A",
            )
        )
        pytest.fail("No exception raised when using a missing phase_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, phase_name is invalid because it is None or empty."
        )

    # event_name missing
    try:
        lifecycle.delete_event(
            DeleteEventRequest(
                project="Tutorial Project",
                phase_name="On The Road",
                event_name="",
            )
        )
        pytest.fail("No exception raised when using a missing event_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, event_name is invalid because it is None or empty."
        )

    if lifecycle._is_connection_up():
        # valid request but false event_name
        try:
            lifecycle.delete_event(
                DeleteEventRequest(
                    project="Tutorial Project",
                    phase_name="On The Road",
                    event_name="NonExistingEvent",
                )
            )
            pytest.fail("No exception raised for server error response")
        except Exception as e:
            assert isinstance(e, SherlockDeleteError)

        # valid request with actual event
        response = lifecycle.delete_event(
            DeleteEventRequest(
                project="Tutorial Project",
                phase_name=phase_name,
                event_name=event_name,
            )
        )
        assert response.value == 0


def helper_test_delete_phase(lifecycle: Lifecycle, phase_name: str):
    # project missing
    try:
        lifecycle.delete_phase(
            DeletePhaseRequest(
                project="",
                phase_name="SomePhase",
            )
        )
        pytest.fail("No exception raised when using a missing project parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, project is invalid because it is None or empty."
        )

    # phase_name missing
    try:
        lifecycle.delete_phase(
            DeletePhaseRequest(
                project="Tutorial Project",
                phase_name="",
            )
        )
        pytest.fail("No exception raised when using a missing phase_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, phase_name is invalid because it is None or empty."
        )

    if lifecycle._is_connection_up():
        # valid request but false phase_name
        try:
            lifecycle.delete_phase(
                DeletePhaseRequest(
                    project="Tutorial Project",
                    phase_name="NonExistingPhase",
                )
            )
            pytest.fail("No exception raised for server error response")
        except Exception as e:
            assert isinstance(e, SherlockDeleteError)

        # valid request with actual phase
        response = lifecycle.delete_phase(
            DeletePhaseRequest(
                project="Tutorial Project",
                phase_name=phase_name,
            )
        )
        assert response.value == 0


def helper_test_update_life_phase(lifecycle: Lifecycle):

    project = "Tutorial Project"
    phase_name = "Environmental"
    new_phase_name = "Environment"
    new_num_of_cycles = 100
    new_cycle_type = "PER DAY"
    new_description = "new description"
    new_duration = 24
    new_duration_units = "hr"
    result_archive_file_name = "Tutorial Project Results 10_7_2025"

    # project missing
    try:
        lifecycle.update_life_phase(
            UpdateLifePhaseRequest(
                project="",
                phase_name=phase_name,
            )
        )
        pytest.fail("No exception raised when using a missing project parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, project is invalid because it is None or empty."
        )

    # phase_name missing
    try:
        lifecycle.update_life_phase(
            UpdateLifePhaseRequest(
                project=project,
                phase_name="",
            )
        )
        pytest.fail("No exception raised when using a missing phase_name parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, phase_name is invalid because it is None or empty."
        )

    if lifecycle._is_connection_up():
        # valid request but false project
        try:
            lifecycle.update_life_phase(
                UpdateLifePhaseRequest(
                    project="Bad Project",
                    phase_name=phase_name,
                )
            )
            pytest.fail("No exception raised for server error response")
        except Exception as e:
            assert isinstance(e, SherlockUpdateLifePhaseError)

        # valid request but false phase_name
        try:
            lifecycle.update_life_phase(
                UpdateLifePhaseRequest(
                    project=project,
                    phase_name="NonExistingPhase",
                )
            )
            pytest.fail("No exception raised for server error response")
        except Exception as e:
            assert isinstance(e, SherlockUpdateLifePhaseError)

        # test all optionals omitted, i.e., not set or default
        req = UpdateLifePhaseRequest(
            project=project,
            phase_name=phase_name,
        )
        grpc_obj = req._convert_to_grpc()
        assert grpc_obj.project == project
        assert grpc_obj.phaseName == phase_name
        assert not grpc_obj.newPhaseName
        assert not grpc_obj.newDescription
        assert not grpc_obj.newDuration
        assert not grpc_obj.newDurationUnits
        assert not grpc_obj.newNumOfCycles
        assert not grpc_obj.newCycleType
        assert not grpc_obj.resultArchiveFileName

        # test all optionals set
        req = UpdateLifePhaseRequest(
            project=project,
            phase_name=phase_name,
            new_phase_name=new_phase_name,
            new_num_of_cycles=new_num_of_cycles,
            new_cycle_type=new_cycle_type,
            new_description=new_description,
            new_duration=new_duration,
            new_duration_units=new_duration_units,
            result_archive_file_name=result_archive_file_name,
        )
        grpc_obj = req._convert_to_grpc()
        assert grpc_obj.newPhaseName == new_phase_name
        assert grpc_obj.newDescription == new_description
        assert grpc_obj.newDuration == new_duration
        assert grpc_obj.newDurationUnits == new_duration_units
        assert grpc_obj.newNumOfCycles == new_num_of_cycles
        assert grpc_obj.resultArchiveFileName == result_archive_file_name

        # test some optionals set
        req = UpdateLifePhaseRequest(
            project=project,
            phase_name=phase_name,
            new_phase_name=new_phase_name,
            new_duration_units=new_duration_units,
            # rest are omitted (None)
        )
        grpc_obj = req._convert_to_grpc()
        assert grpc_obj.newPhaseName == new_phase_name
        assert grpc_obj.newDurationUnits == new_duration_units
        assert not grpc_obj.newDescription
        assert not grpc_obj.newDuration
        assert not grpc_obj.newNumOfCycles
        assert not grpc_obj.newCycleType
        assert not grpc_obj.resultArchiveFileName

        # valid request but invalid number of cycles param
        try:
            lifecycle.update_life_phase(
                UpdateLifePhaseRequest(
                    project=project,
                    phase_name=phase_name,
                    new_num_of_cycles=-100,
                )
            )
            pytest.fail("No exception raised for server error response")
        except Exception as e:
            assert isinstance(e, SherlockUpdateLifePhaseError)

        # valid request but invalid duration param
        try:
            lifecycle.update_life_phase(
                UpdateLifePhaseRequest(
                    project=project,
                    phase_name=phase_name,
                    new_duration=-100,
                )
            )
            pytest.fail("No exception raised for server error response")
        except Exception as e:
            assert isinstance(e, SherlockUpdateLifePhaseError)

        # valid request but invalid duration units param
        try:
            lifecycle.update_life_phase(
                UpdateLifePhaseRequest(
                    project=project,
                    phase_name=phase_name,
                    new_duration_units="dy",
                )
            )
            pytest.fail("No exception raised for server error response")
        except Exception as e:
            assert isinstance(e, SherlockUpdateLifePhaseError)

        # valid request but invalid cycle type
        try:
            lifecycle.update_life_phase(
                UpdateLifePhaseRequest(
                    project=project,
                    phase_name=phase_name,
                    new_cycle_type="PER DY",
                )
            )
            pytest.fail("No exception raised for server error response")
        except Exception as e:
            assert isinstance(e, SherlockUpdateLifePhaseError)
            assert (
                e.message
                == "Invalid cycle type. Valid options are: COUNT, DUTY CYCLE, PER YEAR, PER DAY, "
                "PER HOUR, PER MIN, PER SEC"
            )

        # valid request but new phase name already exists
        try:
            lifecycle.update_life_phase(
                UpdateLifePhaseRequest(
                    project=project,
                    phase_name=phase_name,
                    new_phase_name="On The Road",
                )
            )
            pytest.fail("No exception raised for server error response")
        except Exception as e:
            assert isinstance(e, SherlockUpdateLifePhaseError)
            assert (
                e.message
                == "The life phase 'On The Road' already exists for the project's life cycle."
            )

        # valid request with all optional params.
        response = lifecycle.update_life_phase(
            UpdateLifePhaseRequest(
                project=project,
                phase_name=phase_name,
                new_phase_name=new_phase_name,
                new_num_of_cycles=new_num_of_cycles,
                new_cycle_type=new_cycle_type,
                new_description=new_description,
                new_duration=new_duration,
                new_duration_units=new_duration_units,
                result_archive_file_name=result_archive_file_name,
            )
        )
        assert response.value == 0

        # valid request with some optional params.
        response = lifecycle.update_life_phase(
            UpdateLifePhaseRequest(
                project=project,
                phase_name=new_phase_name,
                new_phase_name=phase_name,
                new_num_of_cycles=new_num_of_cycles,
                result_archive_file_name=result_archive_file_name,
            )
        )
        assert response.value == 0


def helper_test_save_life_cycle(lifecycle: Lifecycle):

    project = "Tutorial Project"
    file_path = "C:/Temp/LifeCycle_Backup.dfr-lc"
    overwrite_file = True

    # project missing
    try:
        lifecycle.save_life_cycle(
            SaveLifeCycleRequest(project="", file_path=file_path, overwrite_file=overwrite_file)
        )
        pytest.fail("No exception raised when using a missing project parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, project is invalid because it is None or empty."
        )

    # file path missing
    try:
        lifecycle.save_life_cycle(
            SaveLifeCycleRequest(project=project, file_path="", overwrite_file=overwrite_file)
        )
        pytest.fail("No exception raised when using a missing file path parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert str(e.errors()[0]["msg"]) == (
            "Value error, file_path is invalid because it is None or empty."
        )

    if lifecycle._is_connection_up():
        # valid request but false project
        try:
            lifecycle.save_life_cycle(
                SaveLifeCycleRequest(
                    project="bad project", file_path=file_path, overwrite_file=overwrite_file
                )
            )
            pytest.fail("No exception raised for server error response")
        except Exception as e:
            assert isinstance(e, SherlockSaveLifeCycleError)

        # valid request but file path does not exist
        try:
            lifecycle.save_life_cycle(
                SaveLifeCycleRequest(
                    project=project,
                    file_path="C:/Tp/LifeCycle_Backup.dfr-lc",
                    overwrite_file=overwrite_file,
                )
            )
            pytest.fail("No exception raised for server error response")
        except Exception as e:
            assert isinstance(e, SherlockSaveLifeCycleError)

        # test all variables set
        req = SaveLifeCycleRequest(
            project=project, file_path=file_path, overwrite_file=overwrite_file
        )
        grpc_obj = req._convert_to_grpc()
        assert grpc_obj.project == project
        assert grpc_obj.filePath == file_path
        assert grpc_obj.overwriteFile == overwrite_file

        # valid request and file is overwritten
        response = lifecycle.save_life_cycle(
            SaveLifeCycleRequest(
                project=project, file_path=file_path, overwrite_file=overwrite_file
            )
        )
        assert response.value == 0

        # valid request and file is not overwritten
        try:
            lifecycle.save_life_cycle(
                SaveLifeCycleRequest(project=project, file_path=file_path, overwrite_file=False)
            )
            pytest.fail("No exception raised for server error response")
        except Exception as e:
            assert isinstance(e, SherlockSaveLifeCycleError)
            assert (
                e.message == "The existing life cycle file " + file_path + " cannot be overwritten."
            )


if __name__ == "__main__":
    test_all()
