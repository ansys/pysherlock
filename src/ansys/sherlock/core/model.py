# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

"""Module containing different model generation capabilities."""
import os.path
import platform

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
    """Module containing different model generation capabilities."""

    def __init__(self, channel):
        """Initialize a gRPC stub for the Sherlock Model Service."""
        self.channel = channel
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
            trace_drill_hole_max_edge_unit="mm"
    ):
        r"""Export a trace reinforcement model.

        Parameters
        ----------
        project_name : str, required
            The Sherlock project name from which the trace reinforcement model will be generated.

        cca_name : str, required
            The Sherlock CCA name from which the trace reinforcement model will be generated.

        export_file : str, required
            The file path where the files from the trace reinforcement model export will be saved.
            The suffix must be ".wbjn".

        overwrite : bool, optional
            If set to True, overwrite an existing file that has the same file name.
            By default, this is set to True.

        display_model : bool, optional
            At the end of the export, launches and displays the exported model in
            Workbench Mechanical.
            By default, this is set to False.

        generate_models_for_all_layers :  bool, optional
            By default, Sherlock exports only those layers for which you have generated trace
            reinforcement layers. When this is set to True, Sherlock will generate trace models
            for all the other layers and include them in the exported model.
            By default, this is set to False.

        coordinate_units : str, optional
            The units of the model coordinates to use when exporting a model.
            By default, this is set to "mm".

        trace_param_diameter_threshold_val: float, optional
            This value determines whether a hole is modeled with beams or shell
            reinforcement elements. Holes equal to or greater than the Diameter Threshold
            value are modeled with shell reinforcement elements. Smaller holes are modeled
            with beam elements. (A hole buried inside the board is always modeled as a beam.)
            By default, this is set to "2mm".

        trace_param_diameter_threshold_unit: str, optional
            The units associated with the trace_param_diameter_threshold_val.
            By default, this is set to "mm".

        trace_param_min_hole_diameter_val: float, optional
            Vias smaller than the specified diameter will not be exported.
            A value of zero will export all vias.
            By default, this is set to "0.25mm".

        trace_param_min_hole_diameter_unit: str, optional
            The units associated with trace_param_min_hole_diameter_val.
            By default, this is set to "mm".

        trace_drill_hole_modeling: str, optional
            Set to ENABLED to model drill holes in the export.
            By default, this is set to "DISABLED". When this is "DISABLED",
            the parameters trace_drill_hole_min_diameter and trace_drill_hole_max_edge
            will not be used.

        trace_drill_hole_min_diameter_val: float, optional
            Drill holes smaller than the specified diameter will not be exported.
            A value of zero will export all drill holes.
            By default, this is set to "2mm".

        trace_drill_hole_min_diameter_unit: str, optional
            The units associated with trace_drill_hole_min_diameter_val.
            By default, this is set to "mm".

        trace_drill_hole_max_edge_val: float, optional
            This value specifies the maximum segment size used when representing
            round drill holes by a polygon.
            By default, this is set to "1mm".

        trace_drill_hole_max_edge_unit: str, optional
            The units associated with trace_drill_hole_max_edge_val.
            By default, this is set to "mm".

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
                raise SherlockModelServiceError("Project name is required")
            if not cca_name:
                raise SherlockModelServiceError("CCA name is required")
            if export_file == "":
                raise SherlockModelServiceError(message="Export file path required")
            if len(export_file) <= 1 or export_file[1] != ":":
                if platform.system() == "Windows":
                    export_file = f"{os.getcwd()}\\{export_file}"
                else:
                    export_file = f"{os.getcwd()}/{export_file}"
            else:  # For locally rooted path
                if not os.path.exists(os.path.dirname(export_file)):
                    raise SherlockModelServiceError(
                        message=(
                            f"Export file directory ({os.path.dirname(export_file)})"
                            " does not exist"
                        )
                    )
        except Exception as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
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

            return return_code.value, return_code.message
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
            use_snapshot_for_non_image_layer=False
    ):
        r"""Generate one or more trace models for a given project.

        Parameters
        ----------
        project_name : str, required
            The Sherlock project name from which the trace model will be generated.

        cca_name : str, optional
            The Sherlock CCA name from which the trace model will be generated.
            If this is empty, trace models will be generated for CCAs and all layers.

        copper_layer_name : str, optional
            The copper layer from which the trace model will be generated.
            If this is empty, trace models will be generated for all layers for the
            given CCA.

        max_arc_segment : float, required
            Specifies the maximum length of a segment to be generated when Sherlock
            converts EDA arc drawing commands to line segments. Smaller values for
            Max Arc Segment result in smoother arc representations on the FEA model,
            at the cost of generating a larger number of shorter segments. Such short
            segments will then cause the FEA tool to generate a larger number of
            smaller elements to represent the curved solid.

        max_arc_segment_units : str, required
            Units for max_arc_segment

        min_trace_area : float, required
            Specifies the minimum area of any trace polygon to be included in the
            trace model.  Setting this value to zero disables any area filtering.

        min_trace_area_units : str, required
            Units for min_trace_area

        min_hole_area : float, required
            Specifies the minimum hole area of any trace hole to be included in the
            trace model.  Setting this value to zero disables any hole filtering.

        min_hole_area_units : str, required
            Units for min_hole_area

        use_snapshot_for_non_image_layer : bool, optional
            Specifies whether to use an image to generate the trace model for layers that are not
            image layers. If a snapshot image exists for the layer, that snapshot is used.
            Otherwise this creates an image that is identical to creating a snapshot.
            By default, this is set to False.

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
                raise SherlockModelServiceError("Project name is required")
            if not max_arc_segment:
                raise SherlockModelServiceError("Max Arc Segment is required")
            if not max_arc_segment_units:
                raise SherlockModelServiceError("Max Arc Segment Units is required")
            if not min_trace_area:
                raise SherlockModelServiceError("Min Trace Area is required")
            if not min_trace_area_units:
                raise SherlockModelServiceError("Min Trace Area Units is required")
            if not min_hole_area:
                raise SherlockModelServiceError("Min Hole Area is required")
            if not min_hole_area_units:
                raise SherlockModelServiceError("Min Hole Area Units is required")
        except Exception as e:
            LOG.error(str(e))
            raise

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
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

            return return_code.value, return_code.message
        except Exception as e:
            LOG.error(str(e))
            raise


# def set_trace_parameter(
#     trace_param=None,
#     trace_param_diameter_threshold_val=2,
#     trace_param_diameter_threshold_unit="mm",
#     trace_param_min_hole_diameter_val=0.25,
#     trace_param_min_hole_diameter_unit="mm",
# ):
#     """Set the Trace Properties for the Export Trace Reinforcement Model operation."""
#     if trace_param is None:
#         trace_param = SherlockModelService_pb2.ExportTraceReinforcementModelRequest().TraceParam()
#     else:
#         if not isinstance(
#             trace_param, SherlockModelService_pb2.ExportTraceReinforcementModelRequest.TraceParam
#         ):
#             raise SherlockModelServiceError(
#                 "trace_param object is not of type "
#                 "SherlockModelService_pb2.ExportTraceReinforcementModelRequest.TraceParam."
#             )

#     trace_param.diameterThreshold.value = trace_param_diameter_threshold_val
#     trace_param.diameterThreshold.unit = trace_param_diameter_threshold_unit
#     trace_param.minHoleDiameterForShellOrBeam.value = trace_param_min_hole_diameter_val
#     trace_param.minHoleDiameterForShellOrBeam.unit = trace_param_min_hole_diameter_unit

#     return trace_param


# def set_trace_drill_hole_parameter(
#     trace_drill_hole_param=None,
#     trace_drill_hole_modeling="DISABLED",
#     trace_drill_hole_min_diameter_val=2,
#     trace_drill_hole_min_diameter_unit="mm",
#     trace_drill_hole_max_edge_val=1,
#     trace_drill_hole_max_edge_unit="mm",
# ):
#     """Set the Drill Hole Properties for the Export Trace Reinforcement Model operation."""
#     if trace_drill_hole_param is None:
#         trace_drill_hole_param = (
#             SherlockModelService_pb2.ExportTraceReinforcementModelRequest().TraceDrillHoleParam()
#         )
#     else:
#         if not isinstance(
#             trace_drill_hole_param,
#             SherlockModelService_pb2.ExportTraceReinforcementModelRequest.TraceDrillHoleParam,
#         ):
#             raise SherlockModelServiceError(
#                 "trace_drill_hole_param object is not of type "
#                 "SherlockModelService_pb2.ExportTraceReinforcementModelRequest.TraceDrillHoleParam."
#             )

#     trace_drill_hole_param.drillHoleModeling = trace_drill_hole_modeling
#     trace_drill_hole_param.minHoleDiameter.value = trace_drill_hole_min_diameter_val
#     trace_drill_hole_param.minHoleDiameter.unit = trace_drill_hole_min_diameter_unit
#     trace_drill_hole_param.maxEdgeLength.value = trace_drill_hole_max_edge_val
#     trace_drill_hole_param.maxEdgeLength.unit = trace_drill_hole_max_edge_unit

#     return trace_drill_hole_param
