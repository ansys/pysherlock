"""Module for running the gRPC APIs in the SherlockCommonService."""
import errno
import grpc
import SherlockCommonService_pb2
import SherlockCommonService_pb2_grpc

from ansys.sherlock.core.errors import SherlockConnectionError
from ansys.sherlock.core.errors import SherlockCommonServiceError

class Common:
    def __init__(self, channel):
        print("initializing Common obj")
        self.stub = SherlockCommonService_pb2_grpc.SherlockCommonServiceStub(channel)

    def check(self):
        try:
            #__check_grpc_connection()
            response = self.stub.check(SherlockCommonService_pb2.HealthCheckRequest())
            print(str(response))
            LOG.info(str(response))
        except as e:
            LOG.error("Health check failed: ", str(e))


    def exit(self, close_sherlock_client):
        try:
            response = self.stub.exit(SherlockCommonService_pb2.ExitRequest())
            print(str(response))
            LOG.info(str(response))
        except SherlockCommonServiceError as err:
            LOG.error("Exit error: ", err)
            return -1


    def __check_grpc_connection(self):
        if SHERLOCK is None or SHERLOCK.model_stub is None:
            raise SherlockConnectionError("The Sherlock gRPC connection has not been established.")
