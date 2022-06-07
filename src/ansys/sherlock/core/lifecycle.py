"""Module for lifecycle services on client-side."""
import SherlockLifeCycleService_pb2
import SherlockLifeCycleService_pb2_grpc
import grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockCreateLifePhaseError

DURATION_UNIT_LIST = ["ms", "sec", "min", "hr", "day", "year"]
CYCLE_TYPE_LIST = ["COUNT", "DUTY CYCLE", "PER YEAR", "PER DAY", "PER HOUR", "PER MIN", "PER SEC"]


def create_life_phase(
    project, phaseName, duration, durationUnits, numOfCycles, cycleType, description=None
):
    """Create a new lifephase.

    Parameters
    ----------
    project : str, required
        Sherlock project name.
    phaseName : str, required
        The name of new life phase.
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

    Examples
    --------
    TODO: write the examples
    """
    try:
        if phaseName == "":
            raise SherlockCreateLifePhaseError("Invalid Phase Name")
        elif duration < 0.0:
            raise SherlockCreateLifePhaseError("Duration Must Be Greater Than 0")
        elif durationUnits not in DURATION_UNIT_LIST:
            raise SherlockCreateLifePhaseError("Invalid Duration Units")
        elif numOfCycles < 0.0:
            raise SherlockCreateLifePhaseError("Number of Cycles Must Be Greater Than 0")
        elif cycleType not in CYCLE_TYPE_LIST:
            raise SherlockCreateLifePhaseError("Invalid Cycle Type")
    except SherlockCreateLifePhaseError as e:
        LOG.error(str(e))
        return -1, str(e)

    if description is None:
        description = ""

    request = SherlockLifeCycleService_pb2.CreateLifePhaseRequest(
        project=project,
        phaseName=phaseName,
        description=description,
        duration=duration,
        durationUnits=durationUnits,
        numOfCycles=numOfCycles,
        cycleType=cycleType,
    )

    channel = grpc.insecure_channel("localhost:9090")
    stub = SherlockLifeCycleService_pb2_grpc.SherlockLifeCycleService(channel)

    response = stub.createLifePhase(request)

    returnCode = response.returnCode

    try:
        if returnCode.value == -1:
            raise SherlockCreateLifePhaseError(returnCode.message)
        else:
            LOG.info(returnCode.message)
            return returnCode.value, returnCode.message
    except SherlockCreateLifePhaseError as e:
        LOG.error(str(e))
        return returnCode.value, str(e)
