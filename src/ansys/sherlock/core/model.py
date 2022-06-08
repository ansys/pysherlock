"""Module for running the gRPC APIs in the SherlockModelService."""
import SherlockModelService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.grpc_stub import GrpcStub


class Model(GrpcStub):
    """Contains methods for the Sherlock Model Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for the Sherlock Model Service."""
        self.channel = channel
        self.stub = SherlockModelService_pb2_grpc.SherlockModelServiceStub(channel)

    def export_trace_reinforcement_model(self):
        """Export a trace reinforcement model."""
        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        # try:
        #     self.model.export_trace_reinforcement_model(message)
        # except SherlockModelServiceError as err:
        #     LOG.error("export_trace_reinforcement_model error: ", err)
        #     return -1
