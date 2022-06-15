"""Module for lifecycle services on client-side."""
import SherlockLifeCycleService_pb2
import SherlockLifeCycleService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockAddThermalProfileError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Lifecycle(GrpcStub):
    """Contains methods from the Sherlock Lifecycle Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockLifecycleService."""
        self.channel = channel
        self.stub = SherlockLifeCycleService_pb2_grpc.SherlockLifeCycleServiceStub(channel)
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
        self.TIME_UNIT_LIST = ["ms", "sec", "min", "hr", "day", "year"]
        self.TEMP_UNIT_LIST = ["C", "F", "K"]
        self.TYPE_LIST = ["HOLD", "RAMP"]

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

    def _check_random_profile_entries_validity(self, input):
        """Check input array if all elements are valid for random entries."""
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

    def _check_thermal_profile_entries_validity(self, input):
        """Check input array if all elements are valid for thermal entries."""
        if not isinstance(input, list):
            return False, "Invalid entries argument"

        try:
            for i, entry in enumerate(input):
                if len(entry) != 4:
                    return False, f"Invalid entry {i}: Wrong number of args"
                elif not isinstance(str, entry[0]):
                    return False, f"Invalid entry {i}: Invalid step name"
                elif entry[1] not in self.TYPE_LIST:
                    return False, f"Invalid entry {i}: Invalid step type"
                elif entry[2] <= 0:
                    return False, f"Invalid entry{i}: Time must be greater than 0"
                elif not (isinstance(int, entry[3]) or isinstance(float, entry[3])):
                    return False, f"invalid entry {i}: Invalid temp"
        except TypeError:
            return False, f"Invalid entry {i}: Invalid time"

    def _add_random_vibe_profile_entries(self, request, entries):
        """Add the random vibe entries to the request."""
        for e in entries:
            entry = request.randomProfileEntries.add()
            entry.freq = e[0]
            entry.ampl = e[1]

    def _add_thermal_profile_entries(self, request, entries):
        """Add the thermal entries to the request."""
        for e in entries:
            entry = request.thermalProfileEntries.add()
            entry.step = e[0]
            entry.type = e[1]
            entry.time = e[2]
            entry.temp = e[3]

    def add_thermal_profile(
        self,
        project,
        phase_name,
        event_name,
        profile_name,
        time_units,
        temp_units,
        thermal_profile_entries,
    ):
        """Define and add a new thermal life cycle event profile.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        phase_name : str, required
            The name of new life phase.
        event_name : str, required
            Name of the random vibe event.
        profile_name : str, required
            Name of the thermal profile.
        time_units : str, required
            Time Units.
        temp_units : str, required
            Temperature Units.
        thermal_profile_entries : (String, String, double, double) list, required
            List of (step, type, time, temp) entries

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.lifecycle.add_thermal_profile(
            "Test",
            "Example",
            "Event1"
            "Profile1",
            "sec",
            "F",
            [
                ("Increase", "RAMP", 40, 40),
                ("Steady", "HOLD", 20, 20),
                ("Back", "RAMP", 20, 40),
            ],
        )
        """
        try:
            if project == "":
                raise SherlockAddThermalProfileError(message="Invalid Project Name")
            elif phase_name == "":
                raise SherlockAddThermalProfileError(message="Invalid Phase Name")
            elif event_name == "":
                raise SherlockAddThermalProfileError(message="Invalid Event Name")
            elif profile_name == "":
                raise SherlockAddThermalProfileError(message="Invalid Profile Name")
            elif time_units not in self.TIME_UNIT_LIST:
                raise SherlockAddThermalProfileError(message="Invalid Time Unit")
            elif temp_units not in self.TEMP_UNIT_LIST:
                raise SherlockAddThermalProfileError(message="Invalid Temperature Unit")
        except SherlockAddThermalProfileError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e

        try:
            valid1, message1 = self._check_thermal_profile_entries_validity(thermal_profile_entries)
            if not valid1:
                raise SherlockAddThermalProfileError(message=message1)
        except SherlockAddThermalProfileError as e:
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
            timeUnits=time_units,
            temp_units=temp_units,
        )

        self._add_thermal_profile_entries(request, thermal_profile_entries)

        response = self.stub.addRandomProfile(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddThermalProfileError(errorArray=response.errors)
                else:
                    raise SherlockAddThermalProfileError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockAddThermalProfileError as e:
            for error in e.strItr():
                LOG.error(error)
            raise e
