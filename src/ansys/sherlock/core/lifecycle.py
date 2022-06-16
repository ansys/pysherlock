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
