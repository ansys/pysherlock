# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

"""Module containing all project management capabilities."""
import os
from typing import Optional

import grpc

try:
    import SherlockProjectService_pb2
    import SherlockProjectService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockProjectService_pb2
    from ansys.api.sherlock.v0 import SherlockProjectService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockAddCCAError,
    SherlockAddProjectError,
    SherlockAddStrainMapsError,
    SherlockAddThermalMapsError,
    SherlockCreateCCAFromModelingRegionError,
    SherlockDeleteProjectError,
    SherlockExportProjectError,
    SherlockGenerateProjectReportError,
    SherlockImportIpc2581Error,
    SherlockImportODBError,
    SherlockImportProjectZipArchiveError,
    SherlockImportProjectZipArchiveSingleModeError,
    SherlockListCCAsError,
    SherlockListStrainMapsError,
    SherlockListThermalMapsError,
    SherlockNoGrpcConnectionException,
    SherlockUpdateThermalMapsError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub
from ansys.sherlock.core.types.project_types import (
    BoardBounds,
    CsvExcelFile,
    IcepakFile,
    ImageBounds,
    ImageFile,
    LegendBounds,
    StrainMapsFileType,
    ThermalBoardSide,
    ThermalMapsFileType,
)
from ansys.sherlock.core.utils.version_check import require_version


class Project(GrpcStub):
    """Contains all project management capabilities."""

    def __init__(self, channel: grpc.Channel, server_version: int):
        """Initialize a gRPC stub for Sherlock Project service."""
        super().__init__(channel, server_version)
        self.stub = SherlockProjectService_pb2_grpc.SherlockProjectServiceStub(channel)

    @require_version()
    def delete_project(self, project: str) -> int:
        """Delete a Sherlock project.

        Available Since: 2022R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.delete_project("Test Project")
        """
        try:
            if project == "":
                raise SherlockDeleteProjectError("Project name is blank. Specify a project name.")
        except SherlockDeleteProjectError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockProjectService_pb2.DeleteProjectRequest(project=project)

        response = self.stub.deleteProject(request)

        try:
            if response.value == -1:
                raise SherlockDeleteProjectError(response.message)

            LOG.info(response.message)
            return response.value
        except SherlockDeleteProjectError as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def import_odb_archive(
        self,
        archive_file: str,
        process_layer_thickness: bool,
        include_other_layers: bool,
        process_cutout_file: bool,
        guess_part_properties: bool,
        ims_stackup: bool = False,
        project: Optional[str] = None,
        cca_name: Optional[str] = None,
        polyline_simplification: bool = False,
        polyline_tolerance: float = 0.1,
        polyline_tolerance_units: str = "mm",
    ) -> int:
        """Import an ODB++ archive file.

        Available Since: 2021R1

        Parameters
        ----------
        archive_file: str
            Full path to the ODB++ archive file.
        process_layer_thickness: bool
            Whether to assign stackup thickness.
        include_other_layers: bool
            Whether to include other layers.
        process_cutout_file: bool
            Whether to process cutouts.
        guess_part_properties: bool
            Whether to guess part properties.
        ims_stackup: bool, optional
            Whether to generate an IMS stackup
        project: str, optional
            Name of the Sherlock project. The default is ``None``, in which
            case the name of the ODB++ archive file is used for the project name.
        cca_name: str, optional
            Name of the CCA name. The default is ``None``, in which case the
            name of the ODB++ archive file is used for the CCA name.
        polyline_simplification: bool, optional
            Whether to enable polyline simplification
        polyline_tolerance: float, optional
            Polyline simplification tolerance
        polyline_tolerance_units: str, optional
            Polyline simplification tolerance units

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive("ODB++ Tutorial.tgz", True, True,
                                True, True,
                                ims_stackup=True,
                                project="Tutorial",
                                cca_name="Card",
                                polyline_simplification=True,
                                polyline_tolerance=0.1,
                                polyline_tolerance_units="mm")
        """
        try:
            if archive_file == "":
                raise SherlockImportODBError(message="Archive path is required.")
        except SherlockImportODBError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        if project is None:
            project = os.path.splitext(os.path.basename(archive_file))[0]
        if cca_name is None:
            cca_name = os.path.splitext(os.path.basename(archive_file))[0]

        request = SherlockProjectService_pb2.ImportODBRequest(
            archiveFile=archive_file,
            processLayerThickness=process_layer_thickness,
            includeOtherLayers=include_other_layers,
            processCutoutFile=process_cutout_file,
            guessPartProperties=guess_part_properties,
            imsStackup=ims_stackup,
            project=project,
            ccaName=cca_name,
            polylineSimplification=polyline_simplification,
            polylineTolerance=polyline_tolerance,
            polylineToleranceUnits=polyline_tolerance_units,
        )

        response = self.stub.importODBArchive(request)

        try:
            if response.value == -1:
                raise SherlockImportODBError(response.message)

            LOG.info(response.message)
            return response.value
        except SherlockImportODBError as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def import_ipc2581_archive(
        self,
        archive_file: str,
        include_other_layers: bool,
        guess_part_properties: bool,
        project: Optional[str] = None,
        cca_name: Optional[str] = None,
        polyline_simplification: bool = False,
        polyline_tolerance: float = 0.1,
        polyline_tolerance_units: str = "mm",
    ) -> int:
        """Import an IPC-2581 archive file.

        Available Since: 2021R1

        Parameters
        ----------
        archive_file: str
            Full path to the IPC-2581 archive file.
        include_other_layers: bool
            Whether to include other layers.
        guess_part_properties: bool
            Whether to guess part properties
        project: str, optional
            Name of the Sherlock project. The default is ``None``, in which case
            the name of the IPC-2581 archive file is used for the project name.
        cca_name: str, optional
            Name of the CCA. The default is ``None``, in which case the name of
            the IPC-2581 archive file is used for the CCA name.
        polyline_simplification: bool, optional
            Whether to enable polyline simplification
        polyline_tolerance: float, optional
            Polyline simplification tolerance
        polyline_tolerance_units: str, optional
            Polyline simplification tolerance units

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_ipc2581_archive("Tutorial.zip", True, True,
                                project="Tutorial",
                                cca_name="Card",
                                polyline_simplification=True,
                                polyline_tolerance=0.1,
                                polyline_tolerance_units="mm")
        """
        try:
            if archive_file == "":
                raise SherlockImportIpc2581Error(message="Archive file path is required.")
        except SherlockImportIpc2581Error as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        if project is None:
            project = os.path.splitext(os.path.basename(archive_file))[0]
        if cca_name is None:
            cca_name = os.path.splitext(os.path.basename(archive_file))[0]

        request = SherlockProjectService_pb2.ImportIPC2581Request(
            archiveFile=archive_file,
            includeOtherLayers=include_other_layers,
            guessPartProperties=guess_part_properties,
            project=project,
            ccaName=cca_name,
            polylineSimplification=polyline_simplification,
            polylineTolerance=polyline_tolerance,
            polylineToleranceUnits=polyline_tolerance_units,
        )

        response = self.stub.importIPC2581Archive(request)

        try:
            if response.value == -1:
                raise SherlockImportIpc2581Error(response.message)

            LOG.info(response.message)
            return response.value
        except Exception as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def generate_project_report(
        self, project: str, author: str, company: str, report_file: str
    ) -> int:
        """Generate a project report.

        Available Since: 2021R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        author: str
            Name of the author who is generating the report.
        company: str
            Name of the author's company.
        report_file: str
            Full path to where to create the report.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_odb_archive("ODB++ Tutorial.tgz", True, True,
                                True, True,
                                project="Tutorial",
                                cca_name="Card")
        >>> sherlock.project.generate_project_report(
            "Tutorial",
            "John Doe",
            "Example",
            "Project Report.pdf"
        )
        """
        try:
            if project == "":
                raise SherlockGenerateProjectReportError(message="Project name is invalid.")
            if author == "":
                raise SherlockGenerateProjectReportError(message="Author name is invalid.")
            if company == "":
                raise SherlockGenerateProjectReportError(message="Company name is invalid.")
            if report_file == "":
                raise SherlockGenerateProjectReportError(message="Report path is required.")
        except SherlockGenerateProjectReportError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockProjectService_pb2.GenReportRequest(
            project=project,
            author=author,
            company=company,
        )

        try:
            with open(report_file, "wb") as dest:
                for response in self.stub.genReport(request):
                    if response.returnCode.value == -1:
                        raise SherlockGenerateProjectReportError(
                            message=response.returnCode.message
                        )
                    else:
                        dest.write(response.content)
                else:
                    LOG.info(response.returnCode.message)

                return response.returnCode.value
        except Exception as e:
            LOG.error(str(e))
            raise SherlockGenerateProjectReportError(str(e))

    @require_version()
    def list_ccas(
        self, project: str, cca_names: Optional[list[str]] = None
    ) -> dict[str, str | dict[str, str]]:
        """List CCAs and subassembly CCAs assigned to each CCA or given CCAs.

        Available Since: 2023R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_names: list[str], optional
            CCA names. The default is ``None``, in which case all CCAs
            in the project are returned.

        Returns
        -------
        list
            CCAs and subassembly CCAs.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> ccas = sherlock.project.list_ccas("AssemblyTutorial", ["Main Board"])
        """
        try:
            if project == "":
                raise SherlockListCCAsError(message="Project name is invalid.")

            if cca_names is not None and type(cca_names) is not list:
                raise SherlockListCCAsError(message="cca_names is not a list.")

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockProjectService_pb2.ListCCAsRequest(project=project)

            """Add the CCA names to the request."""
            if cca_names is not None:
                for cca_name in cca_names:
                    request.cca.append(cca_name)

            response = self.stub.listCCAs(request)

            return_code = response.returnCode

            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockListCCAsError(error_array=response.errors)

                raise SherlockListCCAsError(message=return_code.message)

        except SherlockListCCAsError as e:
            LOG.error(str(e))
            raise e

        return response.ccas

    @require_version(241)
    def add_cca(self, project: str, cca_properties: list[dict[str, bool | float | str]]) -> int:
        """Add one or more CCAs to a project.

        Available Since: 2023R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_properties: list[dict[str, bool | float | str]]
            List of CCAs to be added consisting of these properties:

            - cca_name: str
                Name of the CCA.
            - description: str
                Description of the CCA. The default is ``None``.
            - default_solder_type: str
                The default solder type. The default is ``None``.
            - default_stencil_thickness: float
                The default stencil thickness. The default is ``None``.
            - default_stencil_thickness_units: str
                Units for default stencil thickness. The default is ``None``.
            - default_part_temp_rise: float
                Default part temp rise. The default is ``None``.
            - default_part_temp_rise_units: str
                Units for default part temp rise. The default is ``None``.
                Options are ``"C"``, ``"F"``, and ``"K"``.
            - guess_part_properties_enabled: bool
                Whether to enable guess part properties. The default is ``None``.

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
        >>> sherlock.project.add_cca(
            "Test",
            [{
                'cca_name': 'Card 2',
                'description': 'Second CCA',
                'default_solder_type': 'SAC305',
                'default_stencil_thickness': 10,
                'default_stencil_thickness_units': 'mm',
                'default_part_temp_rise': 20,
                'default_part_temp_rise_units': 'C',
                'guess_part_properties_enabled': False,
            },
            ]
        )

        """
        try:
            if project == "":
                raise SherlockAddCCAError(message="Project name is invalid.")

            if not isinstance(cca_properties, list):
                raise SherlockAddCCAError(message="CCA properties argument is invalid.")

            if len(cca_properties) == 0:
                raise SherlockAddCCAError(message="One or more CCAs are required.")

            request = SherlockProjectService_pb2.AddCcaRequest(project=project)

            for i, cca in enumerate(cca_properties):
                if not isinstance(cca, dict):
                    raise SherlockAddCCAError(message=f"CCA properties are invalid for CCA {i}.")

                if "cca_name" not in cca.keys():
                    raise SherlockAddCCAError(message=f"CCA name is missing for CCA {i}.")

                cca_request = request.CCAs.add()
                cca_request.ccaName = cca["cca_name"]

                if cca_request.ccaName == "":
                    raise SherlockAddCCAError(message=f"CCA name is invalid for CCA {i}.")

                if "description" in cca.keys():
                    cca_request.description = cca["description"]

                if "default_solder_type" in cca.keys():
                    cca_request.defaultSolderType = cca["default_solder_type"]

                if "default_stencil_thickness" in cca.keys():
                    cca_request.defaultStencilThickness = cca["default_stencil_thickness"]

                if "default_stencil_thickness_units" in cca.keys():
                    cca_request.defaultStencilThicknessUnits = cca[
                        "default_stencil_thickness_units"
                    ]

                if "default_part_temp_rise" in cca.keys():
                    cca_request.defaultPartTempRise = cca["default_part_temp_rise"]

                if "default_part_temp_rise_units" in cca.keys():
                    cca_request.defaultPartTempRiseUnits = cca["default_part_temp_rise_units"]

                if "guess_part_properties_enabled" in cca.keys():
                    cca_request.guessPartPropertiesEnabled = cca["guess_part_properties_enabled"]

        except SherlockAddCCAError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        response = self.stub.addCCA(request)

        try:
            if response.value == -1:
                raise SherlockAddCCAError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockAddCCAError as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def add_strain_maps(
        self,
        project: str,
        strain_maps: list,
    ) -> int:
        """Add strain map files to CCAs in a Sherlock project.

        Available Since: 2023R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project to add strain maps to.
        strain_maps: list
            Strain maps consisting of these properties:

            - strain_map_file: str
                Full path to the CSV file with the strain maps.
            - file_comment: str
                Comment to associate with the file.
            - file_type: StrainMapsFileType
                Strain maps file type. Options are CSV, Excel, and Image.
            - header_row_count: int
                Number of rows before the file's column header.
            - reference_id_column: str
                Name of the column in the file with reference IDs.
            - strain_column: str
                Name of the column in the file with strain values.
            - strain_units: str
                Strain units. Options are ``µε`` and ``ε``.
            - image_file: StrainMapImageFile, optional
                The properties of the strain map file to add.
            - ccas: list, optional
                List of CCA names to assign the file to. When no list is
                specified, the file is assigned to all CCAs in the project.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> from ansys.sherlock.core.types.project_types import (
            BoardBounds,
            ImageBounds,
            ImageFile,
            LegendBounds,
            LegendOrientation,
            StrainMapsFileType,
            StrainMapLegendOrientation,
        )
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.add_strain_maps(
            "Tutorial Project",
                [
                    (
                        "StrainMap.csv",
                        "This is the strain map file for the project",
                        StrainMapsFileType.CSV,
                        0,
                        "refDes",
                        "strain",
                        "µε",
                        ["Main Board"]
                    )
                ]
            )
        >>> properties = (
                BoardBounds([
                    (1.0, 2.0),
                    (3.0, 4.0),
                    (1.0, 2.0),
                    (1.0, 2.0)
                ]),
                "in",
                ImageBounds(0.0, 0.0, 10.0, 8.0),
                LegendBounds(1.0, 2.0, 4.0, 2.0),
                StrainMapLegendOrientation.VERTICAL,
                20.0,
                50.0,
                "µε"
            )
        >>> sherlock.project.add_strain_maps(
            "Tutorial Project",
                [
                    (
                        "StrainMap.jpg",
                        "This is the strain map image for the project",
                        StrainMapsFileType.IMAGE,
                        properties,
                        ["Main Board"]
                    )
                ]
            )
        """
        try:
            if project == "":
                raise SherlockAddStrainMapsError(message="Project name is invalid.")

            if len(strain_maps) == 0:
                raise SherlockAddStrainMapsError(message="Strain maps are missing.")

            # Validate first
            for i, strain_map in enumerate(strain_maps):
                if (
                    strain_map[2] == StrainMapsFileType.CSV
                    or strain_map[2] == StrainMapsFileType.EXCEL
                ):
                    if len(strain_map) < 7 or len(strain_map) > 8:
                        raise SherlockAddStrainMapsError(
                            f"Number of elements ({str(len(strain_maps))}) is wrong for strain map {i}."  # noqa: E501
                        )
                    elif not isinstance(strain_map[0], str) or strain_map[0] == "":
                        raise SherlockAddStrainMapsError(f"Path is required for strain map {i}.")
                    elif not isinstance(strain_map[3], int) or strain_map[3] == "":
                        raise SherlockAddStrainMapsError(
                            f"Header row count is required for strain map {i}."
                        )
                    elif strain_map[3] < 0:
                        raise SherlockAddStrainMapsError(
                            f"Header row count must be greater than or "
                            f"equal to 0 for strain map {i}."
                        )
                    elif not isinstance(strain_map[4], str) or strain_map[4] == "":
                        raise SherlockAddStrainMapsError(
                            f"Reference ID column is required for strain map {i}."
                        )
                    elif not isinstance(strain_map[5], str) or strain_map[5] == "":
                        raise SherlockAddStrainMapsError(
                            f"Strain column is required for strain map {i}."
                        )
                    elif not isinstance(strain_map[6], str) or strain_map[6] == "":
                        raise SherlockAddStrainMapsError(
                            f"Strain units are required for strain map {i}."
                        )
                    elif strain_map[6] != "µε" and strain_map[6] != "ε":
                        raise SherlockAddStrainMapsError(
                            f'Strain units "{strain_map[6]}" are invalid for strain map {i}.'
                        )
                    elif (
                        len(strain_map) == 8
                        and strain_map[7] is not None
                        and type(strain_map[7]) is not list
                    ):
                        raise SherlockAddStrainMapsError(
                            message=f"cca_names is not a list " f"for strain map {i}."
                        )

                elif strain_map[2] == StrainMapsFileType.IMAGE:
                    if len(strain_map) < 4 or len(strain_map) > 5:
                        raise SherlockAddStrainMapsError(
                            f"Number of elements ({str(len(strain_maps))}) "
                            f"is wrong for strain map {i}."
                        )
                    elif not isinstance(strain_map[0], str) or strain_map[0] == "":
                        raise SherlockAddStrainMapsError(f"Path is required for strain map {i}.")
                    elif not isinstance(strain_map[3], tuple) or strain_map[3] == "":
                        raise SherlockAddStrainMapsError(
                            f"image_file is not a list for strain map {i}."
                        )

                    image_file_properties = strain_map[3]

                    if not isinstance(image_file_properties[0], BoardBounds):
                        raise SherlockAddStrainMapsError(
                            f"Invalid board bounds for " f"strain map {i}."
                        )

                    if not isinstance(image_file_properties[1], (str, type(None))):
                        raise SherlockAddStrainMapsError(
                            f"Invalid coordinate units for " f"strain map {i}."
                        )

                    if not isinstance(image_file_properties[2], ImageBounds):
                        raise SherlockAddStrainMapsError(
                            f"Invalid image bounds for " f"strain map {i}."
                        )

                    if not isinstance(image_file_properties[3], LegendBounds):
                        raise SherlockAddStrainMapsError(
                            f"Invalid legend bounds for " f"strain map {i}."
                        )

                    if not isinstance(image_file_properties[4], int):
                        raise SherlockAddStrainMapsError(
                            f"Invalid legend orientation for " f"strain map {i}."
                        )

                    if not isinstance(image_file_properties[5], float):
                        raise SherlockAddStrainMapsError(
                            f"Invalid minimum strain for " f"strain map {i}."
                        )

                    if not isinstance(image_file_properties[6], float):
                        raise SherlockAddStrainMapsError(
                            f"Invalid maximum strain for " f"strain map {i}."
                        )

                    if not isinstance(image_file_properties[7], str):
                        raise SherlockAddStrainMapsError(
                            f"Invalid strain units for " f"strain map {i}."
                        )

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockProjectService_pb2.AddStrainMapRequest(project=project)

            # Add the strain maps to the request
            for s in strain_maps:
                strain_map = request.strainMapFiles.add()
                strain_map.strainMapFile = s[0]
                strain_map.fileComment = s[1]
                strain_map.fileType = s[2]

                if s[2] == StrainMapsFileType.CSV or s[2] == StrainMapsFileType.EXCEL:
                    strain_map.headerRowCount = s[3]
                    strain_map.referenceIDColumn = s[4]
                    strain_map.strainColumn = s[5]
                    strain_map.strainUnits = s[6]

                    """Add the CCA names to the request."""
                    if len(s) == 8:
                        cca_names = s[7]
                        if cca_names is not None:
                            for cca_name in cca_names:
                                strain_map.cca.append(cca_name)

                elif s[2] == StrainMapsFileType.IMAGE:
                    strain_map_image_properties = s[3]
                    image_file_properties = strain_map.imageFile
                    image_properties = strain_map_image_properties

                    for vertex in image_properties[0].bounds:
                        node_coordinate = strain_map.imageFile.boardBounds.add()
                        node_coordinate.vertexX = vertex[0]
                        node_coordinate.vertexY = vertex[1]

                    image_file_properties.coordinateUnits = image_properties[1]
                    image_file_properties.imageBounds.imageX = image_properties[2].image_x
                    image_file_properties.imageBounds.imageY = image_properties[2].image_y
                    image_file_properties.imageBounds.imageH = image_properties[2].height
                    image_file_properties.imageBounds.imageW = image_properties[2].width
                    image_file_properties.legendBounds.legendX = image_properties[3].legend_x
                    image_file_properties.legendBounds.legendY = image_properties[3].legend_y
                    image_file_properties.legendBounds.legendH = image_properties[3].height
                    image_file_properties.legendBounds.legendW = image_properties[3].width
                    image_file_properties.legendOrientation = image_properties[4]
                    image_file_properties.minStrain = image_properties[5]
                    image_file_properties.maxStrain = image_properties[6]
                    image_file_properties.strainUnits = image_properties[7]

                    """Add the CCA names to the request."""
                    if len(s) == 5:
                        cca_names = s[4]
                        if cca_names is not None:
                            for cca_name in cca_names:
                                strain_map.cca.append(cca_name)

            response = self.stub.addStrainMap(request)

            return_code = response.returnCode

            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddStrainMapsError(error_array=response.errors)

                raise SherlockAddStrainMapsError(message=return_code.message)

            return return_code.value
        except SherlockAddStrainMapsError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    @require_version()
    def list_strain_maps(
        self, project: str, cca_names: Optional[list[str]] = None
    ) -> list[SherlockProjectService_pb2.ListStrainMapsResponse.CcaStrainMap]:
        """List the strain maps assigned to each CCA or given CCAs.

        Available Since: 2023R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_names: list[str], optional
            CCA names to provide strain maps for. The default is ``None``,
            in which case all CCAs in the project are returned.

        Returns
        -------
        list[SherlockProjectService_pb2.ListStrainMapsResponse.CcaStrainMap]
            All strain maps or strain maps for the specified CCAs.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> strain_maps = sherlock.project.list_strain_maps(
            "AssemblyTutorial",
            ["Main Board","Power Module"]
        )
        """
        try:
            if project == "":
                raise SherlockListStrainMapsError(message="Project name is invalid.")

            if cca_names is not None and type(cca_names) is not list:
                raise SherlockListStrainMapsError(message="cca_names is not a list.")

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockProjectService_pb2.ListStrainMapsRequest(project=project)

            """Add the CCA names to the request."""
            if cca_names is not None:
                for cca_name in cca_names:
                    request.cca.append(cca_name)

            response = self.stub.listStrainMaps(request)

            return_code = response.returnCode

            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockListStrainMapsError(error_array=response.errors)

                raise SherlockListStrainMapsError(message=return_code.message)

        except Exception as e:
            LOG.error(str(e))
            raise e

        return response.ccaStrainMaps

    @require_version(241)
    def add_project(
        self, project_name: str, project_category: str, project_description: str
    ) -> int:
        """Add a sherlock project to sherlock.

        Available Since: 2024R1

        Parameters
        ----------
        project_name: str
            Name of the Sherlock project.
        project_category: str
            Category of the Sherlock project
        project_description: str
            Description of the Sherlock project

        Returns
        -------
        int
            0 for success otherwise error

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> code = sherlock.project.add_project(
            "project name example",
            "project category example",
            "project description example")
        """
        if project_name is None or project_name == "":
            raise SherlockAddProjectError("Project name cannot be blank")

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockProjectService_pb2.AddProjectRequest(
            project=project_name, category=project_category, description=project_description
        )

        return_code = self.stub.addProject(request)

        if return_code.value == -1:
            raise SherlockAddProjectError(return_code.message)

        return return_code.value

    @require_version(242)
    def list_thermal_maps(self, project: str, cca_names: Optional[list[str]] = None) -> list:
        """List the thermal map files and their type assigned to each CCA of given CCAs.

        Available Since: 2024R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_names: List of str, optional
            List of CCA names to provide thermal maps for. The default is ``None``,
            in which case all CCAs in the project are returned.

        Returns
        -------
        list
            All thermal map files or thermal map files and their type for the specified CCAs.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> thermal_maps = sherlock.project.list_thermal_maps(
            "AssemblyTutorial",
            ["Main Board","Power Module"]
        )
        """
        try:
            if project == "":
                raise SherlockListThermalMapsError(message="Project name is invalid.")

            if cca_names is not None and type(cca_names) is not list:
                raise SherlockListThermalMapsError(message="cca_names is not a list.")

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockProjectService_pb2.ListThermalMapsRequest(project=project)

            if cca_names is not None:
                for cca_name in cca_names:
                    request.cca.append(cca_name)

            response = self.stub.listThermalMaps(request)

            return_code = response.returnCode

            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockListThermalMapsError(error_array=response.errors)

                raise SherlockListThermalMapsError(message=return_code.message)

        except SherlockListThermalMapsError as e:
            LOG.error(str(e))
            raise e

        return response.ccaThermalMaps

    @require_version(242)
    def update_thermal_maps(
        self,
        project: str,
        thermal_map_files: list[
            dict[
                str,
                str
                | ThermalMapsFileType
                | ThermalBoardSide
                | CsvExcelFile
                | IcepakFile
                | ImageFile
                | list[str],
            ]
        ],
    ) -> int:
        """
        Update thermal map files to a Sherlock project.

        Available Since: 2024R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project to update thermal maps to.
        thermal_map_files: list
            List of thermal map files consisting of these properties:

            - file_name: str
                Name of the thermal file to update.
            - file_type: ThermalMapsFileType
                Thermal maps file type.
            - file_comment: str, optional
                Comment to associate with the file.
            - thermal_board_side: ThermalBoardSide
                Thermal board side.
            - file_data: CsvExcelFile|IcepakFile|ImageFile
                The properties of the thermal map file to update.
            - thermal_profiles: List of str
                List of thermal profiles.
            - cca_names: List of str, optional
                List of CCA names to provide thermal maps for. The default is ``None``,
                in which case all CCAs in the project are returned.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> from ansys.sherlock.core.types.project_types import (
            BoardBounds,
            ImageBounds,
            ImageFile,
            LegendBounds,
            LegendOrientation,
            ThermalBoardSide,
            ThermalMapsFileType,
        )
        >>> sherlock = launch_sherlock()
        >>> thermal_map_properties = ImageFile(board_bounds=BoardBounds([
            (1.0, 2.0),
            (3.0, 4.0),
            (1.0, 2.0),
            (1.0, 2.0)]),
            coordinate_units="in",
            image_bounds=ImageBounds(0.0, 0.0, 10.0, 8.0),
            legend_bounds=LegendBounds(1.0, 2.0, 4.0, 2.0),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=50.0,
            max_temperature_units="C",
            min_temperature=20.0,
            min_temperature_units="C"
        )
        >>> files = [
            {
                "file_name": "thermal_map_file.jpg",
                "file_type": ThermalMapsFileType.IMAGE,
                "file_comment": "Update thermal map",
                "thermal_board_side": ThermalBoardSide.TOP,
                "file_data": thermal_map_properties,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["CCA1", "CCA2"]
            },
        ]
        >>> sherlock.project.update_thermal_maps("Tutorial Project", files)
        """
        try:
            if project == "":
                raise SherlockUpdateThermalMapsError(message="Project name is invalid.")

            if len(thermal_map_files) == 0:
                raise SherlockUpdateThermalMapsError(message="Thermal maps are missing.")

            # Validate first
            for i, thermal_map_file in enumerate(thermal_map_files):
                if len(thermal_map_file) < 6 or len(thermal_map_file) > 7:
                    raise SherlockUpdateThermalMapsError(
                        f"Number of elements ({str(len(thermal_map_file))}) "
                        f"is wrong for thermal map {i}."
                    )
                elif (
                    not isinstance(thermal_map_file["file_name"], str)
                    or thermal_map_file["file_name"] == ""
                ):
                    raise SherlockUpdateThermalMapsError(
                        f"File name is required for thermal map {i}."
                    )
                elif not isinstance(thermal_map_file["file_type"], int):
                    raise SherlockUpdateThermalMapsError(f"Invalid file type for thermal map {i}.")
                elif not isinstance(thermal_map_file["file_comment"], (str, type(None))):
                    raise SherlockUpdateThermalMapsError(
                        f"Invalid file comment for thermal map {i}."
                    )
                elif not isinstance(thermal_map_file["thermal_board_side"], int):
                    raise SherlockUpdateThermalMapsError(
                        f"Invalid thermal board side for thermal map {i}."
                    )
                elif not isinstance(thermal_map_file["thermal_profiles"], list):
                    raise SherlockUpdateThermalMapsError(
                        f"Invalid temperature profiles for thermal map {i}."
                    )
                elif not isinstance(thermal_map_file["cca_names"], list):
                    raise SherlockUpdateThermalMapsError(
                        f"cca_names is not a list for thermal map {i}."
                    )
                elif not isinstance(
                    thermal_map_file["file_data"], (IcepakFile, ImageFile, CsvExcelFile)
                ):
                    raise SherlockUpdateThermalMapsError(f"Invalid properties for thermal map {i}.")
                if isinstance(thermal_map_file["file_data"], ImageFile):
                    file_data = thermal_map_file["file_data"]

                    if not isinstance(file_data.board_bounds, BoardBounds):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid board bounds for thermal map {i}."
                        )
                    if not isinstance(file_data.coordinate_units, (str, type(None))):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid coordinate units for thermal map {i}."
                        )
                    if not isinstance(file_data.image_bounds, ImageBounds):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid image bounds for thermal map {i}."
                        )
                    if not isinstance(file_data.legend_bounds, LegendBounds):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid legend bounds for thermal map {i}."
                        )
                    if not isinstance(file_data.legend_orientation, int):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid legend orientation for thermal map {i}."
                        )
                    if not isinstance(file_data.max_temperature, float):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid maximum temperature for thermal map {i}."
                        )
                    if not isinstance(file_data.max_temperature_units, str):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid maximum temperature units for thermal map {i}."
                        )
                    if not isinstance(file_data.min_temperature, float):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid minimum temperature for thermal map {i}."
                        )
                    if not isinstance(file_data.min_temperature_units, str):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid minimum temperature units for thermal map {i}."
                        )

                elif isinstance(thermal_map_file["file_data"], CsvExcelFile):
                    file_data = thermal_map_file["file_data"]

                    if not isinstance(file_data.header_row_count, int):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid header row count for thermal map {i}."
                        )
                    if not isinstance(file_data.numeric_format, str):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid numeric format for thermal map {i}."
                        )
                    if not isinstance(file_data.reference_id_column, str):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid reference id column for thermal map {i}."
                        )
                    if not isinstance(file_data.temperature_column, str):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid temperature column for thermal map {i}."
                        )
                    if not isinstance(file_data.temperature_units, str):
                        raise SherlockUpdateThermalMapsError(
                            f"Invalid temperature units for thermal map {i}."
                        )

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockProjectService_pb2.UpdateThermalMapRequest(project=project)

            # Add the thermal maps to the request
            for thermal_map in thermal_map_files:
                thermal_map_file = request.thermalMapFiles.add()
                thermal_map_file.fileName = thermal_map["file_name"]
                thermal_map_file.fileType = thermal_map["file_type"]
                thermal_map_file.fileComment = thermal_map["file_comment"]
                thermal_map_file.thermalBoardSide = thermal_map["thermal_board_side"]

                if isinstance(thermal_map["file_data"], CsvExcelFile):
                    thermal_map_file.csvExcelFile.headerRowCount = thermal_map[
                        "file_data"
                    ].header_row_count
                    thermal_map_file.csvExcelFile.numericFormat = thermal_map[
                        "file_data"
                    ].numeric_format
                    thermal_map_file.csvExcelFile.referenceIDColumn = thermal_map[
                        "file_data"
                    ].reference_id_column
                    thermal_map_file.csvExcelFile.temperatureColumn = thermal_map[
                        "file_data"
                    ].temperature_column
                    thermal_map_file.csvExcelFile.temperatureUnits = thermal_map[
                        "file_data"
                    ].temperature_units
                if isinstance(thermal_map["file_data"], ImageFile):
                    thermal_map_file.imageFile.coordinateUnits = thermal_map[
                        "file_data"
                    ].coordinate_units
                    for vertex in thermal_map["file_data"].board_bounds.bounds:
                        node_coordinate = thermal_map_file.imageFile.boardBounds.add()
                        node_coordinate.vertexX = vertex[0]
                        node_coordinate.vertexY = vertex[1]
                    thermal_map_file.imageFile.imageBounds.imageX = thermal_map[
                        "file_data"
                    ].image_bounds.image_x
                    thermal_map_file.imageFile.imageBounds.imageY = thermal_map[
                        "file_data"
                    ].image_bounds.image_y
                    thermal_map_file.imageFile.imageBounds.imageH = thermal_map[
                        "file_data"
                    ].image_bounds.height
                    thermal_map_file.imageFile.imageBounds.imageW = thermal_map[
                        "file_data"
                    ].image_bounds.width
                    thermal_map_file.imageFile.legendBounds.legendX = thermal_map[
                        "file_data"
                    ].legend_bounds.legend_x
                    thermal_map_file.imageFile.legendBounds.legendY = thermal_map[
                        "file_data"
                    ].legend_bounds.legend_y
                    thermal_map_file.imageFile.legendBounds.legendH = thermal_map[
                        "file_data"
                    ].legend_bounds.height
                    thermal_map_file.imageFile.legendBounds.legendW = thermal_map[
                        "file_data"
                    ].legend_bounds.width
                    thermal_map_file.imageFile.legendOrientation = thermal_map[
                        "file_data"
                    ].legend_orientation
                    thermal_map_file.imageFile.minTemperature = thermal_map[
                        "file_data"
                    ].min_temperature
                    thermal_map_file.imageFile.minTemperatureUnits = thermal_map[
                        "file_data"
                    ].min_temperature_units
                    thermal_map_file.imageFile.maxTemperature = thermal_map[
                        "file_data"
                    ].max_temperature
                    thermal_map_file.imageFile.maxTemperatureUnits = thermal_map[
                        "file_data"
                    ].max_temperature_units

                thermal_profiles = thermal_map["thermal_profiles"]
                for thermal_profile in thermal_profiles:
                    thermal_map_file.thermalProfiles.append(thermal_profile)

                """Add the CCA names to the request."""
                cca_names = thermal_map["cca_names"]
                if cca_names is not None:
                    for cca_name in cca_names:
                        thermal_map_file.cca.append(cca_name)

            response = self.stub.updateThermalMaps(request)

            return_code = response.returnCode

            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockUpdateThermalMapsError(error_array=response.errors)

                raise SherlockUpdateThermalMapsError(message=return_code.message)

            return return_code.value

        except SherlockUpdateThermalMapsError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    @require_version(242)
    def add_thermal_maps(
        self,
        project: str,
        add_thermal_map_files: list[
            dict[
                str,
                list[
                    dict[
                        str,
                        str
                        | ThermalMapsFileType
                        | ThermalBoardSide
                        | CsvExcelFile
                        | IcepakFile
                        | ImageFile
                        | list[str],
                    ]
                ]
                | str,
            ]
        ],
    ) -> int:
        """
        Add thermal map files to a Sherlock project.

        Available Since: 2024R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project to add thermal maps to.
        add_thermal_map_files: list[dict[str, list[dict[str, str | ThermalMapsFileType\
                | ThermalBoardSide | CsvExcelFile | IcepakFile | ImageFile | list[str]]] | str]]
            List of thermal map files consisting of these properties:

                - thermal_map_file: str
                    Full path to the thermal map file to add.
                - thermal_map_file_properties: list
                    List of thermal map properties consisting of these properties:

                        - file_name: str
                            Name of the thermal file to update.
                        - file_type: ThermalMapsFileType
                            Thermal maps file type.
                        - file_comment: str, optional
                            Comment to associate with the file.
                        - thermal_board_side: ThermalBoardSide
                            Thermal board side.
                        - file_data: CsvExcelFile | IcepakFile | ImageFile
                            The properties of the thermal map file to update.
                        - thermal_profiles: List of str
                            List of thermal profiles.
                        - cca_names: List of str, optional
                            List of CCA names to provide thermal maps for. The default is ``None``,
                            in which case all CCAs in the project are returned.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> from ansys.sherlock.core.types.project_types import (
            BoardBounds,
            ImageBounds,
            ImageFile,
            LegendBounds,
            LegendOrientation,
            ThermalBoardSide,
            ThermalMapsFileType,
        )
        >>> sherlock = launch_sherlock()
        >>> thermal_map_properties = ImageFile(board_bounds=BoardBounds([
            (1.0, 2.0),
            (3.0, 4.0),
            (1.0, 2.0),
            (1.0, 2.0)]),
            coordinate_units="in",
            image_bounds=ImageBounds(0.0, 0.0, 10.0, 8.0),
            legend_bounds=LegendBounds(1.0, 2.0, 4.0, 2.0),
            legend_orientation=LegendOrientation.VERTICAL,
            min_temperature=20.0,
            min_temperature_units="C",
            max_temperature=50.0,
            max_temperature_units="C"
        )
        >>> files = [
            {
                "thermal_map_file": "Thermal Image.jpg",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Image.jpg",
                        "file_type": ThermalMapsFileType.IMAGE,
                        "file_comment": "Update thermal map",
                        "thermal_board_side": ThermalBoardSide.TOP,
                        "file_data": thermal_map_properties,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["CCA1", "CCA2"]
                    },
                ]
            }
        ]
        >>> sherlock.project.add_thermal_maps("Tutorial Project", files)
        """
        try:
            if project == "":
                raise SherlockAddThermalMapsError(message="Project name is invalid.")

            if len(add_thermal_map_files) == 0:
                raise SherlockAddThermalMapsError(message="Thermal maps are missing.")

            # Validate first
            for i, add_thermal_map_file in enumerate(add_thermal_map_files):
                if len(add_thermal_map_file) < 1 or len(add_thermal_map_file) > 2:
                    raise SherlockAddThermalMapsError(
                        f"Number of elements ({str(len(add_thermal_map_file))}) "
                        f"is wrong for thermal map {i}."
                    )
                elif (
                    not isinstance(add_thermal_map_file["thermal_map_file"], str)
                    or add_thermal_map_file["thermal_map_file"] == ""
                ):
                    raise SherlockAddThermalMapsError(f"File path is required for thermal map {i}.")
                elif not isinstance(add_thermal_map_file["thermal_map_file_properties"], list):
                    raise SherlockAddThermalMapsError(
                        f"thermal_map_file_properties is not a list for thermal map {i}."
                    )

                thermal_map_file_properties = add_thermal_map_file["thermal_map_file_properties"]
                for j, thermal_map_file_property in enumerate(thermal_map_file_properties):
                    if len(thermal_map_file_property) < 6 or len(thermal_map_file_property) > 7:
                        raise SherlockAddThermalMapsError(
                            f"Number of elements ({str(len(thermal_map_file_property))}) "
                            f"is wrong for thermal map {j}."
                        )
                    elif (
                        not isinstance(thermal_map_file_property["file_name"], str)
                        or thermal_map_file_property["file_name"] == ""
                    ):
                        raise SherlockAddThermalMapsError(
                            f"File name is required for thermal map {j}."
                        )
                    elif not isinstance(thermal_map_file_property["file_type"], int):
                        raise SherlockAddThermalMapsError(f"Invalid file type for thermal map {j}.")
                    elif not isinstance(
                        thermal_map_file_property["file_comment"], (str, type(None))
                    ):
                        raise SherlockAddThermalMapsError(
                            f"Invalid file comment for thermal map {j}."
                        )
                    elif not isinstance(thermal_map_file_property["thermal_board_side"], int):
                        raise SherlockAddThermalMapsError(
                            f"Invalid thermal board side for thermal map {j}."
                        )
                    elif not isinstance(thermal_map_file_property["thermal_profiles"], list):
                        raise SherlockAddThermalMapsError(
                            f"Invalid temperature profiles for thermal map {j}."
                        )
                    elif not isinstance(thermal_map_file_property["cca_names"], list):
                        raise SherlockAddThermalMapsError(
                            f"cca_names is not a list for thermal map {j}."
                        )
                    elif not isinstance(
                        thermal_map_file_property["file_data"],
                        (IcepakFile, ImageFile, CsvExcelFile),
                    ):
                        raise SherlockAddThermalMapsError(
                            f"Invalid properties for " f"thermal map {j}."
                        )

                    if isinstance(thermal_map_file_property["file_data"], ImageFile):
                        file_data = thermal_map_file_property["file_data"]

                        if not isinstance(file_data.board_bounds, BoardBounds):
                            raise SherlockAddThermalMapsError(
                                f"Invalid board bounds for thermal map {j}."
                            )
                        if not isinstance(file_data.coordinate_units, (str, type(None))):
                            raise SherlockAddThermalMapsError(
                                f"Invalid coordinate units for thermal map {j}."
                            )
                        if not isinstance(file_data.image_bounds, ImageBounds):
                            raise SherlockAddThermalMapsError(
                                f"Invalid image bounds for thermal map {j}."
                            )
                        if not isinstance(file_data.legend_bounds, LegendBounds):
                            raise SherlockAddThermalMapsError(
                                f"Invalid legend bounds for thermal map {j}."
                            )
                        if not isinstance(file_data.legend_orientation, int):
                            raise SherlockAddThermalMapsError(
                                f"Invalid legend orientation for thermal map {j}."
                            )
                        if not isinstance(file_data.min_temperature, float):
                            raise SherlockAddThermalMapsError(
                                f"Invalid minimum temperature for thermal map {j}."
                            )
                        if not isinstance(file_data.min_temperature_units, str):
                            raise SherlockAddThermalMapsError(
                                f"Invalid minimum temperature units for thermal map {j}."
                            )
                        if not isinstance(file_data.max_temperature, float):
                            raise SherlockAddThermalMapsError(
                                f"Invalid maximum temperature for thermal map {j}."
                            )
                        if not isinstance(file_data.max_temperature_units, str):
                            raise SherlockAddThermalMapsError(
                                f"Invalid maximum temperature units for thermal map {j}."
                            )

                    elif isinstance(thermal_map_file_property["file_data"], CsvExcelFile):
                        file_data = thermal_map_file_property["file_data"]

                        if not isinstance(file_data.header_row_count, int):
                            raise SherlockAddThermalMapsError(
                                f"Invalid header row count for thermal map {j}."
                            )
                        if not isinstance(file_data.numeric_format, str):
                            raise SherlockAddThermalMapsError(
                                f"Invalid numeric format for thermal map {j}."
                            )
                        if not isinstance(file_data.reference_id_column, str):
                            raise SherlockAddThermalMapsError(
                                f"Invalid reference id column for thermal map {j}."
                            )
                        if not isinstance(file_data.temperature_column, str):
                            raise SherlockAddThermalMapsError(
                                f"Invalid temperature column for thermal map {j}."
                            )
                        if not isinstance(file_data.temperature_units, str):
                            raise SherlockAddThermalMapsError(
                                f"Invalid temperature units for thermal map {j}."
                            )

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockProjectService_pb2.AddThermalMapRequest(project=project)

            # Add thermal maps to the request
            for thermal_map in add_thermal_map_files:
                thermal_map_file = request.thermalMapFiles.add()
                thermal_map_file.thermalMapFile = thermal_map["thermal_map_file"]
                properties = thermal_map["thermal_map_file_properties"][0]
                thermal_map_file.thermalMapFileProperties.fileName = properties["file_name"]
                thermal_map_file.thermalMapFileProperties.fileType = properties["file_type"]
                thermal_map_file.thermalMapFileProperties.fileComment = properties["file_comment"]
                thermal_map_file.thermalMapFileProperties.thermalBoardSide = properties[
                    "thermal_board_side"
                ]

                if isinstance(properties["file_data"], CsvExcelFile):
                    csv_excel_file_properties = (
                        thermal_map_file.thermalMapFileProperties.csvExcelFile
                    )
                    file_properties = properties["file_data"]
                    csv_excel_file_properties.headerRowCount = file_properties.header_row_count
                    csv_excel_file_properties.numericFormat = file_properties.numeric_format
                    csv_excel_file_properties.referenceIDColumn = (
                        file_properties.reference_id_column
                    )
                    csv_excel_file_properties.temperatureColumn = file_properties.temperature_column
                    csv_excel_file_properties.temperatureUnits = file_properties.temperature_units

                if isinstance(properties["file_data"], ImageFile):
                    image_file_properties = thermal_map_file.thermalMapFileProperties.imageFile
                    image_properties = properties["file_data"]
                    image_file_properties.coordinateUnits = image_properties.coordinate_units
                    for vertex in image_properties.board_bounds.bounds:
                        node_coordinate = image_file_properties.boardBounds.add()
                        node_coordinate.vertexX = vertex[0]
                        node_coordinate.vertexY = vertex[1]
                    image_file_properties.imageBounds.imageX = image_properties.image_bounds.image_x
                    image_file_properties.imageBounds.imageY = image_properties.image_bounds.image_y
                    image_file_properties.imageBounds.imageH = image_properties.image_bounds.height
                    image_file_properties.imageBounds.imageW = image_properties.image_bounds.width
                    image_file_properties.legendBounds.legendX = (
                        image_properties.legend_bounds.legend_x
                    )
                    image_file_properties.legendBounds.legendY = (
                        image_properties.legend_bounds.legend_y
                    )
                    image_file_properties.legendBounds.legendH = (
                        image_properties.legend_bounds.height
                    )
                    image_file_properties.legendBounds.legendW = (
                        image_properties.legend_bounds.width
                    )
                    image_file_properties.legendOrientation = image_properties.legend_orientation
                    image_file_properties.minTemperature = image_properties.min_temperature
                    image_file_properties.minTemperatureUnits = (
                        image_properties.min_temperature_units
                    )

                    image_file_properties.maxTemperature = image_properties.max_temperature
                    image_file_properties.maxTemperatureUnits = (
                        image_properties.max_temperature_units
                    )

                thermal_profiles = properties["thermal_profiles"]
                for thermal_profile in thermal_profiles:
                    thermal_map_file.thermalMapFileProperties.thermalProfiles.append(
                        thermal_profile
                    )

                """Add the CCA names to the request."""
                cca_names = properties["cca_names"]
                if cca_names is not None:
                    for cca_name in cca_names:
                        thermal_map_file.thermalMapFileProperties.cca.append(cca_name)

            response = self.stub.addThermalMaps(request)

            return_code = response.returnCode

            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockAddThermalMapsError(error_array=response.errors)

                raise SherlockAddThermalMapsError(message=return_code.message)

            return return_code.value

        except SherlockAddThermalMapsError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    @require_version(242)
    def import_project_zip_archive(self, project: str, category: str, archive_file: str) -> int:
        """
        Import a zipped project archive -- multiple project mode.

        Available Since: 2024R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        category: str
            Sherlock project category.
        archive_file: str
            Full path to the .zip archive file containing the project data.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_project_zip_archive("Tutorial Project", "Demos",
        "Tutorial Project.zip")
        """
        try:
            if project == "":
                raise SherlockImportProjectZipArchiveError(message="Project name is invalid.")

            if category == "":
                raise SherlockImportProjectZipArchiveError(message="Project category is invalid.")

            if archive_file == "":
                raise SherlockImportProjectZipArchiveError(message="Archive file path is invalid.")

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockProjectService_pb2.ImportProjectZipRequest(
                project=project, category=category, archiveFile=archive_file
            )

            response = self.stub.importProjectZipArchive(request)

            if response.value == -1:
                raise SherlockImportProjectZipArchiveError(message=response.message)

        except SherlockImportProjectZipArchiveError as e:
            LOG.error(str(e))
            raise e

        return response.value

    @require_version(242)
    def import_project_zip_archive_single_mode(
        self, project: str, category: str, archive_file: str, destination_file_directory: str
    ):
        """
        Import a zipped project archive -- single project mode.

        Available Since: 2024R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        category: str
            Sherlock project category.
        archive_file: str
            Full path to the .zip archive file containing the project data.
        destination_file_directory: str
            Directory in which the Sherlock project folder will be created.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.import_project_zip_archive_single_mode("Tutorial Project",
        "Demos",
        "Tutorial Project.zip",
        "New Tutorial Project")
        """
        try:
            if project == "":
                raise SherlockImportProjectZipArchiveSingleModeError(
                    message="Project name is invalid."
                )

            if category == "":
                raise SherlockImportProjectZipArchiveSingleModeError(
                    message="Project category is invalid."
                )

            if archive_file == "":
                raise SherlockImportProjectZipArchiveSingleModeError(
                    message="Archive file path is invalid."
                )

            if destination_file_directory == "":
                raise SherlockImportProjectZipArchiveSingleModeError(
                    message="Directory of the destination file is invalid."
                )

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockProjectService_pb2.ImportProjectZipSingleModeRequest(
                destFileDir=destination_file_directory
            )

            # Add the other properties to the request
            projZipProperty = request.projZipRequest
            projZipProperty.project = project
            projZipProperty.category = category
            projZipProperty.archiveFile = archive_file

            response = self.stub.importProjectZipArchiveSingleMode(request)

            if response.value == -1:
                raise SherlockImportProjectZipArchiveSingleModeError(message=response.message)

        except SherlockImportProjectZipArchiveSingleModeError as e:
            LOG.error(str(e))
            raise e

        return response.value

    @require_version(251)
    def export_project(
        self,
        project_name: str,
        export_design_files: bool,
        export_result_files: bool,
        export_archive_results: bool,
        export_user_files: bool,
        export_log_files: bool,
        export_system_data: bool,
        export_file_dir: str,
        export_file_name: str,
        overwrite_existing_file: bool,
    ) -> int:
        """
        Export a sherlock project.

        Available Since: 2025R1

        Parameters
        ----------
        project_name: str
            Name of the project being exported.
        export_design_files: bool
            Determines if design files should be exported.
        export_result_files: bool
            Determines if all analysis module result files should be exported.
        export_archive_results: bool
            Determines if all archive result files should be exported.
        export_user_files: bool
            Determines if user properties and custom data files should be exported.
        export_log_files: bool
            Determines if Sherlock console and application log files should be exported.
        export_system_data: bool
            Determines if system technical data should be exported.
        export_file_dir: str
            Destination of export file.
        export_file_name: str
            Name to be given to the exported file.
        overwrite_existing_file: bool
            Determines if exported file will overwrite a previously existing file.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.export_project("Tutorial Project",
        True,
        True,
        True,
        True,
        True,
        True,
        "C:/Path/To/Exported/Project",
        "Exported_Project",
        True)
        """
        try:
            if project_name == "":
                raise SherlockExportProjectError(message="Project name is invalid")

            if export_file_dir == "":
                raise SherlockExportProjectError(message="Export directory is invalid")

            if export_file_name == "":
                raise SherlockExportProjectError(message="Export file name is invalid")

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockProjectService_pb2.ExportProjectRequest(
                project=project_name,
                exportDesignFiles=export_design_files,
                exportResultFiles=export_result_files,
                exportArchivedResults=export_archive_results,
                exportUserFiles=export_user_files,
                exportLogFiles=export_log_files,
                exportSystemData=export_system_data,
                exportFileDirectory=export_file_dir,
                exportFileName=export_file_name,
                overwriteExistingFile=overwrite_existing_file,
            )

            response = self.stub.exportProject(request)

            if response.value == -1:
                raise SherlockExportProjectError(message=response.message)

        except SherlockExportProjectError as e:
            LOG.error(str(e))
            raise e

        return response.value

    @require_version(251)
    def create_cca_from_modeling_region(
        self, project: str, cca_from_mr_properties: list[dict[str, bool | float | str]]
    ) -> int:
        """Create one or more CCAs from modeling regions in a given project.

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_from_mr_properties: list[dict[str, bool | float | str]]
            CCAs to be created from modeling regions consisting of these properties:

            - cca_name: str
                Name of the CCA.
            - modeling_region_id: str
                Name of the modeling region.
            - description: str
                Description of the CCA.
            - default_solder_type: str
                The default solder type. The default is ``None``.
            - default_stencil_thickness: float
                The default stencil thickness. The default is ``None``.
            - default_stencil_thickness_units: str
                Units for default stencil thickness. The default is ``None``.
            - default_part_temp_rise: float
                Default part temp rise. The default is ``None``.
            - default_part_temp_rise_units: str
                Units for default part temp rise. The default is ``None``.
                Options are ``"C"``, ``"F"``, and ``"K"``.
            - guess_part_properties: bool
                Whether to enable guess part properties. The default is ``None``.
            - generate_image_layers: bool
                Whether to generate image layers or not.  The default is ``None``.

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
        >>> sherlock.project.create_cca_from_modeling_region(
            "Test",
            [{
                'cca_name': 'Card',
                'modeling_region_id': 'MR1'
                'description': 'Test',
                'default_solder_type': 'SAC305',
                'default_stencil_thickness': 10,
                'default_stencil_thickness_units': 'mm',
                'default_part_temp_rise': 20,
                'default_part_temp_rise_units': 'C',
                'guess_part_properties': False,
                'generate_image_layers': False,
            },
            ]
        )
        """
        try:
            if project == "":
                raise SherlockCreateCCAFromModelingRegionError(message="Project name is invalid.")

            if not isinstance(cca_from_mr_properties, list):
                raise SherlockCreateCCAFromModelingRegionError(
                    message="CCA properties argument is invalid."
                )

            if len(cca_from_mr_properties) == 0:
                raise SherlockCreateCCAFromModelingRegionError(
                    message="One or more CCAs are required."
                )

            request = SherlockProjectService_pb2.CreateCcaFromModelingRegionRequest(project=project)

            for i, cca in enumerate(cca_from_mr_properties):
                cca_request = request.cCAsFromModelingRegions.add()

                if not isinstance(cca, dict):
                    raise SherlockCreateCCAFromModelingRegionError(
                        message=f"CCA properties are invalid for CCA {i}."
                    )

                if "cca_name" not in cca.keys():
                    raise SherlockCreateCCAFromModelingRegionError(
                        message=f"CCA name is missing for CCA {i}."
                    )

                if "modeling_region_id" not in cca.keys():
                    raise SherlockCreateCCAFromModelingRegionError(
                        message=f"Modeling Region ID is missing for CCA {i}."
                    )

                cca_request.ccaName = cca["cca_name"]
                cca_request.modelingRegionID = cca["modeling_region_id"]

                if cca_request.ccaName == "":
                    raise SherlockCreateCCAFromModelingRegionError(
                        message=f"CCA name is invalid for CCA {i}."
                    )

                if cca_request.modelingRegionID == "":
                    raise SherlockCreateCCAFromModelingRegionError(
                        message=f"Modeling Region ID is invalid for CCA {i}."
                    )

                if "description" in cca.keys():
                    cca_request.description = cca["description"]

                if "default_solder_type" in cca.keys():
                    cca_request.defaultSolderType = cca["default_solder_type"]

                if "default_stencil_thickness" in cca.keys():
                    cca_request.defaultStencilThickness = cca["default_stencil_thickness"]

                if "default_stencil_thickness_units" in cca.keys():
                    cca_request.defaultStencilThicknessUnits = cca[
                        "default_stencil_thickness_units"
                    ]

                if "default_part_temp_rise" in cca.keys():
                    cca_request.defaultPartTempRise = cca["default_part_temp_rise"]

                if "default_part_temp_rise_units" in cca.keys():
                    cca_request.defaultPartTempRiseUnits = cca["default_part_temp_rise_units"]

                if "guess_part_properties" in cca.keys():
                    cca_request.guessPartProperties = cca["guess_part_properties"]

                if "generate_image_layers" in cca.keys():
                    cca_request.generateImageLayers = cca["generate_image_layers"]

        except SherlockCreateCCAFromModelingRegionError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        response = self.stub.createCCAFromModelingRegion(request)

        try:
            if response.value == -1:
                raise SherlockCreateCCAFromModelingRegionError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockCreateCCAFromModelingRegionError as e:
            LOG.error(str(e))
            raise e
