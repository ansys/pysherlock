"""Module for basic project services on client-side."""
import os

import SherlockProjectService_pb2
import SherlockProjectService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockDeleteProjectError, SherlockImportODBError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Project(GrpcStub):
    """Contains methods from the Sherlock Project Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockProjectService."""
        self.channel = channel
        self.stub = SherlockProjectService_pb2_grpc.SherlockProjectServiceStub(channel)

    def import_odb_archive(
        self,
        archiveFile,
        processLayerThickness,
        includeOtherLayers,
        processCutoutFile,
        guessPartProperties,
        project=None,
        ccaName=None,
    ):
        """Import an ODB++ archive.

        Parameters
        ----------
        archiveFile : str, required
            Full path to the ODB++ arhicve file to be imported.
        processLayerThickness : bool, required
            Option to assign stackup thickness.
        includeOtherLayers : bool, required
            Option to include other layers.
        processCutoutFile : bool, required
            Option to process cutouts.
        guessPartProperties: bool, required
            Option to guess part properties
        project: str, optional
            Sherlock project name. If empty, the filename will be used for the project name.
        ccaName : str, optional
            Project CCA name. If empty, the filename will be used for the CCA name.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive("ODB++ Tutorial.tgz", True, True,
                                True, True,
                                project="Tutorial",
                                ccaName="Card")

        """
        try:
            if not os.path.exists(archiveFile):
                raise SherlockImportODBError("Invalid file path")
        except SherlockImportODBError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        if project is None:
            project = os.path.splitext(os.path.basename(archiveFile))[0]
        if ccaName is None:
            ccaName = os.path.splitext(os.path.basename(archiveFile))[0]

        request = SherlockProjectService_pb2.ImportODBRequest(
            archiveFile=archiveFile,
            processLayerThickness=processLayerThickness,
            includeOtherLayers=includeOtherLayers,
            processCutoutFile=processCutoutFile,
            guessPartProperties=guessPartProperties,
            project=project,
            ccaName=ccaName,
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
