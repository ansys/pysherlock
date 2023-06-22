# © 2023 ANSYS, Inc. All rights reserved

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
    SherlockAddStrainMapsError,
    SherlockDeleteProjectError,
    SherlockGenerateProjectReportError,
    SherlockImportIpc2581Error,
    SherlockImportODBError,
    SherlockListCCAsError,
    SherlockListStrainMapsError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub


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
        project=None,
        cca_name=None,
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
        project: str, optional
            Name of the Sherlock project. The default is ``None``, in which
            case the name of the ODB++ archive file is used for the project name.
        cca_name : str, optional
            Name of the CCA name. The default is ``None``, in which case the
            name of the ODB++ archive file is used for the CCA name.

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
            project=project,
            ccaName=cca_name,
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
        self, archive_file, include_other_layers, guess_part_properties, project=None, cca_name=None
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
                                cca_name="Card")
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

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> project.add_strain_maps("Tutorial Project",
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

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> strain_maps = project.list_strain_maps("AssemblyTutorial",["Main Board","Power Module"])
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
