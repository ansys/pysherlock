import SherlockProjectService_pb2_grpc
import SherlockProjectService_pb2
from ansys.sherlock.core.errors import SherlockDeleteProjectError
from ansys.sherlock.core import LOG
import grpc


def delete_project(project):
    #   """Deletes an existing project
    #
    #   Parameters
    #   ----------
    #   project : str, required
    #       The name of the project to be deleted
    #   """
    try:
        if project == "":
            raise SherlockDeleteProjectError("Empty Project Name")
    except SherlockDeleteProjectError as e:
        LOG.error(str(e))
        return
    
    channel = grpc.insecure_channel('localhost:9090')
    stub = SherlockProjectService_pb2_grpc.SherlockProjectServiceStub(channel)

    request = SherlockProjectService_pb2.DeleteProjectRequest(project=project)

    # The stub represents the initialized services available to client
    # TODO: What is the right way to initialize/generate the stub, Miu Lin has conncecting object
    response = stub.deleteProject(request)

    try:
        if response.value == -1:
            raise SherlockDeleteProjectError(response.message)
        else:
            LOG.info(response.message)
    except SherlockDeleteProjectError as e:
        LOG.error(str(e))
        return
    

