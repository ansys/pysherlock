"""Module containing all the lifecycle management capabilities."""

try:
    import SherlockLifeCycleService_pb2
    import SherlockLifeCycleService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockLifeCycleService_pb2
    from ansys.api.sherlock.v0 import SherlockLifeCycleService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockAddHarmonicEventError,
    SherlockAddHarmonicProfileError,
    SherlockAddRandomVibeEventError,
    SherlockAddRandomVibeProfileError,
    SherlockAddShockEventError,
    SherlockAddShockProfileError,
    SherlockAddThermalEventError,
    SherlockAddThermalProfileError,
    SherlockCreateLifePhaseError,
    SherlockInvalidHarmonicProfileEntriesError,
    SherlockInvalidLoadDirectionError,
    SherlockInvalidOrientationError,
    SherlockInvalidRandomVibeProfileEntriesError,
    SherlockInvalidShockProfileEntriesError,
    SherlockInvalidThermalProfileEntriesError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub


class Lifecycle(GrpcStub):
    """Module containing all the lifecycle management capabilities."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockLifeCycleService."""
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
        """Initialize TIME_UNIT_LIST."""
        if self._is_connection_up():
            duration_unit_request = SherlockLifeCycleService_pb2.ListDurationUnitsRequest()
            duration_unit_response = self.stub.listDurationUnits(duration_unit_request)
            if duration_unit_response.returnCode.value == 0:
                self.TIME_UNIT_LIST = duration_unit_response.durationUnits

    def _init_cycle_types(self):
        """Initialize CYCLE_TYPE_LIST."""
        if self._is_connection_up():
            cycle_type_request = SherlockLifeCycleService_pb2.ListLCTypesRequest()
            cycle_type_response = self.stub.listLifeCycleTypes(cycle_type_request)
            if cycle_type_response.returnCode.value == 0:
                self.CYCLE_TYPE_LIST = cycle_type_response.types

    def _init_rv_profile_types(self):
        """Initialize RV_PROFILE_TYPE_LIST."""
        if self._is_connection_up():
            rv_profile_request = SherlockLifeCycleService_pb2.ListRandomProfileTypesRequest()
            rv_profile_response = self.stub.listRandomProfileTypes(rv_profile_request)
            if rv_profile_response.returnCode.value == 0:
                self.RV_PROFILE_TYPE_LIST = rv_profile_response.types

    def _init_harmonic_profile_types(self):
        """Initialize HARMONIC_PROFILE_TYPE_LIST."""
        if self._is_connection_up():
            harmonic_profile_request = (
                SherlockLifeCycleService_pb2.ListHarmonicProfileTypesRequest()
            )
            harmonic_profile_response = self.stub.listHarmonicProfileTypes(harmonic_profile_request)
            if harmonic_profile_response.returnCode.value == 0:
                self.HARMONIC_PROFILE_TYPE_LIST = harmonic_profile_response.types

    def _init_freq_units(self):
        """Initialize FREQ_UNIT_LIST."""
        if self._is_connection_up():
            freq_unit_request = SherlockLifeCycleService_pb2.ListFreqUnitsRequest()
            freq_type_response = self.stub.listFreqUnits(freq_unit_request)
            if freq_type_response.returnCode.value == 0:
                self.FREQ_UNIT_LIST = freq_type_response.freqUnits

    def _init_ampl_units(self):
        """Initialize AMPL_UNIT_LIST."""
        if self._is_connection_up():
            ampl_unit_request = SherlockLifeCycleService_pb2.ListAmplUnitsRequest()
            ampl_type_response = self.stub.listAmplUnits(ampl_unit_request)
            if ampl_type_response.returnCode.value == 0:
                self.AMPL_UNIT_LIST = ampl_type_response.amplUnits

    def _init_cycle_states(self):
        """Initialize CYCLE_STATES_LIST."""
        if self._is_connection_up():
            cycle_state_request = SherlockLifeCycleService_pb2.ListLCStatesRequest()
            cycle_state_response = self.stub.listLifeCycleStates(cycle_state_request)
            if cycle_state_response.returnCode.value == 0:
                self.CYCLE_STATE_LIST = cycle_state_response.states

    def _init_temp_units(self):
        """Initialize TEMP_UNIT_LIST."""
        if self._is_connection_up():
            temp_unit_request = SherlockLifeCycleService_pb2.ListTempUnitsRequest()
            temp_unit_response = self.stub.listTempUnits(temp_unit_request)
            if temp_unit_response.returnCode.value == 0:
                self.TEMP_UNIT_LIST = temp_unit_response.tempUnits

    def _init_load_units(self):
        """Initialize LOAD_UNIT_LIST."""
        if self._is_connection_up():
            load_unit_request = SherlockLifeCycleService_pb2.ListShockLoadUnitsRequest()
            load_unit_response = self.stub.listShockLoadUnits(load_unit_request)
            if load_unit_response.returnCode.value == 0:
                self.LOAD_UNIT_LIST = load_unit_response.units

    def _init_shock_shapes(self):
        """Initialize SHOCK_SHAPE_LIST."""
        if self._is_connection_up():
            shock_shape_request = SherlockLifeCycleService_pb2.ListShockPulsesRequest()
            shock_shape_response = self.stub.listShockPulses(shock_shape_request)
            if shock_shape_response.returnCode.value == 0:
                self.SHOCK_SHAPE_LIST = shock_shape_response.shockPulse

    def _check_load_direction_validity(self, input):
        """Check input string if it is a valid load."""
        directions = input.split(",")

        if len(directions) != 3:
            raise SherlockInvalidLoadDirectionError("Invalid number of direction coordinates")

        try:
            nonzero = 0
            for dir in directions:
                if float(dir) != 0:
                    nonzero += 1

            if nonzero == 0:
                raise SherlockInvalidLoadDirectionError(
                    "At least one direction coordinate must be non-zero"
                )
            return
        except TypeError:
            raise SherlockInvalidLoadDirectionError("Invalid direction coordinates")

    def _check_orientation_validity(self, input):
        """Check input string if it is a valid orientation."""
        orientation = input.split(",")

        if len(orientation) != 2:
            raise SherlockInvalidOrientationError("Invalid number of spherical coordinates")

        try:
            float(orientation[0])
        except:
            raise SherlockInvalidOrientationError("Invalid azimuth value")

        try:
            float(orientation[1])
            return
        except:
            raise SherlockInvalidOrientationError("Invalid elevation value")

    def _check_random_vibe_profile_entries_validity(self, input):
        """Check input array if all elements are valid for random vibe entries."""
        if not isinstance(input, list):
            raise SherlockInvalidRandomVibeProfileEntriesError("Invalid entries argument")

        try:
            for i, entry in enumerate(input):
                if len(entry) != 2:
                    raise SherlockInvalidRandomVibeProfileEntriesError(
                        f"Invalid entry {i}: Wrong number of args"
                    )
                elif entry[0] <= 0:
                    raise SherlockInvalidRandomVibeProfileEntriesError(
                        f"Invalid entry {i}: Frequencies must be greater than 0"
                    )
                elif entry[1] <= 0:
                    raise SherlockInvalidRandomVibeProfileEntriesError(
                        f"Invalid entry {i}: Amplitudes must be greater than 0"
                    )
        except TypeError:
            raise SherlockInvalidRandomVibeProfileEntriesError(
                f"Invalid entry {i}: Invalid freq/ampl"
            )

    def _check_thermal_profile_entries_validity(self, input):
        """Check input array if all elements are valid for thermal entries."""
        if not isinstance(input, list):
            raise SherlockAddThermalProfileError("Invalid entries argument")

        try:
            for i, entry in enumerate(input):
                if len(entry) != 4:
                    raise SherlockInvalidThermalProfileEntriesError(
                        f"Invalid entry {i}: Wrong number of args"
                    )
                elif not isinstance(entry[0], str):
                    raise SherlockInvalidThermalProfileEntriesError(
                        f"Invalid entry {i}: Invalid step name"
                    )
                elif entry[1] not in self.STEP_TYPE_LIST:
                    raise SherlockInvalidThermalProfileEntriesError(
                        f"Invalid entry {i}: Invalid step type"
                    )
                elif entry[2] <= 0:
                    raise SherlockInvalidThermalProfileEntriesError(
                        f"Invalid entry {i}: Time must be greater than 0"
                    )
                elif not isinstance(entry[3], (int, float)):
                    raise SherlockInvalidThermalProfileEntriesError(
                        f"Invalid entry {i}: Invalid temp"
                    )
        except TypeError:
            raise SherlockInvalidThermalProfileEntriesError(f"Invalid entry {i}: Invalid time")

    def _check_harmonic_profile_entries_validity(self, input):
        """Check input array if all elements are valid for harmonic entries."""
        if not isinstance(input, list):
            raise SherlockInvalidHarmonicProfileEntriesError(message="Invalid entries argument")

        try:
            for i, entry in enumerate(input):
                if len(entry) != 2:
                    raise SherlockInvalidHarmonicProfileEntriesError(
                        message=f"Invalid entry {i}: Wrong number of args"
                    )
                elif entry[0] <= 0:
                    raise SherlockInvalidHarmonicProfileEntriesError(
                        message=f"Invalid entry {i}: Frequencies must be greater than 0"
                    )
                elif entry[1] <= 0:
                    raise SherlockInvalidHarmonicProfileEntriesError(
                        message=f"Invalid entry {i}: Load must be greater than 0"
                    )
            return
        except TypeError:
            raise SherlockInvalidHarmonicProfileEntriesError(
                message=f"Invalid entry {i}: Invalid freq/load"
            )

    def _check_shock_profile_entries_validity(self, input):
        """Check input array if all elements are valid for shock entries."""
        if not isinstance(input, list):
            raise SherlockInvalidShockProfileEntriesError(message="Invalid entries argument")

        try:
            for i, entry in enumerate(input):
                if len(entry) != 4:
                    raise SherlockInvalidShockProfileEntriesError(
                        message=f"Invalid entry {i}: Wrong number of args"
                    )
                elif not isinstance(entry[0], str):
                    raise SherlockInvalidShockProfileEntriesError(
                        message=f"Invalid entry {i}: Invalid shape name"
                    )
                elif (self.SHOCK_SHAPE_LIST is not None) and (
                    entry[0] not in self.SHOCK_SHAPE_LIST
                ):
                    raise SherlockInvalidShockProfileEntriesError(
                        message=f"Invalid entry {i}: Invalid shape type"
                    )
                elif entry[1] <= 0:
                    raise SherlockInvalidShockProfileEntriesError(
                        message=f"Invalid entry {i}: Load must be greater than 0"
                    )
                elif entry[2] <= 0:
                    raise SherlockInvalidShockProfileEntriesError(
                        message=f"Invalid entry {i}: Frequency must be greater than 0"
                    )
                elif entry[3] < 0:
                    raise SherlockInvalidShockProfileEntriesError(
                        message=f"Invalid entry {i}: Decay must be nonnegative"
                    )
            return
        except TypeError:
            raise SherlockInvalidShockProfileEntriesError(
                message=f"Invalid entry {i}: Invalid load/freq/decay"
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
        """Define and add a new life phase.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        phase_name : str, required
            The name of new life phase.
        duration : double, required
            Event duration length.
        duration_units : str, required
            Event duration length units. For example: "ms", "sec", "min", etc.
        num_of_cycles : double, required
            Number of cycles defined for new life phase.
        cycle_type : str, required
            The cycle type. For example: "COUNT", "DUTY CYCLE", "PER YEAR", "PER HOUR", etc.
        description : str, optional
            Description of new life phase.
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
                raise SherlockCreateLifePhaseError(message="Invalid project name")
            elif phase_name == "":
                raise SherlockCreateLifePhaseError(message="Invalid phase name")
            elif (self.TIME_UNIT_LIST is not None) and (duration_units not in self.TIME_UNIT_LIST):
                raise SherlockCreateLifePhaseError(message="Invalid duration unit specified")
            elif duration <= 0.0:
                raise SherlockCreateLifePhaseError(message="Duration must be greater than 0")
            elif (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockCreateLifePhaseError(message="Invalid cycle type")
            elif num_of_cycles <= 0.0:
                raise SherlockCreateLifePhaseError(
                    message="Number of cycles must be greater than 0"
                )
        except SherlockCreateLifePhaseError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
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
                else:
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
        """Define and add a new random vibe life cycle event.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        phase_name : str, required
            The name of the life cycle phase to add this event to.
        event_name : str, required
            Name of the random vibe event.
        duration : double, required
            Event duration length.
        duration_units : str, required
            Event duration length units.
        num_of_cycles : double, required
            Number of cycles defined for this random vibe event.
        cycle_type : str, required
            The cycle type. For example: "COUNT", "DUTY CYCLE", "PER YEAR", "PER HOUR", etc.
        orientation : str, required
            PCB orientation in the format of azimuth, elevation. Example: 30,15
        profile_type : str, required
            Random load profile type. Example valid value is "Uniaxial".
        load_direction : str, required
            Load direction in the format of x,y,z. Example: 0,0,1
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
                raise SherlockAddRandomVibeEventError(message="Invalid project name")
            elif phase_name == "":
                raise SherlockAddRandomVibeEventError(message="Invalid phase name")
            elif event_name == "":
                raise SherlockAddRandomVibeEventError(message="Invalid event name")
            elif (self.TIME_UNIT_LIST is not None) and (duration_units not in self.TIME_UNIT_LIST):
                raise SherlockAddRandomVibeEventError(message="Invalid duration unit specified")
            elif duration <= 0.0:
                raise SherlockAddRandomVibeEventError(message="Duration must be greater than 0")
            elif (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockAddRandomVibeEventError(message="Invalid cycle type")
            elif num_of_cycles <= 0.0:
                raise SherlockAddRandomVibeEventError(
                    message="Number of cycles must be greater than 0"
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
                    message="Valid profile type for a random event can only be Uniaxial"
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
                else:
                    raise SherlockAddRandomVibeEventError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddRandomVibeEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def add_random_vibe_profile(
        self,
        project,
        phase_name,
        event_name,
        profile_name,
        freq_units,
        ampl_units,
        random_vibe_profile_entries,
    ):
        """Add a new random vibe profile to a random vibe event.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        phase_name : str, required
            The name of the life cycle phase this event is associated.
        event_name : str, required
            Name of the random vibe event.
        profile_name : str, required
            Name of the random vibe profile.
        freq_units : str, required
            Frequency Units.
        ampl_units : str, required
            Amplitude Units.
        random_vibe_profile_entries : (double, double) list, required
            List of (frequency, amplitude) entries
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
        >>> sherlock.lifecycle.add_random_vibe_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "HZ",
            "G2/Hz",
            [(4,8), (5, 50)],
        )
        """
        if self.FREQ_UNIT_LIST is None:
            self._init_freq_units()
        if self.AMPL_UNIT_LIST is None:
            self._init_ampl_units()

        try:
            if project == "":
                raise SherlockAddRandomVibeProfileError(message="Invalid project name")
            elif phase_name == "":
                raise SherlockAddRandomVibeProfileError(message="Invalid phase name")
            elif event_name == "":
                raise SherlockAddRandomVibeProfileError(message="Invalid event name")
            elif profile_name == "":
                raise SherlockAddRandomVibeProfileError(message="Invalid profile name")
            elif (self.FREQ_UNIT_LIST is not None) and (freq_units not in self.FREQ_UNIT_LIST):
                raise SherlockAddRandomVibeProfileError(message="Invalid frequency unit")
            elif (self.AMPL_UNIT_LIST is not None) and (ampl_units not in self.AMPL_UNIT_LIST):
                raise SherlockAddRandomVibeProfileError(message="Invalid amplitude type")
        except SherlockAddRandomVibeProfileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        try:
            self._check_random_vibe_profile_entries_validity(random_vibe_profile_entries)
        except SherlockInvalidRandomVibeProfileEntriesError as e:
            LOG.error(f"Add random vibe profile error: {str(e)}")
            raise SherlockAddRandomVibeProfileError(message=str(e))

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        request = SherlockLifeCycleService_pb2.AddRandomVibeProfileRequest(
            project=project,
            phaseName=phase_name,
            eventName=event_name,
            profileName=profile_name,
            freqUnits=freq_units,
            amplUnits=ampl_units,
        )

        self._add_random_vibe_profile_entries(request, random_vibe_profile_entries)

        response = self.stub.addRandomVibeProfile(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddRandomVibeProfileError(error_array=response.errors)
                else:
                    raise SherlockAddRandomVibeProfileError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddRandomVibeProfileError as e:
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
        """Add a new thermal event to a life cycle.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        phase_name : str, required
            The name of the life cycle phase to add this event to.
        event_name : str, required
            Name of the thermal event.
        num_of_cycles : double, required
            Number of cycles defined for this thermal event.
        cycle_type : str, required
            The cycle type. For example: "COUNT", "DUTY CYCLE", "PER YEAR", "PER HOUR", etc.
        cycle_state : str, required
            The life cycle state. For example: "OPERATING", "STORAGE".
        description : str, optional
            Description of new thermal event.
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
            "STORAGE,
        )
        """
        if self.CYCLE_TYPE_LIST is None:
            self._init_cycle_types()
        if self.CYCLE_STATE_LIST is None:
            self._init_cycle_states()

        try:
            if project == "":
                raise SherlockAddThermalEventError(message="Invalid project name")
            elif phase_name == "":
                raise SherlockAddThermalEventError(message="Invalid phase name")
            elif event_name == "":
                raise SherlockAddThermalEventError(message="Invalid event name")
            elif (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockAddThermalEventError(message="Invalid cycle type")
            elif num_of_cycles <= 0.0:
                raise SherlockAddThermalEventError(
                    message="Number of cycles must be greater than 0"
                )
            elif (self.CYCLE_STATE_LIST is not None) and (cycle_state not in self.CYCLE_STATE_LIST):
                raise SherlockAddThermalEventError(message="Invalid cycle state")
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
                else:
                    raise SherlockAddThermalEventError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddThermalEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def add_thermal_profile(
        self,
        project,
        phase_name,
        event_name,
        profile_name,
        time_units,
        temp_units,
        thermal_profile_entries,
    ):
        """Define and add a new thermal life cycle event profile.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        phase_name : str, required
            The name of the life cycle phase this event is associated.
        event_name : str, required
            Name of the thermal event.
        profile_name : str, required
            Name of the thermal profile.
        time_units : str, required
            Time Units.
        temp_units : str, required
            Temperature Units.
        thermal_profile_entries : (str, str, double, double) list, required
            List of (step, type, time, temp) entries
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
            "STORAGE,
        )
        >>> sherlock.lifecycle.add_thermal_profile(
            "Test",
            "Example",
            "Event1"
            "Profile1",
            "sec",
            "F",
            [
                ("Steady1", "HOLD", 40, 40),
                ("Steady", "HOLD", 20, 20),
                ("Back", "RAMP", 20, 40),
            ],
        )
        """
        if self.TIME_UNIT_LIST is None:
            self._init_time_units()
        if self.TEMP_UNIT_LIST is None:
            self._init_temp_units()

        try:
            if project == "":
                raise SherlockAddThermalProfileError(message="Invalid project name")
            elif phase_name == "":
                raise SherlockAddThermalProfileError(message="Invalid phase name")
            elif event_name == "":
                raise SherlockAddThermalProfileError(message="Invalid event name")
            elif profile_name == "":
                raise SherlockAddThermalProfileError(message="Invalid profile name")
            elif (self.TIME_UNIT_LIST is not None) and (time_units not in self.TIME_UNIT_LIST):
                raise SherlockAddThermalProfileError(message="Invalid time unit")
            elif (self.TEMP_UNIT_LIST is not None) and (temp_units not in self.TEMP_UNIT_LIST):
                raise SherlockAddThermalProfileError(message="Invalid temperature unit")
        except SherlockAddThermalProfileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        try:
            self._check_thermal_profile_entries_validity(thermal_profile_entries)
        except SherlockInvalidThermalProfileEntriesError as e:
            LOG.error(f"Add thermal profile error: {str(e)}")
            raise SherlockAddThermalProfileError(message=str(e))

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        request = SherlockLifeCycleService_pb2.AddThermalProfileRequest(
            project=project,
            phaseName=phase_name,
            eventName=event_name,
            profileName=profile_name,
            timeUnits=time_units,
            tempUnits=temp_units,
        )

        self._add_thermal_profile_entries(request, thermal_profile_entries)

        response = self.stub.addThermalProfile(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddThermalProfileError(error_array=response.errors)
                else:
                    raise SherlockAddThermalProfileError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddThermalProfileError as e:
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
        """Define and add a new harmonic vibe life cycle event.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        phase_name : str, required
            The name of the life cycle phase to add this event to.
        event_name : str, required
            Name of the harmonic event.
        duration : double, required
            Event duration length.
        duration_units : str, required
            Event duration length units.
        num_of_cycles : double, required
            Number of cycles defined for this harmonic event.
        cycle_type : str, required
            The cycle type. For example: "COUNT", "DUTY CYCLE", "PER YEAR", "PER HOUR", etc.
        sweep_rate : double, required
            Sweep rate for the harmonic event
        orientation : str, required
            PCB orientation in the format of azimuth, elevation. Example: 30,15
        profile_type : str, required
            Harmonic load profile types. Example valid values are "Uniaxial" and "Triaxial".
        load_direction: str, required
            Load direction in the format of x,y,z. Example: 0,0,1
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
            "Uniaxial"
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
                raise SherlockAddHarmonicEventError(message="Invalid project name")
            elif phase_name == "":
                raise SherlockAddHarmonicEventError(message="Invalid phase name")
            elif event_name == "":
                raise SherlockAddHarmonicEventError(message="Invalid event name")
            elif (self.TIME_UNIT_LIST is not None) and (duration_units not in self.TIME_UNIT_LIST):
                raise SherlockAddHarmonicEventError(message="Invalid duration unit specified")
            elif duration <= 0.0:
                raise SherlockAddHarmonicEventError(message="Duration must be greater than 0")
            elif (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockAddHarmonicEventError(message="Invalid cycle type")
            elif num_of_cycles <= 0.0:
                raise SherlockAddHarmonicEventError(
                    message="Number of cycles must be greater than 0"
                )
            elif sweep_rate <= 0.0:
                raise SherlockAddHarmonicEventError(message="Sweep rate must be greater than 0")
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
                raise SherlockAddHarmonicEventError(message="Invalid profile type")
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
                else:
                    raise SherlockAddHarmonicEventError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddHarmonicEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def add_harmonic_profile(
        self,
        project,
        phase_name,
        event_name,
        profile_name,
        freq_units,
        load_units,
        harmonic_profiles_entries,
        triaxial_axis,
    ):
        """Define and add a new harmonic life cycle event profile.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        phase_name : str, required
            The name of the life cycle phase this event is associated.
        event_name : str, required
            Name of the harmonic event.
        profile_name : str, required
            Name of the harmonic profile.
        freq_units : str, required
            Frequency Units.
        load_units : str, required
            Load Units.
        harmonic_profile_entries : (double, double) list, required
            List of (frequency, load) entries
        triaxial_axis : (string, required)
            If the harmonic profile type is "Triaxial", the axis this profile should be assigned to.
            Valid values are: x, y, z.
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
            "Uniaxial"
            "2,4,5",
        )
        >>> sherlock.lifecycle.add_harmonic_profile(
            "Test",
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
        """
        if self.FREQ_UNIT_LIST is None:
            self._init_freq_units()
        if self.LOAD_UNIT_LIST is None:
            self._init_load_units()

        try:
            if project == "":
                raise SherlockAddHarmonicProfileError(message="Invalid project name")
            elif phase_name == "":
                raise SherlockAddHarmonicProfileError(message="Invalid phase name")
            elif event_name == "":
                raise SherlockAddHarmonicProfileError(message="Invalid event name")
            elif profile_name == "":
                raise SherlockAddHarmonicProfileError(message="Invalid profile name")
            elif (self.FREQ_UNIT_LIST is not None) and (freq_units not in self.FREQ_UNIT_LIST):
                raise SherlockAddHarmonicProfileError(message="Invalid frequency unit")
            elif (self.LOAD_UNIT_LIST is not None) and (load_units not in self.LOAD_UNIT_LIST):
                raise SherlockAddHarmonicProfileError(message="Invalid load unit")
        except SherlockAddHarmonicProfileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        try:
            self._check_harmonic_profile_entries_validity(harmonic_profiles_entries)
        except SherlockInvalidHarmonicProfileEntriesError as e:
            LOG.error(f"Add harmonic profile error: {str(e)}")
            raise SherlockAddHarmonicProfileError(message=str(e))

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        request = SherlockLifeCycleService_pb2.AddHarmonicProfileRequest(
            project=project,
            phaseName=phase_name,
            eventName=event_name,
            profileName=profile_name,
            freqUnits=freq_units,
            loadUnits=load_units,
            triaxialAxis=triaxial_axis,
        )

        self._add_harmonic_profile_entries(request, harmonic_profiles_entries)

        response = self.stub.addHarmonicProfile(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddHarmonicProfileError(error_array=response.errors)
                else:
                    raise SherlockAddHarmonicProfileError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddHarmonicProfileError as e:
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
        """Define and add a new shock life cycle event.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        phase_name : str, required
            The name of the life cycle phase to add this event to.
        event_name : str, required
            Name of the shock event.
        duration : double, required
            Event duration length.
        duration_units : str, required
            Event duration length units.
        num_of_cycles : double, required
            Number of cycles defined for this shock event.
        cycle_type : str, required
            The cycle type. For example: "COUNT", "DUTY CYCLE", "PER YEAR", "PER HOUR", etc.
        orientation : str, required
            PCB orientation in the format of azimuth, elevation. Example: 30,15
        load_direction : str, required
            Load direction in the format of x,y,z. Example: 0,0,1
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
                raise SherlockAddShockEventError(message="Invalid project name")
            elif phase_name == "":
                raise SherlockAddShockEventError(message="Invalid phase name")
            elif event_name == "":
                raise SherlockAddShockEventError(message="Invalid event name")
            elif (self.TIME_UNIT_LIST is not None) and (duration_units not in self.TIME_UNIT_LIST):
                raise SherlockAddShockEventError(message="Invalid duration unit specified")
            elif duration <= 0.0:
                raise SherlockAddShockEventError(message="Duration must be greater than 0")
            elif (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockAddShockEventError(message="Invalid cycle type")
            elif num_of_cycles <= 0.0:
                raise SherlockAddShockEventError(message="Number of cycles must be greater than 0")
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
                else:
                    raise SherlockAddShockEventError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddShockEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def add_shock_profile(
        self,
        project,
        phase_name,
        event_name,
        profile_name,
        duration,
        duration_units,
        sample_rate,
        sample_rate_units,
        load_units,
        freq_units,
        shock_profile_entries,
    ):
        """Define and add a new shock life cycle event profile.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        phase_name : str, required
            The name of the life cycle phase this event is associated.
        event_name : str, required
            Name of the shock event.
        profile_name : str, required
            Name of the shock profile.
        duration : double, required
            Pulse duration.
        duration_units : str, required
            Pulse duration unit.
        sample_rate : double, required
            Sample rate.
        sample_rate_units : str, required
            Sample rate unit.
        load_units : str, required
            Load unit.
        freq_units : str, required
            Frequency unit.
        shock_profile_entries : (str, double, double, double) list, required
            Primary shape entry for the shock profile
            List of (shape, load, freq, decay) entries
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
        >>> sherlock.lifecycle.add_shock_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            10.0,
            "ms",
            0.1,
            "ms",
            "G",
            "HZ",
            [
                ("HalfSine", 100.0, 100.0, 0)
            ],
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
                raise SherlockAddShockProfileError(message="Invalid project name")
            elif phase_name == "":
                raise SherlockAddShockProfileError(message="Invalid phase name")
            elif event_name == "":
                raise SherlockAddShockProfileError(message="Invalid event name")
            elif profile_name == "":
                raise SherlockAddShockProfileError(message="Invalid profile name")
            elif duration <= 0:
                raise SherlockAddShockProfileError(message="Duration must be greater than 0")
            elif (self.TIME_UNIT_LIST is not None) and (duration_units not in self.TIME_UNIT_LIST):
                raise SherlockAddShockProfileError(message="Invalid duration unit")
            elif sample_rate <= 0:
                raise SherlockAddShockProfileError(message="Sample rate must be greater than 0")
            elif (self.TIME_UNIT_LIST is not None) and (
                sample_rate_units not in self.TIME_UNIT_LIST
            ):
                raise SherlockAddShockProfileError(message="Invalid sample rate unit")
            elif (self.LOAD_UNIT_LIST is not None) and (load_units not in self.LOAD_UNIT_LIST):
                raise SherlockAddShockProfileError(message="Invalid load unit")
            elif (self.FREQ_UNIT_LIST is not None) and (freq_units not in self.FREQ_UNIT_LIST):
                raise SherlockAddShockProfileError(message="Invalid frequency unit")
        except SherlockAddShockProfileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        try:
            self._check_shock_profile_entries_validity(shock_profile_entries)
        except SherlockInvalidShockProfileEntriesError as e:
            LOG.error(f"Add shock profile error: {str(e)}")
            raise SherlockAddShockProfileError(message=str(e))

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        request = SherlockLifeCycleService_pb2.AddShockProfileRequest(
            project=project,
            phaseName=phase_name,
            eventName=event_name,
            profileName=profile_name,
            duration=duration,
            durationUnits=duration_units,
            sampleRate=sample_rate,
            sampleRateUnits=sample_rate_units,
            loadUnits=load_units,
            freqUnits=freq_units,
        )

        self._add_shock_profile_entries(request, shock_profile_entries)

        response = self.stub.addShockProfile(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddShockProfileError(error_array=response.errors)
                else:
                    raise SherlockAddShockProfileError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddShockProfileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e
