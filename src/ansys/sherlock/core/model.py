# © 2023-2024 ANSYS, Inc. All rights reserved

"""Module containing all model generation capabilities."""
import os.path

try:
    import SherlockModelService_pb2
    import SherlockModelService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockModelService_pb2
    from ansys.api.sherlock.v0 import SherlockModelService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockExportAEDBError, SherlockModelServiceError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Model(GrpcStub):
    """Contains all model generation capabilities."""

    def __init__(self, channel):
        """Initialize a gRPC stub for the Sherlock Model service."""
        super().__init__(channel)
        self.stub = SherlockModelService_pb2_grpc.SherlockModelServiceStub(channel)

    def export_trace_reinforcement_model(
        self,
        project_name,
        cca_name,
        export_file,
        overwrite=True,
        display_model=False,
        generate_models_for_all_layers=False,
        coordinate_units="mm",
        trace_param_diameter_threshold_val=2,
        trace_param_diameter_threshold_unit="mm",
        trace_param_min_hole_diameter_val=0.25,
        trace_param_min_hole_diameter_unit="mm",
        trace_drill_hole_modeling="DISABLED",
        trace_drill_hole_min_diameter_val=2,
        trace_drill_hole_min_diameter_unit="mm",
        trace_drill_hole_max_edge_val=1,
        trace_drill_hole_max_edge_unit="mm",
    ):
        r"""Export a trace reinforcement model.

        Parameters
        ----------
        project_name : str
            Name of the Sherlock project to generate the trace reinforcement model for.
        cca_name : str
            Name of the CCA to generate the trace reinforcement model from.
        export_file : str
            Path for saving exported files to. The file extension must be ``".wbjn"``.
        overwrite : bool, optional
            Whether to overwrite an existing file having the same file name.
            The default is ``True``.
        display_model : bool, optional
            Whether to launch and display the exported model in Ansys Workbench
            Mechanical once the export finishes. The default is ``False``.
        generate_models_for_all_layers :  bool, optional
            Whether to generate and export trace models for not only the generated trace
            reinforcement layers but also all other layers. The default is ``False``, in
            which case only trace reinforcement layers are generated and exported.
        coordinate_units : str, optional
            Units of the model coordinates to use when exporting a model.
            The default is ``"mm"``.
        trace_param_diameter_threshold_val: float, optional
            Threshold value that determines whether a hole is modeled with shell
            reinforcement elements or beam elements. The default is ``2``, with the
            default units being ``"mm"`` as specified by the next parameter. Holes with
            diameters equal to or greater than this threshold value are modeled with shell
            reinforcement elements. Holes with diameters less than this threshold value
            are modeled with beam elements. Holes buried inside the board are always modeled
            with beam elements.
        trace_param_diameter_threshold_unit: str, optional
            Units associated with the threshold value for the trace parameter diameter.
            The default is ``"mm"``.
        trace_param_min_hole_diameter_val: float, optional
            Minimum trace parameter diameter for determining whether a via is exported.
            The default is ``0.25``, with the default units being ``"mm"`` as specified
            by the next parameter. Vias with diameters smaller than this diameter
            are not exported. Setting the value to ``0`` exports all vias.
        trace_param_min_hole_diameter_unit: str, optional
            Units associated with the value for the minimum trace parameter diameter.
            The default is ``"mm"``.
        trace_drill_hole_modeling: str, optional
            Whether to enable or disable the modeling of trace drill holes. Options are
            ``"ENABLED"`` and ``"DISABLED"``. The default is ``"DISABLED"``, in which
            case the ``trace_drill_hole_min_diameter`` and ``trace_drill_hole_max_edge``
            parameters are not used.
        trace_drill_hole_min_diameter_val: float, optional
            Minimimun diameter value for determining whether a trace drill hole is
            exported. The default is ``2``, with the default units being ``"mm"``
            as specified by the next parameter. Trace drill holes with diameters smaller
            than this diameter are not exported. Setting the value to ``0`` exports all
            trace drill holes.
        trace_drill_hole_min_diameter_unit: str, optional
            Units associated with the value for the minimum trace drill hole diameter.
            The default is ``"mm"``.
        trace_drill_hole_max_edge_val: float, optional
            Maximum segment size for representing round drill holes by a polygon.
            The default is ``1``, with the default units being ``"mm"`` as specified
            by the next parameter.
        trace_drill_hole_max_edge_unit: str, optional
            Units associated with the maximum segment for representing round drill holes
            by a polygon. The default is ``"mm"``.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core import launcher
        >>> from ansys.sherlock.core import model
        >>> sherlock = launcher.launch_sherlock()
        >>> sherlock.model.export_trace_reinforcement_model(
            'Tutorial Project', 'Main Board', 'c:\Temp\export.wbjn',
            True, False, False)

        >>> from ansys.sherlock.core import launcher
        >>> from ansys.sherlock.core import model
        >>> sherlock = launcher.launch_sherlock()
        >>> sherlock.model.export_trace_reinforcement_model(
            'Tutorial Project', 'Main Board', 'c:\Temp\export.wbjn',
            True, False, False, "mm", 1.5, "mm", 0, "mm", "ENABLED", 1.5, "mm", 1, "mm")
        """
        try:
            if not project_name:
                raise SherlockModelServiceError("Project name is invalid.")
            if not cca_name:
                raise SherlockModelServiceError("CCA name is invalid.")
            if export_file == "":
                raise SherlockModelServiceError(message="Export file path is invalid.")
            else:
                if not os.path.exists(os.path.dirname(export_file)):
                    raise SherlockModelServiceError(
                        message=f'Export file directory "{export_file}" does not exist.'
                    )
        except Exception as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        export_request = SherlockModelService_pb2.ExportTraceReinforcementModelRequest()
        export_request.project = project_name
        export_request.ccaName = cca_name
        export_request.exportFile = export_file
        export_request.overwrite = overwrite
        export_request.displayModel = display_model
        export_request.clearFEADatabase = (
            False  # This only applies to *.apdl files and is not applicable here.
        )
        export_request.coordinateUnits = coordinate_units
        export_request.generateModelsForAllLayers = generate_models_for_all_layers
        export_request.traceParam.diameterThreshold.value = trace_param_diameter_threshold_val
        export_request.traceParam.diameterThreshold.unit = trace_param_diameter_threshold_unit
        export_request.traceParam.minHoleDiameterForShellOrBeam.value = (
            trace_param_min_hole_diameter_val
        )
        export_request.traceParam.minHoleDiameterForShellOrBeam.unit = (
            trace_param_min_hole_diameter_unit
        )

        # export_request.traceDrillHoleParam is Deprecated
        export_request.traceDrillHoleParam.drillHoleModeling = trace_drill_hole_modeling
        export_request.traceDrillHoleParam.minHoleDiameter.value = trace_drill_hole_min_diameter_val
        export_request.traceDrillHoleParam.minHoleDiameter.unit = trace_drill_hole_min_diameter_unit
        export_request.traceDrillHoleParam.maxEdgeLength.value = trace_drill_hole_max_edge_val
        export_request.traceDrillHoleParam.maxEdgeLength.unit = trace_drill_hole_max_edge_unit
        # export_request.traceDrillHoleParam is Deprecated

        # New message to replace traceDrillHoleParam below.
        # Convert ENABLE/ENABLED or DISABLE/DISABLED to boolean
        export_request.drillHoleModeling.drillHoleModelingEnabled = (
            trace_drill_hole_modeling.upper().startswith("ENABLE")
        )
        export_request.drillHoleModeling.minHoleDiameter.value = trace_drill_hole_min_diameter_val
        export_request.drillHoleModeling.minHoleDiameter.units = trace_drill_hole_min_diameter_unit
        export_request.drillHoleModeling.maxEdgeLength.value = trace_drill_hole_max_edge_val
        export_request.drillHoleModeling.maxEdgeLength.units = trace_drill_hole_max_edge_unit

        try:
            return_code = self.stub.exportTraceReinforcementModel(export_request)
            if return_code.value != 0:
                raise SherlockModelServiceError(return_code.message)

            return return_code.value
        except Exception as e:
            LOG.error(str(e))
            raise

    def generate_trace_model(
        self,
        project_name,
        cca_name="",
        copper_layer_name="",
        max_arc_segment=0.0,
        max_arc_segment_units="mm",
        min_trace_area=0.0,
        min_trace_area_units="mm2",
        min_hole_area=0.0,
        min_hole_area_units="mm2",
        use_snapshot_for_non_image_layer=False,
    ):
        r"""Generate one or more trace models for a project.

        Parameters
        ----------
        project_name : str
            Name of the Sherlock project to generate one or more trace models for.
        cca_name : str, optional
            Name of the CCA to generate one or more trace models from. The default is
            ``""``, in which case trace models are generated for CCAs and
            all layers.
        copper_layer_name : str, optional
            Name of the copper layer to generate one or more trace models from. The default
            is ``""``, in which case trace models are generated either for the given CCA
            or for all layers.
        max_arc_segment : float, optional
            Maximum length of the segment to generate when Sherlock
            converts EDA arc drawing commands to line segments. The default is
            ``0.0``. Smaller values for the maximum arc segment result in smoother
            arc representations on the FEA model. However, the cost of generating a
            larger number of shorter segments is higher. Such short segments cause
            the FEA tool to generate a larger number of smaller elements to represent
            the curved solid.
        max_arc_segment_units : str, optional
            Units for the maximum arc segment. The default is ``"mm"``.
        min_trace_area : float, optional
            Minimum area of any trace polygon to include in the trace model.
            The default is ``0.0``, which turns off any area filtering.
        min_trace_area_units : str, optional
            Units for the minimum trace area. The default is ``"mm2"``.
        min_hole_area : float, optional
            Minimum area of any trace hole to include in the trace model.
            The default is ``0.0``, which turns off any hole filtering.
        min_hole_area_units : str, optional
            Units for the minimum hole area. The default is ``"mm2"``.
        use_snapshot_for_non_image_layer : bool, optional
            Whether to use an image to generate the trace model for layers that are not
            image layers. The default is ``False``. If ``True`` and a snapshot image for
            the layer exists, the snapshot image is used. Otherwise, an image is created
            in the same way as a snapshot image is created.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core import launcher
        >>> from ansys.sherlock.core import model
        >>> sherlock = launcher.launch_sherlock()
        >>> sherlock.model.generate_trace_model(
            'Tutorial Project', 'Main Board', 0.05, 'mm'
            0.0, 'mm2', 0.0, 'mm2')

        """
        try:
            if not project_name:
                raise SherlockModelServiceError("Project name is invalid.")
            if not cca_name:
                raise SherlockModelServiceError("CCA name is invalid.")
            if not copper_layer_name:
                raise SherlockModelServiceError("Copper layer name is required.")
            if max_arc_segment is None:
                raise SherlockModelServiceError("Maximum arc segment is required.")
            if not max_arc_segment_units:
                raise SherlockModelServiceError("Maximum arc segment units are required.")
            if min_trace_area is None:
                raise SherlockModelServiceError("Minimum trace area is required.")
            if not min_trace_area_units:
                raise SherlockModelServiceError("Minimum trace area units are required.")
            if min_hole_area is None:
                raise SherlockModelServiceError("Minimum hole area is required.")
            if not min_hole_area_units:
                raise SherlockModelServiceError("Minimum hole area units are required.")
        except Exception as e:
            LOG.error(str(e))
            raise

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            raise

        gen_request = SherlockModelService_pb2.GenerateTraceModelRequest()
        gen_request.project = project_name
        gen_request.ccaName = cca_name
        gen_request.copperLayerName = copper_layer_name
        gen_request.maxArcSegment = max_arc_segment
        gen_request.maxArcSegmentUnits = max_arc_segment_units
        gen_request.minTraceArea = min_trace_area
        gen_request.minTraceAreaUnits = min_trace_area_units
        gen_request.minHoleArea = min_hole_area
        gen_request.minHoleAreaUnits = min_hole_area_units
        gen_request.useSnapshotForNonImageLayer = use_snapshot_for_non_image_layer

        try:
            return_code = self.stub.generateTraceModel(gen_request)
            if return_code.value != 0:
                raise SherlockModelServiceError(return_code.message)

            return return_code.value
        except Exception as e:
            LOG.error(str(e))
            raise

    def export_aedb(
        self,
        project_name,
        cca_name,
        export_file,
        overwrite=True,
        display_model=False,
    ):
        r"""Export an Electronics Desktop model.

        Parameters
        ----------
        project_name : str
            Name of the Sherlock project to generate the EDB model for.
        cca_name : str
            Name of the CCA to generate the EDB model from.
        export_file : str
            Directory for saving exported model to.
        overwrite : bool, optional
            Whether to overwrite an existing file having the same file name.
            The default is ``True``.
        display_model : bool, optional
            Whether to launch and display the exported model in Ansys Electronics
            Desktop once the export finishes. The default is ``False``.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core import launcher
        >>> from ansys.sherlock.core import model
        >>> sherlock = launcher.launch_sherlock()
        >>> sherlock.model.export_aedb(
            'Tutorial Project', 'Main Board', 'c:\Temp\export.aedb',
            True, False)
        """
        try:
            if not project_name:
                raise SherlockExportAEDBError("Project name is invalid.")
            if not cca_name:
                raise SherlockExportAEDBError("CCA name is invalid.")
            if export_file == "":
                raise SherlockExportAEDBError(message="Export filepath is required.")
        except Exception as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        export_request = SherlockModelService_pb2.ExportAEDBRequest()
        export_request.project = project_name
        export_request.ccaName = cca_name
        export_request.exportFile = export_file
        export_request.overwrite = overwrite
        export_request.displayModel = display_model

        try:
            return_code = self.stub.exportAEDB(export_request)
            if return_code.value != 0:
                raise SherlockExportAEDBError(return_code.message)

            return return_code.value
        except Exception as e:
            LOG.error(str(e))
            raise

    def exportTraceModel(self, layer_params: list) -> int:
        r"""Export a trace model to a specified output file.

        Parameters
        ----------
        layer_params : list
            list of parameters for export a trace model of a single copper layer

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core import launcher
        >>> from ansys.sherlock.core import model
        >>> sherlock = launcher.launch_sherlock()
        >>> list_of_params_for_layers = []
        >>> list_of_params_for_layers.add(
                sherlock.model.createExportTraceCopperLayerParams(
                    "Tutorial Project",
                    "Main Board",
                    "outputfile.stp",
                    "copper-01.odb",
                    False,
                    False,
                    False,
        use_FEA_model_ID: bool = False,
        coord_units: str = "mm",
        # Mesh Type Params
        mesh_type: MeshType = MeshType.NONE,
        is_modeling_region_enabled: bool = False,
        # Trace Params
        trace_output_type: TraceOutputType = TraceOutputType.ALL_REGIONS,
        element_order: ElementOrder = ElementOrder.LINEAR,
        max_mesh_size: float = 1.0,
        max_holes_per_trace: int = 1,
        is_drill_hole_modeling_enabled: bool = False,
        drill_hole_min_diameter: float = 1.0,
        drill_hole_min_diameter_units = "mm",
        drill_hole_max_edge_length: float = 1.0,
        drill_hole_max_edge_length_units: str = "mm",
                )
            )
        >>> sherlock.model.exportTraceModel(list_of_params_for_layers)
        """
        try:
            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                raise

            request = SherlockModelService_pb2.ExportTraceModelRequest()
            for layer_param in layer_params:
                request.traceModelExportParams.add(layer_param)

            returnCode = self.stub.exportTraceModel(request)
            if return_code.value != 0:
                # Return error from the server
                raise SherlockModelServiceError(return_code.message)

            return returnCode.value
        except Exception as e:
            LOG.error(str(e))
            raise

    def createExportTraceCopperLayerParams(
        self,
        project_name: str,
        cca_name: str,
        output_file_path: str,
        copper_layer: str,
        overwrite: bool = False,
        display_after: bool = False,
        clear_FEA_database: bool = False,
        use_FEA_model_ID: bool = False,
        coord_units: str = "mm",
        # Mesh Type Params
        mesh_type: MeshType = MeshType.NONE,
        is_modeling_region_enabled: bool = False,
        # Trace Params
        trace_output_type: TraceOutputType = TraceOutputType.ALL_REGIONS,
        element_order: ElementOrder = ElementOrder.LINEAR,
        max_mesh_size: float = 1.0,
        max_holes_per_trace: int = 1,
        is_drill_hole_modeling_enabled: bool = False,
        drill_hole_min_diameter: float = 1.0,
        drill_hole_min_diameter_units: str = "mm",
        drill_hole_max_edge_length: float = 1.0,
        drill_hole_max_edge_length_units: str = "mm",
    ) -> SherlockModelService_pb2.TraceModelExportParams:
        r"""Create a set of parameters to be used to export a single copper layer.

        Parameters
        ----------
        project_name: str
        cca_name: str
        output_file_path: str
        copper_layer: str
        overwrite: bool = False
        display_after: bool = False
        clear_FEA_database: bool = False
        use_FEA_model_ID: bool = False
        coord_units: str = "mm"
        # Mesh Type Params
        mesh_type: MeshType = MeshType.NONE
        is_modeling_region_enabled: bool = False
        # Trace Params
        trace_output_type: TraceOutputType = TraceOutputType.ALL_REGIONS
        element_order: ElementOrder = ElementOrder.LINEAR
        max_mesh_size: float = 1.0
        max_holes_per_trace: int = 1
        is_drill_hole_modeling_enabled: bool = False
        drill_hole_min_diameter: float = 1.0
        drill_hole_min_diameter_units = "mm"
        drill_hole_max_edge_length: float = 1.0
        drill_hole_max_edge_length_units: str = "mm"
        """
        try:
            if not project_name:
                raise SherlockModelServiceError("Project name is invalid.")
            if not cca_name:
                raise SherlockModelServiceError("CCA name is invalid.")
            if not output_file_path:
                raise SherlockModelServiceError("Output File path is required")
            if not copper_layer:
                raise SherlockModelServiceError("Copper layer name is required.")
        except Exception as e:
            LOG.error(str(e))
            raise

        ret = SherlockModelService_pb2.TraceModelExportParams()

        ret.project = project_name
        ret.ccaName = cca_name
        ret.filePath = output_file_path
        ret.copperLayerName = copper_layer
        ret.overwriteExistingFile = overwrite
        ret.displayModelAfterExport = display_after
        ret.clearFEADatabase = clear_FEA_database
        ret.useFEAModelID = use_FEA_model_ID
        ret.coordUnits = coord_units

        # Mesh Type Params
        pmp = SherlockModelService_pb2.TraceModelExportParams.PcbMeshPropParam()
        pmp.meshType = mesh_type
        pmp.isModelingRegionEnabled = is_modeling_region_enabled
        ret.pcbMeshPropParam = pmp

        # Trace Params
        tpp = SherlockModelService_pb2.TraceModelExportParams.TracePropParam()
        tpp.traceOutputs = trace_output_type
        tpp.elementOrder = element_order
        tpp.maxMeshSize = max_mesh_size
        tpp.maxHolesPerTrace = max_holes_per_trace
        ret.tracePropParam = tpp

        # Drill Hole Params
        dhm = SherlockModelService_pb2.DrillHoleModeling()
        dhm.drillHoleModelingEnabled = is_drill_hole_modeling_enabled
        dhm.minHoleDiameter.value = drill_hole_min_diameter
        dhm.minHoleDiameter.units = drill_hole_min_diameter_units
        dhm.maxEdgeLength.value = drill_hole_max_edge_length
        dhm.maxEdgeLength.units = drill_hole_max_edge_length_units
        ret.drillHoleModeling = dhm
        return ret
