# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

"""Module for running the gRPC APIs in the Sherlock Common service."""

import grpc

from ansys.sherlock.core.types.common_types import ListUnitsRequestUnitType

try:
    import SherlockCommonService_pb2
    import SherlockCommonService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockCommonServiceError, SherlockNoGrpcConnectionException
from ansys.sherlock.core.grpc_stub import GrpcStub
from ansys.sherlock.core.utils.version_check import require_version


class Common(GrpcStub):
    """Contains methods from the Sherlock Common service."""

    def __init__(self, channel: grpc.Channel, server_version: int):
        """Initialize a gRPC stub for the Sherlock Common service."""
        super().__init__(channel, server_version)
        self.stub = SherlockCommonService_pb2_grpc.SherlockCommonServiceStub(channel)

    @require_version()
    def check(self) -> bool:
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

    @require_version()
    def is_sherlock_client_loading(self) -> bool:
        """Check if the Sherlock client is opened and done initializing.

        Available Since: 2023R2

        Returns
        -------
        bool
            Whether the Sherlock client is opened and done initializing.
        """
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        message = SherlockCommonService_pb2.IsSherlockClientLoadingRequest()
        response = self.stub.isSherlockClientLoading(message)

        if response.value == 0:
            LOG.info("Sherlock client has finished initializing.")
            return True
        else:
            LOG.error("Sherlock client has not finished initializing.")
            return False

    @require_version()
    def exit(self, close_sherlock_client: bool = False):
        """Close the gRPC connection.

        Available Since: 2023R1

        Parameters
        ----------
        close_sherlock_client : bool, optional
            Whether to close the Sherlock client when the gRPC connection is closed. The default
            is ``False``, in which case the Sherlock client remains open when the gRPC connection
            is closed.
        """
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        try:
            exit_message = SherlockCommonService_pb2.ExitRequest()
            exit_message.closeSherlockClient = close_sherlock_client
            response = self.stub.exit(exit_message)
            LOG.info(str(response))
        except SherlockCommonServiceError as err:
            LOG.error("Exit error: ", str(err))

    @require_version()
    def list_units(self, unit_type: ListUnitsRequestUnitType) -> str:
        """List units for a unit type.

        Available Since: 2023R2

        Parameters
        ----------
        unit_type : ListUnitsRequestUnitType
            Unit type.

        Returns
        -------
        str
            Units for the unit type.
        """
        if unit_type == "":
            raise SherlockCommonServiceError(message="Unit type is missing.")

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockCommonService_pb2.ListUnitsRequest(unitType=unit_type)

        try:
            response = self.stub.listUnits(request)
            return_code = response.returnCode
            if return_code.value == -1:
                raise SherlockCommonServiceError(message=return_code.message)
        except SherlockCommonServiceError as e:
            raise e

        return response.units

    @require_version()
    def list_solder_materials(self) -> list[str]:
        """List valid solders.

        Available Since: 2024R1

        Returns
        -------
        list[str]
            Valid solder names.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.common.list_solder_materials()
        """
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockCommonService_pb2.GetSoldersRequest()
        response = self.stub.getSolders(request)

        return response.solderName

    @require_version(251)
    def get_sherlock_info(self) -> str:
        """Get server Sherlock version.

        Returns
        -------
        SherlockInfoResponse
            Sherlock information containing
            releaseVersion, defaultProjectDir and isSingleProjectMode flag

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> release_version = sherlock.common.get_sherlock_info().releaseVersion
        >>> default_dir = sherlock.common.get_sherlock_info().defaultProjectDir
        >>> is_single_project = sherlock.common.get_sherlock_info().isSingleProjectMode
        """
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockCommonService_pb2.SherlockInfoRequest()
        response = self.stub.getSherlockInfo(request)
        if response is not None:
            return response
