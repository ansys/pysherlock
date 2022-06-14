"""Module for lifecycle services on client-side."""
import SherlockLifeCycleService_pb2
import SherlockLifeCycleService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockAddThermalEventError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Lifecycle(GrpcStub):
    """Contains methods from the Sherlock Lifecycle Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockLifecycleService."""
        self.channel = channel
        self.stub = SherlockLifeCycleService_pb2_grpc.SherlockLifeCycleServiceStub(channel)
        self.DURATION_UNIT_LIST = ["ms", "sec", "min", "hr", "day", "year"]
        self.CYCLE_TYPE_LIST = [
            "COUNT",
            "DUTY CYCLE",
            "PER YEAR",
            "PER DAY",
            "PER HOUR",
            "PER MIN",
            "PER SEC",
        ]
        self.CYCLE_STATE_LIST = ["OPERATING", "STORAGE"]

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

    def add_thermal_event(
        self,
        project,
        phase_name,
        event_name,
        num_of_cycles,
        cycle_type,
        cycle_state,
        description=None,
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
            Number of cycles defined for new life phase.
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
        >>> sherlock.lifecycle.add_thermal_event(
            "Test",
            "Example",
            "Event1"
            4.0,
            "PER SEC",
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
            elif cycle_type not in self.CYCLE_TYPE_LIST:
                raise SherlockAddThermalEventError(message="Invalid Cycle Type")
            elif num_of_cycles <= 0.0:
                raise SherlockAddThermalEventError(
                    message="Number of Cycles Must Be Greater Than 0"
                )
            elif cycle_state not in self.CYCLE_STATE_LIST:
                raise SherlockAddThermalEventError(message="Invalid Cycle State")
        except SherlockAddThermalEventError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e

        if description is None:
            description = ""

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
                    raise SherlockAddThermalEventError(errorArray=response.errors)
                else:
                    raise SherlockAddThermalEventError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddThermalEventError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e
