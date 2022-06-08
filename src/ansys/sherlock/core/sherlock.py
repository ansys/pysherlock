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
from ansys.sherlock.core.model import Model


class Sherlock:
    """Sherlock gRPC connection object."""

    def __init__(self, channel):
        """Initialize Sherlock gRPC connection object."""
        self.common = Common(channel)
        self.model = Model(channel)
