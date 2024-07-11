# © 2023-2024 ANSYS, Inc. All rights reserved

"""Module containing all layer management capabilities."""
from ansys.sherlock.core.types.layer_types import (
    CircularShape,
    PCBShape,
    PolygonalShape,
    RectangularShape,
    SlotShape,
)

try:
    import SherlockLayerService_pb2
    import SherlockLayerService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockLayerService_pb2
    from ansys.api.sherlock.v0 import SherlockLayerService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockAddPottingRegionError,
    SherlockDeleteAllICTFixturesError,
    SherlockDeleteAllMountPointsError,
    SherlockDeleteAllTestPointsError,
    SherlockExportAllMountPoints,
    SherlockExportAllTestFixtures,
    SherlockExportAllTestPoints,
    SherlockUpdateMountPointsByFileError,
    SherlockUpdateTestFixturesByFileError,
    SherlockUpdateTestPointsByFileError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub


class Layer(GrpcStub):
    """Module containing all the layer management capabilities."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockLayerService."""
        super().__init__(channel)
        self.stub = SherlockLayerService_pb2_grpc.SherlockLayerServiceStub(channel)

    def add_potting_region(
        self,
        project,
        potting_regions,
    ):
        """Add one or more potting regions to a given project.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        potting_regions : list
            List of potting region properties consisting of these properties:

            - cca_name: str
                Name of the CCA.
            - potting_id: str
                Potting ID. The default is ``None``.
            - side: str
                The side to add the potting region to. The default is ``None``.
                Options are ``"TOP"``, ``"BOTTOM"``, and ``"BOT"``.
            - material: str
                The potting material. The default is ``None``.
            - potting_units: str
                The potting region units. The default is ``None``.
            - thickness: float
                The potting thickness. The default is ``None``.
            - standoff: float
                The potting standoff. The default is ``None``.
            - shape: PolygonalShape|RectangularShape|SlotShape|CircularShape|PCBShape
                The shape of the potting region.


        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> from ansys.sherlock.core.types.layer_types import PolygonalShape
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
        >>> polygonal_shape = PolygonalShape(points=[
                        (0, 0),
                        (0, 6.35),
                        (9.77, 0)
                    ], rotation=87.8)
        >>> sherlock.layer.add_potting_region(
            "Test",
            [{
                'cca_name': 'Card',
                'potting_id': 'Test Region',
                'side': 'TOP',
                'material': 'epoxyencapsulant',
                'potting_units': 'in',
                'thickness': 0.1,
                'standoff': 0.2,
                'shape': polygonal_shape
            },
            ]
        )

        """
        try:
            if project == "":
                raise SherlockAddPottingRegionError(message="Project name is invalid.")

            if not isinstance(potting_regions, list):
                raise SherlockAddPottingRegionError(message="Potting regions argument is invalid.")

            if len(potting_regions) == 0:
                raise SherlockAddPottingRegionError(
                    message="One or more potting regions are required."
                )

            request = SherlockLayerService_pb2.AddPottingRegionRequest(project=project)

            for i, potting_region in enumerate(potting_regions):
                if not isinstance(potting_region, dict):
                    raise SherlockAddPottingRegionError(
                        message=f"Potting region argument is invalid for potting region {i}."
                    )

                if "cca_name" not in potting_region.keys():
                    raise SherlockAddPottingRegionError(
                        message=f"CCA name is missing for potting region {i}."
                    )

                region_request = request.pottingRegions.add()
                region_request.ccaName = potting_region["cca_name"]

                if region_request.ccaName == "":
                    raise SherlockAddPottingRegionError(
                        message=f"CCA name is invalid for potting region {i}."
                    )

                if "potting_id" in potting_region.keys():
                    region_request.pottingID = potting_region["potting_id"]
                if "side" in potting_region.keys():
                    region_request.pottingSide = potting_region["side"]
                if "material" in potting_region.keys():
                    region_request.pottingMaterial = potting_region["material"]
                if "potting_units" in potting_region.keys():
                    region_request.pottingUnits = potting_region["potting_units"]
                if "thickness" in potting_region.keys():
                    region_request.pottingThickness = potting_region["thickness"]
                if "standoff" in potting_region.keys():
                    region_request.pottingStandoff = potting_region["standoff"]
                if "shape" not in potting_region.keys():
                    raise SherlockAddPottingRegionError(
                        message=f"Shape missing for potting region {i}."
                    )

                shape = potting_region["shape"]

                if isinstance(shape, PolygonalShape):
                    if not isinstance(shape.points, list):
                        raise SherlockAddPottingRegionError(
                            message=f"Invalid points argument for potting region {i}."
                        )

                    for j, point in enumerate(shape.points):
                        point_message = region_request.polygonalShape.points.add()

                        if not isinstance(point, tuple) or len(point) != 2:
                            raise SherlockAddPottingRegionError(
                                message=f"Point {j} invalid for potting region {i}."
                            )
                        point_message.x = point[0]
                        point_message.y = point[1]
                    region_request.polygonalShape.rotation = shape.rotation
                elif isinstance(shape, RectangularShape):
                    region_request.rectangularShape.length = shape.length
                    region_request.rectangularShape.width = shape.width
                    region_request.rectangularShape.centerX = shape.center_x
                    region_request.rectangularShape.centerY = shape.center_y
                    region_request.rectangularShape.rotation = shape.rotation
                elif isinstance(shape, SlotShape):
                    region_request.slotShape.length = shape.length
                    region_request.slotShape.width = shape.width
                    region_request.slotShape.nodeCount = shape.node_count
                    region_request.slotShape.centerX = shape.center_x
                    region_request.slotShape.centerY = shape.center_y
                    region_request.slotShape.rotation = shape.rotation
                elif isinstance(shape, CircularShape):
                    region_request.circularShape.diameter = shape.diameter
                    region_request.circularShape.nodeCount = shape.node_count
                    region_request.circularShape.centerX = shape.center_x
                    region_request.circularShape.centerY = shape.center_y
                    region_request.circularShape.rotation = shape.rotation
                elif isinstance(shape, PCBShape):
                    region_request.pCBShape.CopyFrom(SherlockLayerService_pb2.PCBShape())
                else:
                    raise SherlockAddPottingRegionError(
                        message=f"Shape invalid for potting region {i}."
                    )

        except SherlockAddPottingRegionError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        response = self.stub.addPottingRegion(request)

        try:
            if response.value == -1:
                raise SherlockAddPottingRegionError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockAddPottingRegionError as e:
            LOG.error(str(e))
            raise e

    def update_mount_points_by_file(
        self,
        project,
        cca_name,
        file_path,
    ):
        """Update mount point properties of a CCA from a CSV file.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        file_path : str
            Path for the CSV file with the mount point properties.

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
        >>> sherlock.layer.update_mount_points_by_file(
            "Test",
            "Card",
            "MountPointImport.csv",
        )
        """
        try:
            if project == "":
                raise SherlockUpdateMountPointsByFileError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdateMountPointsByFileError(message="CCA name is invalid.")
            if file_path == "":
                raise SherlockUpdateMountPointsByFileError(message="File path is required.")
        except SherlockUpdateMountPointsByFileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        request = SherlockLayerService_pb2.UpdateMountPointsByFileRequest(
            project=project,
            ccaName=cca_name,
            filePath=file_path,
        )

        response = self.stub.updateMountPointsByFile(request)

        return_code = response.returnCode

        try:
            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockUpdateMountPointsByFileError(error_array=response.updateError)

                raise SherlockUpdateMountPointsByFileError(message=return_code.message)
            else:
                LOG.info(return_code.message)
                return return_code.value
        except SherlockUpdateMountPointsByFileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def delete_all_mount_points(self, project, cca_name):
        """Delete all mount points for a CCA.

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
        >>> sherlock.layer.update_mount_points_by_file(
            "Test",
            "Card",
            "MountPointImport.csv",
        )
        >>> sherlock.layer.delete_all_mount_points("Test", "Card")
        """
        try:
            if project == "":
                raise SherlockDeleteAllMountPointsError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockDeleteAllMountPointsError(message="CCA name is invalid.")

            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                return

            request = SherlockLayerService_pb2.DeleteAllMountPointsRequest(
                project=project,
                ccaName=cca_name,
            )

            response = self.stub.deleteAllMountPoints(request)

            if response.value == -1:
                raise SherlockDeleteAllMountPointsError(message=response.message)

        except SherlockDeleteAllMountPointsError as e:
            LOG.error(str(e))
            raise e

        return response.value

    def delete_all_ict_fixtures(self, project, cca_name):
        """Delete all ICT fixtures for a CCA.

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
        >>> sherlock.layer.update_ict_fixtures_by_file(
            "Test",
            "Card",
            "ICTFixturesImport.csv",
        )
        >>> sherlock.layer.delete_all_ict_fixtures("Test", "Card")
        """
        try:
            if project == "":
                raise SherlockDeleteAllICTFixturesError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockDeleteAllICTFixturesError(message="CCA name is invalid.")

            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                return

            request = SherlockLayerService_pb2.DeleteAllICTFixturesRequest(
                project=project,
                ccaName=cca_name,
            )

            response = self.stub.deleteAllICTFixtures(request)

            if response.value == -1:
                raise SherlockDeleteAllICTFixturesError(message=response.message)

        except SherlockDeleteAllICTFixturesError as e:
            LOG.error(str(e))
            raise e

        return response.value

    def delete_all_test_points(self, project, cca_name):
        """Delete all test points for a CCA.

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
        >>> sherlock.layer.update_test_points_by_file(
            "Test",
            "Card",
            "TestPointsImport.csv",
        )
        >>> sherlock.layer.delete_all_test_points("Test", "Card")
        """
        try:
            if project == "":
                raise SherlockDeleteAllTestPointsError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockDeleteAllTestPointsError(message="CCA name is invalid.")

            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                return

            request = SherlockLayerService_pb2.DeleteAllTestPointsRequest(
                project=project,
                ccaName=cca_name,
            )

            response = self.stub.deleteAllTestPoints(request)

            if response.value == -1:
                raise SherlockDeleteAllTestPointsError(message=response.message)

        except SherlockDeleteAllTestPointsError as e:
            LOG.error(str(e))
            raise e

        return response.value

    def update_test_points_by_file(
        self,
        project,
        cca_name,
        file_path,
    ):
        """Update test point properties of a CCA from a CSV file.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        file_path : str
            Path for the CSV file with the test point properties.

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
        >>> sherlock.layer.update_test_points_by_file(
            "Test",
            "Card",
            "TestPointsImport.csv",
        )
        """
        try:
            if project == "":
                raise SherlockUpdateTestPointsByFileError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdateTestPointsByFileError(message="CCA name is invalid.")
            if file_path == "":
                raise SherlockUpdateTestPointsByFileError(message="File path is required.")

            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                return

            request = SherlockLayerService_pb2.UpdateTestPointsByFileRequest(
                project=project,
                ccaName=cca_name,
                filePath=file_path,
            )

            response = self.stub.updateTestPointsByFile(request)

            return_code = response.returnCode

            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockUpdateTestPointsByFileError(error_array=response.updateError)

                raise SherlockUpdateTestPointsByFileError(message=return_code.message)

            else:
                LOG.info(return_code.message)
                return return_code.value

        except SherlockUpdateTestPointsByFileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def update_test_fixtures_by_file(
        self,
        project,
        cca_name,
        file_path,
    ):
        """Update test fixture properties of a CCA from a CSV file.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        file_path : str
            Path for the CSV file with the test fixture properties.

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
        >>> sherlock.layer.update_test_fixtures_by_file(
            "Test",
            "Card",
            "TestFixturesImport.csv",
        )
        """
        try:
            if project == "":
                raise SherlockUpdateTestFixturesByFileError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdateTestFixturesByFileError(message="CCA name is invalid.")
            if file_path == "":
                raise SherlockUpdateTestFixturesByFileError(message="File path is required.")

            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                return

            request = SherlockLayerService_pb2.UpdateICTFixturesByFileRequest(
                project=project,
                ccaName=cca_name,
                filePath=file_path,
            )

            response = self.stub.updateICTFixturesByFile(request)

            return_code = response.returnCode

            if return_code.value == -1:
                if return_code.message == "":
                    raise SherlockUpdateTestFixturesByFileError(error_array=response.updateError)

                raise SherlockUpdateTestFixturesByFileError(message=return_code.message)

            else:
                LOG.info(return_code.message)
                return return_code.value

        except SherlockUpdateTestFixturesByFileError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def export_all_test_points(
        self,
        project,
        cca_name,
        export_file,
        length_units="DEFAULT",
        displacement_units="DEFAULT",
        force_units="DEFAULT",
    ):
        """Export the test point properties for a CCA.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        export_file : str
            Full path for the CSV file to export the test points list to.
        length_units : str, optional
            Length units to use when exporting the test points.
            The default is ``DEFAULT``.
        displacement_units : str, optional
            Displacement units to use when exporting the test points.
            The default is ``DEFAULT``.
        force_units : str, optional
            Force units to use when exporting the test points.
            The default is ``DEFAULT``.

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
            project="Tutorial Project",
            cca_name="Card",
        )
        >>> sherlock.layer.export_all_test_points(
            "Tutorial Project",
            "Card",
            "TestPointsExport.csv",
            "DEFAULT",
            "DEFAULT",
            "DEFAULT",
        )
        """
        try:
            if project == "":
                raise SherlockExportAllTestPoints(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockExportAllTestPoints(message="CCA name is invalid.")
            if export_file == "":
                raise SherlockExportAllTestPoints(message="File path is required.")

            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                return

            request = SherlockLayerService_pb2.ExportAllTestPointsRequest(
                project=project,
                ccaName=cca_name,
                filePath=export_file,
                lengthUnits=length_units,
                displacementUnits=displacement_units,
                forceUnits=force_units,
            )

            return_code = self.stub.exportAllTestPoints(request)

            if return_code.value != 0:
                raise SherlockExportAllTestPoints(error_array=return_code.message)

            return return_code.value

        except SherlockExportAllTestPoints as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    def export_all_test_fixtures(
        self,
        project,
        cca_name,
        export_file,
        units="DEFAULT",
    ):
        """Export the test fixture properties for a CCA.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        export_file : str
            Full path for the CSV file to export the text fixtures list to.
        units : str, optional
            Units to use when exporting the test fixtures.
            The default is ``DEFAULT``.


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
            project="Tutorial Project",
            cca_name="Card",
        )
        >>> sherlock.layer.export_all_test_fixtures(
            "Tutorial Project",
            "Card",
            "TestFixturesExport.csv",
            "DEFAULT",
        )
        """
        try:
            if project == "":
                raise SherlockExportAllTestFixtures(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockExportAllTestFixtures(message="CCA name is invalid.")
            if export_file == "":
                raise SherlockExportAllTestFixtures(message="File path is required.")

            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                return

            request = SherlockLayerService_pb2.ExportAllICTFixturesRequest(
                project=project,
                ccaName=cca_name,
                filePath=export_file,
                units=units,
            )

            response = self.stub.exportAllICTFixtures(request)

            if response.value == -1:
                raise SherlockExportAllTestFixtures(message=response.message)

        except SherlockExportAllTestFixtures as e:
            LOG.error(str(e))
            raise e

        return response.value

    def export_all_mount_points(
        self,
        project,
        cca_name,
        export_file,
        units="DEFAULT",
    ):
        """Export the mount point properties for a CCA.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        export_file : str
            Full path for the CSV file to export the mount points list to.
        units : str, optional
            Units to use when exporting the mount points.
            The default is ``DEFAULT``.


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
            project="Tutorial Project",
            cca_name="Card",
        )
        >>> sherlock.layer.export_all_mount_points(
            "Tutorial Project",
            "Card",
            "MountPointsExport.csv",
            "DEFAULT",
        )
        """
        try:
            if project == "":
                raise SherlockExportAllMountPoints(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockExportAllMountPoints(message="CCA name is invalid.")
            if export_file == "":
                raise SherlockExportAllMountPoints(message="File path is required.")

            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                return

            request = SherlockLayerService_pb2.ExportAllMountPointsRequest(
                project=project,
                ccaName=cca_name,
                filePath=export_file,
                units=units,
            )

            response = self.stub.exportAllMountPoints(request)

            if response.value == -1:
                raise SherlockExportAllMountPoints(message=response.message)

        except SherlockExportAllMountPoints as e:
            LOG.error(str(e))
            raise e

        return response.value
