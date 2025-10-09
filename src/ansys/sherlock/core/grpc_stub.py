# © 2023-2025 ANSYS, Inc. All rights reserved

"""Module for shared methods for the gRPC stubs."""
try:
    import SherlockCommonService_pb2
    import SherlockCommonService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2_grpc
import grpc


class GrpcStub:
    """Provides the gRPC stub."""

    def __init__(self, channel):
        """Initialize the gRPC stub."""
        self.channel = channel
        # Stub is created once per channel
        self.stub = SherlockCommonService_pb2_grpc.SherlockCommonServiceStub(channel)

    def _is_connection_up(self) -> bool:
        """Check if the gRPC connection is alive."""
        try:
            self.stub.check(SherlockCommonService_pb2.HealthCheckRequest())
            return True
        except grpc.RpcError:
            return False
