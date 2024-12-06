# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

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
    SherlockExportNetListError,
    SherlockExportPartsListError,
    SherlockGetPartLocationError,
    SherlockImportPartsListError,
    SherlockNoGrpcConnectionException,
    SherlockUpdatePartsFromAVLError,
    SherlockUpdatePartsListError,
    SherlockUpdatePartsListPropertiesError,
    SherlockUpdatePartsLocationsByFileError,
    SherlockUpdatePartsLocationsError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub
from ansys.sherlock.core.types.common_types import TableDelimiter
from ansys.sherlock.core.types.parts_types import (
    AVLDescription,
    AVLPartNum,
    PartLocation,
    PartsListSearchDuplicationMode,
)
from ansys.sherlock.core.utils.version_check import require_version


class Parts(GrpcStub):
    """Contains all parts management capabilities."""

    def __init__(self, channel, server_version):
        """Initialize a gRPC stub for the Sherlock Parts service."""
        super().__init__(channel, server_version)
        self.stub = SherlockPartsService_pb2_grpc.SherlockPartsServiceStub(channel)
        self.PART_LOCATION_UNITS = None
        self.BOARD_SIDES = None

    @staticmethod
    def _add_part_loc_request(
        request: SherlockPartsService_pb2.UpdatePartsLocationsRequest,
        parts: list[tuple[str, str, str, str, str, str, str]],
    ) -> None:
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

    def _check_part_loc_validity(
        self, part_locations: list[tuple[str, str, str, str, str, str, str]]
    ) -> None:
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
        """Initialize units for part location.

        Available since: 2022R1
        """
        if self._is_connection_up():
            part_location_request = SherlockPartsService_pb2.GetPartLocationUnitsRequest()
            part_location_response = self.stub.getPartLocationUnits(part_location_request)
            if part_location_response.returnCode.value == 0:
                self.PART_LOCATION_UNITS = part_location_response.units

    def _init_board_sides(self):
        """Initialize board sides.

        Available Since: 2022R1
        """
        if self._is_connection_up():
            board_sides_request = SherlockPartsService_pb2.GetBoardSidesRequest()
            board_sides_response = self.stub.getBoardSides(board_sides_request)
            if board_sides_response.returnCode.value == 0:
                self.BOARD_SIDES = board_sides_response.boardSides

    @require_version()
    def update_parts_list(
        self,
        project: str,
        cca_name: str,
        part_library: str,
        matching_mode: str,
        duplication_mode: PartsListSearchDuplicationMode,
    ) -> int:
        """Update a parts list based on matching and duplication preferences.

        Available Since: 2021R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        part_library: str
            Name of the parts library.
        matching_mode: str
            Matching mode for updates.
        duplication_mode: PartsListSearchDuplicationMode
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
            "Both",
            PartsListSearchDuplicationMode.ERROR
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
            raise SherlockNoGrpcConnectionException()

        request = SherlockPartsService_pb2.UpdatePartsListRequest(
            project=project,
            ccaName=cca_name,
            partLibrary=part_library,
            matching=matching_mode,
            duplication=duplication_mode,
        )

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

    @require_version()
    def update_parts_locations(
        self, project: str, cca_name: str, part_loc: list[tuple[str, str, str, str, str, str, str]]
    ) -> int:
        """Update one or more part locations.

        Available Since: 2022R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        part_loc: list[tuple[str, str, str, str, str, str, str]]
            List defining the part locations. The list consists
            of these properties:

            - refDes: str
                Reference designator of the part.
            - x: str
                Value for the x coordinate.
            - y: str
                Value for the y coordinate.
            - rotation: str
                Rotation.
            - location_units: str
                Locations units.
            - board_side: str
                Board side.
            - mirrored: str
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
            raise SherlockNoGrpcConnectionException()

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

    @require_version()
    def update_parts_locations_by_file(
        self, project: str, cca_name: str, file_path: str, numeric_format: str = ""
    ) -> int:
        """Update one or more part locations using a CSV file.

        Available Since: 2023R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        file_path: str
            Full path to the file with the components and location properties.
        numeric_format: str, optional
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
            "Parts Locations.csv"
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
            raise SherlockNoGrpcConnectionException()

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

    @require_version()
    def import_parts_list(
        self, project: str, cca_name: str, import_file: str, import_as_user_src: bool
    ) -> int:
        """Import a parts list for a CCA.

        Available Since: 2021R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        import_file: str
            Full path to the CSV file with the parts list.
        import_as_user_src: bool
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
            False
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
            raise SherlockNoGrpcConnectionException()

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

    @require_version()
    def export_parts_list(self, project: str, cca_name: str, export_file: str) -> int:
        """Export a parts list for a CCA.

        Available Since: 2021R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        export_file: str
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
            "Parts List.csv"
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
            raise SherlockNoGrpcConnectionException()

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

    @require_version()
    def enable_lead_modeling(self, project: str, cca_name: str):
        """Enable lead modeling for leaded parts.

        Available Since: 2021R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
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
            "Card"
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

    @require_version()
    def get_part_location(
        self, project: str, cca_name: str, ref_des: str, location_units: str
    ) -> list[PartLocation]:
        """Return the location properties for one or more part.

        Available Since: 2022R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        ref_des: str
            Comma separated list of reference designators of parts to retrieve locations for.
        location_units: str
            Valid units for a part's location.

        Returns
        -------
        list[PartLocation]
            PartLocation for each part that corresponds to the reference designators.

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
                raise SherlockNoGrpcConnectionException()

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

    @require_version(241)
    def update_parts_from_AVL(
        self,
        project: str,
        cca_name: str,
        matching_mode: str,
        duplication_mode: PartsListSearchDuplicationMode,
        avl_part_num: AVLPartNum,
        avl_description: AVLDescription,
    ) -> SherlockPartsService_pb2.UpdatePartsListFromAVLResponse:
        r"""Update the parts list from the Approved Vendor List (AVL).

        Available Since: 2024R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        matching_mode: str
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
            - returnCode: ReturnCode
                - value: int
                    Status code of the response. 0 for success.
                - message: str
                    Indicates general errors that occurred while attempting to update parts
            - numPartsUpdated: int
                Number of parts updated
            - updateErrors: list<str>
                Errors found when updating part

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> from ansys.sherlock.core.types.parts_types import (
            AVLDescription,
            AVLPartNum,
            PartsListSearchDuplicationMode,
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
            matching_mode="Both",
            duplication=PartsListSearchDuplicationMode.FIRST,
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
                raise SherlockNoGrpcConnectionException()

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

    @require_version(242)
    def update_parts_list_properties(
        self,
        project: str,
        cca_name: str,
        part_properties: list[dict[str, list[dict[str, str]] | list[str]]],
    ) -> int:
        """
        Update one or more properties of one or more parts in a parts list.

        Available Since: 2024R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        part_properties: list[dict[str, list[str] | list[dict[str, str]]]]
            Part properties consisting of these properties:

                - reference_designators: list[str], optional
                    Reference designator for each part to be updated. If not included,
                    update properties for all parts in the CCA.
                - properties: list[dict[str, str]]
                    Part properties consisting of these properties:

                        - name: str
                            Name of property to be updated.
                        - value: str
                            Value to be applied to the chosen part property.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.parts.update_parts_list_properties(
                "Test",
                "Card",
                [
                    {
                        "reference_designators": ["C1"],
                        "properties": [
                            {"name": "partType", "value": "RESISTOR"}
                        ]
                    },
                    {
                        "reference_designators": ["C2"],
                        "properties": [
                            {"name": "locX", "value": "1"}
                        ]
                    }
                ]
            )
        """
        try:
            if project == "":
                raise SherlockUpdatePartsListPropertiesError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdatePartsListPropertiesError(message="CCA name is invalid.")
            if len(part_properties) == 0:
                raise SherlockUpdatePartsListPropertiesError(message="Part properties are missing.")

            for i, part_property in enumerate(part_properties):
                if len(part_property) < 1 or len(part_property) > 2:
                    raise SherlockUpdatePartsListPropertiesError(
                        f"Number of elements ({len(part_property)}) "
                        f"is wrong for part list property {i}."
                    )
                elif not isinstance(part_property["reference_designators"], list):
                    raise SherlockUpdatePartsListPropertiesError(
                        f"reference_designators is not a list " f"for parts list property {i}."
                    )

                properties = part_property["properties"]
                for j, prop in enumerate(properties):
                    if len(prop) < 1 or len(prop) > 2:
                        raise SherlockUpdatePartsListPropertiesError(
                            f"Number of elements ({len(prop)}) " f"is wrong for property {j}."
                        )
                    elif not isinstance(prop["name"], str) or prop["name"] == "":
                        raise SherlockUpdatePartsListPropertiesError(
                            f"Name is required " f"for property {j}."
                        )
                    elif not isinstance(prop["value"], str):
                        raise SherlockUpdatePartsListPropertiesError(message="Value is invalid.")

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockPartsService_pb2.UpdatePartsListPropertiesRequest(
                project=project, ccaName=cca_name
            )

            # Add part properties to the request
            for part_prop in part_properties:
                prop = request.partProperties.add()
                reference_designators = part_prop["reference_designators"]
                if reference_designators is not None:
                    for ref_des in reference_designators:
                        prop.refDes.append(ref_des)

                props = part_prop["properties"]
                if props is not None:
                    for prop_dict in props:
                        property_obj = prop.properties.add()
                        property_obj.name = prop_dict["name"]
                        property_obj.value = prop_dict["value"]

            response = self.stub.updatePartsListProperties(request)

            return_code = response.returnCode

            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockUpdatePartsListPropertiesError(error_array=response.errors)

                raise SherlockUpdatePartsListPropertiesError(message=return_code.message)

            return return_code.value

        except SherlockUpdatePartsListPropertiesError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    @require_version(242)
    def export_net_list(
        self,
        project: str,
        cca_name: str,
        output_file: str,
        col_delimiter: str = TableDelimiter.COMMA,
        overwrite_existing: bool = False,
        utf8_enabled: bool = False,
    ) -> int:
        """Export a net list to a delimited output file.

        Available Since: 2024R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        output_file: str
            Full path for the output file where the net list will be written.
        col_delimiter: TableDelimiter, optional
            The delimiter character to be used. Defaults to TableDelimiter.COMMA.
        overwrite_existing: bool, optional
            Flag to determine if existing .CSV files should be overwritten
            if they match the output_file. Defaults to False.
        utf8_enabled: bool, optional
            Flag that specifies if UTF-8 will be used for .CSV files. Defaults to False.

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
        >>> sherlock.parts.export_net_list(
            "Test",
            "Card",
            "Net List.csv",
            col_delimiter=TableDelimiter.TAB,
            overwrite_existing=True,
            utf8_enabled=True
        )
        """
        try:
            if project == "":
                raise SherlockExportNetListError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockExportNetListError(message="CCA name is invalid.")
            if output_file == "":
                raise SherlockExportNetListError(message="Output file path is required.")

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockPartsService_pb2.ExportNetListRequest(
                project=project,
                ccaName=cca_name,
                outputFilePath=output_file,
                overwriteExisting=overwrite_existing,
                colDelimiter=col_delimiter,
                utf8Enabled=utf8_enabled,
            )

            response = self.stub.exportNetList(request)

            if response.value == -1:
                raise SherlockExportNetListError(response.message)

        except SherlockExportNetListError as e:
            LOG.error(str(e))
            raise e

        return response.value
