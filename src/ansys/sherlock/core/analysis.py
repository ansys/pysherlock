# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

"""Module containing all analysis capabilities."""

try:
    import SherlockAnalysisService_pb2
    import SherlockAnalysisService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2
    from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockRunAnalysisError,
    SherlockRunStrainMapAnalysisError,
    SherlockUpdateNaturalFrequencyPropsError,
    SherlockUpdatePcbModelingPropsError,
    SherlockUpdateRandomVibePropsError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub


class Analysis(GrpcStub):
    """Contains all analysis capabilities."""

    def __init__(self, channel):
        """Initialize a gRPC stub for the Sherlock Analysis service."""
        super().__init__(channel)
        self.stub = SherlockAnalysisService_pb2_grpc.SherlockAnalysisServiceStub(channel)
        self.FIELD_NAMES = {
            "analysisTemp": "analysis_temp",
            "analysisTemp (optional)": "analysis_temp",
            "analysisTempUnits": "analysis_temp_units",
            "analysisTempUnits (optional)": "analysis_temp_units",
            "filterByEventFrequency": "filter_by_event_frequency",
            "forceModelRebuild": "force_model_rebuild",
            "harmonicVibeDamping": "harmonic_vibe_damping",
            "harmonicVibeCount": "harmonic_vibe_count",
            "modelSource": "model_source",
            "naturalFreqCount": "natural_freq_count",
            "naturalFreqMin": "natural_freq_min",
            "naturalFreqMinUnits": "natural_freq_min_units",
            "naturalFreqMax": "natural_freq_max",
            "naturalFreqMaxUnits": "natural_freq_max_units",
            "partValidationEnabled": "part_validation_enabled",
            "performNFFreqRangeCheck": "perform_nf_freq_range_check",
            "randomVibeDamping": "random_vibe_damping",
            "requireMaterialAssignmentEnabled": "require_material_assignment_enabled",
            "reuseModalAnalysis": "reuse_modal_analysis",
            "strainMapNaturalFreqs": "strain_map_natural_freqs",
        }

    @staticmethod
    def _add_analyses(request, analyses):
        """Add analyses."""
        for a in analyses:
            analysis = request.analyses.add()
            analysis.type = a[0]
            for p in a[1]:
                phase = analysis.phases.add()
                phase.name = p[0]
                for e in p[1]:
                    event = phase.events.add()
                    event.name = e

    def run_analysis(
        self,
        project,
        cca_name,
        analyses,
    ):
        """Run one or more Sherlock analyses.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        analyses : list of ``elements``

            - elements: list
                List of tuples (``type``, ``event``)

                - analysis_type : RunAnalysisRequest.Analysis.AnalysisType
                    Type of analysis to run.

                - event : list
                    List of tuples (``phase_name``, ``event_name``)

                    - phase_name : str
                        Name of the life cycle phase.
                    - event_name : str
                        Name of the life cycle event.

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
        >>> sherlock.analysis.run_analysis(
            "Test",
            "Card",
            [
                (SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.AnalysisType.NaturalFreq,
                [
                    ("Phase 1", ["Harmonic Event"])
                ]
                )
            ]
        )
        """
        try:
            if project == "":
                raise SherlockRunAnalysisError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockRunAnalysisError(message="CCA name is invalid.")
            if not isinstance(analyses, list):
                raise SherlockRunAnalysisError("Analyses argument is invalid.")
            if len(analyses) == 0:
                raise SherlockRunAnalysisError("One or more analyses are missing.")
        except SherlockRunAnalysisError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        request = SherlockAnalysisService_pb2.RunAnalysisRequest(
            project=project,
            ccaName=cca_name,
        )

        self._add_analyses(request, analyses)

        response = self.stub.runAnalysis(request)

        try:
            if response.value == -1:
                raise SherlockRunAnalysisError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockRunAnalysisError as e:
            LOG.error(str(e))
            raise e

    def get_harmonic_vibe_input_fields(self):
        """Get harmonic vibe property fields based on the user configuration.

        Returns
        -------
        list
            List of harmonic vibe property fields based on the user configuration.

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
        >>> sherlock.analysis.get_harmonic_vibe_input_fields()
        """
        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        message = SherlockAnalysisService_pb2.GetHarmonicVibeInputFieldsRequest(
            modelSource="GENERATED"
        )
        response = self.stub.getHarmonicVibeInputFields(message)

        fields = self._translate_field_names(response.fieldName)
        LOG.info(fields)

        return fields

    def get_random_vibe_input_fields(self, model_source=None):
        """Get random vibe property fields based on the user configuration.

        Parameters
        ----------
        model_source : ModelSource, optional
            Model source to get the random vibe property fields from.

        Returns
        -------
        list
            List of random vibe property fields based on the user configuration.

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
        >>> sherlock.analysis.get_random_vibe_input_fields(
            model_source=SherlockAnalysisService_pb2.ModelSource.STRAIN_MAP
        )
        """
        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        message = SherlockAnalysisService_pb2.GetRandomVibeInputFieldsRequest(
            modelSource=model_source
        )
        response = self.stub.getRandomVibeInputFields(message)

        fields = self._translate_field_names(response.fieldName)
        LOG.info(fields)

        return fields

    def _translate_field_names(self, names_list):
        names = ""
        for name in list(names_list):
            names = names + "\n" + self.FIELD_NAMES.get(name)

        return names

    def update_random_vibe_props(
        self,
        project,
        cca_name,
        random_vibe_damping=None,
        natural_freq_min=None,
        natural_freq_min_units=None,
        natural_freq_max=None,
        natural_freq_max_units=None,
        analysis_temp=None,
        analysis_temp_units=None,
        part_validation_enabled=None,
        force_model_rebuild=None,
        reuse_modal_analysis=None,
        perform_nf_freq_range_check=None,
        require_material_assignment_enabled=None,
        model_source=None,
        strain_map_natural_freqs=None,
    ):
        """Update properties for a random vibe analysis.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        random_vibe_damping: str, optional
            One or more modal damping ratios. The default is ``None``.
            Separate multiple float values with commas.
        natural_freq_min: double, optional
            Minimum frequency. The default is ``None``.
            This parameter is for NX Nastran analysis only.
        natural_freq_min_units: str, optional
            Minimum frequency units. The default is ``None``.
            Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            This parameter is for NX Nastran analysis only.
        natural_freq_max: double, optional
            Maximum frequency. The default is ``None``.
            This parameter is for NX Nastran analysis only.
        natural_freq_max_units: str, optional
            Maximum frequency units. The default is ``None``.
            Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            This parameter is for NX Nastran analysis only.
        analysis_temp: double, optional
            Temperature. The default is ``None``.
        analysis_temp_units: str, optional
            Temperature units. The default is ``None``.
            Options are ``"C"``, ``"F"``, and ``"K"``.
        part_validation_enabled: bool, optional
            Whether to enable part validation. The default is ``None``.
        force_model_rebuild: str, optional
            How to handle rebuilding of the model. The default is ``None``.
            Options are ``"FORCE"`` and ``"AUTO"``.
        reuse_modal_analysis: bool, optional
            Whether to reuse the natural frequency for modal analysis. The
            default is ``None``. This parameter is for NX Nastran analysis only.
        perform_nf_freq_range_check: bool, optional
            Whether to perform a frequency range check. The default is ``None``.
            This parameter is for NX Nastran analysis only.
        require_material_assignment_enabled: bool, optional
            Whether to require material assignment. The default is ``None``.
        model_source: ModelSource, optional
            Model source.
            This parameter is required for strain map analysis.
        strain_map_natural_freqs : list, optional
            List of natural frequencies. The default is ``None``.
            This parameter is required for strain map analysis.

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
        >>> sherlock.analysis.update_random_vibe_props(
            "Test",
            "Card",
            random_vibe_damping="0.01, 0.05",
            analysis_temp=20,
            analysis_temp_units="C",
            model_source=SherlockAnalysisService_pb2.ModelSource.STRAIN_MAP,
        )

        """
        try:
            if project == "":
                raise SherlockUpdateRandomVibePropsError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdateRandomVibePropsError(message="CCA name is invalid.")
            if random_vibe_damping == "":
                raise SherlockUpdateRandomVibePropsError(
                    message="Random vibe damping value is invalid."
                )
            if model_source == SherlockAnalysisService_pb2.ModelSource.STRAIN_MAP and (
                strain_map_natural_freqs is None or strain_map_natural_freqs == ""
            ):
                raise SherlockUpdateRandomVibePropsError(message="Natural frequencies are invalid.")

        except SherlockUpdateRandomVibePropsError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        request = SherlockAnalysisService_pb2.UpdateRandomVibePropsRequest(
            project=project,
            ccaName=cca_name,
            randomVibeDamping=random_vibe_damping,
            naturalFreqMin=natural_freq_min,
            naturalFreqMinUnits=natural_freq_min_units,
            naturalFreqMax=natural_freq_max,
            naturalFreqMaxUnits=natural_freq_max_units,
            analysisTemp=analysis_temp,
            analysisTempUnits=analysis_temp_units,
            partValidationEnabled=part_validation_enabled,
            forceModelRebuild=force_model_rebuild,
            reuseModalAnalysis=reuse_modal_analysis,
            performNFFreqRangeCheck=perform_nf_freq_range_check,
            requireMaterialAssignmentEnabled=require_material_assignment_enabled,
            modelSource=model_source,
        )

        if model_source == SherlockAnalysisService_pb2.ModelSource.STRAIN_MAP:
            request.strainMapNaturalFreqs = strain_map_natural_freqs

        response = self.stub.updateRandomVibeProps(request)

        try:
            if response.value == -1:
                raise SherlockUpdateRandomVibePropsError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockUpdateRandomVibePropsError as e:
            LOG.error(str(e))
            raise e

    def get_natural_frequency_input_fields(self):
        """Get natural frequency property fields based on the user configuration.

        Returns
        -------
        list
            List of natural frequency property fields based on the user configuration.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock.project.import_odb_archive(
        >>> sherlock = launch_sherlock()
                "ODB++ Tutorial.tgz",
                True,
                True,
                True,
                True,
                project="Test",
                cca_name="Card",
            )
            >>> sherlock.analysis.get_natural_frequency_input_fields()
        """
        if not self._is_connection_up():
            LOG.error("There is not connected to a gRPC service.")
            return

        message = SherlockAnalysisService_pb2.GetNaturalFrequencyInputFieldsRequest()
        response = self.stub.getNaturalFrequencyInputFields(message)

        fields = self._translate_field_names(response.fieldName)
        LOG.info(fields)

        return fields

    def update_natural_frequency_props(
        self,
        project,
        cca_name,
        natural_freq_count,
        natural_freq_min,
        natural_freq_min_units,
        natural_freq_max,
        natural_freq_max_units,
        part_validation_enabled,
        require_material_assignment_enabled,
        analysis_temp=None,
        analysis_temp_units=None,
    ):
        """Update properties for a natural frequency analysis.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the CCA.
        natural_freq_count: int
            Natural frequecy result count.
        natural_freq_min: double, optional
            Minimum frequency. This parameter is for NX Nastran analysis only.
        natural_freq_min_units: str, optional
            Minimum frequency units. Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            This parameter is for NX Nastran analysis only.
        natural_freq_max: double, optional
            Maximum frequency. This parameter is for NX Nastran analysis only.
        natural_freq_max_units: str, optional
            Maximum frequency units. Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            This parameter is for NX Nastran analysis only.
        part_validation_enabled: bool
            Whether part validation is enabled.
        require_material_assignment_enabled: bool
            Whether to require material assignment.
        analysis_temp: double, optional
            Temperature.
        analysis_temp_units: str, optional
            Temperature units. Options are ``"C"``, ``"F"``, and ``"K"``.

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
            cca_name="Card"
        )
        >>> sherlock.analysis.update_natural_frequency_props(
            "Test",
            "Card",
            natural_freq_count=2,
            natural_freq_min=10,
            natural_freq_min_units="HZ",
            natural_freq_max=100,
            natural_freq_max_units="HZ",
            part_validation_enabled=True,
            require_material_assignment_enabled=False,
            analysis_temp=25,
            analysis_temp_units="C"
        )

        """
        try:
            if project == "":
                raise SherlockUpdateNaturalFrequencyPropsError(message="Project name is invalid.")
            if cca_name == "":
                raise SherlockUpdateNaturalFrequencyPropsError(message="CCA name is invalid.")
        except SherlockUpdateNaturalFrequencyPropsError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("There is no connection to a gRPC service.")
            return

        request = SherlockAnalysisService_pb2.UpdateNaturalFrequencyPropsRequest(
            project=project,
            ccaName=cca_name,
            naturalFreqCount=natural_freq_count,
            naturalFreqMin=natural_freq_min,
            naturalFreqMinUnits=natural_freq_min_units,
            naturalFreqMax=natural_freq_max,
            naturalFreqMaxUnits=natural_freq_max_units,
            partValidationEnabled=part_validation_enabled,
            requireMaterialAssignmentEnabled=require_material_assignment_enabled,
            analysisTemp=analysis_temp,
            analysisTempUnits=analysis_temp_units,
        )

        response = self.stub.updateNaturalFrequencyProps(request)

        try:
            if response.value == -1:
                raise SherlockUpdateNaturalFrequencyPropsError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockUpdateNaturalFrequencyPropsError as e:
            LOG.error(str(e))
            raise e

    def run_strain_map_analysis(
        self,
        project,
        cca_name,
        strain_map_analyses,
    ):
        """Run one or more strain map analyses.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_name : str
            Name of the main CCA for the analysis.
        strain_map_analyses : list
            List of analyses consisting of these properties:

            - analysis_type : RunStrainMapAnalysisRequest.StrainMapAnalysis.AnalysisType
                Type of analysis to run.
            - event_strain_maps : list
                List of the strain maps assigned to the desired life cycle events for
                a given PCB side. The list consists of these properties:

              - phase_name : str
                  Life cycle phase name for the strain map assignment.
              - event_name : str
                  Life cycle event name for the strain map assignment.
              - pcb_side : str
                  PCB side for the strain map. Options are ``"TOP"`` and ``"BOTTOM"``.
              - strain_map : str
                  Name of the strain map assigned to the life cycle event.
              - sub_assembly_name : str, optional
                  Name of the subassembly CCA to assign the strain map to.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> analysis_request = SherlockAnalysisService_pb2.RunStrainMapAnalysisRequest
        >>> analysis.run_strain_map_analysis(
                "AssemblyTutorial",
                "Main Board",
                [[
                    analysis_request.StrainMapAnalysis.AnalysisType.RandomVibe,
                    [["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                     ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                     ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"]],
                ]]
            )
        """
        try:
            if project == "":
                raise SherlockRunStrainMapAnalysisError(message="Project name is invalid.")

            if cca_name == "":
                raise SherlockRunStrainMapAnalysisError(message="CCA name is invalid.")

            if not isinstance(strain_map_analyses, list):
                raise SherlockRunStrainMapAnalysisError("Analyses argument is invalid.")

            if len(strain_map_analyses) == 0:
                raise SherlockRunStrainMapAnalysisError("One or more analyses are missing.")

            request = SherlockAnalysisService_pb2.RunStrainMapAnalysisRequest(
                project=project,
                ccaName=cca_name,
            )

            for i, analysis in enumerate(strain_map_analyses):
                if not isinstance(analysis, list):
                    raise SherlockRunStrainMapAnalysisError(
                        f"Analyses argument is invalid for strain map analysis {i}."
                    )

                if len(analysis) != 2:
                    raise SherlockRunStrainMapAnalysisError(
                        f"Number of elements ({str(len(analysis))}) is wrong for "
                        f"strain map analysis {i}."
                    )

                analysis_type = analysis[0]
                if analysis_type == "":
                    raise SherlockRunStrainMapAnalysisError(
                        f"Analysis type is missing for strain map analysis {i}."
                    )

                strain_map_analysis_request = request.strainMapAnalyses.add()
                strain_map_analysis_request.type = analysis_type

                if len(analysis[1]) == 0:
                    raise SherlockRunStrainMapAnalysisError(
                        f"One or more event strain maps are missing for strain map analysis {i}."
                    )

                for j, event_strain_map in enumerate(analysis[1]):
                    if not isinstance(event_strain_map, list):
                        raise SherlockRunStrainMapAnalysisError(
                            f"Event strain maps argument is invalid for strain map analysis {i}."
                        )
                    elif len(event_strain_map) < 4:
                        raise SherlockRunStrainMapAnalysisError(
                            f"Number of elements ({str(len(event_strain_map))}) is wrong for "
                            f"event strain map {j} for strain map analysis {i}."
                        )
                    elif event_strain_map[0] == "":
                        raise SherlockRunStrainMapAnalysisError(
                            f"Life phase is missing for event strain map {j} for strain "
                            f"map analysis {i}."
                        )
                    elif event_strain_map[1] == "":
                        raise SherlockRunStrainMapAnalysisError(
                            f"Event name is missing for event strain map {j} for strain "
                            f"map analysis {i}."
                        )
                    elif event_strain_map[2] == "":
                        raise SherlockRunStrainMapAnalysisError(
                            f"PCB side is missing for event strain map {j} for strain "
                            f"map analysis {i}."
                        )
                    elif event_strain_map[3] == "":
                        raise SherlockRunStrainMapAnalysisError(
                            f"Strain map name is missing for event strain map {j} for strain "
                            f"map analysis {i}."
                        )

                    event_strain_map_request = strain_map_analysis_request.eventStrainMaps.add()
                    event_strain_map_request.phaseName = event_strain_map[0]
                    event_strain_map_request.eventName = event_strain_map[1]
                    event_strain_map_request.pcbSide = event_strain_map[2]
                    event_strain_map_request.strainMap = event_strain_map[3]

                    if len(event_strain_map) == 5:
                        event_strain_map_request.subAssemblyName = event_strain_map[4]

            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                return

            response = self.stub.runStrainMapAnalysis(request)

            if response.value == -1:
                raise SherlockRunStrainMapAnalysisError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockRunStrainMapAnalysisError as e:
            LOG.error(str(e))
            raise e

    def update_pcb_modeling_props(self, project, cca_names, analyses):
        """Update FEA PCB Modeling properties for one or more CCAs.

        Parameters
        ----------
        project : str
            Name of the Sherlock project.
        cca_names : list
            Names of the CCAs to be used for the analysis.
        analyses : list
            List of elements consisting of the following properties:

            - analysis_type : UpdatePcbModelingPropsRequest.Analysis.AnalysisType
                Type of analysis applied.
            - pcb_model_type : UpdatePcbModelingPropsRequest.Analysis.PcbModelType
                The PCB modeling mesh type.
            - modeling_region_enabled : bool
                Indicates if modeling regions are enabled.
            - pcb_material_model : UpdatePcbModelingPropsRequest.Analysis.PcbMaterialModel
                The PCB modeling PCB model type.
            - pcb_max_materials : int
                The number of PCB materials for Uniform Elements and Layered Elements PCB model
                types. Not applicable if PCB model is Uniform or Layered.
            - pcb_elem_order : ElementOrder
                The element order for PCB elements.
            - pcb_max_edge_length : float
                The maximum mesh size for PCB elements.
            - pcb_max_edge_length_units : str
                The length units for the maximum mesh size.
            - pcb_max_vertical : float
                The maximum vertical mesh size for PCB elements.
            - pcb_max_vertical_units : str
                The length units for the maximum vertical mesh size.
            - quads_preferred : bool
                Indicates that the meshing engine should attempt to generate quad-shaped elements
                when creating the mesh.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> update_request = SherlockAnalysisService_pb2.UpdatePcbModelingPropsRequest
        >>> sherlock.analysis.update_pcb_modeling_props(
            "Tutorial Project",
            ["Main Board"],
            [
                (
                    update_request.Analysis.AnalysisType.NaturalFreq,
                    update_request.Analysis.PcbModelType.Bonded,
                    True,
                    update_request.Analysis.PcbMaterialModel.Uniform,
                    SherlockAnalysisService_pb2.ElementOrder.SolidShell,
                    6,
                    "mm",
                    3,
                    "mm",
                    True,
                )
            ],
        )
        """
        try:
            if project == "":
                raise SherlockUpdatePcbModelingPropsError(message="Project name is invalid.")
            if not cca_names:
                raise SherlockUpdatePcbModelingPropsError(message="CCA names are invalid.")
            if not analyses:
                raise SherlockUpdatePcbModelingPropsError(message="Analysis input(s) are invalid.")
            if not self._is_connection_up():
                LOG.error("There is no connection to a gRPC service.")
                return

            request = SherlockAnalysisService_pb2.UpdatePcbModelingPropsRequest(
                project=project,
                ccaNames=cca_names,
            )

            """Add PCB Modeling Props to Request"""
            uniform = SherlockAnalysisService_pb2.UpdatePcbModelingPropsRequest.Analysis.Uniform
            layered = SherlockAnalysisService_pb2.UpdatePcbModelingPropsRequest.Analysis.Layered
            for a in analyses:
                analysis = request.analyses.add()
                analysis.type = a[0]
                analysis.modelType = a[1]
                analysis.modelingRegionEnabled = a[2]
                analysis.pcbMaterialModel = a[3]
                if analysis.pcbMaterialModel == uniform or analysis.pcbMaterialModel == layered:
                    analysis.pcbElemOrder = a[4]
                    analysis.pcbMaxEdgeLength = a[5]
                    analysis.pcbMaxEdgeLengthUnits = a[6]
                    analysis.pcbMaxVertical = a[7]
                    analysis.pcbMaxVerticalUnits = a[8]
                    analysis.quadsPreferred = a[9]
                else:
                    analysis.pcbMaxMaterials = a[4]
                    analysis.pcbElemOrder = a[5]
                    analysis.pcbMaxEdgeLength = a[6]
                    analysis.pcbMaxEdgeLengthUnits = a[7]
                    analysis.pcbMaxVertical = a[8]
                    analysis.pcbMaxVerticalUnits = a[9]
                    analysis.quadsPreferred = a[10]

            response = self.stub.updatePcbModelingProps(request)

            if response.value == -1:
                raise SherlockUpdatePcbModelingPropsError(response.message)
            return response.value
        except SherlockUpdatePcbModelingPropsError as e:
            LOG.error(str(e))
            raise e
