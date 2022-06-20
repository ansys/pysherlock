"""Module for lifecycle services on client-side."""
import SherlockLifeCycleService_pb2
import SherlockLifeCycleService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockAddRandomVibeEventError,
    SherlockAddRandomVibeProfileError,
    SherlockAddThermalEventError,
    SherlockCreateLifePhaseError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub


class Lifecycle(GrpcStub):
    """Contains methods from the Sherlock Lifecycle Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockLifeCycleService."""
        self.channel = channel
        self.stub = SherlockLifeCycleService_pb2_grpc.SherlockLifeCycleServiceStub(channel)
        self.TIME_UNIT_LIST = None
        self.CYCLE_TYPE_LIST = None
        self.RV_PROFILE_LIST = None
        self.FREQ_UNIT_LIST = None
        self.AMPL_UNIT_LIST = None
        self.CYCLE_STATE_LIST = None

        if self._is_connection_up():
            duration_unit_request = SherlockLifeCycleService_pb2.ListDurationUnitsRequest()
            duration_unit_response = self.stub.listDurationUnits(duration_unit_request)
            if duration_unit_response.returnCode.value == 0:
                self.TIME_UNIT_LIST = duration_unit_response.durationUnits

            cycle_type_request = SherlockLifeCycleService_pb2.ListLCTypesRequest()
            cycle_type_response = self.stub.listLifeCycleTypes(cycle_type_request)
            if cycle_type_response.returnCode.value == 0:
                self.CYCLE_TYPE_LIST = cycle_type_response.types

            rv_profile_request = SherlockLifeCycleService_pb2.ListRandomProfileTypesRequest()
            rv_profile_response = self.stub.listRandomProfileTypes(rv_profile_request)
            if rv_profile_response.returnCode.value == 0:
                self.RV_PROFILE_LIST = rv_profile_response.types

            freq_unit_request = SherlockLifeCycleService_pb2.ListFreqUnitsRequest()
            freq_type_response = self.stub.listFreqUnits(freq_unit_request)
            if freq_type_response.returnCode.value == 0:
                self.FREQ_UNIT_LIST = freq_type_response.freqUnits

            ampl_unit_request = SherlockLifeCycleService_pb2.ListAmplUnitsRequest()
            ampl_type_response = self.stub.listAmplUnits(ampl_unit_request)
            if ampl_type_response.returnCode.value == 0:
                self.AMPL_UNIT_LIST = ampl_type_response.amplUnits

            cycle_state_request = SherlockLifeCycleService_pb2.ListLCStatesRequest()
            cycle_state_response = self.stub.listLifeCycleStates(cycle_state_request)
            if cycle_state_response.returnCode.value == 0:
                self.CYCLE_STATE_LIST = cycle_state_response.states

    def _check_load_direction_validity(self, input):
        """Check input string if it is a valid load."""
        directions = input.split(",")

        if len(directions) != 3:
            return False, "Invalid number of direction coordinates"

        try:
            nonzero = 0
            for dir in directions:
                if float(dir) != 0:
                    nonzero += 1

            if nonzero == 0:
                return False, "At least one direction coordinate must be non-zero"
            return True, ""
        except:
            return False, "Invalid direction coordinates"

    def _check_orientation_validity(self, input):
        """Check input string if it is a valid orientation."""
        orientation = input.split(",")

        if len(orientation) != 2:
            return False, "Invalid number of spherical coordinates"

        try:
            float(orientation[0])
        except:
            return False, "Invalid azimuth value"

        try:
            float(orientation[1])
            return True, ""
        except:
            return False, "Invalid elevation value"

    def _check_profile_entries_validity(self, input):
        """Check input array if all elements are valid."""
        if not isinstance(input, list):
            return False, "Invalid entries argument"

        try:
            for i, entry in enumerate(input):
                if len(entry) != 2:
                    return False, f"Invalid entry {i}: Wrong number of args"
                elif entry[0] <= 0:
                    return False, f"Invalid entry {i}: Frequencies must be greater than 0"
                elif entry[1] <= 0:
                    return False, f"Invalid entry {i}: Amplitudes must be greater than 0"
            return True, ""
        except TypeError:
            return False, f"Invalid entry {i}: Invalid freq/ampl"

    def _add_profile_entries(self, request, entries):
        """Add the entries to the request."""
        for e in entries:
            entry = request.randomVibeProfileEntries.add()
            entry.freq = e[0]
            entry.ampl = e[1]

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
        try:
            if project == "":
                raise SherlockCreateLifePhaseError(message="Invalid Project Name")
            elif phase_name == "":
                raise SherlockCreateLifePhaseError(message="Invalid Phase Name")
            elif (self.TIME_UNIT_LIST is not None) and (duration_units not in self.TIME_UNIT_LIST):
                raise SherlockCreateLifePhaseError(message="Invalid Duration Unit Specified")
            elif duration <= 0.0:
                raise SherlockCreateLifePhaseError(message="Duration Must Be Greater Than 0")
            elif (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockCreateLifePhaseError(message="Invalid Cycle Type")
            elif num_of_cycles <= 0.0:
                raise SherlockCreateLifePhaseError(
                    message="Number of Cycles Must Be Greater Than 0"
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
        try:
            if project == "":
                raise SherlockAddRandomVibeEventError(message="Invalid Project Name")
            elif phase_name == "":
                raise SherlockAddRandomVibeEventError(message="Invalid Phase Name")
            elif event_name == "":
                raise SherlockAddRandomVibeEventError(message="Invalid Event Name")
            elif (self.TIME_UNIT_LIST is not None) and (duration_units not in self.TIME_UNIT_LIST):
                raise SherlockAddRandomVibeEventError(message="Invalid Duration Unit Specified")
            elif duration <= 0.0:
                raise SherlockAddRandomVibeEventError(message="Duration Must Be Greater Than 0")
            elif (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockAddRandomVibeEventError(message="Invalid Cycle Type")
            elif num_of_cycles <= 0.0:
                raise SherlockAddRandomVibeEventError(
                    message="Number of Cycles Must Be Greater Than 0"
                )
        except SherlockAddRandomVibeEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        try:
            valid1, message1 = self._check_load_direction_validity(load_direction)
            valid2, message2 = self._check_orientation_validity(orientation)
            if not valid1:
                raise SherlockAddRandomVibeEventError(message=message1)
            elif (self.RV_PROFILE_LIST is not None) and (profile_type not in self.RV_PROFILE_LIST):
                raise SherlockAddRandomVibeEventError(
                    message="Valid profile type for a random event can only be Uniaxial"
                )
            elif not valid2:
                raise SherlockAddRandomVibeEventError(message=message2)
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
            The name of new life phase.
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
        try:
            if project == "":
                raise SherlockAddRandomVibeProfileError(message="Invalid Project Name")
            elif phase_name == "":
                raise SherlockAddRandomVibeProfileError(message="Invalid Phase Name")
            elif event_name == "":
                raise SherlockAddRandomVibeProfileError(message="Invalid Event Name")
            elif profile_name == "":
                raise SherlockAddRandomVibeProfileError(message="Invalid Profile Name")
            elif (self.FREQ_UNIT_LIST is not None) and (freq_units not in self.FREQ_UNIT_LIST):
                raise SherlockAddRandomVibeProfileError(message="Invalid Frequency Unit")
            elif (self.AMPL_UNIT_LIST is not None) and (ampl_units not in self.AMPL_UNIT_LIST):
                raise SherlockAddRandomVibeProfileError(message="Invalid Amplitude Type")
        except SherlockAddRandomVibeProfileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        try:
            valid1, message1 = self._check_profile_entries_validity(random_vibe_profile_entries)
            if not valid1:
                raise SherlockAddRandomVibeProfileError(message=message1)
        except SherlockAddRandomVibeProfileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

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

        self._add_profile_entries(request, random_vibe_profile_entries)

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
            The name of new life phase.
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
        try:
            if project == "":
                raise SherlockAddThermalEventError(message="Invalid Project Name")
            elif phase_name == "":
                raise SherlockAddThermalEventError(message="Invalid Phase Name")
            elif event_name == "":
                raise SherlockAddThermalEventError(message="Invalid Event Name")
            elif (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockAddThermalEventError(message="Invalid Cycle Type")
            elif num_of_cycles <= 0.0:
                raise SherlockAddThermalEventError(
                    message="Number of Cycles Must Be Greater Than 0"
                )
            elif (self.CYCLE_STATE_LIST is not None) and (cycle_state not in self.CYCLE_STATE_LIST):
                raise SherlockAddThermalEventError(message="Invalid Cycle State")
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
