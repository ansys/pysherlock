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
