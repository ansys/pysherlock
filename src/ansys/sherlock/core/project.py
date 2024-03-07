# © 2024 ANSYS, Inc. All rights reserved

"""Module containing all project management capabilities."""
import os

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
    SherlockDeleteProjectError,
    SherlockGenerateProjectReportError,
    SherlockImportIpc2581Error,
    SherlockImportODBError,
    SherlockImportProjectZipArchiveError,
    SherlockImportProjectZipArchiveSingleModeError,
    SherlockListCCAsError,
    SherlockListStrainMapsError,
    SherlockListThermalMapsError,
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
)


class Project(GrpcStub):
    """Contains all project management capabilities."""

    def __init__(self, channel):
        """Initialize a gRPC stub for Sherlock Project service."""
        super().__init__(channel)
        self.stub = SherlockProjectService_pb2_grpc.SherlockProjectServiceStub(channel)

    def delete_project(self, project):
        """Delete a Sherlock project.

        Parameters
        ----------
        project : str
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
            LOG.error("There is no connection to a gRPC service.")
            return

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

    def import_odb_archive(
        self,
        archive_file,
        process_layer_thickness,
        include_other_layers,
        process_cutout_file,
        guess_part_properties,
        ims_stackup=False,
        project=None,
        cca_name=None,
        polyline_simplification=False,
        polyline_tolerance=0.1,
        polyline_tolerance_units="mm",
    ):
        """Import an ODB++ archive file.

        Parameters
        ----------
        archive_file : str
            Full path to the ODB++ archive file.
        process_layer_thickness : bool
            Whether to assign stackup thickness.
        include_other_layers : bool
            Whether to include other layers.
        process_cutout_file : bool
            Whether to process cutouts.
        guess_part_properties: bool
            Whether to guess part properties.
        ims_stackup: bool, optional
            Whether to generate an IMS stackup
        project: str, optional
            Name of the Sherlock project. The default is ``None``, in which
            case the name of the ODB++ archive file is used for the project name.
        cca_name : str, optional
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
            LOG.error("There is no connection to a gRPC service.")
            return

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

    def import_ipc2581_archive(
        self,
        archive_file,
        include_other_layers,
        guess_part_properties,
        project=None,
        cca_name=None,
        polyline_simplification=False,
        polyline_tolerance=0.1,
        polyline_tolerance_units="mm",
    ):
        """Import an IPC-2581 archive file.

        Parameters
        ----------
        archive_file : str
            Full path to the IPC-2581 archive file.
        include_other_layers : bool
            Whether to include other layers.
        guess_part_properties: bool
            Whether to guess part properties
        project: str, optional
            Name of the Sherlock project. The default is ``None``, in which case
            the name of the IPC-2581 archive file is used for the project name.
        cca_name : str, optional
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
            LOG.error("There is no connection to a gRPC service.")
            return

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

    def generate_project_report(self, project, author, company, report_file):
        """Generate a project report.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        author : str
            Name of the author who is generating the report.
        company : str
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
            "Project Report.pdf",
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
            LOG.error("There is no connection to a gRPC service.")
            return

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

    def list_ccas(self, project, cca_names=None):
        """List CCAs and subassembly CCAs assigned to each CCA or given CCAs.

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_names : List of str, optional
            List of CCA names. The default is ``None``, in which case all CCAs
            in the project are returned.

        Returns
        -------
        list
            CCAs and subassembly CCAs.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> ccas = project.list_ccas("AssemblyTutorial",["Main Board"])
        """
        try:
            if project == "":
                raise SherlockListCCAsError(message="Project name is invalid.")

            if cca_names is not None and type(cca_names) is not list:
                raise SherlockListCCAsError(message="cca_names is not a list.")

            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                return

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

    def add_cca(self, project, cca_properties):
        """Add one or more CCAs to a project.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_properties : list
            List of CCAs to be added consisting of these properties:

            - cca_name : str
                Name of the CCA.
            - description : str
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
            LOG.error("There is no connection to a gRPC service.")
            return

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

    def add_strain_maps(self, project, strain_maps):
        """Add a CSV file with strain maps to the CCAs.

        Parameters
        ----------
        project: str
            Name of the Sherlock project to add strain maps to.
        strain_maps : list
            List of strain maps consisting of these properties:

            - strain_map_file : str
                Full path to the CSV file with the strain maps.
            - file_comment : str
                Comment to associate with the file.
            - header_row_count : int
                Number of rows before the file's column header.
            - reference_id_column : str
                Name of the column in the file with reference IDs.
            - strain_column : str
                Name of the column in the file with strain values.
            - strain_units : str
                Strain units. Options are ``µε`` and ``ε``.
            - ccas : list, optional
                List of CCA names to assign the file to. When no list is
                specified, the file is assigned to all CCAs in the project.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.project.add_strain_maps("Tutorial Project",
            [("StrainMap.csv",
            "This is the strain map file for the project",
            0,
            "refDes",
            "strain",
            "µε"
            ["Main Board"])
            )],
        """
        try:
            if project == "":
                raise SherlockAddStrainMapsError(message="Project name is invalid.")

            if len(strain_maps) == 0:
                raise SherlockAddStrainMapsError(message="Strain maps are missing.")

            # Validate first
            for i, strain_map in enumerate(strain_maps):
                if len(strain_map) < 6 or len(strain_map) > 7:
                    raise SherlockAddStrainMapsError(
                        f"Number of elements ({str(len(strain_maps))}) is wrong for strain map {i}."  # noqa: E501
                    )
                elif not isinstance(strain_map[0], str) or strain_map[0] == "":
                    raise SherlockAddStrainMapsError(f"Path is required for strain map {i}.")
                elif not isinstance(strain_map[2], int) or strain_map[2] == "":
                    raise SherlockAddStrainMapsError(
                        f"Header row count is required for strain map {i}."
                    )
                elif strain_map[2] < 0:
                    raise SherlockAddStrainMapsError(
                        f"Header row count must be greater than or equal to 0 for strain map {i}."
                    )
                elif not isinstance(strain_map[3], str) or strain_map[3] == "":
                    raise SherlockAddStrainMapsError(
                        f"Reference ID column is required for strain map {i}."
                    )
                elif not isinstance(strain_map[4], str) or strain_map[4] == "":
                    raise SherlockAddStrainMapsError(
                        f"Strain column is required for strain map {i}."
                    )
                elif not isinstance(strain_map[5], str) or strain_map[5] == "":
                    raise SherlockAddStrainMapsError(
                        f"Strain units are required for strain map {i}."
                    )
                elif strain_map[5] != "µε" and strain_map[5] != "ε":
                    raise SherlockAddStrainMapsError(
                        f'Strain units "{strain_map[5]}" are invalid for strain map {i}.'
                    )
                elif (
                    len(strain_map) == 7
                    and strain_map[6] is not None
                    and type(strain_map[6]) is not list
                ):
                    raise SherlockAddStrainMapsError(
                        message=f"cca_names is not a list for strain map {i}."
                    )

            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                return

            request = SherlockProjectService_pb2.AddStrainMapRequest(project=project)

            # Add the strain maps to the request
            for s in strain_maps:
                strain_map = request.strainMapFiles.add()
                strain_map.strainMapFile = s[0]
                strain_map.fileComment = s[1]
                strain_map.headerRowCount = s[2]
                strain_map.referenceIDColumn = s[3]
                strain_map.strainColumn = s[4]
                strain_map.strainUnits = s[5]

                """Add the CCA names to the request."""
                if len(s) == 7:
                    cca_names = s[6]
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

    def list_strain_maps(self, project, cca_names=None):
        """List the strain maps assigned to each CCA or given CCAs.

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_names : List of str, optional
            List of CCA names to provide strain maps for. The default is ``None``,
            in which case all CCAs in the project are returned.

        Returns
        -------
        list
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
                LOG.error("There is no connection to a gRPC service.")
                return

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

    def add_project(self, project_name: str, project_category: str, project_description: str):
        """Add a sherlock project to sherlock.

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
            LOG.error("There is no connection to a gRPC service.")
            return

        request = SherlockProjectService_pb2.AddProjectRequest(
            project=project_name, category=project_category, description=project_description
        )

        return_code = self.stub.addProject(request)

        if return_code.value == -1:
            raise SherlockAddProjectError(return_code.message)

        return return_code.value

    def list_thermal_maps(self, project, cca_names=None):
        """List the thermal map files and their type assigned to each CCA of given CCAs.

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_names : List of str, optional
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
                LOG.error("There is no connection to a gRPC service.")
                return

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

    def update_thermal_maps(self, project, thermal_map_files):
        """
        Update thermal map files to a Sherlock project.

        Parameters
        ----------
        project : str
            Name of the Sherlock project to update thermal maps to.
        thermal_map_files : list
            List of thermal map files consisting of these properties:

            - file_name : str
                Name of the thermal file to update.
            - file_type : ThermalMapsFileType
                Thermal maps file type.
            - file_comment : str, optional
                Comment to associate with the file.
            - thermal_board_side : ThermalBoardSide
                Thermal board side.
            - file_data : CsvExcelFile|IcepakFile|ImageFile
                The properties of the thermal map file to update.
            - thermal_profiles : List of str
                List of thermal profiles.
            - cca_names : List of str, optional
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
        >>> thermal_map_files = [
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
        >>> sherlock.project.update_thermal_maps("Tutorial Project", thermal_map_files)
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
                LOG.error("There is no connection to a gRPC service.")
                return

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

    def add_thermal_maps(self, project, add_thermal_map_files):
        """
        Add thermal map files to a Sherlock project.

        Parameters
        ----------
        project : str
            Name of the Sherlock project to add thermal maps to.
        add_thermal_map_files : list
            List of thermal map files consisting of these properties:

                - thermal_map_file : str
                    Full path to the thermal map file to add.
                - thermal_map_file_properties : list
                    List of thermal map properties consisting of these properties:

                        - file_name : str
                            Name of the thermal file to update.
                        - file_type : ThermalMapsFileType
                            Thermal maps file type.
                        - file_comment : str, optional
                            Comment to associate with the file.
                        - thermal_board_side : ThermalBoardSide
                            Thermal board side.
                        - file_data : CsvExcelFile|IcepakFile|ImageFile
                            The properties of the thermal map file to update.
                        - thermal_profiles : List of str
                            List of thermal profiles.
                        - cca_names : List of str, optional
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
        >>> add_thermal_map_files = [
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
        >>> sherlock.project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
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
                LOG.error("There is no connection to a gRPC service.")
                return

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

    def import_project_zip_archive(self, project, category, archive_file):
        """
        Import a zipped project archive -- multiple project mode.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        category : str
            Sherlock project category.
        archive_file : str
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
                LOG.error("There is no connection to a gRPC service.")
                return

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

    def import_project_zip_archive_single_mode(
        self, project, category, archive_file, destination_file_directory
    ):
        """
        Import a zipped project archive -- single project mode.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        category : str
            Sherlock project category.
        archive_file : str
            Full path to the .zip archive file containing the project data.
        destination_file_directory : str
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
                LOG.error("There is no connection to a gRPC service.")
                return

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
