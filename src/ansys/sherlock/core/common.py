# © 2023 ANSYS, Inc. All rights reserved

"""Module for running the gRPC APIs in the Sherlock Common service."""
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
    """Contains methods from the Sherlock Common service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for the Sherlock Common service."""
        super().__init__(channel)
        self.stub = SherlockCommonService_pb2_grpc.SherlockCommonServiceStub(channel)

    def check(self):
        """Perform a health check on the gRPC connection.

        Returns
        -------
        bool
            Whether the Sherlock client is connected via gRPC.

        """
        if not self._is_connection_up():
            LOG.error("Health check failed.")
            return False
        else:
            LOG.info("Connection is healthy.")
            return True

    def is_sherlock_client_loading(self):
        """Check if the Sherlock client is opened and done initializing.

        Returns
        -------
        bool
            Whether the Sherlock client is opened and done initializing.

        """
        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
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
        close_sherlock_client : bool, optional
            Whether to close the Sherlock client when the gRPC connection is closed. The default
            is ``False``, in which case the Sherlock client remains open when the gRPC connection
            is closed.
        """
        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        try:
            exit_message = SherlockCommonService_pb2.ExitRequest()
            exit_message.closeSherlockClient = close_sherlock_client
            response = self.stub.exit(exit_message)
            LOG.info(str(response))
        except SherlockCommonServiceError as err:
            LOG.error("Exit error: ", str(err))

    def list_units(self, unitType):
        """List units for a unit type.

        Parameters
        ----------
        unitType : ListUnitsRequestUnitType
            Unit type.

        Returns
        -------
        str
            Units for the unit type.
        """
        if unitType == "":
            raise SherlockCommonServiceError(message="Unit type is missing.")

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return ""

        request = SherlockCommonService_pb2.ListUnitsRequest(unitType=unitType)

        try:
            response = self.stub.listUnits(request)
            return_code = response.returnCode
            if return_code.value == -1:
                raise SherlockCommonServiceError(message=return_code.message)
        except SherlockCommonServiceError as e:
            raise e

        return response.units

    def list_solder_materials(self):
        """List valid solders.

        Returns
        -------
        list
            List of valid solder names.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.common.list_solder_materials()
        """
        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        request = SherlockCommonService_pb2.GetSoldersRequest()
        response = self.stub.getSolders(request)

        return response.solderName
