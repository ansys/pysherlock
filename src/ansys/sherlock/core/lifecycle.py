"""Module for basic project services on client-side."""
import SherlockLifeCycleService_pb2
import SherlockLifeCycleService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockAddRandomVibeProfileError
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
        self.FREQ_UNIT_LIST = ["HZ", "KHZ", "MHZ", "GHZ"]
        self.AMPL_UNIT_LIST = ["G2/Hz", "m2/s4/Hz", "mm2/s4/Hz", "in2/s4/Hz", "ft2/s4/Hz"]

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
            entry = request.randomProfileEntries.add()
            entry.freq = e[0]
            entry.ampl = e[1]

    def add_random_vibe_profile(
        self,
        project,
        phase_name,
        event_name,
        profile_name,
        freq_units,
        ampl_units,
        random_profile_entries,
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
        random_profile_entries : (double, double) list, required
            List of (frequency, amplitude) entries

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()

        >>> sherlock.lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1"
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
            elif freq_units not in self.FREQ_UNIT_LIST:
                raise SherlockAddRandomVibeProfileError(message="Invalid Frequency Unit")
            elif ampl_units not in self.AMPL_UNIT_LIST:
                raise SherlockAddRandomVibeProfileError(message="Invalid Amplitude Type")
        except SherlockAddRandomVibeProfileError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e

        try:
            valid1, message1 = self._check_profile_entries_validity(random_profile_entries)
            if not valid1:
                raise SherlockAddRandomVibeProfileError(message=message1)
        except SherlockAddRandomVibeProfileError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        request = SherlockLifeCycleService_pb2.AddRandomProfileRequest(
            project=project,
            phaseName=phase_name,
            eventName=event_name,
            profileName=profile_name,
            freqUnits=freq_units,
            amplUnits=ampl_units,
        )

        self._add_profile_entries(request, random_profile_entries)

        response = self.stub.addRandomProfile(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddRandomVibeProfileError(errorArray=response.errors)
                else:
                    raise SherlockAddRandomVibeProfileError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddRandomVibeProfileError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e
