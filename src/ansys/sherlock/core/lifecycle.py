"""Module for basic project services on client-side."""
import SherlockLifeCycleService_pb2
import SherlockLifeCycleService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockAddRandomVibeEventError
from ansys.sherlock.core.grpc_stub import GrpcStub

DURATION_UNIT_LIST = ["ms", "sec", "min", "hr", "day", "year"]
CYCLE_TYPE_LIST = ["COUNT", "DUTY CYCLE", "PER YEAR", "PER DAY", "PER HOUR", "PER MIN", "PER SEC"]


class Lifecycle(GrpcStub):
    """Contains methods from the Sherlock Lifecycle Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockLifecycleService."""
        self.channel = channel
        self.stub = SherlockLifeCycleService_pb2_grpc.SherlockLifeCycleServiceStub(channel)

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

    def add_random_vibe_event(
        self,
        project,
        phaseName,
        eventName,
        duration,
        durationUnits,
        numOfCycles,
        cycleType,
        orientation,
        profileType,
        loadDirection,
        description=None,
    ):
        """Add a new random vibe event to a life cycle.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        phaseName : str, required
            The name of new life phase.
        eventName : str, required
            Name of the random vibe event.
        description : str, optional
            Description of new life phase.
        duration : double, required
            Event duration length.
        durationUnits : str, required
            Event duration length units.
        numOfCycles : double, required
            Number of cycles defined for new life phase.
        cycleType : str, required
            The cycle type. For example: "COUNT", "DUTY CYCLE", "PER YEAR", "PER HOUR", etc.
        orientation : str, required
            PCB orientation in the format of azimuth, elevation. Example: 30,15
        profileType : str, required
            Random load profile type. Example valid value is "Uniaxial".
        loadDirection : str, required
            Load direction in the format of x,y,z. Example: 0,0,1
        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        ""Example: There exists a project named 'Test' with a life cycle named 'Example""
        >>> sherlock.lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1"
            1.5,
            "sec",
            4.0,
            "PER SEC",
            "45,45",
            "Uniaxial"
            "2,4,5",
        )
        """
        try:
            if project == "":
                raise SherlockAddRandomVibeEventError(message="Invalid Project Name")
            elif phaseName == "":
                raise SherlockAddRandomVibeEventError(message="Invalid Phase Name")
            elif eventName == "":
                raise SherlockAddRandomVibeEventError(message="Invalid Event Name")
            elif durationUnits not in DURATION_UNIT_LIST:
                raise SherlockAddRandomVibeEventError(message="Invalid Duration Unit Specified")
            elif duration <= 0.0:
                raise SherlockAddRandomVibeEventError(message="Duration Must Be Greater Than 0")
            elif cycleType not in CYCLE_TYPE_LIST:
                raise SherlockAddRandomVibeEventError(message="Invalid Cycle Type")
            elif numOfCycles <= 0.0:
                raise SherlockAddRandomVibeEventError(
                    message="Number of Cycles Must Be Greater Than 0"
                )
        except SherlockAddRandomVibeEventError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e

        try:
            valid1, message1 = self._check_load_direction_validity(loadDirection)
            valid2, message2 = self._check_orientation_validity(orientation)
            if not valid1:
                raise SherlockAddRandomVibeEventError(message=message1)
            elif profileType != "Uniaxial":
                raise SherlockAddRandomVibeEventError(
                    message="Valid profile type for a Random event can only be Uniaxial"
                )
            elif not valid2:
                raise SherlockAddRandomVibeEventError(message=message2)
        except SherlockAddRandomVibeEventError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e

        if description is None:
            description = ""

        request = SherlockLifeCycleService_pb2.AddRandomVibeEventRequest(
            project=project,
            phaseName=phaseName,
            eventName=eventName,
            description=description,
            duration=duration,
            durationUnits=durationUnits,
            numOfCycles=numOfCycles,
            cycleType=cycleType,
            orientation=orientation,
            profileType=profileType,
            loadDirection=loadDirection,
        )

        response = self.stub.addRandomVibeEvent(request)

        returnCode = response.returnCode

        try:
            if returnCode.value == -1:
                if returnCode.message == "":
                    raise SherlockAddRandomVibeEventError(errorArray=response.errors)
                else:
                    raise SherlockAddRandomVibeEventError(message=returnCode.message)
            else:
                LOG.info(returnCode.message)
                return
        except SherlockAddRandomVibeEventError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e
