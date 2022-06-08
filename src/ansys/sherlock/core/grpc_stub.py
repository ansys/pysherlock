import grpc
import SherlockCommonService_pb2
import SherlockCommonService_pb2_grpc

class GrpcStub:
    def __init__(self, channel):
        self.channel = channel


    def _is_connection_up(self):
        try:
            stub = SherlockCommonService_pb2_grpc.SherlockCommonServiceStub(self.channel)
            stub.check(SherlockCommonService_pb2.HealthCheckRequest())
            return True
        except grpc.RpcError as rpc_error:
            return False
        return False