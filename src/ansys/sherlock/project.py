"""Module for basic project services on client-side."""
import SherlockProjectService_pb2
import SherlockProjectService_pb2_grpc
import grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockDeleteProjectError


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
