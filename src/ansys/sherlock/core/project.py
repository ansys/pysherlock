"""Module for basic project services on client-side."""
import os

import SherlockProjectService_pb2
import SherlockProjectService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockDeleteProjectError,
    SherlockImportIpc2581Error,
    SherlockImportODBError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub


class Project(GrpcStub):
    """Contains methods from the Sherlock Project Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockProjectService."""
        self.channel = channel
        self.stub = SherlockProjectService_pb2_grpc.SherlockProjectServiceStub(channel)

    def import_ipc2581_archive(
        self,
        archive_file,
        include_other_layers,
        guess_part_properties,
        project=None,
        cca_name=None,
    ):
        """Import an IPC2581 archive.

        Parameters
        ----------
        archive_file : str, required
            Full path to the ODB++ arhicve file to be imported.
        include_other_layers : bool, required
            Option to include other layers.
        guess_part_properties: bool, required
            Option to guess part properties
        project: str, optional
            Sherlock project name. If empty, the filename will be used for the project name.
        cca_name : str, optional
            Project CCA name. If empty, the filename will be used for the CCA name.
        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_ipc2581_archive("Tutorial.zip", True, True,
                                project="Tutorial",
                                cca_name="Card")
        """
        try:
            if not os.path.exists(archive_file):
                raise SherlockImportIpc2581Error("Invalid file path")
        except SherlockImportIpc2581Error as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        if project is None:
            project = os.path.splitext(os.path.basename(archive_file))[0]
        if cca_name is None:
            cca_name = os.path.splitext(os.path.basename(archive_file))[0]

        request = SherlockProjectService_pb2.ImportIPC2581Request(
            archiveFile=archive_file,
            includeOtherLayers=include_other_layers,
            guessPartProperties=guess_part_properties,
            project=project,
            ccaName=cca_name,
        )

        response = self.stub.importIPC2581Archive(request)

        try:
            if response.value == -1:
                raise SherlockImportIpc2581Error(response.message)
            else:
                LOG.info(response.message)
                return
        except SherlockImportIpc2581Error as e:
            LOG.error(str(e))
            raise e

    def import_odb_archive(
        self,
        archive_file,
        process_layer_thickness,
        include_other_layers,
        process_cutout_file,
        guess_part_properties,
        project=None,
        cca_name=None,
    ):
        """Import an ODB++ archive.

        Parameters
        ----------
        archive_file : str, required
            Full path to the ODB++ arhicve file to be imported.
        process_layer_thickness : bool, required
            Option to assign stackup thickness.
        include_other_layers : bool, required
            Option to include other layers.
        process_cutout_file : bool, required
            Option to process cutouts.
        guess_part_properties: bool, required
            Option to guess part properties
        project: str, optional
            Sherlock project name. If empty, the filename will be used for the project name.
        cca_name : str, optional
            Project CCA name. If empty, the filename will be used for the CCA name.
        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive("ODB++ Tutorial.tgz", True, True,
                                True, True,
                                project="Tutorial",
                                cca_name="Card")
        """
        try:
            if not os.path.exists(archive_file):
                raise SherlockImportODBError("Invalid file path")
        except SherlockImportODBError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        if project is None:
            project = os.path.splitext(os.path.basename(archive_file))[0]
        if cca_name is None:
            cca_name = os.path.splitext(os.path.basename(archive_file))[0]

        request = SherlockProjectService_pb2.ImportODBRequest(
            archiveFile=archive_file,
            processLayerThickness=process_layer_thickness,
            includeOtherLayers=include_other_layers,
            processCutoutFile=process_cutout_file,
            guessPartProperties=guess_part_properties,
            project=project,
            ccaName=cca_name,
        )

        response = self.stub.importODBArchive(request)

        try:
            if response.value == -1:
                raise SherlockImportODBError(response.message)
            else:
                LOG.info(response.message)
                return
        except SherlockImportODBError as e:
            LOG.error(str(e))
            raise e

    def delete_project(self, project):
        """Delete an existing project.

        Parameters
        ----------
        project : str, required
            The name of the project to be deleted
        Examples
        --------
        >>> from ansys.sherlock.project import delete_project
        >>> delete_project("Test Project")
        """
        try:
            if project == "":
                raise SherlockDeleteProjectError("Invalid Blank Project Name")
        except SherlockDeleteProjectError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        request = SherlockProjectService_pb2.DeleteProjectRequest(project=project)

        response = self.stub.deleteProject(request)

        try:
            if response.value == -1:
                raise SherlockDeleteProjectError(response.message)
            else:
                LOG.info(response.message)
                return
        except SherlockDeleteProjectError as e:
            LOG.error(str(e))
            raise e
