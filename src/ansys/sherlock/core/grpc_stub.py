# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

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

    def __init__(self, channel: grpc.Channel, server_version: int):
        """Initialize the gRPC stub."""
        self.channel = channel
        self._server_version = server_version

    def _is_connection_up(self):
        try:
            stub = SherlockCommonService_pb2_grpc.SherlockCommonServiceStub(self.channel)
            stub.check(SherlockCommonService_pb2.HealthCheckRequest())
            return True
        except grpc.RpcError:
            return False
