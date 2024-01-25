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
    SherlockDeleteProjectError,
    SherlockGenerateProjectReportError,
    SherlockImportIpc2581Error,
    SherlockImportODBError,
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

    def update_thermal_maps(self, project, thermal_maps):
        """
        Update thermal map files to a Sherlock project.

        Parameters
        ----------
        project : str
            Name of the Sherlock project to update thermal maps to.
        thermal_maps : list
            List of thermal maps consisting of these properties:

            - file_name : str
                Name of the thermal file to update.
            - file_type : ThermalMapsFileType
                Thermal maps file type.
            - file_comment : str, optional
                Comment to associate with the file.
            - thermal_board_side : ThermalMapsBoardSide
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
            ThermalMapsBoardSide,
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
        >>> thermal_maps = [
            {
                "file_name": "thermal_map.jpg",
                "file_type": ThermalMapsFileType.IMAGE,
                "file_comment": "Update thermal map",
                "thermal_board_side": ThermalBoardSide.TOP,
                "file_data": thermal_map_properties,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["CCA1", "CCA2"]
            },
        ]
        >>> sherlock.project.update_thermal_maps("Tutorial Project", thermal_maps)
        """
        try:
            if project == "":
                raise SherlockUpdateThermalMapsError(message="Project name is invalid.")

            if len(thermal_maps) == 0:
                raise SherlockUpdateThermalMapsError(message="Thermal maps are missing.")

            # Validate first
            for i, thermal_map in enumerate(thermal_maps):
                if len(thermal_map) < 6 or len(thermal_map) > 7:
                    raise SherlockUpdateThermalMapsError(
                        f"Number of elements ({str(len(thermal_maps))}) "
                        f"is wrong for thermal map {i}."  # noqa: E501
                    )
                elif (
                    not isinstance(thermal_map["file_name"], str) or thermal_map["file_name"] == ""
                ):
                    raise SherlockUpdateThermalMapsError(
                        f"File name is required for thermal map {i}."
                    )
                elif not isinstance(thermal_map["file_type"], int):
                    raise SherlockUpdateThermalMapsError(f"Invalid file type for thermal map {i}.")
                elif not isinstance(thermal_map["file_comment"], (str, type(None))):
                    raise SherlockUpdateThermalMapsError(
                        f"Invalid file comment for thermal map {i}."
                    )
                elif not isinstance(thermal_map["thermal_board_side"], int):
                    raise SherlockUpdateThermalMapsError(
                        f"Invalid thermal board side for thermal map {i}."
                    )
                elif not isinstance(thermal_map["thermal_profiles"], list):
                    raise SherlockUpdateThermalMapsError(
                        f"Invalid temperature profiles for thermal map {i}."
                    )
                elif not isinstance(thermal_map["cca_names"], list):
                    raise SherlockUpdateThermalMapsError(
                        f"cca_names is not a list for thermal map {i}."
                    )
                elif not isinstance(
                    thermal_map["file_data"], (IcepakFile, ImageFile, CsvExcelFile)
                ):
                    raise SherlockUpdateThermalMapsError(f"Invalid properties for thermal map {i}.")
                if isinstance(thermal_map["file_data"], ImageFile):
                    file_data = thermal_map["file_data"]

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

                elif isinstance(thermal_map["file_data"], CsvExcelFile):
                    file_data = thermal_map["file_data"]

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
            for s in thermal_maps:
                thermal_map = request.thermalMapFiles.add()
                thermal_map.fileName = s["file_name"]
                thermal_map.fileType = s["file_type"]
                thermal_map.fileComment = s["file_comment"]
                thermal_map.thermalBoardSide = s["thermal_board_side"]

                if isinstance(s["file_data"], CsvExcelFile):
                    thermal_map.csvExcelFile.headerRowCount = s["file_data"].header_row_count
                    thermal_map.csvExcelFile.numericFormat = s["file_data"].numeric_format
                    thermal_map.csvExcelFile.referenceIDColumn = s["file_data"].reference_id_column
                    thermal_map.csvExcelFile.temperatureColumn = s["file_data"].temperature_column
                    thermal_map.csvExcelFile.temperatureUnits = s["file_data"].temperature_units
                if isinstance(s["file_data"], ImageFile):
                    thermal_map.imageFile.coordinateUnits = s["file_data"].coordinate_units
                    for vertex in s["file_data"].board_bounds.bounds:
                        node_coordinate = thermal_map.imageFile.boardBounds.add()
                        node_coordinate.vertexX = vertex[0]
                        node_coordinate.vertexY = vertex[1]
                    thermal_map.imageFile.imageBounds.imageX = s["file_data"].image_bounds.image_x
                    thermal_map.imageFile.imageBounds.imageY = s["file_data"].image_bounds.image_y
                    thermal_map.imageFile.imageBounds.imageH = s["file_data"].image_bounds.height
                    thermal_map.imageFile.imageBounds.imageW = s["file_data"].image_bounds.width
                    thermal_map.imageFile.legendBounds.legendX = s[
                        "file_data"
                    ].legend_bounds.legend_x
                    thermal_map.imageFile.legendBounds.legendY = s[
                        "file_data"
                    ].legend_bounds.legend_y
                    thermal_map.imageFile.legendBounds.legendH = s["file_data"].legend_bounds.height
                    thermal_map.imageFile.legendBounds.legendW = s["file_data"].legend_bounds.width
                    thermal_map.imageFile.legendOrientation = s["file_data"].legend_orientation
                    thermal_map.imageFile.minTemperature = s["file_data"].min_temperature
                    thermal_map.imageFile.minTemperatureUnits = s["file_data"].min_temperature_units
                    thermal_map.imageFile.maxTemperature = s["file_data"].max_temperature
                    thermal_map.imageFile.maxTemperatureUnits = s["file_data"].max_temperature_units

                thermal_profiles = s["thermal_profiles"]
                for thermal_profile in thermal_profiles:
                    thermal_map.thermalProfiles.append(thermal_profile)

                """Add the CCA names to the request."""
                if len(s) == 7:
                    cca_names = s["cca_names"]
                    if cca_names is not None:
                        for cca_name in cca_names:
                            thermal_map.cca.append(cca_name)

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
