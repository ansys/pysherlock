"""Module for shared methods for the gRPC stubs."""
import SherlockCommonService_pb2
import SherlockCommonService_pb2_grpc
import grpc


class GrpcStub:
    """gRPC stub class."""

    def __init__(self, channel):
        """Initialize GrpcStub."""
        self.channel = channel

    def _is_connection_up(self):
        try:
            stub = SherlockCommonService_pb2_grpc.SherlockCommonServiceStub(self.channel)
            stub.check(SherlockCommonService_pb2.HealthCheckRequest())
            return True
        except grpc.RpcError as rpc_error:
            return False
        return False
