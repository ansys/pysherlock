"""Module for basic project services on client-side."""
import SherlockProjectService_pb2
import SherlockProjectService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockDeleteProjectError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Project(GrpcStub):
    """Contains methods from the Sherlock Project Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockProjectService."""
        self.channel = channel
        self.stub = SherlockProjectService_pb2_grpc.SherlockProjectServiceStub(channel)

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
            return -1, str(e)

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
                return response.value, response.message
        except SherlockDeleteProjectError as e:
            LOG.error(str(e))
            return response.value, str(e)
