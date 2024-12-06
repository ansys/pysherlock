# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

"""Module containing all layer management capabilities."""
import grpc

from ansys.sherlock.core.types.layer_types import (
    CircularShape,
    CopyPottingRegionRequest,
    DeletePottingRegionRequest,
    PCBShape,
    PolygonalShape,
    RectangularShape,
    SlotShape,
    UpdatePottingRegionRequest,
)

try:
    import SherlockCommonService_pb2
    import SherlockLayerService_pb2
    from SherlockLayerService_pb2 import ModelingRegion
    import SherlockLayerService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2
    from ansys.api.sherlock.v0 import SherlockLayerService_pb2
    from ansys.api.sherlock.v0 import SherlockLayerService_pb2_grpc
    from ansys.api.sherlock.v0.SherlockLayerService_pb2 import ModelingRegion

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockAddModelingRegionError,
    SherlockAddPottingRegionError,
    SherlockCopyModelingRegionError,
    SherlockDeleteAllICTFixturesError,
    SherlockDeleteAllMountPointsError,
    SherlockDeleteAllTestPointsError,
    SherlockDeleteModelingRegionError,
    SherlockExportAllMountPoints,
    SherlockExportAllTestFixtures,
    SherlockExportAllTestPointsError,
    SherlockNoGrpcConnectionException,
    SherlockUpdateModelingRegionError,
    SherlockUpdateMountPointsByFileError,
    SherlockUpdateTestFixturesByFileError,
    SherlockUpdateTestPointsByFileError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub
from ansys.sherlock.core.utils.version_check import require_version


class Layer(GrpcStub):
    """Module containing all the layer management capabilities."""

    def __init__(self, channel: grpc.Channel, server_version: int):
        """Initialize a gRPC stub for SherlockLayerService."""
        super().__init__(channel, server_version)
        self.stub = SherlockLayerService_pb2_grpc.SherlockLayerServiceStub(channel)

    @require_version(241)
    def add_potting_region(
        self,
        project: str,
        potting_regions: list[
            dict[
                str,
                float
                | str
                | PolygonalShape
                | RectangularShape
                | SlotShape
                | CircularShape
                | PCBShape,
            ]
        ],
    ) -> int:
        """Add one or more potting regions to a given project.

        Available Since: 2024R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        potting_regions: list[dict[str, float | str | PolygonalShape | RectangularShape | SlotShape\
 | CircularShape | PCBShape]]
            Potting region properties consisting of these properties:

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
            raise SherlockNoGrpcConnectionException()

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

    @require_version(251)
    def update_potting_region(
        self, request: UpdatePottingRegionRequest
    ) -> list[SherlockCommonService_pb2.ReturnCode]:
        """Update one or more potting regions in a specific project.

        Available Since: 2025R1

        Parameters
        ----------
        request: UpdatePottingRegionRequest
            Contains all the information needed to update one or more potting regions per project.

        Returns
        -------
        list[SherlockCommonService_pb2.ReturnCode]
            Return codes for each request.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> from ansys.sherlock.core.types.layer_types import PolygonalShape
        >>> from ansys.sherlock.core.types.layer_types import PottingRegionUpdateData
        >>> from ansys.sherlock.core.types.layer_types import PottingRegion
        >>> sherlock = launch_sherlock()
        >>>
        >>> update_request1 = PottingRegionUpdateData(
            potting_region_id_to_update=potting_id,
            potting_region=PottingRegionData(
                cca_name=cca_name,
                potting_id=potting_id,
                potting_side=potting_side,
                potting_material=potting_material,
                potting_units=potting_units,
                potting_thickness=potting_thickness,
                potting_standoff=potting_standoff,
                shape=PolygonalShape(
                    points=[(0, 1), (5, 1), (5, 5), (1, 5)],
                    rotation=45.0
                )
            )
        )
        >>> update_request2 = PottingRegionUpdateData(
            potting_region_id_to_update=potting_id,
            potting_region=PottingRegionData(
                cca_name=cca_name,
                potting_id=potting_id,
                potting_side=potting_side,
                potting_material=potting_material,
                potting_units=potting_units,
                potting_thickness=potting_thickness,
                potting_standoff=potting_standoff,
                shape=PolygonalShape(
                    points=[(0, 1), (5, 1), (5, 5), (1, 5)],
                    rotation=0.0
                )
            )
        )
        >>> potting_region_requests = [
            update_request1,
            update_request2
        ]
        >>> return_codes = sherlock.layer.update_potting_region(request)
        """
        update_request = request._convert_to_grpc()

        responses = []
        for grpc_return_code in self.stub.updatePottingRegion(update_request):
            responses.append(grpc_return_code)
        return responses

    @require_version(251)
    def copy_potting_region(
        self, request: CopyPottingRegionRequest
    ) -> list[SherlockCommonService_pb2.ReturnCode]:
        """Copy one or more potting regions in a specific project.

        Available Since: 2025R1

        Parameters
        ----------
        request: CopyPottingRegionRequest
             Contains all the information needed to copy one or more potting regions per project.

        Returns
        -------
        list[SherlockCommonService_pb2.ReturnCode]
            Return codes for each request.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> from ansys.sherlock.core.types.layer_types import CopyPottingRegionRequest
        >>> from ansys.sherlock.core.types.layer_types import PottingRegionCopyData
        >>> sherlock = launch_sherlock()
        >>>
        >>> copy_request_example = CopyPottingRegionRequest(
            project=project,
            potting_region_copy_data=[
                PottingRegionCopyData(
                    cca_name=cca_name,
                    potting_id=potting_id,
                    copy_potting_id=new_id,
                    center_x=center_x,
                    center_y=center_y
                ),
                PottingRegionCopyData(
                    cca_name=cca_name,
                    potting_id=new_id,
                    copy_potting_id=new_id+"1",
                    center_x=center_x,
                    center_y=center_y
                )
            ]
        )
        >>> responses_example = sherlock.layer.copy_potting_region(copy_request_example)
        """
        copy_request = request._convert_to_grpc()

        responses = []
        for grpc_return_code in self.stub.copyPottingRegion(copy_request):
            responses.append(grpc_return_code)
        return responses

    @require_version(251)
    def delete_potting_region(
        self, request: DeletePottingRegionRequest
    ) -> list[SherlockCommonService_pb2.ReturnCode]:
        """Delete on or more potting regions in a specific project.

        Available Since: 2025R1

        Parameters
        ----------
        request: DeletePottingRegionRequest
             Contains all the information needed to delete one or more potting regions per project.

        Returns
        -------
        list[SherlockCommonService_pb2.ReturnCode]
            Return codes for each request.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> from ansys.sherlock.core.types.layer_types import DeletePottingRegionRequest
        >>> from ansys.sherlock.core.types.layer_types import PottingRegionDeleteData
        >>> sherlock = launch_sherlock()
        >>>
        >>> delete_request_example = DeletePottingRegionRequest(
            project=project,
            potting_region_delete_data=[
                PottingRegionDeleteData(
                    cca_name=cca_name,
                    potting_id=potting_id
                )
            ]
        )
        >>> responses_example = sherlock.layer.delete_potting_region(delete_request_example)
        """
        delete_request = request._convert_to_grpc()

        responses = []
        for grpc_return_code in self.stub.deletePottingRegion(delete_request):
            responses.append(grpc_return_code)
        return responses

    @require_version()
    def update_mount_points_by_file(
        self,
        project: str,
        cca_name: str,
        file_path: str,
    ) -> int:
        """Update mount point properties of a CCA from a CSV file.

        Available Since: 2023R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        file_path: str
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
            "MountPointImport.csv"
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
            raise SherlockNoGrpcConnectionException()

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

    @require_version(222)
    def delete_all_mount_points(self, project: str, cca_name: str) -> int:
        """Delete all mount points for a CCA.

        Available Since: 2022R2

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
                raise SherlockNoGrpcConnectionException()

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

    @require_version(231)
    def delete_all_ict_fixtures(self, project: str, cca_name: str) -> int:
        """Delete all ICT fixtures for a CCA.

        Available Since: 2023R1

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
                raise SherlockNoGrpcConnectionException()

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

    @require_version(231)
    def delete_all_test_points(self, project: str, cca_name: str) -> int:
        """Delete all test points for a CCA.

        Available Since: 2023R1

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
                raise SherlockNoGrpcConnectionException()

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

    @require_version(231)
    def update_test_points_by_file(
        self,
        project: str,
        cca_name: str,
        file_path: str,
    ) -> int:
        """Update test point properties of a CCA from a CSV file.

        Available Since: 2023R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        file_path: str
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
            "TestPointsImport.csv"
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
                raise SherlockNoGrpcConnectionException()

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

    @require_version(231)
    def update_test_fixtures_by_file(
        self,
        project: str,
        cca_name: str,
        file_path: str,
    ) -> int:
        """Update test fixture properties of a CCA from a CSV file.

        Available Since: 2023R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        file_path: str
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
            "TestFixturesImport.csv"
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
                raise SherlockNoGrpcConnectionException()

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

    @require_version(231)
    def export_all_test_points(
        self,
        project: str,
        cca_name: str,
        export_file: str,
        length_units: str = "DEFAULT",
        displacement_units: str = "DEFAULT",
        force_units: str = "DEFAULT",
    ) -> int:
        """Export the test point properties for a CCA.

        Available Since: 2023R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        export_file: str
            Full path for the CSV file to export the test points list to.
        length_units: str, optional
            Length units to use when exporting the test points.
            The default is ``DEFAULT``.
        displacement_units: str, optional
            Displacement units to use when exporting the test points.
            The default is ``DEFAULT``.
        force_units: str, optional
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
            "DEFAULT"
        )
        """
        try:
            if project == "":
                raise SherlockExportAllTestPointsError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockExportAllTestPointsError(message="CCA name is invalid.")
            if export_file == "":
                raise SherlockExportAllTestPointsError(message="File path is required.")

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockLayerService_pb2.ExportAllTestPointsRequest(
                project=project,
                ccaName=cca_name,
                filePath=export_file,
                lengthUnits=length_units,
                displacementUnits=displacement_units,
                forceUnits=force_units,
            )

            response = self.stub.exportAllTestPoints(request)

            if response.value == -1:
                raise SherlockExportAllTestPointsError(message=response.message)

        except SherlockExportAllTestPointsError as e:
            LOG.error(str(e))
            raise e

        return response.value

    @require_version(231)
    def export_all_test_fixtures(
        self,
        project: str,
        cca_name: str,
        export_file: str,
        units: str = "DEFAULT",
    ) -> int:
        """Export the test fixture properties for a CCA.

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        export_file: str
            Full path for the CSV file to export the text fixtures list to.
        units: str, optional
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
            "DEFAULT"
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
                raise SherlockNoGrpcConnectionException()

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

    @require_version(222)
    def export_all_mount_points(
        self,
        project: str,
        cca_name: str,
        export_file: str,
        units: str = "DEFAULT",
    ) -> int:
        """Export the mount point properties for a CCA.

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        export_file: str
            Full path for the CSV file to export the mount points list to.
        units: str, optional
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
            "DEFAULT"
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
                raise SherlockNoGrpcConnectionException()

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

    @require_version(251)
    def add_modeling_region(
        self,
        project: str,
        modeling_regions: list[
            dict[str, bool | float | str | dict[str, bool | float | str] | dict[str, float | str]]
        ],
    ) -> int:
        """
        Add one or more modeling regions to a specific project.

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        modeling_regions: list[dict[str, bool | float | str | dict[str, bool | float | str]\
                | dict[str, float | str]]]
            Modeling regions to add. Each dictionary should contain:

            - cca_name: str
                Name of the CCA.
            - region_id: str
                Unique region ID of the modeling region.
            - region_units: str
                Units of the modeling region.
            - model_mode: str
                Mode that specifies how the region is used. Valid values are ``Enabled``,
                ``Disabled`` and ``Excluded``.
            - shape: PolygonalShape|RectangularShape|SlotShape|CircularShape|PCBShape
                The shape of the modeling region.
            - pcb_model_props: dict[str, bool | float | str]
                PCB model parameters consisting of these properties:

                    - export_model_type: str
                        The type of model to be generated for a given modeling region.
                        Valid values are ``Default``, ``Sherlock``, ``Sweep`` and ``None``.
                    - elem_order: str
                        The type of 3D elements to be created for the PCB in the modeling region.
                        Valid values are ``First_Order``, ``Second_Order`` and ``Solid_Shell``.
                    - max_mesh_size: float
                        The maximum size of the mesh to be used in the region.
                    - max_mesh_size_units: str
                        Units for the maximum mesh size.
                    - quads_preferred: bool
                        Whether to generate quad-shaped elements when creating the mesh if true.
            - trace_model_props: dict[str, float | str]
                Trace model parameters consisting of these properties:

                    - trace_model_type : str
                        The specification of whether trace modeling should be performed
                        within the region. Valid values are ``Default``, ``Enabled`` and
                        ``Disabled``.
                    - elem_order: str, optional
                        The type of 3D elements to be created for the PCB in the modeling region.
                        Valid values are ``First_Order``, ``Second_Order`` and ``Solid_Shell``.
                    - trace_mesh_size : float, optional
                        The maximum mesh size to be used in the region when trace modeling
                        is enabled.
                    - trace_mesh_size_units: str, optional
                        Units for the maximum mesh size when trace modeling is enabled.


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
        >>> modeling_regions = [
            {
                "cca_name": "Card",
                "region_id": "Region001",
                "region_units": "mm",
                "model_mode": "Enabled",
                "shape": PolygonalShape(points=[
                    (0, 0),
                    (0, 6.35),
                    (9.77, 0)
                ], rotation=87.8),
                "pcb_model_props": {
                    "export_model_type": "Sherlock",
                    "elem_order": "First_Order",
                    "max_mesh_size": 0.5,
                    "max_mesh_size_units": "mm",
                    "quads_preferred": True
                },
                "trace_model_props": {
                    "trace_model_type": "Enabled",
                    "elem_order": "Second_Order",
                    "trace_mesh_size": 0.3,
                    "trace_mesh_size_units": "mm"
                }
            }
        ]
        >>> result = sherlock.layer.add_modeling_region("Tutorial Project", modeling_regions)
        """
        try:
            if not project:
                raise SherlockAddModelingRegionError(message="Project name is invalid.")

            if not modeling_regions:
                raise SherlockAddModelingRegionError(message="Modeling regions list is empty.")

            for region in modeling_regions:
                if "cca_name" not in region or not region["cca_name"]:
                    raise SherlockAddModelingRegionError(message="CCA name is invalid.")
                if "region_id" not in region or not region["region_id"]:
                    raise SherlockAddModelingRegionError(message="Region ID is invalid.")
                if "region_units" not in region or not region["region_units"]:
                    raise SherlockAddModelingRegionError(message="Region units are invalid.")
                if "shape" not in region:
                    raise SherlockAddModelingRegionError(message="Shape is missing.")
                elif not isinstance(
                    region["shape"],
                    (
                        PolygonalShape,
                        RectangularShape,
                        SlotShape,
                        CircularShape,
                        PCBShape,
                    ),
                ):
                    raise SherlockAddModelingRegionError(message="Shape is not of a valid type.")

                pcb_model_props = region.get("pcb_model_props", {})
                if pcb_model_props:
                    if (
                        "export_model_type" not in pcb_model_props
                        or pcb_model_props["export_model_type"] == ""
                    ):
                        raise SherlockAddModelingRegionError(
                            message="PCB model export type is invalid."
                        )
                    if "elem_order" not in pcb_model_props or pcb_model_props["elem_order"] == "":
                        raise SherlockAddModelingRegionError(
                            message="PCB element order is invalid."
                        )
                    if "max_mesh_size" not in pcb_model_props or not isinstance(
                        pcb_model_props["max_mesh_size"], float
                    ):
                        raise SherlockAddModelingRegionError(
                            message="PCB max mesh size is invalid."
                        )
                    if "quads_preferred" not in pcb_model_props or not isinstance(
                        pcb_model_props["quads_preferred"], bool
                    ):
                        raise SherlockAddModelingRegionError(
                            message="PCB quads preferred is invalid."
                        )

                trace_model_props = region.get("trace_model_props", {})
                if trace_model_props:
                    if (
                        "trace_model_type" not in trace_model_props
                        or trace_model_props["trace_model_type"] == ""
                    ):
                        raise SherlockAddModelingRegionError(message="Trace model type is invalid.")

                if not self._is_connection_up():
                    raise SherlockNoGrpcConnectionException()

                add_modeling_region_request = SherlockLayerService_pb2.AddModelingRegionRequest()
                add_modeling_region_request.project = project

                for region_request in modeling_regions:
                    modeling_region = add_modeling_region_request.modelingRegions.add()
                    modeling_region.ccaName = region_request["cca_name"]
                    modeling_region.regionId = region_request["region_id"]
                    modeling_region.regionUnits = region_request["region_units"]
                    modeling_region.modelMode = ModelingRegion.ModelingMode.Value(
                        region_request["model_mode"]
                    )

                    shape = region_request["shape"]
                    if isinstance(shape, PolygonalShape):
                        polygonal_shape = modeling_region.polygonalShape
                        for point in shape.points:
                            polygonal_point = polygonal_shape.points.add()
                            polygonal_point.x = point[0]
                            polygonal_point.y = point[1]
                        polygonal_shape.rotation = shape.rotation
                    elif isinstance(shape, RectangularShape):
                        rectangular_shape = modeling_region.rectangularShape
                        rectangular_shape.length = shape.length
                        rectangular_shape.width = shape.width
                        rectangular_shape.centerX = shape.center_x
                        rectangular_shape.centerY = shape.center_y
                        rectangular_shape.rotation = shape.rotation
                    elif isinstance(shape, SlotShape):
                        slot_shape = modeling_region.slotShape
                        slot_shape.length = shape.length
                        slot_shape.width = shape.width
                        slot_shape.nodeCount = shape.node_count
                        slot_shape.centerX = shape.center_x
                        slot_shape.centerY = shape.center_y
                        slot_shape.rotation = shape.rotation
                    elif isinstance(shape, CircularShape):
                        circular_shape = modeling_region.circularShape
                        circular_shape.diameter = shape.diameter
                        circular_shape.nodeCount = shape.node_count
                        circular_shape.centerX = shape.center_x
                        circular_shape.centerY = shape.center_y
                        circular_shape.rotation = shape.rotation
                    else:
                        raise SherlockAddModelingRegionError(
                            message="Shape is not of a valid type."
                        )

                    export_model_type = ModelingRegion.PCBModelingProperties.ExportModelType
                    pcb_model_props = region_request.get("pcb_model_props", {})
                    modeling_region.pcbModelProps.exportModelType = getattr(
                        export_model_type,
                        pcb_model_props["export_model_type"],
                    )
                    modeling_region.pcbModelProps.elemOrder = getattr(
                        ModelingRegion.ElementOrder,
                        pcb_model_props["elem_order"],
                    )
                    modeling_region.pcbModelProps.maxMeshSize = pcb_model_props["max_mesh_size"]
                    modeling_region.pcbModelProps.maxMeshSizeUnits = pcb_model_props[
                        "max_mesh_size_units"
                    ]
                    modeling_region.pcbModelProps.quadsPreferred = pcb_model_props[
                        "quads_preferred"
                    ]

                    trace_modeling_type = ModelingRegion.TraceModelingProperties.TraceModelingType
                    trace_model_props = region_request.get("trace_model_props", {})
                    modeling_region.traceModelProps.traceModelType = getattr(
                        trace_modeling_type,
                        trace_model_props["trace_model_type"],
                    )
                    if "elem_order" in trace_model_props:
                        modeling_region.traceModelProps.elemOrder = getattr(
                            ModelingRegion.ElementOrder,
                            trace_model_props["elem_order"],
                        )
                    if "trace_mesh_size" in trace_model_props:
                        modeling_region.traceModelProps.traceMeshSize = trace_model_props[
                            "trace_mesh_size"
                        ]
                    if "trace_mesh_size_units" in trace_model_props:
                        modeling_region.traceModelProps.traceMeshSizeUnits = trace_model_props[
                            "trace_mesh_size_units"
                        ]

                return_code = self.stub.addModelingRegion(add_modeling_region_request)
                if return_code.value != 0:
                    raise SherlockAddModelingRegionError(message=return_code.message)

                return return_code.value

        except SherlockAddModelingRegionError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    @require_version(251)
    def update_modeling_region(
        self,
        project: str,
        modeling_regions: list[
            dict[
                str,
                bool | float | str | dict[str, bool | float | str] | dict[str, bool | float | str],
            ]
        ],
    ) -> int:
        """
        Update one or more modeling regions in a specific project.

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        modeling_regions : list[dict]
            Modeling regions to update. Each dictionary should contain:

            - cca_name: str
                Name of the CCA.
            - region_id: str
                Unique region ID of the modeling region.
            - region_units: str
                Units of the modeling region.
            - model_mode: str
                Mode that specifies how the region is used. Valid values are ``Enabled``,
                ``Disabled`` and ``Excluded``.
            - shape: PolygonalShape|RectangularShape|SlotShape|CircularShape|PCBShape
                The shape of the modeling region.
            - pcb_model_props: dict[str, bool | float | str]
                PCB model parameters consisting of these properties:

                    - export_model_type: str
                        The type of model to be generated for a given modeling region.
                        Valid values are ``Default``, ``Sherlock``, ``Sweep`` and ``None``.
                    - elem_order: str
                        The type of 3D elements to be created for the PCB in the modeling region.
                        Valid values are ``First_Order``, ``Second_Order`` and ``Solid_Shell``.
                    - max_mesh_size: float
                        The maximum size of the mesh to be used in the region.
                    - max_mesh_size_units: str
                        Units for the maximum mesh size.
                    - quads_preferred: bool
                        Whether to generate quad-shaped elements when creating the mesh if true.
            - trace_model_props: dict[str, float | str]
                Trace model parameters consisting of these properties:

                    - trace_model_type: str
                        The specification of whether trace modeling should be performed
                        within the region. Valid values are ``Default``, ``Enabled`` and
                        ``Disabled``.
                    - elem_order: str, optional
                        The type of 3D elements to be created for the PCB in the modeling region.
                        Valid values are ``First_Order``, ``Second_Order`` and ``Solid_Shell``.
                    - trace_mesh_size: float, optional
                        The maximum mesh size to be used in the region when trace modeling
                        is enabled.
                    - trace_mesh_size_units: str, optional
                        Units for the maximum mesh size when trace modeling is enabled.
            - region_id_replacement: str, optional
                Represents a unique region id that will replace the existing regionId value during
                a modeling region update if a value exists.

        Returns
        -------
        int
            Status code of the response. 0 for success.

         Example
        -------
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
        >>> modeling_regions = [
        >>>     {
        >>>         "cca_name": "Card",
        >>>         "region_id": "Region001",
        >>>         "region_units": "mm",
        >>>         "model_mode": "Enabled",
        >>>         "shape": PolygonalShape(points=[(0, 0), (1, 1)], rotation=0),
        >>>         "pcb_model_props": {
        >>>             "export_model_type": "Sherlock",
        >>>             "elem_order": "Second_Order",
        >>>             "max_mesh_size": 0.5,
        >>>             "max_mesh_size_units": "mm",
        >>>             "quads_preferred": True,
        >>>         },
        >>>         "trace_model_props": {
        >>>             "trace_model_type": "Enabled",
        >>>             "elem_order": "Second_Order",
        >>>             "trace_mesh_size": 0.1,
        >>>             "trace_mesh_size_units": "mm",
        >>>         },
        >>>         "region_id_replacement": "NewRegion001",
        >>>     }
        >>> ]
        >>> result = sherlock.layer.update_modeling_region("Tutorial Project", modeling_regions)
        """
        try:
            if not project:
                raise SherlockUpdateModelingRegionError(message="Project name is invalid.")

            if not modeling_regions:
                raise SherlockUpdateModelingRegionError(message="Modeling regions list is empty.")

            for region in modeling_regions:
                if "cca_name" not in region:
                    raise SherlockUpdateModelingRegionError(message="CCA name is invalid.")
                if "region_id" not in region:
                    raise SherlockUpdateModelingRegionError(message="Region ID is invalid.")
                if "region_units" not in region:
                    raise SherlockUpdateModelingRegionError(message="Region units are invalid.")
                if "shape" not in region:
                    raise SherlockUpdateModelingRegionError(message="Shape is missing.")
                elif not isinstance(
                    region["shape"],
                    (
                        PolygonalShape,
                        RectangularShape,
                        SlotShape,
                        CircularShape,
                        PCBShape,
                    ),
                ):
                    raise SherlockUpdateModelingRegionError(message="Shape is not of a valid type.")

                pcb_model_props = region.get("pcb_model_props", {})
                if pcb_model_props:
                    if (
                        "export_model_type" not in pcb_model_props
                        or pcb_model_props["export_model_type"] == ""
                    ):
                        raise SherlockUpdateModelingRegionError(
                            message="PCB model export type is invalid."
                        )
                    if "elem_order" not in pcb_model_props or pcb_model_props["elem_order"] == "":
                        raise SherlockUpdateModelingRegionError(
                            message="PCB element order is invalid."
                        )
                    if "max_mesh_size" not in pcb_model_props or not isinstance(
                        pcb_model_props["max_mesh_size"], float
                    ):
                        raise SherlockUpdateModelingRegionError(
                            message="PCB max mesh size is invalid."
                        )
                    if "quads_preferred" not in pcb_model_props or not isinstance(
                        pcb_model_props["quads_preferred"], bool
                    ):
                        raise SherlockUpdateModelingRegionError(
                            message="PCB quads preferred is invalid."
                        )

                trace_model_props = region.get("trace_model_props", {})
                if trace_model_props:
                    if (
                        "trace_model_type" not in trace_model_props
                        or trace_model_props["trace_model_type"] == ""
                    ):
                        raise SherlockUpdateModelingRegionError(
                            message="Trace model type is invalid."
                        )

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            update_modeling_region_request = SherlockLayerService_pb2.UpdateModelingRegionRequest()
            update_modeling_region_request.project = project

            for region_request in modeling_regions:
                modeling_region = update_modeling_region_request.modelingRegions.add()
                modeling_region.ccaName = region_request["cca_name"]
                modeling_region.regionId = region_request["region_id"]
                modeling_region.regionUnits = region_request["region_units"]
                modeling_region.modelMode = ModelingRegion.ModelingMode.Value(
                    region_request["model_mode"]
                )

                shape = region_request["shape"]
                if isinstance(shape, PolygonalShape):
                    polygonal_shape = modeling_region.polygonalShape
                    for point in shape.points:
                        polygonal_point = polygonal_shape.points.add()
                        polygonal_point.x = point[0]
                        polygonal_point.y = point[1]
                    polygonal_shape.rotation = shape.rotation
                elif isinstance(shape, RectangularShape):
                    rectangular_shape = modeling_region.rectangularShape
                    rectangular_shape.length = shape.length
                    rectangular_shape.width = shape.width
                    rectangular_shape.centerX = shape.center_x
                    rectangular_shape.centerY = shape.center_y
                    rectangular_shape.rotation = shape.rotation
                elif isinstance(shape, SlotShape):
                    slot_shape = modeling_region.slotShape
                    slot_shape.length = shape.length
                    slot_shape.width = shape.width
                    slot_shape.nodeCount = shape.node_count
                    slot_shape.centerX = shape.center_x
                    slot_shape.centerY = shape.center_y
                    slot_shape.rotation = shape.rotation
                elif isinstance(shape, CircularShape):
                    circular_shape = modeling_region.circularShape
                    circular_shape.diameter = shape.diameter
                    circular_shape.nodeCount = shape.node_count
                    circular_shape.centerX = shape.center_x
                    circular_shape.centerY = shape.center_y
                    circular_shape.rotation = shape.rotation

                export_model_type = ModelingRegion.PCBModelingProperties.ExportModelType
                pcb_model_props = region_request.get("pcb_model_props", {})
                modeling_region.pcbModelProps.exportModelType = getattr(
                    export_model_type,
                    pcb_model_props["export_model_type"],
                )
                modeling_region.pcbModelProps.elemOrder = getattr(
                    ModelingRegion.ElementOrder,
                    pcb_model_props["elem_order"],
                )
                modeling_region.pcbModelProps.maxMeshSize = pcb_model_props["max_mesh_size"]
                modeling_region.pcbModelProps.maxMeshSizeUnits = pcb_model_props[
                    "max_mesh_size_units"
                ]
                modeling_region.pcbModelProps.quadsPreferred = pcb_model_props["quads_preferred"]

                trace_modeling_type = ModelingRegion.TraceModelingProperties.TraceModelingType
                trace_model_props = region_request.get("trace_model_props", {})
                modeling_region.traceModelProps.traceModelType = getattr(
                    trace_modeling_type,
                    trace_model_props["trace_model_type"],
                )
                if "elem_order" in trace_model_props:
                    modeling_region.traceModelProps.elemOrder = getattr(
                        ModelingRegion.ElementOrder,
                        trace_model_props["elem_order"],
                    )
                if "trace_mesh_size" in trace_model_props:
                    modeling_region.traceModelProps.traceMeshSize = trace_model_props[
                        "trace_mesh_size"
                    ]
                if "trace_mesh_size_units" in trace_model_props:
                    modeling_region.traceModelProps.traceMeshSizeUnits = trace_model_props[
                        "trace_mesh_size_units"
                    ]

                if "region_id_replacement" in region_request:
                    modeling_region.regionIdReplacement = region_request["region_id_replacement"]

            return_code = self.stub.updateModelingRegion(update_modeling_region_request)
            if return_code.value != 0:
                raise SherlockUpdateModelingRegionError(message=return_code.message)

            return return_code.value

        except SherlockUpdateModelingRegionError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    @require_version(251)
    def copy_modeling_region(
        self,
        project: str,
        copy_regions: list[dict[str, float | str]],
    ) -> int:
        """
        Copy one or more modeling regions in a specific project.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        copy_regions : list[dict[str, float | str]]
            Modeling regions to copy along with their corresponding "copy to" parameters.
            Each dictionary should contain:

            - cca_name : str
                Name of the CCA.
            - region_id : str
                Region ID of the existing modeling region to copy.
            - region_id_copy : str
                Region ID of the modeling region copy. Must be unique.
            - center_x : float
                The center x coordinate of the modeling region copy. Used for location placement in
                the Layer Viewer.
            - center_y : float
                The center y coordinate of the modeling region copy. Used for location placement in
                the Layer Viewer.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Example
        -------
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
        >>> modeling_regions = [
        >>>     {
        >>>         "cca_name": "Card",
        >>>         "region_id": "Region001",
        >>>         "region_id_copy": "RegionCopy001",
        >>>         "center_x": 10.0,
        >>>         "center_y": 20.0,
        >>>     }
        >>> ]
        >>> result = sherlock.layer.copy_modeling_region("Tutorial Project", modeling_regions)
        """
        try:
            if not project:
                raise SherlockCopyModelingRegionError(message="Project name is invalid.")

            if not copy_regions:
                raise SherlockCopyModelingRegionError(message="Copy regions list is empty.")

            for region in copy_regions:
                if "cca_name" not in region or region["cca_name"] == "":
                    raise SherlockCopyModelingRegionError(message="CCA name is invalid.")
                if "region_id" not in region or region["region_id"] == "":
                    raise SherlockCopyModelingRegionError(message="Region ID is invalid.")
                if "region_id_copy" not in region or region["region_id_copy"] == "":
                    raise SherlockCopyModelingRegionError(message="Region ID copy is invalid.")
                if "center_x" not in region or not isinstance(region["center_x"], float):
                    raise SherlockCopyModelingRegionError(message="Center X coordinate is invalid.")
                if "center_y" not in region or not isinstance(region["center_y"], float):
                    raise SherlockCopyModelingRegionError(message="Center Y coordinate is invalid.")

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            copy_regions_request = []

            for region in copy_regions:
                copy_region = (
                    SherlockLayerService_pb2.CopyModelingRegionRequest.CopyModelingRegionInfo(
                        ccaName=region["cca_name"],
                        regionId=region["region_id"],
                        regionIdCopy=region["region_id_copy"],
                        centerX=region["center_x"],
                        centerY=region["center_y"],
                    )
                )
                copy_regions_request.append(copy_region)

            request = SherlockLayerService_pb2.CopyModelingRegionRequest(
                project=project,
                copyRegions=copy_regions_request,
            )

            response = self.stub.copyModelingRegion(request)

            if response.value == -1:
                raise SherlockCopyModelingRegionError(message=response.message)

            return response.value

        except SherlockCopyModelingRegionError as e:
            for error in e.str_itr():
                LOG.error(error)
            raise e

    @require_version(251)
    def delete_modeling_region(self, project: str, delete_regions: list[dict[str, str]]) -> int:
        """Delete one or more modeling regions for a specific project.

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        delete_regions: list[dict[str, str]]
            Modeling regions to delete. Each dictionary should contain:
            - "cca_name": str, Name of the CCA.
            - "region_id": str, Unique region ID of the modeling region to delete.

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
        >>> modeling_regions = [{"cca_name": "Card", "region_id": "12345"}]
        >>> sherlock.layer.delete_modeling_region("Test", modeling_regions)
        """
        try:
            if project == "":
                raise SherlockDeleteModelingRegionError(message="Project name is invalid.")
            if not isinstance(delete_regions, list):
                raise SherlockDeleteModelingRegionError(message="Delete regions should be a list.")
            if not delete_regions:
                raise SherlockDeleteModelingRegionError(message="Delete regions list is empty.")

            for region in delete_regions:
                if not isinstance(region, dict):
                    raise SherlockDeleteModelingRegionError(
                        message="Each region should be a dictionary."
                    )
                if "cca_name" not in region or region["cca_name"] == "":
                    raise SherlockDeleteModelingRegionError(message="CCA name is invalid.")
                if "region_id" not in region or region["region_id"] == "":
                    raise SherlockDeleteModelingRegionError(message="Region ID is invalid.")

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            delete_regions_info = [
                SherlockLayerService_pb2.DeleteModelingRegionRequest.DeleteModelingRegionInfo(
                    ccaName=region["cca_name"], regionId=region["region_id"]
                )
                for region in delete_regions
            ]

            request = SherlockLayerService_pb2.DeleteModelingRegionRequest(
                project=project, deleteRegions=delete_regions_info
            )

            response = self.stub.deleteModelingRegion(request)

            if response.value == -1:
                raise SherlockDeleteModelingRegionError(message=response.message)

        except SherlockDeleteModelingRegionError as e:
            LOG.error(str(e))
            raise e

        return response.value
