# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

"""Module for shared methods for the gRPC stubs."""
try:
    import SherlockCommonService_pb2
    import SherlockCommonService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2_grpc

import grpc

from ansys.sherlock.core import LOG


class GrpcStub:
    """Provides the gRPC stub."""

    def __init__(self, channel: grpc.Channel, server_version: int):
        """Initialize the gRPC stub."""
        self.channel = channel
        self._server_version = server_version

    def _is_connection_up(self):
        try:
            stub = SherlockCommonService_pb2_grpc.SherlockCommonServiceStub(self.channel)
            response = stub.check(SherlockCommonService_pb2.HealthCheckRequest())
            LOG.info(f"Health check response: {response}. Port: {response.port}")
            healthy = SherlockCommonService_pb2.HealthCheckResponse.ServingStatus.SERVING
            LOG.info(f"Health check response status: {response.status}")
            if (
                response.status
                == SherlockCommonService_pb2.HealthCheckResponse.ServingStatus.SERVING
            ):
                LOG.info("Connection is healthy.")
            elif (
                response.status
                == SherlockCommonService_pb2.HealthCheckResponse.ServingStatus.NOT_SERVING
            ):
                LOG.error("Connection is unhealthy.")
            elif (
                response.status
                == SherlockCommonService_pb2.HealthCheckResponse.ServingStatus.UNKNOWN
            ):
                LOG.error("Connection status is unknown.")
            elif (
                response.status
                == SherlockCommonService_pb2.HealthCheckResponse.ServingStatus.UNRECOGNIZED
            ):
                LOG.error("Connection status is UNRECOGNIZED.")
            elif response.status is None:
                LOG.error("Connection status is None.")
            elif response.status == -1:
                LOG.error("Connection status is -1.")
            else:
                LOG.error("Connection status is not recognized.")

            return response.status == healthy
        except grpc.RpcError:
            return False
