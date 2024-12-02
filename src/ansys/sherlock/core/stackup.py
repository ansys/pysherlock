# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

"""Module containing all stackup management capabilities."""
from typing import Optional

from grpc import Channel

try:
    import SherlockStackupService_pb2
    import SherlockStackupService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockStackupService_pb2
    from ansys.api.sherlock.v0 import SherlockStackupService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockGenStackupError,
    SherlockGetLayerCountError,
    SherlockGetStackupPropsError,
    SherlockGetTotalConductorThicknessError,
    SherlockInvalidConductorPercentError,
    SherlockInvalidGlassConstructionError,
    SherlockInvalidLayerIDError,
    SherlockInvalidMaterialError,
    SherlockInvalidThicknessArgumentError,
    SherlockListConductorLayersError,
    SherlockListLaminateLayersError,
    SherlockNoGrpcConnectionException,
    SherlockUpdateConductorLayerError,
    SherlockUpdateLaminateLayerError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub
from ansys.sherlock.core.types.stackup_types import StackupProperties
from ansys.sherlock.core.utils.version_check import require_version


class Stackup(GrpcStub):
    """Contains all stackup management capabilities."""

    def __init__(self, channel: Channel, server_version: int):
        """Initialize a gRPC stub for Sherlock Stackup service."""
        super().__init__(channel, server_version)
        self.stub = SherlockStackupService_pb2_grpc.SherlockStackupServiceStub(channel)
        self.LAMINATE_THICKNESS_UNIT_LIST = None
        self.LAMINATE_MATERIAL_MANUFACTURER_LIST = None
        self.CONDUCTOR_MATERIAL_LIST = None
        self.LAYER_TYPE_LIST = ["SIGNAL", "POWER", "SUBSTRATE"]
        self.CONSTRUCTION_STYLE_LIST = None
        self.FIBER_MATERIAL_LIST = None

    def _init_laminate_thickness_units(self):
        """Initialize the list of units for the laminate thickness.

        Available Since: 2021R1
        """
        if self._is_connection_up():
            laminate_thickness_unit_request = (
                SherlockStackupService_pb2.ListLaminateThicknessUnitsRequest()
            )
            laminate_thickness_unit_response = self.stub.listLaminateThicknessUnits(
                laminate_thickness_unit_request
            )
            if laminate_thickness_unit_response.returnCode.value == 0:
                self.LAMINATE_THICKNESS_UNIT_LIST = laminate_thickness_unit_response.unit

    def _init_laminate_material_manufacturers(self):
        """Initialize list of laminate material manufacturers.

        Available Since: 2021R1
        """
        if self._is_connection_up():
            laminate_material_manufacturer_request = (
                SherlockStackupService_pb2.ListLaminateMaterialsManufacturersRequest()
            )
            laminate_material_manufacturer_response = self.stub.listLaminateMaterialsManufacturers(
                laminate_material_manufacturer_request
            )
            if laminate_material_manufacturer_response.returnCode.value == 0:
                self.LAMINATE_MATERIAL_MANUFACTURER_LIST = (
                    laminate_material_manufacturer_response.manufacturer
                )

    def _init_conductor_materials(self):
        """Initialize list of conductor materials.

        Available Since: 2021R1
        """
        if self._is_connection_up():
            conductor_materials_request = SherlockStackupService_pb2.ListConductorMaterialsRequest()
            conductor_materials_response = self.stub.listConductorMaterials(
                conductor_materials_request
            )
            if conductor_materials_response.returnCode.value == 0:
                self.CONDUCTOR_MATERIAL_LIST = conductor_materials_response.conductorMaterial

    def _init_construction_styles(self):
        """Initialize list of construction styles.

        Available Since: 2021R1
        """
        if self._is_connection_up():
            construction_style_request = SherlockStackupService_pb2.ListConstructionStylesRequest()
            construction_style_response = self.stub.listConstructionStyles(
                construction_style_request
            )
            if construction_style_response.returnCode.value == 0:
                self.CONSTRUCTION_STYLE_LIST = construction_style_response.constructionStyle

    def _init_fiber_materials(self):
        """Initialize list of fiber materials.

        Available Since: 2021R1
        """
        if self._is_connection_up():
            fiber_material_request = SherlockStackupService_pb2.ListFiberMaterialsRequest()
            fiber_material_response = self.stub.listFiberMaterials(fiber_material_request)
            if fiber_material_response.returnCode.value == 0:
                self.FIBER_MATERIAL_LIST = fiber_material_response.fiberMaterial

    def _check_pcb_material_validity(self, manufacturer: str, grade: str, material: str):
        """Check PCB arguments to see if they are valid.

        Available Since: 2021R1
        """
        if (self.LAMINATE_MATERIAL_MANUFACTURER_LIST is not None) and (
            manufacturer not in self.LAMINATE_MATERIAL_MANUFACTURER_LIST
        ):
            raise SherlockInvalidMaterialError(message="Laminate manufacturer is invalid.")
        if self._is_connection_up():
            request = SherlockStackupService_pb2.ListLaminateMaterialsRequest(
                manufacturer=manufacturer
            )
            response = self.stub.listLaminateMaterials(request)
            if response.returnCode.value == 0:
                manufacturer_materials = response.manufacturerMaterials[0]
                assert manufacturer_materials.manufacturer == manufacturer

                for grade_material in manufacturer_materials.gradeMaterials:
                    if grade == grade_material.grade:
                        if material in grade_material.laminateMaterial:
                            return

                        raise SherlockInvalidMaterialError("Laminate material is invalid.")
                else:
                    raise SherlockInvalidMaterialError("Laminate grade is invalid.")

    @staticmethod
    def _check_glass_construction_validity(glass_construction: list[tuple[str, float, float, str]]):
        """Check input to see if it is a valid glass construction argument."""
        if not isinstance(glass_construction, list):
            raise SherlockInvalidGlassConstructionError(
                message="glass_construction argument is invalid."
            )

        i = 0
        try:
            for i, layer in enumerate(glass_construction):
                if len(layer) != 4:
                    raise SherlockInvalidGlassConstructionError(
                        message=f"Invalid layer {i}: Number of elements is wrong."
                    )
        except SherlockInvalidThicknessArgumentError as e:
            raise SherlockInvalidGlassConstructionError(message=f"Invalid layer {i}: {str(e)}")

    @staticmethod
    def _add_glass_construction_layers(
        request: SherlockStackupService_pb2.UpdateLaminateRequest,
        layers: list[tuple[str, float, float, str]],
    ):
        """Add the layers to the request."""
        for l in layers:
            layer = request.glassConstruction.add()
            layer.style = l[0]
            layer.resinPercentage = l[1]
            layer.thickness = l[2]
            layer.thicknessUnit = l[3]

    @require_version()
    def gen_stackup(
        self,
        project: str,
        cca_name: str,
        board_thickness: float,
        board_thickness_unit: str,
        pcb_material_manufacturer: str,
        pcb_material_grade: str,
        pcb_material: str,
        conductor_layers_cnt: int,
        signal_layer_thickness: float,
        signal_layer_thickness_unit: str,
        min_laminate_thickness: float,
        min_laminate_thickness_unit: str,
        maintain_symmetry: bool,
        power_layer_thickness: float,
        power_layer_thickness_unit: str,
    ) -> int:
        """Generate a new stackup from given properties.

        Available Since: 2021R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        board_thickness: float
            Board thickness.
        board_thickness_unit: str
            Units for the board thickness.
        pcb_material_manufacturer: str
            Manufacturer for the PCB material.
        pcb_material_grade: str
            Grade for the PCB material.
        pcb_material: str
            Material for the PCB.
        conductor_layers_cnt: int32
            Number of conductor layers.
        signal_layer_thickness: float
            Signal layer thickness.
        signal_layer_thickness_unit: str
            Units for the signal layer thickness.
        min_laminate_thickness: float
            Minimum thickness of laminate layers.
        min_laminate_thickness_unit: str
            Units for the minimum thickness of laminate layers.
        maintain_symmetry: bool
            Whether to maintain symmetry.
        power_layer_thickness: float
            Power layer thickness.
        power_layer_thickness_unit: str
            Units for the power layer thickness.

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
        >>> sherlock.stackup.gen_stackup(
            "Test",
            "Card",
            82.6,
            "mil",
            "Generic",
            "FR-4",
            "Generic FR-4",
            6,
            0.5,
            "oz",
            1.0,
            "mil",
            False,
            1.0,
            "mil"
        )
        """
        if self.LAMINATE_THICKNESS_UNIT_LIST is None:
            self._init_laminate_thickness_units()
        if self.LAMINATE_MATERIAL_MANUFACTURER_LIST is None:
            self._init_laminate_material_manufacturers()

        try:
            if project == "":
                raise SherlockGenStackupError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockGenStackupError(message="CCA name is invalid.")
            self._check_pcb_material_validity(
                pcb_material_manufacturer, pcb_material_grade, pcb_material
            )
            if conductor_layers_cnt <= 1:
                raise SherlockGenStackupError(
                    message="Number of conductor layers must be greater than 1."
                )
            if signal_layer_thickness < 0:
                raise SherlockGenStackupError(message="Conductor thickness is invalid.")
        except SherlockGenStackupError as e:
            LOG.error(str(e))
            raise e
        except (SherlockInvalidMaterialError, SherlockInvalidThicknessArgumentError) as e:
            LOG.error(f"Generate stackup error: {str(e)}")
            raise SherlockGenStackupError(message=str(e))

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockStackupService_pb2.GenStackupRequest(
            project=project,
            ccaName=cca_name,
            boardThickness=board_thickness,
            boardThicknessUnit=board_thickness_unit,
            pcbMaterialManufacturer=pcb_material_manufacturer,
            pcbMaterialGrade=pcb_material_grade,
            pcbMaterial=pcb_material,
            conductorLayersCnt=conductor_layers_cnt,
            signalLayerThickness=signal_layer_thickness,
            signalLayerThicknessUnit=signal_layer_thickness_unit,
            minLaminateThickness=min_laminate_thickness,
            minLaminateThicknessUnit=min_laminate_thickness_unit,
            maintainSymmetry=maintain_symmetry,
            powerLayerThickness=power_layer_thickness,
            powerLayerThicknessUnit=power_layer_thickness_unit,
        )

        response = self.stub.genStackup(request)

        try:
            if response.value == -1:
                raise SherlockGenStackupError(response.message)

            LOG.info(response.message)
            return response.value
        except SherlockGenStackupError as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def update_conductor_layer(
        self,
        project: str,
        cca_name: str,
        layer: str,
        layer_type: str = "",
        material: str = "",
        thickness: float = 0,
        thickness_unit: str = "",
        conductor_percent: str = "",
        resin_material: str = "",
    ) -> int:
        """Update a conductor layer with given properties.

        Available Since: 2021R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        layer: str
            Layer ID associated with the conductor layer.
        layer_type: str, optional
            Layer type. The default is ``""``. For example,
            ``"SIGNAL"``, ``"POWER"``, or ``"SUBSTRATE"``.
        material: str, optional
            Conductor material. The default is ``""``.
        thickness: float, optional
            Conductor layer thickness. The default is ``0``.
        thickness_unit: str, optional
            Units for the conductor layer thickness. The
            default is ``""``.
        conductor_percent: str, optional
            Conductor percentage. The default is ``""``.
        resin_material: str, optional
            Resin material. The default is ``""``.

        Note
        ----
        Using the default value for a property causes no changes for that property.

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
            project="Test",
            cca_name="Card",
        )
        >>> sherlock.stackup.update_conductor_layer(
            "Test",
            "Card",
            "3",
            "POWER",
            "COPPER",
            1.0,
            "oz",
            "94.2",
            "Generic FR-4 Generic FR-4"
        )
        """
        if self.LAMINATE_THICKNESS_UNIT_LIST is None:
            self._init_laminate_thickness_units()
        if self.CONDUCTOR_MATERIAL_LIST is None:
            self._init_conductor_materials()

        try:
            if project == "":
                raise SherlockUpdateConductorLayerError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdateConductorLayerError(message="CCA name is invalid.")
            if (layer_type != "") and layer_type not in self.LAYER_TYPE_LIST:
                raise SherlockUpdateConductorLayerError(
                    message=(
                        "Conductor type is invalid. "
                        'Options are "SIGNAL", "POWER", and "SUBSTRATE".'
                    )
                )
            if material != "":
                if (self.CONDUCTOR_MATERIAL_LIST is not None) and (
                    material not in self.CONDUCTOR_MATERIAL_LIST
                ):
                    raise SherlockUpdateConductorLayerError(
                        message="Conductor material is invalid."
                    )
        except SherlockUpdateConductorLayerError as e:
            LOG.error(str(e))
            raise e
        except (
            SherlockInvalidLayerIDError,
            SherlockInvalidConductorPercentError,
            SherlockInvalidThicknessArgumentError,
        ) as e:
            LOG.error(f"Update conductor layer error: {str(e)}")
            raise SherlockUpdateConductorLayerError(message=str(e))

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockStackupService_pb2.UpdateConductorLayerRequest(
            project=project,
            ccaName=cca_name,
            layer=layer,
            type=layer_type,
            material=material,
            thickness=thickness,
            thicknessUnit=thickness_unit,
            conductorPercent=conductor_percent,
            resinMaterial=resin_material,
        )

        response = self.stub.updateConductorLayer(request)

        try:
            if response.value == -1:
                raise SherlockUpdateConductorLayerError(response.message)

            LOG.info(response.message)
            return response.value
        except SherlockUpdateConductorLayerError as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def update_laminate_layer(
        self,
        project,
        cca_name,
        layer,
        manufacturer: str = "",
        grade: str = "",
        material: str = "",
        thickness: float = 0,
        thickness_unit: str = "",
        construction_style: str = "",
        glass_construction: Optional[list[tuple[str, float, float, str]]] = None,
        fiber_material: str = "",
        conductor_material: str = "",
        conductor_percent: str = "",
    ) -> int:
        """Update a laminate layer with given properties.

        Available Since: 2021R1

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        layer : str
            Layer ID associated with the conductor layer.
        manufacturer : str, optional
            Manufacturer of the material for the laminate layer.
            The default is ``""``. To update the material, the
            ``manufacturer``, ``grade``, and ``material`` parameters
            must be specified. When the ``manufacturer`` is specified,
            there are checks to ensure that the corresponding parameters
            are provided.
        grade : str, optional
            Material grade. The default is ``""``.
        material : str, optional
            Material name. The default is ``""``.
        thickness : float, optional
            Laminate thickness. The default is ``0``.
        thickness_unit : str, optional
            Units for the laminate thickness. The default is ``""``.
        construction_style : str, optional
            Construction style. The default is ``""``.
        glass_construction : list[tuple[str, float, float, str]], optional
            List representing a glass construction. This list consists
            of objects with these properties:

           - style : str
               Style of the glass construction.
           - resinPercentage : float
               Resin percentage.
           - thickness: float
               Thickness.
           - thicknessUnit: str
               Units for the thickness.

        fiber_material : str, optional
            Fiber material. The default is ``""``. This parameter is only
            updated for a glass construction.
        conductor_material : str, optional
            Conductor material. The default is ``""``.
        conductor_percent : str, optional
            Conductor percentage. The default is ``""``.

        Note
        ----
        Using the default value for a property causes no changes for that property.

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
            project="Test",
            cca_name="Card",
        )
        >>> sherlock.stackup.update_laminate_layer(
            "Test",
            "Card",
            "2",
            "Generic",
            "FR-4",
            "Generic FR-4",
            0.015,
            "in",
            "106",
            [
                ("106", 68.0, 0.015, "in")
            ],
            "E-GLASS",
            "COPPER",
            "0.0"
        )
        """
        if self.LAMINATE_THICKNESS_UNIT_LIST is None:
            self._init_laminate_thickness_units()
        if self.LAMINATE_MATERIAL_MANUFACTURER_LIST is None:
            self._init_laminate_material_manufacturers()
        if self.CONSTRUCTION_STYLE_LIST is None:
            self._init_construction_styles()
        if self.FIBER_MATERIAL_LIST is None:
            self._init_fiber_materials()
        if self.CONDUCTOR_MATERIAL_LIST is None:
            self._init_conductor_materials()
        if glass_construction is None:
            glass_construction = []

        try:
            if project == "":
                raise SherlockUpdateLaminateLayerError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdateLaminateLayerError(message="CCA name is invalid.")
            if manufacturer != "":
                self._check_pcb_material_validity(manufacturer, grade, material)
            if construction_style != "":
                if (self.CONSTRUCTION_STYLE_LIST is not None) and (
                    construction_style not in self.CONSTRUCTION_STYLE_LIST
                ):
                    raise SherlockUpdateLaminateLayerError(message="Construction style is invalid.")
                self._check_glass_construction_validity(glass_construction)
            if fiber_material != "":
                if (self.FIBER_MATERIAL_LIST is not None) and (
                    fiber_material not in self.FIBER_MATERIAL_LIST
                ):
                    raise SherlockUpdateLaminateLayerError(message="Fiber material is invalid.")
            if conductor_material != "":
                if (self.CONDUCTOR_MATERIAL_LIST is not None) and (
                    conductor_material not in self.CONDUCTOR_MATERIAL_LIST
                ):
                    raise SherlockUpdateLaminateLayerError(message="Conductor material is invalid.")
        except SherlockUpdateLaminateLayerError as e:
            LOG.error(str(e))
            raise e
        except (
            SherlockInvalidLayerIDError,
            SherlockInvalidMaterialError,
            SherlockInvalidConductorPercentError,
            SherlockInvalidThicknessArgumentError,
            SherlockInvalidGlassConstructionError,
        ) as e:
            LOG.error(f"Update laminate layer error: %s", {str(e)})
            raise SherlockUpdateLaminateLayerError(message=str(e))

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockStackupService_pb2.UpdateLaminateRequest(
            project=project,
            ccaName=cca_name,
            layer=layer,
            manufacturer=manufacturer,
            grade=grade,
            material=material,
            thickness=thickness,
            thicknessUnit=thickness_unit,
            constructionStyle=construction_style,
            fiberMaterial=fiber_material,
            conductorMaterial=conductor_material,
            conductorPercent=conductor_percent,
        )

        self._add_glass_construction_layers(request, glass_construction)

        response = self.stub.updateLaminate(request)

        try:
            if response.value == -1:
                raise SherlockUpdateLaminateLayerError(response.message)

            LOG.info(response.message)
            return response.value
        except SherlockUpdateLaminateLayerError as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def list_conductor_layers(
        self, project: str
    ) -> list[SherlockStackupService_pb2.ListConductorLayersResponse.CCAConductorLayerProp]:
        """List CCA conductor layers.

        Available Since: 2021R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.

        Returns
        -------
        list[SherlockStackupService_pb2.ListConductorLayersResponse.CCAConductorLayerProp]
            The conductor layers of all CCAs in the project.

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
            project="Test",
            cca_name="Card",
        )
        >>> conductorLayers = sherlock.stackup.list_conductor_layers(project="Tutorial")
        >>> for layer in conductorLayers:
        >>>     properties = layer.conductorLayerProps
        >>>     for prop in properties:
        >>>     print(f"{prop}")
        """
        if self.LAMINATE_THICKNESS_UNIT_LIST is None:
            self._init_laminate_thickness_units()
        if self.CONDUCTOR_MATERIAL_LIST is None:
            self._init_conductor_materials()

        if project == "":
            raise SherlockListConductorLayersError(message="Project name is invalid.")

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        try:

            request = SherlockStackupService_pb2.ListConductorLayersRequest(project=project)
            response = self.stub.listConductorLayers(request)
            if response.returnCode.value == -1:
                raise SherlockListConductorLayersError(response.returnCode.message)

            return response.ccaConductorLayerProps

        except SherlockListConductorLayersError as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def list_laminate_layers(
        self, project: str
    ) -> list[SherlockStackupService_pb2.ListLaminatesResponse.CCALaminateProp]:
        """List all laminate layers and their properties.

        Available Since: 2021R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.

        Returns
        -------
        list[SherlockStackupService_pb2.ListLaminatesResponse.CCALaminateProp]
            The laminate layers of all CCAs in the project.

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
            project="Test",
            cca_name="Card",
        )
        >>> laminateLayers = sherlock.stackup.list_laminate_layers(project="Tutorial")
        >>> for layer in laminateLayers:
        >>>     properties = layer.laminateProps
        >>>     for prop in properties:
        >>>     print(f"{prop}")
        """
        if self.LAMINATE_THICKNESS_UNIT_LIST is None:
            self._init_laminate_thickness_units()
        if self.LAMINATE_MATERIAL_MANUFACTURER_LIST is None:
            self._init_laminate_material_manufacturers()
        if self.CONSTRUCTION_STYLE_LIST is None:
            self._init_construction_styles()
        if self.FIBER_MATERIAL_LIST is None:
            self._init_fiber_materials()
        if self.CONDUCTOR_MATERIAL_LIST is None:
            self._init_conductor_materials()

        if project == "":
            raise SherlockListLaminateLayersError(message="Project name is invalid.")
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        try:
            request = SherlockStackupService_pb2.ListLaminatesRequest(project=project)
            response = self.stub.listLaminates(request)
            if response.returnCode.value == -1:
                raise SherlockListLaminateLayersError(response.returnCode.message)

            return response.ccaLaminateProps

        except SherlockListLaminateLayersError as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def get_layer_count(self, project: str, cca_name: str) -> int:
        """Get the number of CCA layers in a stackup.

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
            The number of layers of the CCA in the project.

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
            project="Test",
            cca_name="Card",
        )
        >>> conductor_layer_count = sherlock.stackup.get_layer_count(
        >>>    project="Test",
        >>>    cca_name="Card")
        >>> print(f"{conductor_layer_count}")
        """
        if project == "":
            raise SherlockGetLayerCountError(message="Project name is invalid.")
        if cca_name == "":
            raise SherlockGetLayerCountError(message="CCA name is invalid.")
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockStackupService_pb2.GetLayerCountRequest(project=project, ccaName=cca_name)
        response = self.stub.getLayerCount(request)
        try:
            if response.returnCode.value == -1:
                raise SherlockGetLayerCountError(response.returnCode.message)

            return response.count
        except SherlockGetLayerCountError as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def get_stackup_props(self, project: str, cca_name: str) -> StackupProperties:
        """Get the stackup properties from a CCA.

        Available Since: 2021R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.

        Returns
        -------
        StackupProperties
            Object containing the properties of the stackup.

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
            project="Test",
            cca_name="Card",
        )
        >>> stackup_props = sherlock.stackup.get_stackup_props(
               project="Tutorial",
               cca_name="Main Board"
            )
        >>> print(f"{stackup_props}")
        """
        if project == "":
            raise SherlockGetStackupPropsError(message="Project name is invalid.")
        if cca_name == "":
            raise SherlockGetStackupPropsError(message="CCA name is invalid.")
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockStackupService_pb2.GetStackupPropsRequest(
            project=project, ccaName=cca_name
        )
        response = self.stub.getStackupProps(request)
        try:
            if response.returnCode.value == -1:
                raise SherlockGetLayerCountError(response.returnCode.message)

            return StackupProperties(response)
        except SherlockGetStackupPropsError as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def get_total_conductor_thickness(
        self, project: str, cca_name: str, thickness_unit: str
    ) -> float:
        """Return the total conductor thickness.

        Available Since: 2021R2

        Parameters
        ----------
        project: str
            Sherlock project name.
        cca_name: str
            The CCA name.
        thickness_unit: str, optional
            Units for laminate thickness.

        Returns
        -------
        float
            The conductor thickness of the CCA in the specified units.

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
            project="Test",
            cca_name="Card",
        )
        >>> total_thickness = sherlock.stackup.get_total_conductor_thickness(project="Tutorial",
                                                                 cca_name="Main Board",
                                                                 thickness_unit="oz")
        >>>print(f"{total_thickness}")
        """
        if project == "":
            raise SherlockGetTotalConductorThicknessError(message="Invalid project name")
        if cca_name == "":
            raise SherlockGetTotalConductorThicknessError(message="Invalid CCA name")
        if thickness_unit == "":
            raise SherlockGetTotalConductorThicknessError(message="Invalid thickness unit")
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockStackupService_pb2.GetTotalConductorThicknessRequest(
            project=project, ccaName=cca_name, thicknessUnit=thickness_unit
        )
        response = self.stub.getTotalConductorThickness(request)

        try:
            if response.returnCode.value == -1:
                raise SherlockGetTotalConductorThicknessError(response.returnCode.message)

            return response.totalThickness
        except SherlockGetTotalConductorThicknessError as e:
            LOG.error(str(e))
            raise e
