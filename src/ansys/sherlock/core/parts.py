"""Module for parts services on client-side."""
import os

try:
    import SherlockPartsService_pb2
    import SherlockPartsService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockPartsService_pb2
    from ansys.api.sherlock.v0 import SherlockPartsService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockExportPartsListError,
    SherlockImportPartsListError,
    SherlockUpdatePartsListError,
    SherlockUpdatePartsLocationsByFileError,
    SherlockUpdatePartsLocationsError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub


class Parts(GrpcStub):
    """Contains methods form the Sherlock Parts Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockPartsService."""
        self.channel = channel
        self.stub = SherlockPartsService_pb2_grpc.SherlockPartsServiceStub(channel)
        self.PART_LOCATION_UNITS = None
        self.BOARD_SIDES = None
        self.MATCHING_ARGS = ["Both", "Part"]
        self.DUPLICATION_ARGS = ["First", "Error", "Ignore"]

    def _add_matching_duplication(self, request, matching, duplication):
        """Add matching/duplication arguments to the request."""
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

    def _add_part_loc_request(self, request, parts):
        """Add part locations to the request."""
        for p in parts:
            part = request.partLoc.add()
            part.refDes = p[0]
            part.x = p[1]
            part.y = p[2]
            part.rotation = p[3]
            part.locationUnits = p[4]
            part.boardSide = p[5]
            part.mirrored = p[6]

    def _check_part_loc_validity(self, input):
        """Check input if it is a valid part location list."""
        if not isinstance(input, list):
            raise SherlockUpdatePartsLocationsError(message="Invalid part_loc argument")

        if len(input) == 0:
            raise SherlockUpdatePartsLocationsError(message="Missing part location properties")
        for i, part in enumerate(input):
            if len(part) != 7:
                raise SherlockUpdatePartsLocationsError(
                    message=f"Invalid part location {i}: Invalid number of fields"
                )
            if part[0] == "":
                raise SherlockUpdatePartsLocationsError(
                    message=f"Invalid part location {i}: Missing ref des"
                )
            if part[4] != "":
                if self.PART_LOCATION_UNITS is not None and part[4] not in self.PART_LOCATION_UNITS:
                    raise SherlockUpdatePartsLocationsError(
                        message=f"Invalid part location {i}: Invalid location units specified"
                    )
            if part[1] != "":
                if part[4] == "":
                    raise SherlockUpdatePartsLocationsError(
                        message=f"Invalid part location {i}: Missing location units"
                    )
                try:
                    float(part[1])
                except ValueError:
                    raise SherlockUpdatePartsLocationsError(
                        message=(
                            f"Invalid part location {i}: "
                            f"Invalid location X coordinate specified"
                        )
                    )
            if part[2] != "":
                if part[4] == "":
                    raise SherlockUpdatePartsLocationsError(
                        message=f"Invalid part location {i}: Missing location units"
                    )
                try:
                    float(part[2])
                except ValueError:
                    raise SherlockUpdatePartsLocationsError(
                        message=(
                            f"Invalid part location {i}: "
                            f"Invalid location Y coordinate specified"
                        )
                    )
            if part[3] != "":
                try:
                    rotation = float(part[3])
                    if rotation < -360 or rotation > 360:
                        raise SherlockUpdatePartsLocationsError(
                            message=(
                                f"Invalid part location {i}: "
                                f"Invalid location rotation specified"
                            )
                        )
                except ValueError:
                    raise SherlockUpdatePartsLocationsError(
                        message=f"Invalid part location {i}: Invalid location rotation specified"
                    )
            if part[5] != "":
                if self.BOARD_SIDES is not None and part[5] not in self.BOARD_SIDES:
                    raise SherlockUpdatePartsLocationsError(
                        message=f"Invalid part location {i}: Invalid location board side specified"
                    )
            if part[6] != "":
                if part[6] != "True" and part[6] != "False":
                    raise SherlockUpdatePartsLocationsError(
                        message=f"Invalid part location {i}: Invalid location mirrored specified"
                    )

    def _init_location_units(self):
        """Initialize PART_LOCATION_UNITS."""
        if self._is_connection_up():
            part_location_request = SherlockPartsService_pb2.GetPartLocationUnitsRequest()
            part_location_response = self.stub.getPartLocationUnits(part_location_request)
            if part_location_response.returnCode.value == 0:
                self.PART_LOCATION_UNITS = part_location_response.units

    def _init_board_sides(self):
        """Initialize BOARD_SIDES."""
        if self._is_connection_up():
            board_sides_request = SherlockPartsService_pb2.GetBoardSidesRequest()
            board_sides_response = self.stub.getBoardSides(board_sides_request)
            if board_sides_response.returnCode.value == 0:
                self.BOARD_SIDES = board_sides_response.boardSides

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
        try:
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
        except SherlockUpdatePartsListError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

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

    def update_parts_locations(
        self,
        project,
        cca_name,
        part_loc,
    ):
        """Set parts' locations.

        Parameters
        ----------
        project : str, required
            Sherlock project name
        cca_name : str, required
            The cca name
        part_loc : (str, str, str, str, str, str, str) list, required
            (refDes, x, y, rotation, location_units, board_side, mirrored)
            Definitions of part locations
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
        >>> sherlock.parts.update_parts_locations(
            "Test",
            "Card",
            [
                ("C1", "-2.7", "-1.65", "0", "in", "TOP", "False"),
                ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
            ]
        )
        """
        if self.PART_LOCATION_UNITS is None:
            self._init_location_units()
        if self.BOARD_SIDES is None:
            self._init_board_sides()

        try:
            if project == "":
                raise SherlockUpdatePartsLocationsError(message="Invalid project name")
            if cca_name == "":
                raise SherlockUpdatePartsLocationsError(message="Invalid cca name")
            self._check_part_loc_validity(part_loc)
        except SherlockUpdatePartsLocationsError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        request = SherlockPartsService_pb2.UpdatePartsLocationsRequest(
            project=project,
            ccaName=cca_name,
        )

        self._add_part_loc_request(request, part_loc)

        response = self.stub.updatePartsLocations(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockUpdatePartsLocationsError(error_array=response.updateError)
                else:
                    raise SherlockUpdatePartsLocationsError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockUpdatePartsLocationsError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def update_parts_locations_by_file(
        self,
        project,
        cca_name,
        file_path,
        numeric_format="",
    ):
        """Update one or more parts' locations using a CSV file.

        Parameters
        ----------
        project : str, required
            Sherlock project name
        cca_name : str, required
            The cca name
        file_path : str, required
            File that contains the components and location properties.
        numeric_format : str, optional
            Numeric format for the file.
            If not provided, it will default to "English (United States)".
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
        >>> sherlock.parts.update_parts_locations_by_file(
            "Test",
            "Card",
            "Parts Locations.csv",
        )
        """
        try:
            if project == "":
                raise SherlockUpdatePartsLocationsByFileError(message="Invalid project name")
            if cca_name == "":
                raise SherlockUpdatePartsLocationsByFileError(message="Invalid cca name")
            if file_path == "":
                raise SherlockUpdatePartsLocationsByFileError(message="File path required")
            if len(file_path) <= 1 or file_path[1] != ":":
                file_path = f"{os.getcwd()}\\{file_path}"
            if not os.path.exists(file_path):
                raise SherlockUpdatePartsLocationsByFileError("Invalid file path")
        except SherlockUpdatePartsLocationsByFileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        request = SherlockPartsService_pb2.UpdatePartsLocationsByFileRequest(
            project=project,
            ccaName=cca_name,
            numericFormat=numeric_format,
            filePath=file_path,
        )

        response = self.stub.updatePartsLocationsByFile(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockUpdatePartsLocationsByFileError(error_array=response.updateError)
                else:
                    raise SherlockUpdatePartsLocationsByFileError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return
        except SherlockUpdatePartsLocationsByFileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def import_parts_list(
        self,
        project,
        cca_name,
        import_file,
        import_as_user_src,
    ):
        """Import a parts list for a project CCA.

        Parameters
        ----------
        project : str, required
            Sherlock project name
        cca_name : str, required
            The cca name
        import_file : str, required
            Full file path to the parts list .csv file.
        import_as_user_src : bool, required
            If true, set the data source of the properties to "User".
            Otherwise, set the data source to the name of the importFile.

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
        >>> sherlock.parts.import_parts_list(
            "Test",
            "Card",
            "Parts List.csv",
            False,
        )
        """
        try:
            if project == "":
                raise SherlockImportPartsListError(message="Invalid project name")
            if cca_name == "":
                raise SherlockImportPartsListError(message="Invalid cca name")
            if import_file == "":
                raise SherlockImportPartsListError(message="Import file path required")
            if len(import_file) <= 1 or import_file[1] != ":":
                import_file = f"{os.getcwd()}\\{import_file}"
            if not os.path.exists(import_file):
                raise SherlockImportPartsListError("Invalid file path")
        except SherlockImportPartsListError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        request = SherlockPartsService_pb2.ImportPartsListRequest(
            project=project,
            ccaName=cca_name,
            importFile=import_file,
            importAsUserSrc=import_as_user_src,
        )

        response = self.stub.importPartsList(request)

        try:
            if response.value == -1:
                raise SherlockImportPartsListError(response.message)
            else:
                LOG.info(response.message)
                return
        except SherlockImportPartsListError as e:
            LOG.error(str(e))
            raise e

    def export_parts_list(
        self,
        project,
        cca_name,
        export_file,
    ):
        """Export a parts list for a project CCA.

        Parameters
        ----------
        project : str, required
            Sherlock project name
        cca_name : str, required
            The cca name
        export_file : str, required
            Full file path to the export parts list .csv file.

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
        >>> sherlock.parts.export_parts_list(
            "Test",
            "Card",
            "Parts List.csv",
        )
        """
        try:
            if project == "":
                raise SherlockExportPartsListError(message="Invalid project name")
            if cca_name == "":
                raise SherlockExportPartsListError(message="Invalid cca name")
            if export_file == "":
                raise SherlockExportPartsListError(message="Export file path required")
            if len(export_file) <= 1 or export_file[1] != ":":
                export_file = f"{os.getcwd()}\\{export_file}"
            else:  # For locally rooted path
                if not os.path.exists(os.path.dirname(export_file)):
                    raise SherlockExportPartsListError(
                        message="Export file directory does not exist"
                    )
        except SherlockExportPartsListError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        request = SherlockPartsService_pb2.ExportPartsListRequest(
            project=project,
            ccaName=cca_name,
            exportFile=export_file,
        )

        response = self.stub.exportPartsList(request)

        try:
            if response.value == -1:
                raise SherlockExportPartsListError(response.message)
            else:
                LOG.info(response.message)
                return
        except SherlockExportPartsListError as e:
            LOG.error(str(e))
            raise e
