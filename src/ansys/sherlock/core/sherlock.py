import grpc
import SherlockCommonService_pb2
import SherlockCommonService_pb2_grpc
import SherlockLayerService_pb2
import SherlockLayerService_pb2_grpc
import SherlockLifeCycleService_pb2
import SherlockLifeCycleService_pb2_grpc
import SherlockModelService_pb2
import SherlockModelService_pb2_grpc
import SherlockPartsService_pb2
import SherlockPartsService_pb2_grpc
import SherlockProjectService_pb2
import SherlockProjectService_pb2_grpc
import SherlockStackupService_pb2
import SherlockStackupService_pb2_grpc

from ansys.sherlock.core.common import Common


class Sherlock:
    """pysherlock logger."""

    def __init__(self, channel):
        """Initialize Sherlock gRPC connection object."""
        self.channel = channel
        #self.analysis = SherlockAnalysisService_pb2_grpc.SherlockAnalysisServiceStub(channel)
        self.common = Common(channel)
        #self.layer = SherlockLayerService_pb2_grpc.SherlockLayerServiceStub(channel)
        #self.lifecycle = SherlockLifeCycleService_pb2_grpc.SherlockLifeCycleServiceStub(channel)
        #self.parts = SherlockPartsService_pb2_grpc.SherlockPartsServiceStub(channel)
        #self.project = SherlockProjectService_pb2_grpc.SherlockProjectServiceStub(channel)
        #self.model = SherlockModelService_pb2_grpc.SherlockModelServiceStub(channel)
        #self.stackup = SherlockStackupService_pb2_grpc.SherlockStackupServiceStub(channel)
        