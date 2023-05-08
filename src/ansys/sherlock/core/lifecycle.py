# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

"""Module containing all lifecycle management capabilities."""

try:
    import SherlockLifeCycleService_pb2
    import SherlockLifeCycleService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockLifeCycleService_pb2
    from ansys.api.sherlock.v0 import SherlockLifeCycleService_pb2_grpc

from ansys.sherlock.core import LOG
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
    SherlockInvalidHarmonicProfileEntriesError,
    SherlockInvalidLoadDirectionError,
    SherlockInvalidOrientationError,
    SherlockInvalidRandomVibeProfileEntriesError,
    SherlockInvalidShockProfileEntriesError,
    SherlockInvalidThermalProfileEntriesError,
    SherlockLoadHarmonicProfileError,
    SherlockLoadRandomVibeProfileError,
    SherlockLoadThermalProfileError,
    SherlockLoadRandomVibeProfileError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub


class Lifecycle(GrpcStub):
    """Contains all lifecycle management capabilities."""

    def __init__(self, channel):
        """Initialize a gRPC stub for the Sherlock LifeCycle service."""
        self.channel = channel
        self.stub = SherlockLifeCycleService_pb2_grpc.SherlockLifeCycleServiceStub(channel)
        self.TIME_UNIT_LIST = None
        self.CYCLE_TYPE_LIST = None
        self.RV_PROFILE_TYPE_LIST = None
        self.HARMONIC_PROFILE_TYPE_LIST = None
        self.FREQ_UNIT_LIST = None
        self.AMPL_UNIT_LIST = None
        self.CYCLE_STATE_LIST = None
        self.TEMP_UNIT_LIST = None
        self.LOAD_UNIT_LIST = None
        self.SHOCK_SHAPE_LIST = None
        self.STEP_TYPE_LIST = ["RAMP", "HOLD"]

    def _init_time_units(self):
        """Initialize the list for time units."""
        if self._is_connection_up():
            duration_unit_request = SherlockLifeCycleService_pb2.ListDurationUnitsRequest()
            duration_unit_response = self.stub.listDurationUnits(duration_unit_request)
            if duration_unit_response.returnCode.value == 0:
                self.TIME_UNIT_LIST = duration_unit_response.durationUnits

    def _init_cycle_types(self):
        """Initialize the list for cycle types."""
        if self._is_connection_up():
            cycle_type_request = SherlockLifeCycleService_pb2.ListLCTypesRequest()
            cycle_type_response = self.stub.listLifeCycleTypes(cycle_type_request)
            if cycle_type_response.returnCode.value == 0:
                self.CYCLE_TYPE_LIST = cycle_type_response.types

    def _init_rv_profile_types(self):
        """Initialize the list for RV profile types."""
        if self._is_connection_up():
            rv_profile_request = SherlockLifeCycleService_pb2.ListRandomVibeProfileTypesRequest()
            rv_profile_response = self.stub.listRandomVibeProfileTypes(rv_profile_request)
            if rv_profile_response.returnCode.value == 0:
                self.RV_PROFILE_TYPE_LIST = rv_profile_response.types

    def _init_harmonic_profile_types(self):
        """Initialize the list for harmonic profile types."""
        if self._is_connection_up():
            harmonic_profile_request = (
                SherlockLifeCycleService_pb2.ListHarmonicProfileTypesRequest()
            )
            harmonic_profile_response = self.stub.listHarmonicProfileTypes(harmonic_profile_request)
            if harmonic_profile_response.returnCode.value == 0:
                self.HARMONIC_PROFILE_TYPE_LIST = harmonic_profile_response.types

    def _init_freq_units(self):
        """Initialize the list for frequency units."""
        if self._is_connection_up():
            freq_unit_request = SherlockLifeCycleService_pb2.ListFreqUnitsRequest()
            freq_type_response = self.stub.listFreqUnits(freq_unit_request)
            if freq_type_response.returnCode.value == 0:
                self.FREQ_UNIT_LIST = freq_type_response.freqUnits

    def _init_ampl_units(self):
        """Initialize the list for amplitude units."""
        if self._is_connection_up():
            ampl_unit_request = SherlockLifeCycleService_pb2.ListAmplUnitsRequest()
            ampl_type_response = self.stub.listAmplUnits(ampl_unit_request)
            if ampl_type_response.returnCode.value == 0:
                self.AMPL_UNIT_LIST = ampl_type_response.amplUnits

    def _init_cycle_states(self):
        """Initialize the list for cycle states."""
        if self._is_connection_up():
            cycle_state_request = SherlockLifeCycleService_pb2.ListLCStatesRequest()
            cycle_state_response = self.stub.listLifeCycleStates(cycle_state_request)
            if cycle_state_response.returnCode.value == 0:
                self.CYCLE_STATE_LIST = cycle_state_response.states

    def _init_temp_units(self):
        """Initialize the list for temperature units."""
        if self._is_connection_up():
            temp_unit_request = SherlockLifeCycleService_pb2.ListTempUnitsRequest()
            temp_unit_response = self.stub.listTempUnits(temp_unit_request)
            if temp_unit_response.returnCode.value == 0:
                self.TEMP_UNIT_LIST = temp_unit_response.tempUnits

    def _init_load_units(self):
        """Initialize the list for load units."""
        if self._is_connection_up():
            load_unit_request = SherlockLifeCycleService_pb2.ListShockLoadUnitsRequest()
            load_unit_response = self.stub.listShockLoadUnits(load_unit_request)
            if load_unit_response.returnCode.value == 0:
                self.LOAD_UNIT_LIST = load_unit_response.units

    def _init_shock_shapes(self):
        """Initialize the list for shock shapes."""
        if self._is_connection_up():
            shock_shape_request = SherlockLifeCycleService_pb2.ListShockPulsesRequest()
            shock_shape_response = self.stub.listShockPulses(shock_shape_request)
            if shock_shape_response.returnCode.value == 0:
                self.SHOCK_SHAPE_LIST = shock_shape_response.shockPulse

    def _check_load_direction_validity(self, input):
        """Check that the input string is a valid load."""
        directions = input.split(",")

        if len(directions) != 3:
            raise SherlockInvalidLoadDirectionError("Number of direction coordinates is invalid.")

        try:
            nonzero = 0
            for dir in directions:
                if float(dir) != 0:
                    nonzero += 1

            if nonzero == 0:
                raise SherlockInvalidLoadDirectionError(
                    "At least one direction coordinate must be non-zero."
                )
            return
        except TypeError:
            raise SherlockInvalidLoadDirectionError("Direction coordinates are invalid.")

    def _check_orientation_validity(self, input):
        """Check input string if it is a valid orientation."""
        orientation = input.split(",")

        if len(orientation) != 2:
            raise SherlockInvalidOrientationError("Number of spherical coordinates is invalid.")

        try:
            float(orientation[0])
        except:
            raise SherlockInvalidOrientationError("Azimuth value is invalid.")

        try:
            float(orientation[1])
            return
        except:
            raise SherlockInvalidOrientationError("Elevation value is invalid.")

    def _check_random_vibe_profile_entries_validity(self, input):
        """Check input array to see if all elements are valid for random vibe entries."""
        if not isinstance(input, list):
            raise SherlockInvalidRandomVibeProfileEntriesError("Entries argument is invalid.")

        try:
            for i, entry in enumerate(input):
                if len(entry) != 2:
                    raise SherlockInvalidRandomVibeProfileEntriesError(
                        f"Invalid entry {i}: Number of arguments is wrong"
                    )
                if entry[0] <= 0:
                    raise SherlockInvalidRandomVibeProfileEntriesError(
                        f"Invalid entry {i}: Frequencies must be greater than 0"
                    )
                if entry[1] <= 0:
                    raise SherlockInvalidRandomVibeProfileEntriesError(
                        f"Invalid entry {i}: Amplitudes must be greater than 0"
                    )
        except TypeError:
            raise SherlockInvalidRandomVibeProfileEntriesError(
                f"Invalid entry {i}: Frequency or amplitude is invalid"
            )

    def _check_thermal_profile_entries_validity(self, input):
        """Check input array to see if all elements are valid for thermal entries."""
        if not isinstance(input, list):
            raise SherlockAddThermalProfilesError("Entries argument is invalid.")

        try:
            for i, entry in enumerate(input):
                if len(entry) != 4:
                    raise SherlockInvalidThermalProfileEntriesError(
                        f"Invalid entry {i}: Number of arguments is wrong"
                    )
                if not isinstance(entry[0], str):
                    raise SherlockInvalidThermalProfileEntriesError(
                        f"Invalid entry {i}: Step name is invalid"
                    )
                if entry[1] not in self.STEP_TYPE_LIST:
                    raise SherlockInvalidThermalProfileEntriesError(
                        f"Invalid entry {i}: Step type is invalid"
                    )
                if entry[2] <= 0:
                    raise SherlockInvalidThermalProfileEntriesError(
                        f"Invalid entry {i}: Time must be greater than 0"
                    )
                if not isinstance(entry[3], (int, float)):
                    raise SherlockInvalidThermalProfileEntriesError(
                        f"Invalid entry {i}: Temperature is invalid"
                    )
        except TypeError:
            raise SherlockInvalidThermalProfileEntriesError(f"Invalid entry {i}: Time is invalid")

    def _check_harmonic_profile_entries_validity(self, input):
        """Check input array if all elements are valid for harmonic entries."""
        if not isinstance(input, list):
            raise SherlockInvalidHarmonicProfileEntriesError(message="Entries argument is invalid.")

        try:
            for i, entry in enumerate(input):
                if len(entry) != 2:
                    raise SherlockInvalidHarmonicProfileEntriesError(
                        message=f"Invalid entry {i}: Number of arguments is wrong"
                    )
                if entry[0] <= 0:
                    raise SherlockInvalidHarmonicProfileEntriesError(
                        message=f"Invalid entry {i}: Frequencies must be greater than 0"
                    )
                if entry[1] <= 0:
                    raise SherlockInvalidHarmonicProfileEntriesError(
                        message=f"Invalid entry {i}: Load must be greater than 0"
                    )
            return
        except TypeError:
            raise SherlockInvalidHarmonicProfileEntriesError(
                message=f"Invalid entry {i}: Frequency or load is invalid"
            )

    def _check_shock_profile_entries_validity(self, input):
        """Check input array to see if all elements are valid for shock entries."""
        if not isinstance(input, list):
            raise SherlockInvalidShockProfileEntriesError(message="Entries argument is invalid.")

        try:
            for i, entry in enumerate(input):
                if len(entry) != 4:
                    raise SherlockInvalidShockProfileEntriesError(
                        message=f"Invalid entry {i}: Number of arguments is wrong"
                    )
                if not isinstance(entry[0], str):
                    raise SherlockInvalidShockProfileEntriesError(
                        message=f"Invalid entry {i}: Shape name is invalid"
                    )
                if (self.SHOCK_SHAPE_LIST is not None) and (entry[0] not in self.SHOCK_SHAPE_LIST):
                    raise SherlockInvalidShockProfileEntriesError(
                        message=f"Invalid entry {i}: Shape type is invalid"
                    )
                if entry[1] <= 0:
                    raise SherlockInvalidShockProfileEntriesError(
                        message=f"Invalid entry {i}: Load must be greater than 0"
                    )
                if entry[2] <= 0:
                    raise SherlockInvalidShockProfileEntriesError(
                        message=f"Invalid entry {i}: Frequency must be greater than 0"
                    )
                if entry[3] < 0:
                    raise SherlockInvalidShockProfileEntriesError(
                        message=f"Invalid entry {i}: Decay must be non-negative"
                    )
            return
        except TypeError:
            raise SherlockInvalidShockProfileEntriesError(
                message=f"Invalid entry {i}: Load, frequency, or decay is invalid"
            )

    def _add_random_vibe_profile_entries(self, request, entries):
        """Add the random vibe entries to the request."""
        for e in entries:
            entry = request.randomVibeProfileEntries.add()
            entry.freq = e[0]
            entry.ampl = e[1]

    def _add_thermal_profile_entries(self, request, entries):
        """Add the thermal entries to the request."""
        for e in entries:
            entry = request.thermalProfileEntries.add()
            entry.step = e[0]
            entry.type = e[1]
            entry.time = e[2]
            entry.temp = e[3]

    def _add_harmonic_profile_entries(self, request, entries):
        """Add the entries to the harmonic profile request."""
        for e in entries:
            entry = request.harmonicProfileEntries.add()
            entry.freq = e[0]
            entry.load = e[1]

    def _add_shock_profile_entries(self, request, entries):
        """Add the shock entries to the request."""
        for e in entries:
            entry = request.shockProfileEntries.add()
            entry.shape = e[0]
            entry.load = e[1]
            entry.freq = e[2]
            entry.decay = e[3]

    def create_life_phase(
        self,
        project,
        phase_name,
        duration,
        duration_units,
        num_of_cycles,
        cycle_type,
        description=None,
    ):
        """Add and define a life phase.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        phase_name : str
            Name of the new life phase.
        duration : double
            Event duration length.
        duration_units : str
            Units for the event duration length. Options include ``"ms"``,
            ``"sec"``, and ``"min"``.
        num_of_cycles : double
            Number of cycles for the new life phase.
        cycle_type : str
            Cycle type. Options include ``"COUNT"``, ``"DUTY CYCLE"``,
            ``"PER YEAR"``, and ``"PER HOUR"``.
        description : str, optional
            Description of the new life phase.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
        )
        >>> sherlock.lifecycle.create_life_phase(
            "Test",
            "Example",
            1.5,
            "sec",
            4.0,
            "COUNT",
        )
        """
        if self.TIME_UNIT_LIST is None:
            self._init_time_units()
        if self.CYCLE_TYPE_LIST is None:
            self._init_cycle_types()

        try:
            if project == "":
                raise SherlockCreateLifePhaseError(message="Project name is invalid.")
            if phase_name == "":
                raise SherlockCreateLifePhaseError(message="Phase name is invalid.")
            if (self.TIME_UNIT_LIST is not None) and (duration_units not in self.TIME_UNIT_LIST):
                raise SherlockCreateLifePhaseError(message="Duration unit is invalid.")
            if duration <= 0.0:
                raise SherlockCreateLifePhaseError(message="Duration must be greater than 0.")
            if (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockCreateLifePhaseError(message="Cycle type is invalid.")
            if num_of_cycles <= 0.0:
                raise SherlockCreateLifePhaseError(
                    message="Number of cycles must be greater than 0."
                )
        except SherlockCreateLifePhaseError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        if description is None:
            description = ""

        request = SherlockLifeCycleService_pb2.CreateLifePhaseRequest(
            project=project,
            phaseName=phase_name,
            description=description,
            duration=duration,
            durationUnits=duration_units,
            numOfCycles=num_of_cycles,
            cycleType=cycle_type,
        )

        response = self.stub.createLifePhase(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockCreateLifePhaseError(error_array=response.errors)

                raise SherlockCreateLifePhaseError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockCreateLifePhaseError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def add_random_vibe_event(
        self,
        project,
        phase_name,
        event_name,
        duration,
        duration_units,
        num_of_cycles,
        cycle_type,
        orientation,
        profile_type,
        load_direction,
        description="",
    ):
        """Add a random vibe life cycle event.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        phase_name : str
            Bame of the life cycle phase to add this event to.
        event_name : str
            Name of the random vibe event.
        duration : double
            Event duration length.
        duration_units : str
            Event duration units. Options are ``"ms"``, ``"sec"``, ``"min"``,
            ``"hr"``, ``"day"``, and ``"year"``.
        num_of_cycles : double
            Number of cycles for this random vibe event.
        cycle_type : str
            Cycle type. Options are ``"COUNT"``, ``"DUTY_CYCLE"``, ``"PER_YEAR"``,
            ``"PER_DAY"``, ``"PER_HOUR"``, ``"PER_MIN"``, and ``"PER_SEC"``.
        orientation : str
            PCB orientation in the format of azimuth, elevation. For example, ``30,15``.
        profile_type : str
            Random load profile type. Options are ``"Uniaxial"``.
        load_direction : str
            Load direction in the format of ``x,y,z``. For example, ``0,0,1``.
        description : str, optional
            Description of the random vibe event.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
        )
        >>> sherlock.lifecycle.create_life_phase(
            "Test",
            "Example",
            1.5,
            "sec",
            4.0,
            "COUNT",
        )
        >>> sherlock.lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            "45,45",
            "Uniaxial",
            "2,4,5",
        )
        """
        if self.TIME_UNIT_LIST is None:
            self._init_time_units()
        if self.CYCLE_TYPE_LIST is None:
            self._init_cycle_types()
        if self.RV_PROFILE_TYPE_LIST is None:
            self._init_rv_profile_types()

        try:
            if project == "":
                raise SherlockAddRandomVibeEventError(message="Project name is invalid.")
            if phase_name == "":
                raise SherlockAddRandomVibeEventError(message="Phase name is invalid.")
            if event_name == "":
                raise SherlockAddRandomVibeEventError(message="Event name is invalid.")
            if (self.TIME_UNIT_LIST is not None) and (duration_units not in self.TIME_UNIT_LIST):
                raise SherlockAddRandomVibeEventError(message="Duration unit is invalid.")
            if duration <= 0.0:
                raise SherlockAddRandomVibeEventError(message="Duration must be greater than 0.")
            if (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockAddRandomVibeEventError(message="Cycle type is invalid.")
            if num_of_cycles <= 0.0:
                raise SherlockAddRandomVibeEventError(
                    message="Number of cycles must be greater than 0."
                )
        except SherlockAddRandomVibeEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        try:
            self._check_load_direction_validity(load_direction)
            if (self.RV_PROFILE_TYPE_LIST is not None) and (
                profile_type not in self.RV_PROFILE_TYPE_LIST
            ):
                raise SherlockAddRandomVibeEventError(
                    message="Profile type for a random event can only be Uniaxial."
                )
            self._check_orientation_validity(orientation)
        except (SherlockInvalidLoadDirectionError, SherlockInvalidOrientationError) as e:
            LOG.error(f"Add random vibe event error: {str(e)}")
            raise SherlockAddRandomVibeEventError(message=str(e))
        except SherlockAddRandomVibeEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        request = SherlockLifeCycleService_pb2.AddRandomVibeEventRequest(
            project=project,
            phaseName=phase_name,
            eventName=event_name,
            description=description,
            duration=duration,
            durationUnits=duration_units,
            numOfCycles=num_of_cycles,
            cycleType=cycle_type,
            orientation=orientation,
            profileType=profile_type,
            loadDirection=load_direction,
        )

        response = self.stub.addRandomVibeEvent(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddRandomVibeEventError(error_array=response.errors)

                raise SherlockAddRandomVibeEventError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddRandomVibeEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def add_random_vibe_profiles(
        self,
        project,
        random_vibe_profiles,
    ):
        """Add new random vibe lifecycle event profiles.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        random_vibe_profiles : list of (phase_name, event_name, profile_name, freq_units, \
            ampl_units, random_vibe_entries) profiles
            phase_name : str
                Name of the lifecycle phase to associate this profile to.
            event_name : str
                Name of the random vibe event for the profile.
            profile_name : str
                Name of the random vibe profile.
            freq_units : str
                Frequency units. Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            ampl_units : str
                Amplitude units. Options are ``"G2/Hz"``, ``"m2/s4/Hz"``, ``"mm2/s4/Hz"``, \
                ``"in2/s4/Hz"``, and ``"ft2/s4/Hz"``.
            random_vibe_profile_entries : list of (frequency, amplitude) entries
                frequency : double
                    Frequency of the profile entry expressed in frequency units.
                amplitude : double
                    Amplitude of the profile entry expressed in amplitude units.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
        )
        >>> sherlock.lifecycle.create_life_phase(
            "Test",
            "Example",
            1.5,
            "sec",
            4.0,
            "COUNT",
        )
        >>> sherlock.lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            "45,45",
            "Uniaxial",
            "2,4,5",
        )
        >>> sherlock.lifecycle.add_random_vibe_profiles(
            "Test",
             [(
                "Example",
                "Event1",
                "Profile1",
                "HZ",
                "G2/Hz",
                [(4,8), (5, 50)],
            )]
        )
        """
        if self.FREQ_UNIT_LIST is None:
            self._init_freq_units()
        if self.AMPL_UNIT_LIST is None:
            self._init_ampl_units()

        try:
            if project == "":
                raise SherlockAddRandomVibeProfilesError(message="Project name is invalid.")

            if len(random_vibe_profiles) == 0:
                raise SherlockAddRandomVibeProfilesError(
                    message="Random vibe profiles are " f"missing."
                )

            for i, profile_entry in enumerate(random_vibe_profiles):
                if len(profile_entry) != 6:
                    raise SherlockAddRandomVibeProfilesError(
                        f"Number of arguments ({str(len(profile_entry))}) is wrong for "
                        f"random vibe profile {i}."
                    )
                elif not isinstance(profile_entry[0], str) or profile_entry[0] == "":
                    raise SherlockAddRandomVibeProfilesError(
                        f"Phase name is invalid for random vibe profile {i}."
                    )
                elif not isinstance(profile_entry[1], str) or profile_entry[1] == "":
                    raise SherlockAddRandomVibeProfilesError(
                        f"Event name is invalid for random vibe profile {i}."
                    )
                elif not isinstance(profile_entry[2], str) or profile_entry[2] == "":
                    raise SherlockAddRandomVibeProfilesError(
                        f"Profile name is invalid for random vibe profile {i}."
                    )
                elif not isinstance(profile_entry[3], str) or (
                    (self.FREQ_UNIT_LIST is not None)
                    and (profile_entry[3] not in self.FREQ_UNIT_LIST)
                ):
                    raise SherlockAddRandomVibeProfilesError(
                        f"Frequency units {profile_entry[3]} are invalid for random vibe "
                        f"profile {i}."
                    )
                elif not isinstance(profile_entry[4], str) or (
                    (self.AMPL_UNIT_LIST is not None)
                    and (profile_entry[4] not in self.AMPL_UNIT_LIST)
                ):
                    raise SherlockAddRandomVibeProfilesError(
                        f"Amplitude type {profile_entry[4]} is invalid for random vibe profile {i}."
                    )

                try:
                    self._check_random_vibe_profile_entries_validity(profile_entry[5])
                except SherlockInvalidRandomVibeProfileEntriesError as e:
                    raise SherlockAddRandomVibeProfilesError(
                        f"{str(e)} for random vibe profile {i}."
                    )

        except SherlockAddRandomVibeProfilesError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        request = SherlockLifeCycleService_pb2.AddRandomVibeProfilesRequest(project=project)

        """Add the random vibe profiles to the request."""
        for r in random_vibe_profiles:
            profile = request.randomVibeProfiles.add()
            profile.phaseName = r[0]
            profile.eventName = r[1]
            profile.profileName = r[2]
            profile.freqUnits = r[3]
            profile.amplUnits = r[4]

            """Add the random vibe entries to the request."""
            for e in r[5]:
                entry = profile.randomVibeProfileEntries.add()
                entry.freq = e[0]
                entry.ampl = e[1]

        response = self.stub.addRandomVibeProfiles(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddRandomVibeProfilesError(error_array=response.errors)
                else:
                    raise SherlockAddRandomVibeProfilesError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddRandomVibeProfilesError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def add_thermal_event(
        self,
        project,
        phase_name,
        event_name,
        num_of_cycles,
        cycle_type,
        cycle_state,
        description="",
    ):
        """Add a thermal event to a life cycle.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        phase_name : str
            Name of the lifecycle phase to add this event to.
        event_name : str
            Name of the thermal event.
        num_of_cycles : double
            Number of cycles for this thermal event.
        cycle_type : str
            Cycle type. Options are ``"COUNT"``, ``"DUTY_CYCLE"``, ``"PER_YEAR"``,
            ``"PER_DAY"``, ``"PER_HOUR"``, ``"PER_MIN"``, and ``"PER_SEC"``.
        cycle_state : str
            Lifecycle state. Options are ``"OPERATING"`` and ``"STORAGE"``.
        description : str, optional
            Description of the new thermal event.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
        )
        >>> sherlock.lifecycle.create_life_phase(
            "Test",
            "Example",
            1.5,
            "year",
            4.0,
            "COUNT",
        )
        >>> sherlock.lifecycle.add_thermal_event(
            "Test",
            "Example",
            "Event1",
            4.0,
            "PER YEAR",
            "STORAGE",
        )
        """
        if self.CYCLE_TYPE_LIST is None:
            self._init_cycle_types()
        if self.CYCLE_STATE_LIST is None:
            self._init_cycle_states()

        try:
            if project == "":
                raise SherlockAddThermalEventError(message="Project name is invalid.")
            if phase_name == "":
                raise SherlockAddThermalEventError(message="Phase name is invalid.")
            if event_name == "":
                raise SherlockAddThermalEventError(message="Event name is invalid.")
            if (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockAddThermalEventError(message="Ccycle type is invalid.")
            if num_of_cycles <= 0.0:
                raise SherlockAddThermalEventError(
                    message="Number of cycles must be greater than 0."
                )
            if (self.CYCLE_STATE_LIST is not None) and (cycle_state not in self.CYCLE_STATE_LIST):
                raise SherlockAddThermalEventError(message="Cycle state is invalid.")
        except SherlockAddThermalEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        request = SherlockLifeCycleService_pb2.AddThermalEventRequest(
            project=project,
            phaseName=phase_name,
            eventName=event_name,
            description=description,
            numOfCycles=num_of_cycles,
            cycleType=cycle_type,
            cycleState=cycle_state,
        )

        response = self.stub.addThermalEvent(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddThermalEventError(error_array=response.errors)

                raise SherlockAddThermalEventError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddThermalEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def add_thermal_profiles(
        self,
        project,
        thermal_profiles,
    ):
        """Add thermal life cycle event profiles.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        thermal_profiles : list of (phase_name, event_name, profile_name, time_units, temp_units, \
                thermal_profile_entries) profiles
            phase_name : str
                Bame of the lifecycle phase this profile is associated with.
            event_name : str
                Name of the thermal event for the profile.
            profile_name : str
                Name of the thermal profile.
            time_units : str
                Time units. Options are ``"ms"``, ``"sec"``, ``"min"``, ``"hr"``,
                ``"day"``, and ``"year"``.
            temp_units : str
                Temperature units. Options are ``"C"``, ``"F"``, and ``"K"``.
            thermal_profile_entries : list of (step, type, time, temp) entries
                step : str
                    Name of the profile step entry.
                type : str
                    Thermal step type. Options are ``"HOLD"`` and ``"RAMP"``.
                time : double
                    Duration of the step entry expressed in time units
                temperature : double
                    Temperature of the step entry expressed in temperature units.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
        )
        >>> sherlock.lifecycle.create_life_phase(
            "Test",
            "Example",
            1.5,
            "year",
            4.0,
            "COUNT",
        )
        >>> sherlock.lifecycle.add_thermal_event(
            "Test",
            "Example",
            "Event1",
            4.0,
            "PER YEAR",
            "STORAGE",
        )
        >>> sherlock.lifecycle.add_thermal_profiles(
            "Test",
            [(
                "Example",
                "Event1",
                "Profile1",
                "sec",
                "F",
                [
                    ("Steady1", "HOLD", 40, 40),
                    ("Steady", "HOLD", 20, 20),
                    ("Back", "RAMP", 20, 40),
                ],
            )]
        )
        """
        if self.TIME_UNIT_LIST is None:
            self._init_time_units()
        if self.TEMP_UNIT_LIST is None:
            self._init_temp_units()

        try:
            if project == "":
                raise SherlockAddThermalProfilesError(message="Project name is invalid.")

            if len(thermal_profiles) == 0:
                raise SherlockAddThermalProfilesError(message="Thermal profiles are missing.")

            for i, profile_entry in enumerate(thermal_profiles):
                if len(profile_entry) != 6:
                    raise SherlockAddThermalProfilesError(
                        f"Number of arguments ({str(len(profile_entry))}) is wrong for "
                        f"thermal profile {i}."
                    )
                elif not isinstance(profile_entry[0], str) or profile_entry[0] == "":
                    raise SherlockAddThermalProfilesError(
                        f"Phase name is invalid for thermal profile {i}."
                    )
                elif not isinstance(profile_entry[1], str) or profile_entry[1] == "":
                    raise SherlockAddThermalProfilesError(
                        f"Event name is invalid for thermal profile {i}."
                    )
                elif not isinstance(profile_entry[2], str) or profile_entry[2] == "":
                    raise SherlockAddThermalProfilesError(
                        f"Profile name is invalid for thermal profile {i}."
                    )
                elif not isinstance(profile_entry[3], str) or (
                    (self.TIME_UNIT_LIST is not None)
                    and (profile_entry[3] not in self.TIME_UNIT_LIST)
                ):
                    raise SherlockAddThermalProfilesError(
                        f"Time units {profile_entry[3]} are invalid for thermal profile {i}."
                    )
                elif not isinstance(profile_entry[4], str) or (
                    (self.TEMP_UNIT_LIST is not None)
                    and (profile_entry[4] not in self.TEMP_UNIT_LIST)
                ):
                    raise SherlockAddThermalProfilesError(
                        f"Temperature units {profile_entry[4]} are invalid for thermal profile {i}."
                    )

                try:
                    self._check_thermal_profile_entries_validity(profile_entry[5])

                except (
                    SherlockAddThermalProfilesError,
                    SherlockInvalidThermalProfileEntriesError,
                ) as e:
                    raise SherlockAddThermalProfilesError(f"{str(e)} for thermal profile {i}.")

        except SherlockAddThermalProfilesError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        request = SherlockLifeCycleService_pb2.AddThermalProfilesRequest(project=project)

        """Add the thermal profiles to the request."""
        for t in thermal_profiles:
            profile = request.thermalProfiles.add()
            profile.phaseName = t[0]
            profile.eventName = t[1]
            profile.profileName = t[2]
            profile.timeUnits = t[3]
            profile.tempUnits = t[4]

            """Add the thermal profile entries to the request."""
            for e in t[5]:
                entry = profile.thermalProfileEntries.add()
                entry.step = e[0]
                entry.type = e[1]
                entry.time = e[2]
                entry.temp = e[3]

        response = self.stub.addThermalProfiles(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddThermalProfilesError(error_array=response.errors)
                else:
                    raise SherlockAddThermalProfilesError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddThermalProfilesError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def add_harmonic_event(
        self,
        project,
        phase_name,
        event_name,
        duration,
        duration_units,
        num_of_cycles,
        cycle_type,
        sweep_rate,
        orientation,
        profile_type,
        load_direction,
        description="",
    ):
        """Add a harmonic vibe life cycle event.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        phase_name : str
            Bame of the lifecycle phase to add this event to.
        event_name : str
            Name of the harmonic event.
        duration : double
            Event duration length.
        duration_units : str
            Event duration units. Options are ``"ms"``, ``"sec"``, ``"min"``,
            ``"hr"``, ``"day"``, and ``"year"``.
        num_of_cycles : double
            Number of cycles for this harmonic vibe event.
        cycle_type : str
            Cycle type. Options are ``"COUNT"``, ``"DUTY_CYCLE"``, ``"PER_YEAR"``,
            ``"PER_DAY"``, ``"PER_HOUR"``, ``"PER_MIN"``, and ``"PER_SEC"``.
        sweep_rate : double
            Sweep rate for the harmonic event.
        orientation : str
            PCB orientation in the format of ``azimuth, elevation``. For example, ``30,15``.
        profile_type : str
            Harmonic load profile types. Options are ``"Uniaxial"`` and ``"Triaxial"``.
        load_direction: str
            Load direction in the format of ``x,y,z``. For example, ``0,0,1``.
        description : str, optional
            Description of the harmonic vibe event.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test"
        )
        >>> sherlock.lifecycle.create_life_phase(
            "Test",
            "Example",
            1.5,
            "year",
            4.0,
            "COUNT",
        )
        >>> sherlock.lifecycle.add_harmonic_event(
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
            "2,4,5",
        )
        """
        if self.TIME_UNIT_LIST is None:
            self._init_time_units()
        if self.CYCLE_TYPE_LIST is None:
            self._init_cycle_types()
        if self.HARMONIC_PROFILE_TYPE_LIST is None:
            self._init_harmonic_profile_types()

        try:
            if project == "":
                raise SherlockAddHarmonicEventError(message="Project name is invalid.")
            if phase_name == "":
                raise SherlockAddHarmonicEventError(message="Phase name is invalid.")
            if event_name == "":
                raise SherlockAddHarmonicEventError(message="Event name is invalid.")
            if (self.TIME_UNIT_LIST is not None) and (duration_units not in self.TIME_UNIT_LIST):
                raise SherlockAddHarmonicEventError(message="Duration units are invalid.")
            if duration <= 0.0:
                raise SherlockAddHarmonicEventError(message="Duration must be greater than 0.")
            if (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockAddHarmonicEventError(message="Cycle type is invalid.")
            if num_of_cycles <= 0.0:
                raise SherlockAddHarmonicEventError(
                    message="Number of cycles must be greater than 0."
                )
            if sweep_rate <= 0.0:
                raise SherlockAddHarmonicEventError(message="Sweep rate must be greater than 0.")
        except SherlockAddHarmonicEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        try:
            self._check_load_direction_validity(load_direction)
            self._check_orientation_validity(orientation)
            if (self.HARMONIC_PROFILE_TYPE_LIST is not None) and (
                profile_type not in self.HARMONIC_PROFILE_TYPE_LIST
            ):
                raise SherlockAddHarmonicEventError(message="Profile type is invalid.")
        except (SherlockInvalidLoadDirectionError, SherlockInvalidOrientationError) as e:
            LOG.error(f"Add harmonic event error: {str(e)}")
            raise SherlockAddHarmonicEventError(message=str(e))
        except SherlockAddHarmonicEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        request = SherlockLifeCycleService_pb2.AddHarmonicEventRequest(
            project=project,
            phaseName=phase_name,
            eventName=event_name,
            description=description,
            duration=duration,
            durationUnits=duration_units,
            numOfCycles=num_of_cycles,
            cycleType=cycle_type,
            sweepRate=sweep_rate,
            orientation=orientation,
            profileType=profile_type,
            loadDirection=load_direction,
        )

        response = self.stub.addHarmonicEvent(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddHarmonicEventError(error_array=response.errors)

                raise SherlockAddHarmonicEventError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddHarmonicEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def add_harmonic_vibe_profiles(
        self,
        project,
        harmonic_vibe_profiles,
    ):
        """Add harmonic life cycle event profiles.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        harmonic_vibe_profiles : list of (phase_name, event_name, profile_name,
                                    freq_units, load_units,
                                    harmonic_vibe_profile_entries) profiles, required
            phase_name : str
                Name of the lifecycle phase this profile is associated with.
            event_name : str
                Name of the harmonic event for the profile.
            profile_name : str
                Name of the harmonic profile.
            freq_units : str
                Frequency units. Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            load_units : str
                Load units. Options are ``"G"``, ```"m/s2"``, ``"mm/s2"``, "``in/s2"``,
                and ``"ft/s2"``.
            harmonic_profile_entries : list of (frequency, load) entries, required
                frequency : double
                    Frequency of the profile entry expressed in frequency units.
                load : double
                    Load of the profile entry expressed in load units.
            triaxial_axis : (string, required)
                Axis this profile should be assigned to if the harmonic profile type is
                ``"Triaxial"``. Options are: ``"x"``, ``"y"``, and ``"z"``.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
        )
        >>> sherlock.lifecycle.create_life_phase(
            "Test",
            "Example",
            1.5,
            "sec",
            4.0,
            "COUNT",
        )
        >>> sherlock.lifecycle.add_harmonic_event(
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
            "2,4,5",
        )
        >>> sherlock.lifecycle.add_harmonic_profiles(
            "Test",
            [(
                "Example",
                "Event1",
                "Profile1",
                "HZ",
                "G",
                [
                    (10, 1),
                    (1000, 1),
                ],
                "",
            )]
        )
        """
        if self.FREQ_UNIT_LIST is None:
            self._init_freq_units()
        if self.LOAD_UNIT_LIST is None:
            self._init_load_units()

        try:
            if project == "":
                raise SherlockAddHarmonicVibeProfilesError(message="Project name is invalid.")

            for i, profile_entry in enumerate(harmonic_vibe_profiles):
                if len(profile_entry) != 7:
                    raise SherlockAddHarmonicVibeProfilesError(
                        f"Number of arguments ({str(len(profile_entry))}) is wrong for "
                        f"harmonic vibe profile {i}."
                    )
                elif not isinstance(profile_entry[0], str) or profile_entry[0] == "":
                    raise SherlockAddHarmonicVibeProfilesError(
                        f"Phase name is invalid for harmonic vibe profile {i}."
                    )
                elif not isinstance(profile_entry[1], str) or profile_entry[1] == "":
                    raise SherlockAddHarmonicVibeProfilesError(
                        f"Event name is invalid for harmonic vibe profile {i}."
                    )
                elif not isinstance(profile_entry[2], str) or profile_entry[2] == "":
                    raise SherlockAddHarmonicVibeProfilesError(
                        f"Profile name is invalid for harmonic vibe profile {i}."
                    )
                elif not isinstance(profile_entry[3], str) or (
                    (self.FREQ_UNIT_LIST is not None)
                    and (profile_entry[3] not in self.FREQ_UNIT_LIST)
                ):
                    raise SherlockAddHarmonicVibeProfilesError(
                        f"Frequency units {profile_entry[3]} are invalid for harmonic vibe "
                        f"profile {i}."
                    )
                elif not isinstance(profile_entry[4], str) or (
                    (self.LOAD_UNIT_LIST is not None)
                    and (profile_entry[4] not in self.LOAD_UNIT_LIST)
                ):
                    raise SherlockAddHarmonicVibeProfilesError(
                        f"Load units {profile_entry[4]} are invalid for harmonic vibe profile {i}."
                    )

            try:
                self._check_harmonic_profile_entries_validity(profile_entry[5])
            except SherlockInvalidHarmonicProfileEntriesError as e:
                raise SherlockAddHarmonicVibeProfilesError(
                    f"{str(e)} for harmonic vibe profile {i}."
                )

        except SherlockAddHarmonicVibeProfilesError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        request = SherlockLifeCycleService_pb2.AddHarmonicVibeProfilesRequest(project=project)

        """Add the harmonic vibe profiles to the request."""
        for h in harmonic_vibe_profiles:
            profile = request.harmonicVibeProfiles.add()
            profile.phaseName = h[0]
            profile.eventName = h[1]
            profile.profileName = h[2]
            profile.freqUnits = h[3]
            profile.loadUnits = h[4]

            """Add the entries to the harmonic profile request."""
            for e in h[5]:
                entry = profile.harmonicVibeProfileEntries.add()
                entry.freq = e[0]
                entry.load = e[1]

            profile.triaxialAxis = h[6]

        response = self.stub.addHarmonicVibeProfiles(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddHarmonicVibeProfilesError(error_array=response.errors)
                else:
                    raise SherlockAddHarmonicVibeProfilesError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddHarmonicVibeProfilesError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def add_shock_event(
        self,
        project,
        phase_name,
        event_name,
        duration,
        duration_units,
        num_of_cycles,
        cycle_type,
        orientation,
        load_direction,
        description="",
    ):
        """Add a shock life cycle event.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        phase_name : str
            Name of the lifecycle phase to add this event to.
        event_name : str
            Name of the shock event.
        duration : double
            Event duration length.
        duration_units : str
            Event duration units. Options are ``"ms"``, ``"sec"``, ``"min"``, ``"hr"``,
            ``"day"``, and ``"year"``.
        num_of_cycles : double
            Number of cycles for the shock event.
        cycle_type : str
            Cycle type. Options include ``"COUNT"``, ``"DUTY CYCLE"``,
            ``"PER YEAR"``, and ``"PER HOUR"``.
        orientation : str
            PCB orientation in the format of ``azimuth, elevation``. For example, ``30,15``.
        load_direction : str
            Load direction in the format of ``x,y,z``. For example, ``0,0,1``.
        description : str, optional
            Description of the shock event.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
        )
        >>> sherlock.lifecycle.create_life_phase(
            "Test",
            "Example",
            1.5,
            "sec",
            4.0,
            "COUNT",
        )
        >>> sherlock.lifecycle.add_shock_event(
            "Test",
            "Example",
            "Event1",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            "45,45",
            "2,4,5",
        )
        """
        if self.TIME_UNIT_LIST is None:
            self._init_time_units()
        if self.CYCLE_TYPE_LIST is None:
            self._init_cycle_types()

        try:
            if project == "":
                raise SherlockAddShockEventError(message="Project name is invalid.")
            if phase_name == "":
                raise SherlockAddShockEventError(message="Phase name is invalid.")
            if event_name == "":
                raise SherlockAddShockEventError(message="Event name is invalid.")
            if (self.TIME_UNIT_LIST is not None) and (duration_units not in self.TIME_UNIT_LIST):
                raise SherlockAddShockEventError(message="Duration units are invalid.")
            if duration <= 0.0:
                raise SherlockAddShockEventError(message="Duration must be greater than 0.")
            if (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockAddShockEventError(message="Cycle type is invalid.")
            if num_of_cycles <= 0.0:
                raise SherlockAddShockEventError(message="Number of cycles must be greater than 0.")
        except SherlockAddShockEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        try:
            self._check_load_direction_validity(load_direction)
            self._check_orientation_validity(orientation)
        except (SherlockInvalidLoadDirectionError, SherlockInvalidOrientationError) as e:
            LOG.error(f"Add shock event error: {str(e)}")
            raise SherlockAddShockEventError(message=str(e))

        request = SherlockLifeCycleService_pb2.AddShockEventRequest(
            project=project,
            phaseName=phase_name,
            eventName=event_name,
            description=description,
            duration=duration,
            durationUnits=duration_units,
            numOfCycles=num_of_cycles,
            cycleType=cycle_type,
            orientation=orientation,
            loadDirection=load_direction,
        )

        response = self.stub.addShockEvent(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddShockEventError(error_array=response.errors)

                raise SherlockAddShockEventError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddShockEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def add_shock_profiles(
        self,
        project,
        shock_profiles,
    ):
        """Add shock life cycle event profiles.

        Parameters
        ----------
        project : str
            Name of the Sherlock project
        shock_profiles : List of (phase_name, event_name, profile_name, duration, duration_units,
                            sample_rate, sample_rate_units, load_units, freq_units,
                            shock_profile_entries) profiles, required
            phase_name : str
                Bame of the lifecycle phase this profile is associated with.
            event_name : str
                Name of the shock event for the profile.
            profile_name : str
                Name of the shock profile.
            duration : double
                Pulse duration.
            duration_units : str
                Pulse duration units. Options are ``"ms"``, ``"sec"``, ``"min"``, ``"hr"``,
                ``"day"``, and ``"year"``.
            sample_rate : double
                Sample rate.
            sample_rate_units : str
                Sample rate units. Options are ``"ms"``, ``"sec"``, ``"min"``, ``"hr"``,
                ``"day"``, and ``"year"``.
            load_units : str
                Load units. Options are: ``"G"``, ``"m/s2"``, ``"mm/s2"``, ``"in/s2"",
                and ``"ft/s2"``.
            freq_units : str
                Frequency units. Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            shock_profile_entries : list of (shape, load, freq, decay) entries, required
                shape : str
                    Shape of the shock profile entry. Options are ``"FullSine"``,
                    ``"HalfSine"``, ``"Haversine"``, ``"Triangle"``, ``"Sawtooth"``,
                    ``"FullSquare"``, and ``"HalfSquare"``.
                load : double
                    Load of the profile entry expressed in load units.
                freq : double
                    Frequency of the profile entry expressed in frequency units.
                decay : double
                    Decay value of the profile entry.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
        )
        >>> sherlock.lifecycle.create_life_phase(
            "Test",
            "Example",
            1.5,
            "sec",
            4.0,
            "COUNT",
        )
        >>> sherlock.lifecycle.add_shock_event(
            "Test",
            "Example",
            "Event1",
            1.5,
            "sec",
            4.0,
            "PER MIN",
            "45,45",
            "2,4,5",
        )
        >>> sherlock.lifecycle.add_shock_profiles(
            "Test",
            [(
                "Example",
                "Event1",
                "Profile1",
                10.0, "ms",
                0.1, "ms",
                "G",
                "HZ",
                [("HalfSine", 100.0, 100.0, 0)],
            )]
        )
        """
        if self.TIME_UNIT_LIST is None:
            self._init_time_units()
        if self.LOAD_UNIT_LIST is None:
            self._init_load_units()
        if self.FREQ_UNIT_LIST is None:
            self._init_freq_units()
        if self.SHOCK_SHAPE_LIST is None:
            self._init_shock_shapes()

        try:
            if project == "":
                raise SherlockAddShockProfilesError(message="Project name is invalid.")

            for i, profile_entry in enumerate(shock_profiles):
                if len(profile_entry) != 10:
                    raise SherlockAddShockProfilesError(
                        f"Number of arguments ({str(len(profile_entry))}) is wrong for shock "
                        f"profile {i}."
                    )
                elif not isinstance(profile_entry[0], str) or profile_entry[0] == "":
                    raise SherlockAddShockProfilesError(
                        f"Phase name is invalid for shock profile {i}."
                    )
                elif not isinstance(profile_entry[1], str) or profile_entry[1] == "":
                    raise SherlockAddShockProfilesError(
                        f"Event name is invalid for shock profile {i}."
                    )
                elif not isinstance(profile_entry[2], str) or profile_entry[2] == "":
                    raise SherlockAddShockProfilesError(
                        f"Profile name is invalid for shock profile {i}."
                    )
                elif profile_entry[3] <= 0:
                    raise SherlockAddShockProfilesError(
                        f"Duration must be greater than 0 for shock profile {i}."
                    )
                elif not isinstance(profile_entry[4], str) or (
                    (self.TIME_UNIT_LIST is not None)
                    and (profile_entry[4] not in self.TIME_UNIT_LIST)
                ):
                    raise SherlockAddShockProfilesError(
                        f"Duration units {profile_entry[4]} are invalid for shock profile {i}."
                    )
                elif profile_entry[5] <= 0:
                    raise SherlockAddShockProfilesError(
                        f"Sample rate must be greater than 0 for shock profile {i}."
                    )
                elif not isinstance(profile_entry[6], str) or (
                    (self.TIME_UNIT_LIST is not None)
                    and (profile_entry[6] not in self.TIME_UNIT_LIST)
                ):
                    raise SherlockAddShockProfilesError(
                        f"Sample rate unit {profile_entry[6]} are invalid for shock profile {i}."
                    )
                elif not isinstance(profile_entry[7], str) or (
                    (self.LOAD_UNIT_LIST is not None)
                    and (profile_entry[7] not in self.LOAD_UNIT_LIST)
                ):
                    raise SherlockAddShockProfilesError(
                        f"Load units {profile_entry[7]} are invalid for shock profile {i}."
                    )
                elif not isinstance(profile_entry[8], str) or (
                    (self.FREQ_UNIT_LIST is not None)
                    and (profile_entry[8] not in self.FREQ_UNIT_LIST)
                ):
                    raise SherlockAddShockProfilesError(
                        f"Frequency units {profile_entry[8]} are invalid for shock profile {i}."
                    )

            try:
                self._check_shock_profile_entries_validity(profile_entry[9])
            except SherlockInvalidShockProfileEntriesError as e:
                raise SherlockAddShockProfilesError(f"{str(e)} for shock profile {i}.")

        except SherlockAddShockProfilesError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        request = SherlockLifeCycleService_pb2.AddShockProfilesRequest(project=project)

        for s in shock_profiles:
            profile = request.shockProfiles.add()
            profile.phaseName = s[0]
            profile.eventName = s[1]
            profile.profileName = s[2]
            profile.duration = s[3]
            profile.durationUnits = s[4]
            profile.sampleRate = s[5]
            profile.sampleRateUnits = s[6]
            profile.loadUnits = s[7]
            profile.freqUnits = s[8]

        """Add the shock entries to the request."""
        for e in s[9]:
            entry = profile.shockProfileEntries.add()
            entry.shape = e[0]
            entry.load = e[1]
            entry.freq = e[2]
            entry.decay = e[3]

        response = self.stub.addShockProfiles(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddShockProfilesError(error_array=response.errors)
                else:
                    raise SherlockAddShockProfilesError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddShockProfilesError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def load_random_vibe_profile(self, project, phase_name, event_name, file_path):
        """Load random vibe profile from .csv or .dat file.

        Parameters
        ----------
        project : str
            Name of the Sherlock project
        phase_name : str
            Name of the lifecycle phase to add this event to.
        event_name : str
            Name of the random vibe event.
        file_path : str
            File path for thermal profile .dat or .csv file

        Example
        -------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
            cca_name="Card",
        )
            >>> sherlock.lifecycle.load_random_vibe_profile(
                    project="Tutorial",
                    phase_name="Phase 1",
                    event_name="Random Event",
                    file_path="TestProfile.dat",
        )
        """
        try:
            if project == "":
                raise SherlockLoadRandomVibeProfileError(message="Project name is invalid.")
            if phase_name == "":
                raise SherlockLoadRandomVibeProfileError(message="Phase name is invalid.")
            if event_name == "":
                raise SherlockLoadRandomVibeProfileError(message="Event name is invalid.")
            if file_path == "":
                raise SherlockLoadRandomVibeProfileError(message="File path is invalid.")
            if not self._is_connection_up():
                LOG.error("Not connected to a gRPC service.")
                return
            request = SherlockLifeCycleService_pb2.LoadRandomVibeProfileRequest(
                project=project,
                phaseName=phase_name,
                eventName=event_name,
                filePath=file_path,
            )
            response = self.stub.loadRandomVibeProfile(request)
            return response
        except SherlockLoadRandomVibeProfileError as e:
            LOG.error(str(e))
            raise e

    def load_thermal_profile(self, project, phase_name, event_name, file_path):
        """Load a thermal profile from a .dat or .csv file.

        Parameters
        ----------
        project : str
            Name of the Sherlock project
        phase_name : str
            Name of the lifecycle phase to add this event to.
        event_name : str
            Name of the random vibe event.
        file_path : str
            File path for thermal profile .dat or .csv file

        Example
        -------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
            cca_name="Card",
        )
         >>>loaded = sherlock.lifecycle.load_thermal_profile(
                project="Tutorial",
                phase_name="Phase 1",
                event_name="Thermal Event",
                file_path="Tutorial_Profile.dat"
        )
        """
        try:
            if project == "":
                raise SherlockLoadThermalProfileError(message="Project name is invalid.")
            if phase_name == "":
                raise SherlockLoadThermalProfileError(message="Phase name is invalid.")
            if event_name == "":
                raise SherlockLoadThermalProfileError(message="Event name is invalid.")
            if file_path == "":
                raise SherlockLoadThermalProfileError(message="File path is invalid.")
            if not self._is_connection_up():
                LOG.error("Not connected to a gRPC service.")
                return

            request = SherlockLifeCycleService_pb2.LoadThermalProfileRequest(
                project=project,
                phaseName=phase_name,
                eventName=event_name,
                filePath=file_path,
            )
            response = self.stub.loadThermalProfile(request)
            return response
        except SherlockLoadThermalProfileError as e:
            LOG.error(str(e))
            raise e

    def load_harmonic_profile(self, project, phase_name, event_name, file_path):
        """Load Harmonic profile from a .dat or .csv file.

        Parameters
        ----------
        project : str
            Name of the Sherlock project
        phase_name : str
            Name of the lifecycle phase to add this event to.
        event_name : str
            Name of the random vibe event.
        file_path : str
            File path for thermal profile .dat or .csv file

        Example
        -------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
            cca_name="Card",
        )

        >>> loaded = sherlock.lifecycle.load_harmonic_profile(
                project="Tutorial",
                phase_name="Phase 1",
                event_name="Harmonic Event",
                file_path="Test_Profile.dat"
        )
        """
        try:
            if project == "":
                raise SherlockLoadHarmonicProfileError(message="Project name is invalid.")
            if phase_name == "":
                raise SherlockLoadHarmonicProfileError(message="Phase name is invalid.")
            if event_name == "":
                raise SherlockLoadHarmonicProfileError(message="Event name is invalid.")
            if file_path == "":
                raise SherlockLoadHarmonicProfileError(message="File name is invalid.")
            if not self._is_connection_up():
                LOG.error("Not connected to a gRPC service.")
                return
            request = SherlockLifeCycleService_pb2.LoadHarmonicProfileRequest(
                project=project,
                phaseName=phase_name,
                eventName=event_name,
                filePath=file_path,
            )
            response = self.stub.loadHarmonicProfile(request)
            return response
        except SherlockLoadHarmonicProfileError as e:
            LOG.error(str(e))
            raise e

    def load_random_vibe_profile(self, project, phase_name, event_name, file_path):
        """Load random vibe profile from .csv or .dat file,"""

        try:
            if project == "":
                raise SherlockLoadRandomVibeProfileError(message="Project name is invalid.")
            if phase_name == "":
                raise SherlockLoadRandomVibeProfileError(message="Phase name is invalid.")
            if event_name == "":
                raise SherlockLoadRandomVibeProfileError(message="Event name is invalid.")
            if file_path == "":
                raise SherlockLoadRandomVibeProfileError(message="File path is invalid.")
            if not self._is_connection_up():
                LOG.error("Not connected to a gRPC service.")
                return

            request = SherlockLifeCycleService_pb2.LoadRandomVibeProfileRequest(
                project=project,
                phaseName=phase_name,
                eventName=event_name,
                filePath=file_path,
            )
            request = self.stub.loadRandomVibeProfile(request)

            return request
        except SherlockLoadRandomVibeProfileError as e:
            LOG.error(str(e))
            raise e

