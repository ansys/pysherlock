"""Module for basic project services on client-side."""
import SherlockLifeCycleService_pb2
import SherlockLifeCycleService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockAddRandomVibeProfileError
from ansys.sherlock.core.grpc_stub import GrpcStub

DURATION_UNIT_LIST = ["ms", "sec", "min", "hr", "day", "year"]
CYCLE_TYPE_LIST = ["COUNT", "DUTY CYCLE", "PER YEAR", "PER DAY", "PER HOUR", "PER MIN", "PER SEC"]

FREQ_UNIT_LIST = ["HZ", "KHZ", "MHZ", "GHZ"]
AMPL_UNIT_LIST = ["G2/Hz", "m2/s4/Hz", "mm2/s4/Hz", "in2/s4/Hz", "ft2/s4/Hz"]


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

    def _check_profile_entries_validity(self, input):
        """Check input array if all elements are valid."""
        try:
            for i in input:
                if len(i) != 2:
                    return False, "Invalid entries"
                elif i[0] <= 0:
                    return False, "Frequencies must be greater than 0"
                elif i[1] <= 0:
                    return False, "Amplitudes must be greater than 0"
            return True, ""
        except:
            return False, "Invalid entry arguments"

    def add_random_vibe_profile(
        self,
        project,
        phaseName,
        eventName,
        profileName,
        freqUnits,
        amplUnits,
        randomProfileEntries,
    ):
        """Add a new random vibe profile to a random vibe event.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        phaseName : str, required
            The name of new life phase.
        eventName : str, required
            Name of the random vibe event.
        pofileName : str, required
            Name of the random vibe profile.
        freqUnits : str, required
            Frequency Units.
        amplUnits : str, required
            Amplitude Units.
        randomProfileEntries : (double, double) list, required
            List of (frequency, amplitude) entries

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
        TODO: Fix the example
        """
        try:
            if project == "":
                raise SherlockAddRandomVibeProfileError(message="Invalid Project Name")
            elif phaseName == "":
                raise SherlockAddRandomVibeProfileError(message="Invalid Phase Name")
            elif eventName == "":
                raise SherlockAddRandomVibeProfileError(message="Invalid Event Name")
            elif profileName == "":
                raise SherlockAddRandomVibeProfileError(message="Invalid Profile Name")
            elif freqUnits not in FREQ_UNIT_LIST:
                raise SherlockAddRandomVibeProfileError(message="Invalid Frequency Unit")
            elif amplUnits not in AMPL_UNIT_LIST:
                raise SherlockAddRandomVibeProfileError(message="Invalid Amplitude Type")
        except SherlockAddRandomVibeProfileError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e

        try:
            valid1, message1 = self._check_profile_entries_validity(randomProfileEntries)
            if not valid1:
                raise SherlockAddRandomVibeProfileError(message=message1)
        except SherlockAddRandomVibeProfileError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e

        if description is None:
            description = ""

        request = SherlockLifeCycleService_pb2.AddRandomProfileRequest(
            project=project,
            phaseName=phaseName,
            eventName=eventName,
            profileName=profileName,
            freqUnits=freqUnits,
            amplUnits=amplUnits,
            randomProfileEntries=randomProfileEntries,
        )
        # TODO: Investigate how to handle the entries

        response = self.stub.addRandomProfile(request)

        returnCode = response.returnCode

        try:
            if returnCode.value == -1:
                if returnCode.message == "":
                    raise SherlockAddRandomVibeProfileError(errorArray=response.errors)
                else:
                    raise SherlockAddRandomVibeProfileError(message=returnCode.message)
            else:
                LOG.info(returnCode.message)
                return
        except SherlockAddRandomVibeProfileError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e
