"""Module for stackup service on client-side."""

import SherlockStackupService_pb2
import SherlockStackupService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockGenStackupError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Stackup(GrpcStub):
    """Contains the methods from the Sherlock Stackup Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockStackupService."""
        self.channel = channel
        self.stub = SherlockStackupService_pb2_grpc.SherlockStackupServiceStub(channel)

    #     /**
    #  * Represents the properties of a new stackup to be generated.
    #  */
    # message GenStackupRequest {
    #   string project					= 1;	//
    #   string ccaName					= 2;	// The CCA name.
    #   double boardThickness				= 3;	// Board thickness.
    #   string boardThicknessUnit 		= 4;	// Board thickness unit.
    #   string pcbMaterialManufacturer	= 5;	// PCB material manufacturer.
    #   string pcbMaterialGrade			= 6;	// PCB material grade.
    #   string pcbMaterial				= 7;	// PCB material.
    #   int32 conductorLayersCnt			= 8;	// Number of conductor layers.
    #   double signalLayerThickness		= 9;	// Signal layer thickness.
    #   string signalLayerThicknessUnit	= 10;	// Signal layer thickness unit.
    #   double minLaminateThickness		= 11;	// Minimum laminate layer thickness.
    #   string minLaminateThicknessUnit	= 12;	// Minimum laminate layer thickness unit.
    #   bool maintainSymmetry				= 13;	// If set to true, maintain symmetry.
    # }

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
        Examples
        --------
        TODO: Write example
        """
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
