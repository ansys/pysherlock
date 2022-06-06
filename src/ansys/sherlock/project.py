"""Module for basic project services on client-side."""
import os

import SherlockProjectService_pb2
import SherlockProjectService_pb2_grpc
import grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockDeleteProjectError, SherlockImportIpc2581Error


def delete_project(project):
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
        return -1, str(e)

    channel = grpc.insecure_channel("localhost:9090")
    stub = SherlockProjectService_pb2_grpc.SherlockProjectServiceStub(channel)

    request = SherlockProjectService_pb2.DeleteProjectRequest(project=project)

    # The stub represents the initialized services available to client
    response = stub.deleteProject(request)

    try:
        if response.value == -1:
            raise SherlockDeleteProjectError(response.message)
        else:
            LOG.info(response.message)
            return response.value, response.message
    except SherlockDeleteProjectError as e:
        LOG.error(str(e))
        return response.value, str(e)


def import_ipc2581_archive(
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
        Full path to the IPC2581 arhicve file to be imported.
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
    >>> from ansys.sherlock.project import import_ipc2581_archive
    >>> import_ipc2581_archive("Tutorial.zip", True, True,
                            project="Tutorial",
                            ccaName="Card")
    """
    try:
        if not os.path.exists(archiveFile):
            raise SherlockImportIpc2581Error("Invalid file path")
    except SherlockImportIpc2581Error as e:
        LOG.error(str(e))
        return -1, str(e)

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

    channel = grpc.insecure_channel("localhost:9090")
    stub = SherlockProjectService_pb2_grpc.SherlockProjectServiceStub(channel)

    response = stub.importIPC2581Archive(request)

    try:
        if response.value == -1:
            raise SherlockImportIpc2581Error(response.message)
        else:
            LOG.info(response.message)
            return response.value, response.message
    except SherlockImportIpc2581Error as e:
        LOG.error(str(e))
        return response.value, str(e)
