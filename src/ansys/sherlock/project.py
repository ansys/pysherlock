"""Module for basic project services on client-side."""
import os

import SherlockProjectService_pb2
import SherlockProjectService_pb2_grpc
import grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockDeleteProjectError, SherlockImportODBError


def import_odb_archive(
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
    >>> from ansys.sherlock.project import import_ODB_archive
    >>> TODO

    """
    try:
        if not os.path.exists(archiveFile):
            raise SherlockImportODBError("Invalid project path")
    except SherlockImportODBError as e:
        LOG.error(str(e))
        return -1, str(e)

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

    channel = grpc.insecure_channel("localhost:9090")
    stub = SherlockProjectService_pb2_grpc.SherlockProjectServiceStub(channel)

    response = stub.importODBArchive(request)

    try:
        if response.value == -1:
            raise SherlockImportODBError(response.message)
        else:
            LOG.info(response.message)
            return response.value, response.message
    except SherlockImportODBError as e:
        LOG.error(str(e))
        return response.value, str(e)


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
