# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

"""Module containing all model generation capabilities."""
import os.path

import grpc

from ansys.sherlock.core.types.analysis_types import ElementOrder

try:
    import SherlockModelService_pb2
    from SherlockModelService_pb2 import MeshType, TraceOutputType
    import SherlockModelService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockModelService_pb2
    from ansys.api.sherlock.v0.SherlockModelService_pb2 import MeshType, TraceOutputType
    from ansys.api.sherlock.v0 import SherlockModelService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockExportAEDBError,
    SherlockExportFEAModelError,
    SherlockModelServiceError,
    SherlockNoGrpcConnectionException,
)
from ansys.sherlock.core.grpc_stub import GrpcStub
from ansys.sherlock.core.types.common_types import Measurement
from ansys.sherlock.core.utils.version_check import require_version


class Model(GrpcStub):
    """Contains all model generation capabilities."""

    def __init__(self, channel: grpc.Channel, server_version: int):
        """Initialize a gRPC stub for the Sherlock Model service."""
        super().__init__(channel, server_version)
        self.stub = SherlockModelService_pb2_grpc.SherlockModelServiceStub(channel)

    @require_version()
    def export_trace_reinforcement_model(
        self,
        project_name: str,
        cca_name: str,
        export_file: str,
        overwrite: bool = True,
        display_model: bool = False,
        generate_models_for_all_layers: bool = False,
        coordinate_units: str = "mm",
        trace_param_diameter_threshold_val: float = 2,
        trace_param_diameter_threshold_unit: str = "mm",
        trace_param_min_hole_diameter_val: float = 0.25,
        trace_param_min_hole_diameter_unit: str = "mm",
        trace_drill_hole_modeling: str = "DISABLED",
        trace_drill_hole_min_diameter_val: float = 2,
        trace_drill_hole_min_diameter_unit: str = "mm",
        trace_drill_hole_max_edge_val: float = 1,
        trace_drill_hole_max_edge_unit: str = "mm",
    ) -> int:
        r"""Export a trace reinforcement model.

        Available Since: 2023R1

        Parameters
        ----------
        project_name: str
            Name of the Sherlock project to generate the trace reinforcement model for.
        cca_name: str
            Name of the CCA to generate the trace reinforcement model from.
        export_file: str
            Path for saving exported files to. The file extension must be ``.wbjn``.
        overwrite: bool, optional
            Whether to overwrite an existing file having the same file name.
            The default is ``True``.
        display_model: bool, optional
            Whether to launch and display the exported model in Ansys Workbench
            Mechanical once the export finishes. The default is ``False``.
        generate_models_for_all_layers:  bool, optional
            Whether to generate and export trace models for not only the generated trace
            reinforcement layers but also all other layers. The default is ``False``, in
            which case only trace reinforcement layers are generated and exported.
        coordinate_units: str, optional
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
            raise SherlockNoGrpcConnectionException()

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

    @require_version()
    def generate_trace_model(
        self,
        project_name,
        cca_name: str = "",
        copper_layer_name: str = "",
        max_arc_segment: float = 0.0,
        max_arc_segment_units: str = "mm",
        min_trace_area: float = 0.0,
        min_trace_area_units: str = "mm2",
        min_hole_area: float = 0.0,
        min_hole_area_units: str = "mm2",
        use_snapshot_for_non_image_layer: bool = False,
    ) -> int:
        r"""Generate one or more trace models for a project.

        Available Since: 2023R2

        Parameters
        ----------
        project_name: str
            Name of the Sherlock project to generate one or more trace models for.
        cca_name: str, optional
            Name of the CCA to generate one or more trace models from. The default is
            ``""``, in which case trace models are generated for CCAs and
            all layers.
        copper_layer_name: str, optional
            Name of the copper layer to generate one or more trace models from. The default
            is ``""``, in which case trace models are generated either for the given CCA
            or for all layers.
        max_arc_segment: float, optional
            Maximum length of the segment to generate when Sherlock
            converts EDA arc drawing commands to line segments. The default is
            ``0.0``. Smaller values for the maximum arc segment result in smoother
            arc representations on the FEA model. However, the cost of generating a
            larger number of shorter segments is higher. Such short segments cause
            the FEA tool to generate a larger number of smaller elements to represent
            the curved solid.
        max_arc_segment_units: str, optional
            Units for the maximum arc segment. The default is ``"mm"``.
        min_trace_area: float, optional
            Minimum area of any trace polygon to include in the trace model.
            The default is ``0.0``, which turns off any area filtering.
        min_trace_area_units: str, optional
            Units for the minimum trace area. The default is ``"mm2"``.
        min_hole_area: float, optional
            Minimum area of any trace hole to include in the trace model.
            The default is ``0.0``, which turns off any hole filtering.
        min_hole_area_units: str, optional
            Units for the minimum hole area. The default is ``"mm2"``.
        use_snapshot_for_non_image_layer: bool, optional
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

        except Exception as e:
            LOG.error(str(e))
            raise

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

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

    @require_version(242)
    def export_aedb(
        self,
        project_name: str,
        cca_name: str,
        export_file: str,
        overwrite: bool = True,
        display_model: bool = False,
    ) -> int:
        r"""Export an Electronics Desktop model.

        Available Since: 2024R2

        Parameters
        ----------
        project_name: str
            Name of the Sherlock project to generate the EDB model for.
        cca_name: str
            Name of the CCA to generate the EDB model from.
        export_file: str
            Directory for saving exported model to.
        overwrite: bool, optional
            Whether to overwrite an existing file having the same file name.
            The default is ``True``.
        display_model: bool, optional
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
            raise SherlockNoGrpcConnectionException()

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

    @require_version(242)
    def exportTraceModel(self, layer_params: list[bool | int | float | str]) -> int:
        r"""Export a trace model to a specified output file.

        Available Since: 2024R2

        Parameters
        ----------
        layer_params : list[bool | int | float | str]
            list of parameters for export a trace model of a single copper layer.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.types.analysis_types import ElementOrder
        >>> from ansys.sherlock.core import launcher
        >>> from ansys.api.sherlock.v0 import SherlockModelService_pb2
        >>> sherlock = launcher.launch_sherlock()
        >>> list_of_params_for_layers = []
        >>> list_of_params_for_layers.append(
                sherlock.model.createExportTraceCopperLayerParams(
                    "Tutorial Project",
                    "Main Board",
                    ".\\outputfile_path.stp",
                    "copper-01.odb",
                    False,
                    False,
                    False,
                    False,
                    "mm",
                    SherlockModelService_pb2.MeshType.NONE,
                    False,
                    SherlockModelService_pb2.TraceOutputType.ALL_REGIONS,
                    ElementOrder.LINEAR,
                    1.0,
                    "mm".
                    1,
                    False,
                    1.0,
                    "mm",
                    1.0
                )
            )
        >>> sherlock.model.exportTraceModel(list_of_params_for_layers)
        """
        try:
            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            request = SherlockModelService_pb2.ExportTraceModelRequest()
            request.traceModelExportParams.extend(layer_params)

            return_code = self.stub.exportTraceModel(request)
            if return_code.value != 0:
                # Return error from the server
                raise SherlockModelServiceError(return_code.message)

            return return_code.value
        except Exception as e:
            LOG.error(str(e))
            raise

    @require_version(242)
    def createExportTraceCopperLayerParams(
        self,
        project_name,
        cca_name,
        output_file_path,
        copper_layer,
        overwrite: bool = False,
        display_after: bool = False,
        clear_FEA_database: bool = False,
        use_FEA_model_ID: bool = False,
        coord_units: str = "mm",
        mesh_type: int = MeshType.NONE,
        is_modeling_region_enabled: bool = False,
        trace_output_type: int = TraceOutputType.ALL_REGIONS,
        element_order: ElementOrder = ElementOrder.LINEAR,
        max_mesh_size: float = 1.0,
        max_mesh_size_units: str = "mm",
        max_holes_per_trace: int = 2,
        is_drill_hole_modeling_enabled: bool = False,
        drill_hole_min_diameter: float = 1.0,
        drill_hole_min_diameter_units: str = "mm",
        drill_hole_max_edge_length: float = 1.0,
        drill_hole_max_edge_length_units: str = "mm",
    ) -> SherlockModelService_pb2.TraceModelExportParams:
        r"""Create a set of parameters to be used to export a single copper layer.

        Creates TraceModelExportParams object that can be added to an export trace model request.
        Should be used in conjunction with exportTraceModel method to export multiple trace layers
        all at once. See example below.

        Parameters
        ----------
        project_name: str
            Name of the Sherlock project containing trace layer to export.
        cca_name: str
            Name of the CCA containing the trace layer to export.
        output_file_path: str
            File path including the file name and extension where the trace layer will be exported.
            Valid file extensions: .py, .bdf, .apdl, .cdb, .wbjn, .stp, .step, .tcl, .stl
            Note: relative paths will be relative to sherlock install directory,
            not the python script.
        copper_layer: str
            Name of the copper layer in the given CCA to export.
        overwrite: bool = False
            Determines if sherlock should overwrite the output file if it exists.
        display_after: bool = False
            Determines if the output file should automatically display after export.
        clear_FEA_database: bool = False
            Determines if sherlock should clear the database after export.
            Applicable file extensions: .apdl, and .cdb.
        use_FEA_model_ID: bool = False
            Determines if the FEA model id is used or not.
        coord_units: str = "mm"
            Units of the coordinate system. Applicable to .py .wbjn, .stp, .step.
        mesh_type: MeshType = MeshType.NONE
            Options of difference trace meshing strategies
        is_modeling_region_enabled: bool = False
            Determines if pre-defined modeling regions will be applied to the exported trace model.
        trace_output_type: TraceOutputType = TraceOutputType.ALL_REGIONS
            Options to select which trace regions to include in the 3D model.
        element_order: ElementOrder = ElementOrder.LINEAR
            Type of FEA element to be used when modeling each component.
        max_mesh_size: float = 1.0
            Indicates the desired element sizes.
        max_mesh_size_units: str = "mm"
            Indicates the units to be used with max_mesh_size.
        max_holes_per_trace: int = 2
            Maximum number of holes allowed in a trace before partitioning it into multiple traces.
        is_drill_hole_modeling_enabled: bool = False
            Determines if drill holes will be modeled or not.
        drill_hole_min_diameter: float = 1.0
            All drill holes with a diameter < this value will not be modeled.
        drill_hole_min_diameter_units : str = "mm"
            Units associated with drill_hole_min_diameter.
        drill_hole_max_edge_length: float = 1.0
            Specifies the length of the line segments used to represent round drill holes.
        drill_hole_max_edge_length_units: str = "mm"
            Units associated with drill_hole_max_edge_length.

        Returns
        -------
        TraceModelExportParams
            Object that holds the data for a single export trace request.

        Examples
        --------
        >>> from ansys.sherlock.core import launcher
        >>> from ansys.sherlock.core.types.analysis_types import ElementOrder
        >>> from ansys.api.sherlock.v0 import SherlockModelService_pb2
        >>> sherlock = launcher.launch_sherlock()
        >>> copper_1_layer = sherlock.model.createExportTraceCopperLayerParams(
                "Tutorial Project",
                "Main Board",
                ".\\outputfile_path.stp",
                "copper-01.odb",
                False,
                False,
                False,
                False,
                "mm",
                SherlockModelService_pb2.MeshType.NONE,
                False,
                SherlockModelService_pb2.TraceOutputType.ALL_REGIONS,
                ElementOrder.LINEAR,
                1.0,
                "mm",
                2,
                False,
                1.0,
                "mm",
                1.0
            )
        >>> copper_2_layer = sherlock.model.createExportTraceCopperLayerParams(
                "Tutorial Project",
                "Main Board",
                ".\\outputfile_path2.stp",
                "copper-02.odb",
                False,
                False,
                False,
                False,
                "mm",
                SherlockModelService_pb2.MeshType.NONE,
                False,
                SherlockModelService_pb2.TraceOutputType.ALL_REGIONS,
                ElementOrder.LINEAR,
                1.0,
                "mm",
                2,
                False,
                1.0,
                "mm",
                1.0
            )
        >>> sherlock.model.exportTraceModel([copper_1_layer, copper_2_layer])
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
        pmp = ret.pcbMeshPropParam
        pmp.meshType = mesh_type
        pmp.isModelingRegionEnabled = is_modeling_region_enabled

        # Trace Params
        tpp = ret.tracePropParam
        tpp.traceOutputs = trace_output_type
        tpp.elementOrder = element_order
        tpp.maxMeshSize.value = max_mesh_size
        tpp.maxMeshSize.units = max_mesh_size_units
        tpp.maxHolesPerTrace = max_holes_per_trace

        # Drill Hole Params
        dhm = ret.drillHoleModeling
        dhm.drillHoleModelingEnabled = is_drill_hole_modeling_enabled
        dhm.minHoleDiameter.value = drill_hole_min_diameter
        dhm.minHoleDiameter.units = drill_hole_min_diameter_units
        dhm.maxEdgeLength.value = drill_hole_max_edge_length
        dhm.maxEdgeLength.units = drill_hole_max_edge_length_units

        return ret

    def export_FEA_model(
        self,
        project: str,
        cca_name: str,
        export_file: str,
        analysis: str,
        drill_hole_parameters: list[dict[str, str | Measurement]],
        detect_lead_modeling: str,
        lead_model_parameters: list[dict[str, int | str | Measurement]],
        display_model: bool,
        clear_FEA_database: bool,
        use_FEA_model_id: bool,
        coordinate_units: str,
    ) -> int:
        """
        Export a FEA model.

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        export_file: str
            Full path for saving exported files to. The file extension must be ``.wbjn``.
        analysis: str
            The type of analysis that is being exported. Valid values are ``NaturalFreq``,
            ``HarmonicVibe``, ``ICTAnalysis``, ``MechanicalShock`` or ``RandomVibe``.
        drill_hole_parameters: list[dict[str, str | Measurement]]
            List of the drill hole parameters consisting of these properties:

                - drill_hole_modeling: str
                    The status of the drill hole modeling feature. If enabled, automatically enable
                    drill hole modeling. Valid values are ``ENABLED/enabled`` or
                    ``DISABLED/disabled``.
                - min_hole_diameter: MinHoleDiameter
                    The properties of the minimum hole diameter.
                - max_edge_length: MaxEdgeLength
                    The properties of the maximum edge length.
        detect_lead_modeling: str
            The status of the detect lead modeling feature. If enabled, automatically enable lead
            modeling if any part has lead geometry defined. Valid values are ``ENABLED`` or
            ``DISABLED``.
        lead_model_parameters: list[dict[str, int | str | Measurement]]
            List of the lead model parameters consisting of these properties:

                - lead_modeling: str
                    The status of the lead modeling feature. If enabled, automatically enable lead
                    modeling. Valid values are ``ENABLED`` or ``DISABLED``.
                - lead_element_order: str
                     The type of the element order. Valid values are ``First Order (Linear)``,
                     ``Second Order (Quadratic)``, or ``Solid Shell``.
                - max_mesh_size: MaxMeshSize
                    The properties of the maximum mesh size.
                - vertical_mesh_size: VerticalMeshSize
                    The properties of the vertical mesh size.
                - thicknessCount: int, optional
                    The number of elements through the lead thickness that will be created per lead.
                     The default value is 3 and the maximum is 5. Only used when the advanced lead
                     mesh setting is enabled.
                - aspectRatio: int, optional
                    The aspect ratio is multiplied by the lead thickness divided by the through
                    thickness count to give the lead element height. The default value is 2 and the
                    maximum is 10. Only used when the advanced lead mesh setting is enabled.
        display_model: bool
            Whether to display the model after export.
        clear_FEA_database: bool
            Whether to clear FEA database before defining model.
        use_FEA_model_id: bool
            Whether to use FEA model ID.
        coordinate_units: str
            Units of the model coordinates to use when exporting a model.


        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> from ansys.sherlock.core.types.common_types import (
            Measurement,
        )
        >>> sherlock = launch_sherlock()
        >>> sherlock.model.export_FEA_model(
                project="Test Project",
                cca_name="Main Board",
                export_file="C:/Temp/export.wbjn",
                analysis="NaturalFreq",
                drill_hole_parameters=[
                    {
                        "drill_hole_modeling": "ENABLED",
                        "min_hole_diameter": Measurement(value=0.5, unit="mm"),
                        "max_edge_length": Measurement(value=1.0, unit="mm")
                    }
                ],
                detect_lead_modeling="ENABLED",
                lead_model_parameters=[
                    {
                        "lead_modeling": "ENABLED",
                        "lead_element_order": "First Order (Linear)",
                        "max_mesh_size": Measurement(value=0.5, unit="mm"),
                        "vertical_mesh_size": Measurement(value=0.1, unit="mm"),
                        "thicknessCount": 3,
                        "aspectRatio": 2
                    }
                ],
                display_model=True,
                clear_FEA_database=True,
                use_FEA_model_id=True,
                coordinate_units="mm"
            )
        """
        try:
            if not project:
                raise SherlockExportFEAModelError(message="Project name is invalid.")

            if not cca_name:
                raise SherlockExportFEAModelError(message="CCA name is invalid.")

            if not export_file:
                raise SherlockExportFEAModelError(message="Export file path is invalid.")

            if not os.path.exists(os.path.dirname(export_file)):
                raise SherlockExportFEAModelError(
                    message=f"Export file directory " f'"{export_file}" ' f"does not exist."
                )

            for param in drill_hole_parameters:
                min_hole_diameter = param.get("min_hole_diameter")
                if not isinstance(min_hole_diameter, Measurement):
                    raise SherlockExportFEAModelError(message="Minimum hole diameter is invalid.")

                max_edge_length = param.get("max_edge_length")
                if not isinstance(max_edge_length, Measurement):
                    raise SherlockExportFEAModelError(message="Maximum edge length is invalid.")

            for param in lead_model_parameters:
                max_mesh_size = param.get("max_mesh_size")
                if not isinstance(max_mesh_size, Measurement):
                    raise SherlockExportFEAModelError(message="Maximum mesh size is invalid.")

                vertical_mesh_size = param.get("vertical_mesh_size")
                if not isinstance(vertical_mesh_size, Measurement):
                    raise SherlockExportFEAModelError(message="Vertical mesh size is invalid.")

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            export_request = SherlockModelService_pb2.ExportFEAModelRequest()
            export_request.project = project
            export_request.ccaName = cca_name
            export_request.exportFile = export_file
            export_request.analysis = (
                SherlockModelService_pb2.ExportFEAModelRequest.ExportAnalysis.Value(analysis)
            )

            for param in drill_hole_parameters:
                export_request.drillHoleParam.drillHoleModeling = param.get("drill_hole_modeling")

                min_hole_diameter = param.get("min_hole_diameter")
                export_request.drillHoleParam.minHoleDiameter.value = min_hole_diameter.value
                export_request.drillHoleParam.minHoleDiameter.unit = min_hole_diameter.unit

                max_edge_length = param.get("max_edge_length")
                export_request.drillHoleParam.maxEdgeLength.value = max_edge_length.value
                export_request.drillHoleParam.maxEdgeLength.unit = max_edge_length.unit

            export_request.detectLeadModeling = detect_lead_modeling.upper()

            for param in lead_model_parameters:
                export_request.leadModelParam.leadModeling = param.get("lead_modeling").upper()

                export_request.leadModelParam.leadElemOrder = param.get("lead_element_order")

                max_mesh_size = param.get("max_mesh_size")
                export_request.leadModelParam.maxMeshSize.value = max_mesh_size.value
                export_request.leadModelParam.maxMeshSize.unit = max_mesh_size.unit

                vertical_mesh_size = param.get("vertical_mesh_size")
                export_request.leadModelParam.verticalMeshSize.value = vertical_mesh_size.value
                export_request.leadModelParam.verticalMeshSize.unit = vertical_mesh_size.unit

                thickness_count = param.get("thicknessCount", 3)
                export_request.leadModelParam.thicknessCount = thickness_count

                aspect_ratio = param.get("aspectRatio", 2)
                export_request.leadModelParam.aspectRatio = aspect_ratio

            export_request.displayModel = display_model
            export_request.clearFEADatabase = clear_FEA_database
            export_request.useFEAModelID = use_FEA_model_id
            export_request.coordinateUnits = coordinate_units

            return_code = self.stub.exportFEAModel(export_request)
            if return_code.value != 0:
                raise SherlockExportFEAModelError(message=return_code.message)

            return return_code.value

        except SherlockExportFEAModelError as e:
            LOG.error(str(e))
            raise e
