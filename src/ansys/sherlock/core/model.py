# © 2023 ANSYS, Inc. All rights reserved

"""Module containing all model generation capabilities."""
import os.path

try:
    import SherlockModelService_pb2
    import SherlockModelService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockModelService_pb2
    from ansys.api.sherlock.v0 import SherlockModelService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockModelServiceError
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
        export_request.traceDrillHoleParam.drillHoleModeling = trace_drill_hole_modeling
        export_request.traceDrillHoleParam.minHoleDiameter.value = trace_drill_hole_min_diameter_val
        export_request.traceDrillHoleParam.minHoleDiameter.unit = trace_drill_hole_min_diameter_unit
        export_request.traceDrillHoleParam.maxEdgeLength.value = trace_drill_hole_max_edge_val
        export_request.traceDrillHoleParam.maxEdgeLength.unit = trace_drill_hole_max_edge_unit

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
