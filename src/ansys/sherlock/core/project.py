"""Module for basic project services on client-side."""
import os

import SherlockProjectService_pb2
import SherlockProjectService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockImportIpc2581Error
from ansys.sherlock.core.grpc_stub import GrpcStub


class Project(GrpcStub):
    """Contains methods from the Sherlock Project Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockProjectService."""
        self.channel = channel
        self.stub = SherlockProjectService_pb2_grpc.SherlockProjectServiceStub(channel)

    def import_ipc2581_archive(
        self,
        archiveFile,
        includeOtherLayers,
        guessPartProperties,
        project=None,
        ccaName=None,
    ):
        """Import an IPC2581 archive.

        Parameters
        ----------
        archiveFile : str, required
            Full path to the ODB++ arhicve file to be imported.
        includeOtherLayers : bool, required
            Option to include other layers.
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
        >>> sherlock.project.import_ipc2581_archive("Tutorial.zip", True, True,
                                project="Tutorial",
                                ccaName="Card")
        """
        try:
            if not os.path.exists(archiveFile):
                raise SherlockImportIpc2581Error("Invalid file path")
        except SherlockImportIpc2581Error as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        if project is None:
            project = os.path.splitext(os.path.basename(archiveFile))[0]
        if ccaName is None:
            ccaName = os.path.splitext(os.path.basename(archiveFile))[0]

        request = SherlockProjectService_pb2.ImportIPC2581Request(
            archiveFile=archiveFile,
            includeOtherLayers=includeOtherLayers,
            guessPartProperties=guessPartProperties,
            project=project,
            ccaName=ccaName,
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
