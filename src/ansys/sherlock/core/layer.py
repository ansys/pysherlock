"""Module for layer services on client-side."""
import os

import SherlockLayerService_pb2
import SherlockLayerService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockUpdateMountPointsError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Layer(GrpcStub):
    """Contains methods from the Sherlock Layer Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockLayerService."""
        self.channel = channel
        self.stub = SherlockLayerService_pb2_grpc.SherlockLayerServiceStub(channel)

    def update_mount_points_by_file(
        self,
        project,
        cca_name,
        file_path,
    ):
        """Update mount points properties of a CCA from a CSV formatted file.

        Parameters
        ----------
        project : str, required
            Sherlock project name
        cca_name : str, required
            The cca name
        file_path : str, required
            The filepath of the CSV file containing the mount points properties
        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
            cca_name="Card",
        )
        TODO: Write the final example and test it
        """
        try:
            if project == "":
                raise SherlockUpdateMountPointsError(message="Invalid project name")
            elif cca_name == "":
                raise SherlockUpdateMountPointsError(message="Invalid cca name")
        except SherlockUpdateMountPointsError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        try:
            if not os.path.exists(file_path):
                raise SherlockUpdateMountPointsError(message="Invalid file path")
        except SherlockUpdateMountPointsError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        request = SherlockLayerService_pb2.UpdateMountPointsRequest(
            project=project,
            ccaName=cca_name,
            filePath=file_path,
        )

        response = self.stub.updateMountPoints(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockUpdateMountPointsError(error_array=response.updateError)
                else:
                    raise SherlockUpdateMountPointsError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockUpdateMountPointsError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e
