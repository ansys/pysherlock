"""Module for lifecycle services on client-side."""
import SherlockLifeCycleService_pb2
import SherlockLifeCycleService_pb2_grpc
import grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockAddRandomVibeEventError

DURATION_UNIT_LIST = ["ms", "sec", "min", "hr", "day", "year"]
CYCLE_TYPE_LIST = ["COUNT", "DUTY CYCLE", "PER YEAR", "PER DAY", "PER HOUR", "PER MIN", "PER SEC"]


def add_random_vibe_event(
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
    """Create a new lifephase.

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
    TODO: write the examples
    """
    # TODO: See just how far we need to go with checks
    try:
        if project == "":
            raise SherlockAddRandomVibeEventError(message="Invalid Project Name")
        elif phaseName == "":
            raise SherlockAddRandomVibeEventError(message="Invalid Phase Name")
        elif durationUnits not in DURATION_UNIT_LIST:
            raise SherlockAddRandomVibeEventError(message="Invalid Duration Unit Specified")
        elif duration <= 0.0:
            raise SherlockAddRandomVibeEventError(message="Duration Must Be Greater Than 0")
        elif cycleType not in CYCLE_TYPE_LIST:
            raise SherlockAddRandomVibeEventError(message="Invalid Cycle Type")
        elif numOfCycles <= 0.0:
            raise SherlockAddRandomVibeEventError(message="Number of Cycles Must Be Greater Than 0")
    except SherlockAddRandomVibeEventError as e:
        for error in e.strItr():
            LOG.error(error)
        return -1, e.strItr()[0]

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

    channel = grpc.insecure_channel("localhost:9090")
    stub = SherlockLifeCycleService_pb2_grpc.SherlockLifeCycleServiceStub(channel)

    response = stub.addRandomVibeEvent(request)

    returnCode = response.returnCode

    try:
        if returnCode.value == -1:
            if returnCode.message == "":
                raise SherlockAddRandomVibeEventError(errorArray=response.errors)
            else:
                raise SherlockAddRandomVibeEventError(message=returnCode.message)
        else:
            LOG.info(returnCode.message)
            return returnCode.value, returnCode.message
    except SherlockAddRandomVibeEventError as e:
        for error in e.strItr():
            LOG.error(error)
        return returnCode.value, e.strItr()[0]
