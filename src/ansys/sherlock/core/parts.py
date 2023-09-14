# © 2023 ANSYS, Inc. All rights reserved

"""Module containing all parts management capabilities."""

try:
    import SherlockPartsService_pb2
    import SherlockPartsService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockPartsService_pb2
    from ansys.api.sherlock.v0 import SherlockPartsService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockEnableLeadModelingError,
    SherlockExportPartsListError,
    SherlockGetPartLocationError,
    SherlockImportPartsListError,
    SherlockUpdatePartsFromAVLError,
    SherlockUpdatePartsListError,
    SherlockUpdatePartsLocationsByFileError,
    SherlockUpdatePartsLocationsError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub
from ansys.sherlock.core.types.parts_types import (
    AVLDescription,
    AVLPartNum,
    PartLocation,
    PartsListSearchDuplicationMode,
    PartsListSearchMatchingMode,
)


class Parts(GrpcStub):
    """Contains all parts management capabilities."""

    def __init__(self, channel):
        """Initialize a gRPC stub for the Sherlock Parts service."""
        super().__init__(channel)
        self.stub = SherlockPartsService_pb2_grpc.SherlockPartsServiceStub(channel)
        self.PART_LOCATION_UNITS = None
        self.BOARD_SIDES = None
        self.MATCHING_ARGS = ["Both", "Part"]
        self.DUPLICATION_ARGS = ["First", "Error", "Ignore"]
        self.AVL_PART_NUM_ARGS = [
            "AssignInternalPartNum",
            "AssignVendorAndPartNum",
            "DoNotChangeVendorOrPartNum",
        ]
        self.AVL_DESCRIPTION_ARGS = ["AssignApprovedDescription", "DoNotChangeDescription"]

    @staticmethod
    def _add_matching_duplication(request, matching, duplication):
        """Add matching and duplication properties to the request."""
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

    @staticmethod
    def _add_part_loc_request(request, parts):
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

    def _check_part_loc_validity(self, part_locations):
        """Check input to see if it is a valid part location list."""
        if not isinstance(part_locations, list):
            raise SherlockUpdatePartsLocationsError(message="Part location argument is invalid.")

        if len(part_locations) == 0:
            raise SherlockUpdatePartsLocationsError(message="Part location properties are missing.")
        for i, part in enumerate(part_locations):
            if len(part) != 7:
                raise SherlockUpdatePartsLocationsError(
                    message=f"Invalid part location {i}: Number of fields is invalid."
                )
            if part[0] == "":
                raise SherlockUpdatePartsLocationsError(
                    message=f"Invalid part location {i}: Reference designator is missing."
                )
            if part[4] != "":
                if self.PART_LOCATION_UNITS is not None and part[4] not in self.PART_LOCATION_UNITS:
                    raise SherlockUpdatePartsLocationsError(
                        message=f"Invalid part location {i}: Location units are invalid."
                    )
            if part[1] != "":
                if part[4] == "":
                    raise SherlockUpdatePartsLocationsError(
                        message=f"Invalid part location {i}: Location units are missing."
                    )
                try:
                    float(part[1])
                except ValueError:
                    raise SherlockUpdatePartsLocationsError(
                        message=(
                            f"Invalid part location {i}: " f"Location X coordinate is invalid."
                        )
                    )
            if part[2] != "":
                if part[4] == "":
                    raise SherlockUpdatePartsLocationsError(
                        message=f"Invalid part location {i}: Location units are missing."
                    )
                try:
                    float(part[2])
                except ValueError:
                    raise SherlockUpdatePartsLocationsError(
                        message=(
                            f"Invalid part location {i}: " f"Location Y coordinate is invalid."
                        )
                    )
            if part[3] != "":
                try:
                    rotation = float(part[3])
                    if rotation < -360 or rotation > 360:
                        raise SherlockUpdatePartsLocationsError(
                            message=(
                                f"Invalid part location {i}: " f"Location rotation is invalid."
                            )
                        )
                except ValueError:
                    raise SherlockUpdatePartsLocationsError(
                        message=f"Invalid part location {i}: Location rotation is invalid."
                    )
            if part[5] != "":
                if self.BOARD_SIDES is not None and part[5] not in self.BOARD_SIDES:
                    raise SherlockUpdatePartsLocationsError(
                        message=f"Invalid part location {i}: Location board side is invalid."
                    )
            if part[6] != "":
                if part[6] != "True" and part[6] != "False":
                    raise SherlockUpdatePartsLocationsError(
                        message=f"Invalid part location {i}: Location mirrored is invalid."
                    )

    def _init_location_units(self):
        """Initialize units for part location."""
        if self._is_connection_up():
            part_location_request = SherlockPartsService_pb2.GetPartLocationUnitsRequest()
            part_location_response = self.stub.getPartLocationUnits(part_location_request)
            if part_location_response.returnCode.value == 0:
                self.PART_LOCATION_UNITS = part_location_response.units

    def _init_board_sides(self):
        """Initialize board sides."""
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
        matching_mode,
        duplication_mode,
    ):
        """Update a parts list based on matching and duplication preferences.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        part_library : str
            Name of the parts library.
        matching_mode : PartsListSearchMatchingMode
            Matching mode for updates.
        duplication_mode : PartsListSearchDuplicationMode
            How to handle duplication during the update.

        Returns
        -------
        int
            Status code of the response. 0 for success.

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
            UpdatesPartsListRequestMatchingMode.BOTH,
            UpdatesPartsListRequestDuplicationMode.ERROR,
        )
        """
        try:
            if project == "":
                raise SherlockUpdatePartsListError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdatePartsListError(message="CCA name is invalid.")
            if part_library == "":
                raise SherlockUpdatePartsListError(message="Parts library is invalid.")
        except SherlockUpdatePartsListError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        request = SherlockPartsService_pb2.UpdatePartsListRequest(
            project=project, ccaName=cca_name, partLibrary=part_library
        )

        self._add_matching_duplication(request, matching_mode, duplication_mode)

        response = self.stub.updatePartsList(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                raise SherlockUpdatePartsListError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return return_code.value
        except SherlockUpdatePartsListError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def update_parts_locations(self, project, cca_name, part_loc):
        """Update one or more part locations.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        part_loc : list
            List defining the part locations. The list consists
            of these properties:

            - refDes : str
                Reference designator of the part.
            - x : str
                Value for the x coordinate.
            - y : str
                Value for the y coordinate.
            - rotation: str
                Rotation.
            - location_units: str
                Locations units.
            - board_side : str
                Board side.
            - mirrored : str
                Mirrored.

        Returns
        -------
        int
            Status code of the response. 0 for success.

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
                raise SherlockUpdatePartsLocationsError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdatePartsLocationsError(message="CCA name is invalid.")
            self._check_part_loc_validity(part_loc)
        except SherlockUpdatePartsLocationsError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
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

                raise SherlockUpdatePartsLocationsError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return return_code.value
        except SherlockUpdatePartsLocationsError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def update_parts_locations_by_file(self, project, cca_name, file_path, numeric_format=""):
        """Update one or more part locations using a CSV file.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        file_path : str
            Full path to the file with the components and location properties.
        numeric_format : str, optional
            Numeric format for the file, which indicates whether commas or points
            are used as decimal markers. The default is ``""``, in which case
            ``"English (United States)"`` is the numeric format. This
            indicates that points are used as decimal markers.

        Returns
        -------
        int
            Status code of the response. 0 for success.

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
                raise SherlockUpdatePartsLocationsByFileError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdatePartsLocationsByFileError(message="CCA name is invalid.")
            if file_path == "":
                raise SherlockUpdatePartsLocationsByFileError(message="Filepath is required.")
        except SherlockUpdatePartsLocationsByFileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
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

                raise SherlockUpdatePartsLocationsByFileError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return return_code.value
        except SherlockUpdatePartsLocationsByFileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def import_parts_list(self, project, cca_name, import_file, import_as_user_src):
        """Import a parts list for a CCA.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        import_file : str
            Full path to the CSV file with the parts list.
        import_as_user_src : bool
            Whether to set the data source of the properties to ``"User"``.
            Otherwise, the data source is set to the name of the CSV file.

        Returns
        -------
        int
            Status code of the response. 0 for success.

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
                raise SherlockImportPartsListError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockImportPartsListError(message="CCA name is invalid.")
            if import_file == "":
                raise SherlockImportPartsListError(message="Import filepath is required.")
        except SherlockImportPartsListError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
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

            LOG.info(response.message)
            return response.value
        except SherlockImportPartsListError as e:
            LOG.error(str(e))
            raise e

    def export_parts_list(self, project, cca_name, export_file):
        """Export a parts list for a CCA.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        export_file : str
            Full path for the CSV file to export the parts list to.

        Returns
        -------
        int
            Status code of the response. 0 for success.

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
                raise SherlockExportPartsListError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockExportPartsListError(message="CCA name is invalid.")
            if export_file == "":
                raise SherlockExportPartsListError(message="Export filepath is required.")
        except SherlockExportPartsListError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        request = SherlockPartsService_pb2.ExportPartsListRequest(
            project=project, ccaName=cca_name, exportFile=export_file
        )

        response = self.stub.exportPartsList(request)

        try:
            if response.value == -1:
                raise SherlockExportPartsListError(response.message)

            LOG.info(response.message)
            return response.value
        except SherlockExportPartsListError as e:
            LOG.error(str(e))
            raise e

    def enable_lead_modeling(self, project, cca_name):
        """Enable lead modeling for leaded parts.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.

        Returns
        -------
        int
            Status code of the response. 0 for success.

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
        >>> sherlock.parts.enable_lead_modeling(
            "Test",
            "Card",
        )
        """
        try:
            if project == "":
                raise SherlockEnableLeadModelingError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockEnableLeadModelingError(message="CCA name is invalid.")
        except SherlockEnableLeadModelingError as e:
            LOG.error(str(e))
            raise e

        request = SherlockPartsService_pb2.UpdateLeadModelingRequest(
            project=project,
            ccaName=cca_name,
        )

        response = self.stub.updateLeadModeling(request)

        try:
            if response.value == -1:
                raise SherlockEnableLeadModelingError(response.message)

            LOG.info(response.message)
            return response.value
        except SherlockEnableLeadModelingError as e:
            LOG.error(str(e))
            raise e

    def get_part_location(self, project, cca_name, ref_des, location_units):
        """Return the location properties for one or more part.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        ref_des : str
            Reference designator for specific part.
        location_units: str
            Valid units for a part's location.

        Returns
        -------
        list
            List of PartLocation objects.

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
        >>> part_locations = sherlock.parts.get_part_location(
            project="Tutorial",
            cca_name="Main Board",
            ref_des="C1,C2",
            location_units="in",
        )
        >>> print(f"{part_locations}")
        """
        try:
            if project == "":
                raise SherlockGetPartLocationError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockGetPartLocationError(message="CCA name is invalid.")
            if ref_des == "":
                raise SherlockGetPartLocationError(message="Ref Des is invalid.")
            if location_units == "":
                raise SherlockGetPartLocationError(message="Location unit is invalid.")
            if not self._is_connection_up():
                LOG.error("Not connected to a gRPC service.")
                return

            request = SherlockPartsService_pb2.GetPartLocationRequest(
                project=project,
                ccaName=cca_name,
                refDes=ref_des,
                locationUnits=location_units,
            )
            response = self.stub.getPartLocation(request)
            return_code = response.returnCode

            if return_code.value == -1:
                raise SherlockGetPartLocationError(return_code.message)

            locations = []
            for location in response.locationData:
                locations.append(PartLocation(location))
            return locations
        except SherlockGetPartLocationError as e:
            LOG.error(str(e))
            raise e

    def update_parts_from_AVL(
        self,
        project: str,
        cca_name: str,
        matching_mode: PartsListSearchMatchingMode,
        duplication_mode: PartsListSearchDuplicationMode,
        avl_part_num: AVLPartNum,
        avl_description: AVLDescription,
    ) -> SherlockPartsService_pb2.UpdatePartsListFromAVLResponse:
        r"""Update the parts list from the Approved Vendor List (AVL).

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        matching_mode: PartsListSearchMatchingMode
            Determines how parts are matched against the AVL
        duplication_mode: PartsListSearchDuplicationMode
            Determines how duplicate part matches are handled when found
        avl_part_num: AVLPartNum
            Determines what part number info in the parts list is updated from the AVL
        avl_description: AVLDescription
            Determines if the part description is updated or not

        Returns
        -------
        UpdatePartsListFromAVLResponse
            - returnCode : ReturnCode
                - value : int
                    Status code of the response. 0 for success.
                - message : str
                    indicates general errors that occurred while attempting to update parts
            - numPartsUpdated : int
                Number of parts updated
            - updateErrors : list<str>
                Errors found when updating part

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> from ansys.sherlock.core.types.parts_types import (
            AVLDescription,
            AVLPartNum,
            UpdatesPartsListRequestDuplicationMode,
            UpdatesPartsListRequestMatchingMode
        )
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive(
            "C:\\Program Files\\ANSYS Inc\\v241\\sherlock\\tutorial\\ODB++ Tutorial.tgz",
            True,
            True,
            True,
            True,
            project="Test",
            cca_name="Card",
        )
        >>> sherlock.parts.update_parts_from_AVL(
            project="Test",
            cca_name="Card",
            matching_mode=UpdatesPartsListRequestMatchingMode.BOTH,
            duplication=UpdatesPartsListRequestDuplicationMode.FIRST,
            avl_part_num=AVLPartNum.ASSIGN_INTERNAL_PART_NUM,
            avl_description=AVLDescription.ASSIGN_APPROVED_DESCRIPTION
        )
        """
        try:
            if project == "":
                raise SherlockUpdatePartsFromAVLError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdatePartsFromAVLError(message="CCA name is invalid.")

            request = SherlockPartsService_pb2.UpdatePartsListFromAVLRequest(
                project=project,
                ccaName=cca_name,
                matching=matching_mode,
                duplication=duplication_mode,
                avlPartNum=avl_part_num,
                avlDesc=avl_description,
            )

            if not self._is_connection_up():
                LOG.error("Not connected to a gRPC service.")
                return

            # Call method on server
            response = self.stub.updatePartsListFromAVL(request)

            return_code = response.returnCode

            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockUpdatePartsFromAVLError(error_array=response.updateErrors)
                raise SherlockUpdatePartsFromAVLError(message=return_code.message)

            return response
        except SherlockUpdatePartsFromAVLError as e:
            LOG.error(str(e))
            raise e
