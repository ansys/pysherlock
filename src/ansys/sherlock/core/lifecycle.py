"""Module for lifecycle services on client-side."""
import SherlockLifeCycleService_pb2
import SherlockLifeCycleService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockAddHarmonicEventError, SherlockCreateLifePhaseError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Lifecycle(GrpcStub):
    """Contains methods from the Sherlock Lifecycle Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockLifeCycleService."""
        self.channel = channel
        self.stub = SherlockLifeCycleService_pb2_grpc.SherlockLifeCycleServiceStub(channel)
        self.TIME_UNIT_LIST = None
        self.CYCLE_TYPE_LIST = None

        if self._is_connection_up():
            duration_unit_request = SherlockLifeCycleService_pb2.ListDurationUnitsRequest()
            duration_unit_response = self.stub.listDurationUnits(duration_unit_request)
            if duration_unit_response.returnCode.value == 0:
                self.TIME_UNIT_LIST = duration_unit_response.durationUnits

            cycle_type_request = SherlockLifeCycleService_pb2.ListLCTypesRequest()
            cycle_type_response = self.stub.listLifeCycleTypes(cycle_type_request)
            if cycle_type_response.returnCode.value == 0:
                self.CYCLE_TYPE_LIST = cycle_type_response.types

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
            project="Test"
        )
        >>> sherlock.lifecycle.create_life_phase(
            "Test",
            "Example",
            1.5,
            "sec",
            4.0,
            "PER SEC",
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
            for error in e.strItr():
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
                    raise SherlockCreateLifePhaseError(errorArray=response.errors)
                else:
                    raise SherlockCreateLifePhaseError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockCreateLifePhaseError as e:
            for error in e.strItr():
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
            Number of cycles defined for new life phase.
        cycle_type : str, required
            The cycle type. For example: "COUNT", "DUTY CYCLE", "PER YEAR", "PER HOUR", etc.
        sweep_rate : double, required
            Sweep rate for the harmonic event
        orientation : str, required
            PCB orientation in the format of azimuth, elevation. Example: 30,15
        profile_type : str, required
            Random load profile type. Example valid value is "Uniaxial".
        load_direction: str, required
            Load direction in the format of x,y,z. Example: 0,0,1
        description : str, optional
            Description of the random vibe event.
        Examples
        --------
        TODO: Update examples
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
            "sec",
            4.0,
            "COUNT",
        )
        >>> sherlock.lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1"
            1.5,
            "sec",
            4.0,
            "PER MIN",
            "45,45",
            "Uniaxial"
            "2,4,5",
        )
        """
        try:
            if project == "":
                raise SherlockAddHarmonicEventError(message="Invalid Project Name")
            elif phase_name == "":
                raise SherlockAddHarmonicEventError(message="Invalid Phase Name")
            elif event_name == "":
                raise SherlockAddHarmonicEventError(message="Invalid Event Name")
            elif (self.TIME_UNIT_LIST is not None) and (duration_units not in self.TIME_UNIT_LIST):
                raise SherlockAddHarmonicEventError(message="Invalid Duration Unit Specified")
            elif duration <= 0.0:
                raise SherlockAddHarmonicEventError(message="Duration Must Be Greater Than 0")
            elif (self.CYCLE_TYPE_LIST is not None) and (cycle_type not in self.CYCLE_TYPE_LIST):
                raise SherlockAddHarmonicEventError(message="Invalid Cycle Type")
            elif num_of_cycles <= 0.0:
                raise SherlockAddHarmonicEventError(
                    message="Number of Cycles Must Be Greater Than 0"
                )
            elif sweep_rate <= 0.0:
                raise SherlockAddHarmonicEventError(message="Sweep Rate must be greater than 0")
        except SherlockAddHarmonicEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        try:
            valid1, message1 = self._check_load_direction_validity(load_direction)
            valid2, message2 = self._check_orientation_validity(orientation)
            if not valid1:
                raise SherlockAddHarmonicEventError(message=message1)
            elif not valid2:
                raise SherlockAddHarmonicEventError(message=message2)
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
                    raise SherlockAddHarmonicEventError(errorArray=response.errors)
                else:
                    raise SherlockAddHarmonicEventError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddHarmonicEventError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e
