"""Module for parts services on client-side."""
import SherlockPartsService_pb2
import SherlockPartsService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockUpdatePartsListError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Parts(GrpcStub):
    """Contains methods form the Sherlock Parts Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockPartsService."""
        self.channel = channel
        self.stub = SherlockPartsService_pb2_grpc.SherlockPartsServiceStub(channel)
        self.MATCHING_ARGS = ["Both", "Part"]
        self.DUPLICATION_ARGS = ["First", "Error", "Ignore"]

    def _add_matching_duplication(self, request, matching, duplication):
        if matching == "Both":
            request.matching = SherlockPartsService_pb2.UpdatePartsListRequest.Both
        elif matching == "Part":
            request.matching = SherlockPartsService_pb2.UpdatePartsListRequest.Part

        if duplication == "First":
            request.duplication = SherlockPartsService_pb2.UpdatePartsListRequest.First
        elif duplication == "Error":
            request.duplication = SherlockPartsService_pb2.UpdatePartsListRequest.Error
        elif duplication == "Ignore":
            request.duplication = SherlockPartsService_pb2.UpdatePartsListRequest.Ignore

    def update_parts_list(
        self,
        project,
        cca_name,
        part_library,
        matching,
        duplication,
    ):
        """Update a parts list based on matching and duplication preference provided.

        Parameters
        ----------
        project : str, required
            Sherlock project name
        cca_name : str, required
            The cca name
        part_library : str, required
            Parts library name.
        matching : str, required
            Designates the matching mode for updates.
            Valid arguments: "Both", "Part"
        duplication : str, required
            Designates how to handle duplications during update.
            Valid arguments: "First", "Error", "Ignore"
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
        >>> sherlock.parts.update_parts_list(
            "Test",
            "Card",
            "Sherlock Part Library",
            "Both",
            "Error",
        )
        """
        if project == "":
            raise SherlockUpdatePartsListError(message="Invalid project name")
        if cca_name == "":
            raise SherlockUpdatePartsListError(message="Invalid cca name")
        if part_library == "":
            raise SherlockUpdatePartsListError(message="Invalid parts library")
        if matching not in self.MATCHING_ARGS:
            raise SherlockUpdatePartsListError(message="Invalid matching argument")
        if duplication not in self.DUPLICATION_ARGS:
            raise SherlockUpdatePartsListError(message="Invalid duplication argument")

        request = SherlockPartsService_pb2.UpdatePartsListRequest(
            project=project, ccaName=cca_name, partLibrary=part_library
        )

        self._add_matching_duplication(request, matching, duplication)

        response = self.stub.updatePartsList(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockUpdatePartsListError(error_array=response.updateError)
                else:
                    raise SherlockUpdatePartsListError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockUpdatePartsListError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e
