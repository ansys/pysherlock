# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

"""Module for running the gRPC APIs in the SherlockCommonService."""
try:
    import SherlockCommonService_pb2
    import SherlockCommonService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockCommonServiceError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Common(GrpcStub):
    """Contains methods from the Sherlock Common Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockCommonService."""
        self.channel = channel
        self.stub = SherlockCommonService_pb2_grpc.SherlockCommonServiceStub(channel)

    def check(self):
        """Perform a health check on the gRPC connection."""
        if not self._is_connection_up():
            LOG.error("Health check failed.")
            return False
        else:
            LOG.info("Connection is up.")
            return True

    def is_sherlock_client_loading(self):
        """Checks if the Sherlock Client (if opened) is still initializing."""
        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        message = SherlockCommonService_pb2.IsSherlockClientLoadingRequest()
        response = self.stub.isSherlockClientLoading(message)

        if response.value == 0:
            LOG.info("Sherlock client has finished initializing.")
            return True
        else:
            LOG.error("Sherlock client has not finished initializing.")
            return False

    def exit(self, close_sherlock_client=False):
        """Close the gRPC connection.

        Parameters
        ----------
        close_sherlock_client : boolean, optional
            If set to True and if the Sherlock client is open, then closes
            the Sherlock client also.
        """
        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        try:
            exit_message = SherlockCommonService_pb2.ExitRequest()
            exit_message.closeSherlockClient = close_sherlock_client
            response = self.stub.exit(exit_message)
            LOG.info(str(response))
        except SherlockCommonServiceError as err:
            LOG.error("Exit error: ", str(err))

    def list_units(self, unitType):
        """List valid units for the provided unit type.

        Parameters
        ----------
        unitType : string, required
            The unit type. Valid types are: ACCEL_DENSITY, ACCELERATION, AREA, BANDWIDTH,
            CAPACITANCE, CTE, CURRENT, DENSITY, DISP_DENSITY, FORCE, FREQUENCY, INDUCTANCE, LENGTH,
            POWER, RESISTANCE, SIZE, SPECIFIC_HEAT, STRAIN, STRESS, TEMPERATURE,
            THERMAL_CONDUCTIVITY, THERMAL_RESISTANCE, TIME, VELOCITY, VELOCITY_DENSITY, VOLTAGE,
            VOLUME, WEIGHT
        """

        if unitType == "":
            raise SherlockCommonServiceError(message="Missing valid unit type")
        elif unitType == "ACCEL_DENSITY":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.ACCEL_DENSITY
        elif unitType == "ACCELERATION":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.ACCELERATION
        elif unitType == "AREA":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.AREA
        elif unitType == "BANDWIDTH":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.BANDWIDTH
        elif unitType == "CAPACITANCE":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.CAPACITANCE
        elif unitType == "CTE":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.CTE
        elif unitType == "CURRENT":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.CURRENT
        elif unitType == "DENSITY":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.DENSITY
        elif unitType == "DISP_DENSITY":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.DISP_DENSITY
        elif unitType == "FORCE":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.FORCE
        elif unitType == "FREQUENCY":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.FREQUENCY
        elif unitType == "INDUCTANCE":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.INDUCTANCE
        elif unitType == "LENGTH":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.LENGTH
        elif unitType == "POWER":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.POWER
        elif unitType == "RESISTANCE":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.RESISTANCE
        elif unitType == "SIZE":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.SIZE
        elif unitType == "SPECIFIC_HEAT":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.SPECIFIC_HEAT
        elif unitType == "STRAIN":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.STRAIN
        elif unitType == "STRESS":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.STRESS
        elif unitType == "TEMPERATURE":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.TEMPERATURE
        elif unitType == "THERMAL_CONDUCTIVITY":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.THERMAL_CONDUCTIVITY
        elif unitType == "THERMAL_RESISTANCE":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.THERMAL_RESISTANCE
        elif unitType == "TIME":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.TIME
        elif unitType == "VELOCITY":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.VELOCITY
        elif unitType == "VELOCITY_DENSITY":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.VELOCITY_DENSITY
        elif unitType == "VOLTAGE":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.VOLTAGE
        elif unitType == "VOLUME":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.VOLUME
        elif unitType == "WEIGHT":
            unitType = SherlockCommonService_pb2.ListUnitsRequest.WEIGHT
        else:
            raise SherlockCommonServiceError(message=f"Invalid unit type '{unitType}' specified")

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return ""

        request = SherlockCommonService_pb2.ListUnitsRequest(
            unitType=unitType
        )

        try:
            response = self.stub.listUnits(request)

            return_code = response.returnCode

            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockCommonServiceError(error_array=response.errors)

                raise SherlockCommonServiceError(message=return_code.message)

        except SherlockCommonServiceError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        return response.units
