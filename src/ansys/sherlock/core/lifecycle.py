"""Module for lifecycle services on client-side."""
import SherlockLifeCycleService_pb2
import SherlockLifeCycleService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockCreateLifePhaseError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Lifecycle(GrpcStub):
    """Contains methods from the Sherlock Lifecycle Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockLifeCycleService."""
        self.channel = channel
        self.stub = SherlockLifeCycleService_pb2_grpc.SherlockLifeCycleServiceStub(channel)
        self.TIME_UNIT_LIST = ["ms", "sec", "min", "hr", "day", "year"]
        self.CYCLE_TYPE_LIST = [
            "COUNT",
            "DUTY CYCLE",
            "PER YEAR",
            "PER DAY",
            "PER HOUR",
            "PER MIN",
            "PER SEC",
        ]

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
        description : str, optional
            Description of new life phase.
        duration : double, required
            Event duration length.
        duration_units : str, required
            Event duration length units.
        num_of_cycles : double, required
            Number of cycles defined for new life phase.
        cycle_type : str, required
            The cycle type. For example: "COUNT", "DUTY CYCLE", "PER YEAR", "PER HOUR", etc.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
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
            elif duration_units not in self.TIME_UNIT_LIST:
                raise SherlockCreateLifePhaseError(message="Invalid Duration Unit Specified")
            elif duration <= 0.0:
                raise SherlockCreateLifePhaseError(message="Duration Must Be Greater Than 0")
            elif cycle_type not in self.CYCLE_TYPE_LIST:
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
