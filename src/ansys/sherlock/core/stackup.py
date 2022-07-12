"""Module for stackup service on client-side."""

import SherlockStackupService_pb2
import SherlockStackupService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockGenStackupError, SherlockUpdateConductorLayerError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Stackup(GrpcStub):
    """Contains the methods from the Sherlock Stackup Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockStackupService."""
        self.channel = channel
        self.stub = SherlockStackupService_pb2_grpc.SherlockStackupServiceStub(channel)
        self.LAMINATE_THICKNESS_UNIT_LIST = None
        self.LAMINATE_MATERIAL_MANUFACTURER_LIST = None
        self.CONDUCTOR_MATERIAL_LIST = None
        self.LAYER_TYPE_LIST = ["SIGNAL", "POWER", "SUBSTRATE"]

    def _init_laminate_thickness_units(self):
        """Initialize LAMINATE_THICKNESS_UNIT_LIST."""
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
        """Initialize LAMINATE_MATERIAL_MANUFACTURER_LIST."""
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
        """Initialize CONDUCTOR_MATERIAL_LIST."""
        if self._is_connection_up():
            conductor_materials_request = SherlockStackupService_pb2.ListConductorMaterialsRequest()
            conductor_materials_response = self.stub.listConductorMaterials(
                conductor_materials_request
            )
            if conductor_materials_response.returnCode.value == 0:
                self.CONDUCTOR_MATERIAL_LIST = conductor_materials_response.conductorMaterial

    def _check_pcb_material_validity(self, manufacturer, grade, material):
        """Check pcb arguments if they are valid."""
        if (self.LAMINATE_MATERIAL_MANUFACTURER_LIST is not None) and (
            manufacturer not in self.LAMINATE_MATERIAL_MANUFACTURER_LIST
        ):
            raise SherlockGenStackupError(
                message="Invalid laminate manufacturer, grade, or material provided"
            )
        elif self._is_connection_up():
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
                        else:
                            raise SherlockGenStackupError("Invalid laminate material provided")
                else:
                    raise SherlockGenStackupError("Invalid laminate grade provided")

    def _check_layer_id(self, layerid):
        """Check layer argument if it is valid."""
        if layerid == "":
            raise SherlockUpdateConductorLayerError(message="Missing conductor layer ID")
        else:
            try:
                id = int(layerid)
                if id < 0:
                    raise SherlockUpdateConductorLayerError(
                        message="Invalid layer ID provided, it must be an integer greater than 0"
                    )
            except ValueError:
                raise SherlockUpdateConductorLayerError(
                    message="Invalid layer ID, layer ID must be numeric"
                )

    def _check_conductor_percent(self, input):
        """Check input string if it is a valid conductor percent."""
        if input == "":
            return
        else:
            try:
                percent = float(input)
                if percent < 0 or percent > 100:
                    raise SherlockUpdateConductorLayerError(
                        message="Invalid conductor percent provided. It must be between 0 and 100"
                    )
            except ValueError:
                raise SherlockUpdateConductorLayerError(
                    message="Invalid percent, percent must be numeric"
                )

    def gen_stackup(
        self,
        project,
        cca_name,
        board_thickness,
        board_thickness_unit,
        pcb_material_manufacturer,
        pcb_material_grade,
        pcb_material,
        conductor_layers_cnt,
        signal_layer_thickness,
        signal_layer_thickness_unit,
        min_laminate_thickness,
        min_laminate_thickness_unit,
        maintain_symmetry,
        power_layer_thickness,
        power_layer_thickness_unit,
    ):
        """Generate a new stackup from the properties.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        cca_name : str, required
            The CCA name.
        board_thickness : double, required
            Board thickness.
        board_thickness_unit : str, required
            Board thickness unit.
        pcb_material_manufacturer : str, required
            PCB material manufacturer.
        pcb_material_grade : str, required
            PCB material grade.
        pcb_material : str, required
            PCB material.
        conductor_layers_cnt : int32, required
            Number of conductor layers.
        signal_layer_thickness : double, required
            Signal layer thickness.
        signal_layer_thickness_unit : str, required
            Signal layer thickness unit.
        min_laminate_thickness : double, required
            Minimum laminate layer thickness.
        min_laminate_thickness_unit : str, required
            Minimum laminate layer thickness unit.
        maintain_symmetry : bool, required
            If set to true, maintain symmetry.
        power_layer_thickness : double, required
            Power layer thickness.
        power_layer_thickness_unit : str, required
            Power layer thickness unit.
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
            "mil",
        )
        """
        if self.LAMINATE_THICKNESS_UNIT_LIST is None:
            self._init_laminate_thickness_units()
        if self.LAMINATE_MATERIAL_MANUFACTURER_LIST is None:
            self._init_laminate_material_manufacturers()

        try:
            if project == "":
                raise SherlockGenStackupError(message="Invalid project name")
            elif cca_name == "":
                raise SherlockGenStackupError(message="Invalid cca name")
            elif board_thickness < 0:
                raise SherlockGenStackupError(message="Invalid board thickness provided")
            elif board_thickness > 0:
                if (
                    self.LAMINATE_THICKNESS_UNIT_LIST is not None
                ) and board_thickness_unit not in self.LAMINATE_THICKNESS_UNIT_LIST:
                    raise SherlockGenStackupError(message="Invalid board thickness unit provided")
            if (self.LAMINATE_MATERIAL_MANUFACTURER_LIST is not None) and (
                pcb_material_manufacturer not in self.LAMINATE_MATERIAL_MANUFACTURER_LIST
            ):
                raise SherlockGenStackupError(message="Invalid laminate manufacturer provided")
            self._check_pcb_material_validity(
                pcb_material_manufacturer, pcb_material_grade, pcb_material
            )
            if conductor_layers_cnt <= 1:
                raise SherlockGenStackupError(
                    message="The number of conductor layers must be greater than 1"
                )
            elif signal_layer_thickness < 0:
                raise SherlockGenStackupError(message="Invalid conductor thickness provided")
            elif signal_layer_thickness > 0:
                if (
                    (signal_layer_thickness_unit != "oz")
                    and (self.LAMINATE_THICKNESS_UNIT_LIST is not None)
                    and (signal_layer_thickness_unit not in self.LAMINATE_THICKNESS_UNIT_LIST)
                ):
                    raise SherlockGenStackupError(
                        message="Invalid conductor thickness unit provided"
                    )
            if min_laminate_thickness < 0:
                raise SherlockGenStackupError(message="Invalid laminate thickness provided")
            elif min_laminate_thickness > 0:
                if (self.LAMINATE_THICKNESS_UNIT_LIST is not None) and (
                    min_laminate_thickness_unit not in self.LAMINATE_THICKNESS_UNIT_LIST
                ):
                    raise SherlockGenStackupError(
                        message="Invalid laminate thickness unit provided"
                    )
            if power_layer_thickness < 0:
                raise SherlockGenStackupError(message="Invalid power thickness provided")
            elif power_layer_thickness > 0:
                if (
                    (power_layer_thickness_unit != "oz")
                    and (self.LAMINATE_THICKNESS_UNIT_LIST is not None)
                    and (power_layer_thickness_unit not in self.LAMINATE_THICKNESS_UNIT_LIST)
                ):
                    raise SherlockGenStackupError(message="Invalid power thickness unit provided")
        except SherlockGenStackupError as e:
            LOG.error(str(e))
            raise e

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
            else:
                LOG.info(response.message)
                return
        except SherlockGenStackupError as e:
            LOG.error(str(e))
            raise e

    def update_conductor_layer(
        self,
        project,
        cca_name,
        layer,
        type,
        material,
        thickness,
        thickness_unit,
        conductor_percent,
        resin_material,
    ):
        """Update a conductor layer with the given properties.

        Parameters
        ----------
        project : str, required
            Sherlock project name.
        cca_name : str, required
            The CCA name.
        layer : str, required
            The layer ID associated with this conductor layer.
        type : str, required
            Layer type (i.e. SIGNAL, POWER, SUBSTRATE).
        material : str, required
            Name of this conductor material.
        thickness : double, required
            Conductor layer thickness.
        thickness_unit : str, required
            Conductor layer thickness unit.
        conductor_percent : str, required
            Conductor percentage.
        resin_material : str, required
            Resin material.

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
            "Generic FR-4 Generic FR-4",
        )
        """
        if self.LAMINATE_THICKNESS_UNIT_LIST is None:
            self._init_laminate_thickness_units()
        if self.CONDUCTOR_MATERIAL_LIST is None:
            self._init_conductor_materials()

        try:
            if project == "":
                raise SherlockUpdateConductorLayerError(message="Invalid project name")
            if cca_name == "":
                raise SherlockUpdateConductorLayerError(message="Invalid cca name")
            self._check_layer_id(layer)
            if (type != "") and type not in self.LAYER_TYPE_LIST:
                raise SherlockUpdateConductorLayerError(
                    message=(
                        "Invalid conductor type provided. "
                        'Valid values are "SIGNAL", "POWER", or "SUBSTRATE".'
                    )
                )
            if material != "":
                if (self.CONDUCTOR_MATERIAL_LIST is not None) and (
                    material not in self.CONDUCTOR_MATERIAL_LIST
                ):
                    raise SherlockUpdateConductorLayerError(
                        message="Invalid conductor material provided"
                    )
            if thickness < 0:
                raise SherlockUpdateConductorLayerError(message="Invalid board thickness provided")
            if thickness > 0:
                if (
                    thickness_unit != "oz" and self.LAMINATE_THICKNESS_UNIT_LIST is not None
                ) and thickness_unit not in self.LAMINATE_THICKNESS_UNIT_LIST:
                    raise SherlockUpdateConductorLayerError(
                        message="Invalid thickness unit provided"
                    )
            self._check_conductor_percent(conductor_percent)
        except SherlockUpdateConductorLayerError as e:
            LOG.error(str(e))
            raise e

        request = SherlockStackupService_pb2.UpdateConductorLayerRequest(
            project=project,
            ccaName=cca_name,
            layer=layer,
            type=type,
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
            else:
                LOG.info(response.message)
                return
        except SherlockUpdateConductorLayerError as e:
            LOG.error(str(e))
            raise e
