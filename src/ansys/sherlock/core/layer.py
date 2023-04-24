# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

"""Module containing all layer management capabilities."""

import os

try:
    import SherlockLayerService_pb2
    import SherlockLayerService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockLayerService_pb2
    from ansys.api.sherlock.v0 import SherlockLayerService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockUpdateMountPointsByFileError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Layer(GrpcStub):
    """Module containing all the layer management capabilities."""

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
        """Update mount point properties of a CCA from a CSV file.

        Parameters
        ----------
        project : str, required
            Name of the sherlock project.
        cca_name : str, required
            CCA name.
        file_path : str, required
            Filepath of the CSV file with the mount point properties.

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
        >>> sherlock.layer.update_mount_points_by_file(
            "Test",
            "Card",
            "MountPointImport.csv",
        )
        """
        try:
            if project == "":
                raise SherlockUpdateMountPointsByFileError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdateMountPointsByFileError(message="CCA name is invalid.")
        except SherlockUpdateMountPointsByFileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        try:
            if file_path == "":
                raise SherlockUpdateMountPointsByFileError(message="File path is required.")
            if len(file_path) <= 1 or file_path[1] != ":":
                file_path = f"{os.getcwd()}\\{file_path}"
            if not os.path.exists(file_path):
                raise SherlockUpdateMountPointsByFileError("File path is invalid.")
        except SherlockUpdateMountPointsByFileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        request = SherlockLayerService_pb2.UpdateMountPointsByFileRequest(
            project=project,
            ccaName=cca_name,
            filePath=file_path,
        )

        response = self.stub.updateMountPointsByFile(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockUpdateMountPointsByFileError(error_array=response.updateError)

                raise SherlockUpdateMountPointsByFileError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockUpdateMountPointsByFileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e
