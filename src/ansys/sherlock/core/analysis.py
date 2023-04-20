# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

"""Module containing all the analysis capabilities."""

try:
    import SherlockAnalysisService_pb2
    import SherlockAnalysisService_pb2_grpc
    import SherlockLifeCycleService_pb2
    import SherlockLifeCycleService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2
    from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2_grpc
    from ansys.api.sherlock.v0 import SherlockLifeCycleService_pb2
    from ansys.api.sherlock.v0 import SherlockLifeCycleService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockGetRandomVibeInputFieldsError,
    SherlockInvalidPhaseError,
    SherlockRunAnalysisError,
    SherlockRunStrainMapAnalysisError,
    SherlockUpdateNaturalFrequencyPropsError,
    SherlockUpdateRandomVibePropsError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub


class Analysis(GrpcStub):
    """Module containing all the analysis capabilities."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockAnalysisService."""
        self.channel = channel
        self.stub = SherlockAnalysisService_pb2_grpc.SherlockAnalysisServiceStub(channel)
        self.lifecycle = SherlockLifeCycleService_pb2_grpc.SherlockLifeCycleServiceStub(channel)
        self.ANALYSIS_HOME = SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis
        self.ANALYSIS_TYPES = {
            "UNKNOWN": self.ANALYSIS_HOME.UNKNOWN,
            "NATURALFREQ": self.ANALYSIS_HOME.NaturalFreq,
            "HARMONICVIBE": self.ANALYSIS_HOME.HarmonicVibe,
            "ICTANALYSIS": self.ANALYSIS_HOME.ICTAnalysis,
            "MECHANICALSHOCK": self.ANALYSIS_HOME.MechanicalShock,
            "RANDOMVIBE": self.ANALYSIS_HOME.RandomVibe,
            "COMPONENTFAILUREMODE": self.ANALYSIS_HOME.ComponentFailureMode,
            "DFMEAMODULE": self.ANALYSIS_HOME.DFMEAModule,
            "PTHFATIGUE": self.ANALYSIS_HOME.PTHFatigue,
            "PARTVALIDATION": self.ANALYSIS_HOME.PartValidation,
            "SEMICONDUCTORWEAROUT": self.ANALYSIS_HOME.SemiconductorWearout,
            "SOLDERJOINTFATIGUE": self.ANALYSIS_HOME.SolderJointFatigue,
            "THERMALDERATING": self.ANALYSIS_HOME.ThermalDerating,
            "THERMALMECH": self.ANALYSIS_HOME.ThermalMech,
        }
        self.TEMP_UNIT_LIST = None
        self.FREQ_UNIT_LIST = None
        self.FIELD_NAMES = {
            "naturalFreqCount": "natural_freq_count",
            "randomVibeDamping": "random_vibe_damping",
            "naturalFreqMin": "natural_freq_min",
            "naturalFreqMinUnits": "natural_freq_min_units",
            "naturalFreqMax": "natural_freq_max",
            "naturalFreqMaxUnits": "natural_freq_max_units",
            "analysisTemp": "analysis_temp",
            "analysisTemp (optional)": "analysis_temp",
            "analysisTempUnits": "analysis_temp_units",
            "analysisTempUnits (optional)": "analysis_temp_units",
            "partValidationEnabled": "part_validation_enabled",
            "forceModelRebuild": "force_model_rebuild",
            "reuseModalAnalysis": "reuse_modal_analysis",
            "performNFFreqRangeCheck": "perform_nf_freq_range_check",
            "requireMaterialAssignmentEnabled": "require_material_assignment_enabled",
            "modelSource": "model_source",
            "strainMapNaturalFreqs": "strain_map_natural_freqs",
        }

    def _init_freq_units(self):
        """Initialize FREQ_UNIT_LIST."""
        if self._is_connection_up():
            freq_unit_request = SherlockLifeCycleService_pb2.ListFreqUnitsRequest()
            freq_type_response = self.lifecycle.listFreqUnits(freq_unit_request)
            if freq_type_response.returnCode.value == 0:
                self.FREQ_UNIT_LIST = freq_type_response.freqUnits

    def _init_temp_units(self):
        """Initialize TEMP_UNIT_LIST."""
        if self._is_connection_up():
            temp_unit_request = SherlockLifeCycleService_pb2.ListTempUnitsRequest()
            temp_unit_response = self.lifecycle.listTempUnits(temp_unit_request)
            if temp_unit_response.returnCode.value == 0:
                self.TEMP_UNIT_LIST = temp_unit_response.tempUnits

    def _add_analyses(self, request, analyses):
        for a in analyses:
            analysis = request.analyses.add()
            analysis.type = self.ANALYSIS_TYPES[a[0].upper()]
            for p in a[1]:
                phase = analysis.phases.add()
                phase.name = p[0]
                for e in p[1]:
                    event = phase.events.add()
                    event.name = e

    def _check_analyses(self, input):
        """Check the input array if it is a valid analyses argument."""
        if not isinstance(input, list):
            raise SherlockRunAnalysisError("Invalid analyses argument")
        if len(input) == 0:
            raise SherlockRunAnalysisError("Missing one or more analyses")
        for i, analysis in enumerate(input):
            try:
                if analysis[0].upper() not in self.ANALYSIS_TYPES:
                    raise SherlockRunAnalysisError(
                        f"Invalid analysis {i}: Invalid analysis provided"
                    )
                self._check_phases(analysis[1])
            except SherlockInvalidPhaseError as e:
                raise SherlockRunAnalysisError(f"Invalid analysis {i}: {str(e)}")

    def _check_phases(self, input):
        """Check input array if its a valid phases argument."""
        if not isinstance(input, list):
            raise SherlockInvalidPhaseError("Invalid phases argument")
        for i, phase in enumerate(input):
            if phase[0] == "":
                raise SherlockInvalidPhaseError(f"Invalid phase {i}: Invalid phase name")
            if not isinstance(phase[1], list):
                raise SherlockInvalidPhaseError(f"Invalid phase {i}: Invalid events argument")
            if "" in phase[1]:
                raise SherlockInvalidPhaseError(f"Invalid phase {i}: Invalid event(s) name")

    def run_analysis(
        self,
        project,
        cca_name,
        analyses,
    ):
        """Run one or more Sherlock analysis.

        Parameters
        ----------
        project : str, required
            Sherlock project name
        cca_name : str, required
            The cca name
        analyses : (str, phases) list, required
            (AnalysisType, _) list
            AnalysisType: "UNKNOWN", "NATURALFREQ", "HARMONICVIBE", "ICTANALYSIS",
            "MECHANICALSHOCK", "RANDOMVIBE", "COMPONENTFAILUREMODE",
            "DFMEAMODULE", "PTHFATIGUE", "PARTVALIDATION", "SEMICONDUCTORWEAROUT",
            "SOLDERJOINTFATIGUE", "THERMALDERATING", "THERMALMECH"
        phases : (str, events) list
            (PhaseName, _) list
        events : (str) list
            (EventName) list
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
                ("NATURALFREQ",
                [
                    ("Phase 1", ["Harmonic Event"])
                ]
                )
            ]
        )
        """
        try:
            if project == "":
                raise SherlockRunAnalysisError(message="Invalid project name")
            if cca_name == "":
                raise SherlockRunAnalysisError(message="Invalid cca name")
            self._check_analyses(analyses)
        except SherlockRunAnalysisError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
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
                return
        except SherlockRunAnalysisError as e:
            LOG.error(str(e))
            raise e

    def get_random_vibe_input_fields(self, model_source=None):
        """Return the list of valid Random Vibe property fields based on the user configuration.

        Parameters
        ----------
        model_source : str, optional
            The model source for which to get the random vibe input fields. When not specified,
            defaults to the Generated input form. Valid values are: GENERATED, STRAIN_MAP
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
        >>> sherlock.analysis.get_random_vibe_input_fields()
        """
        if model_source is None or model_source == "GENERATED":
            model_source = SherlockAnalysisService_pb2.ModelSource.GENERATED
        elif model_source == "STRAIN_MAP":
            model_source = SherlockAnalysisService_pb2.ModelSource.STRAIN_MAP
        else:
            msg = f"Invalid model source {model_source} specified"
            LOG.error(msg)
            raise SherlockGetRandomVibeInputFieldsError(message=msg)

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
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
        """Update the properties for Random Vibe analysis.

        Parameters
        ----------
        project : str, required
            Sherlock project name
        cca_name : str, required
            The cca name
        random_vibe_damping: str, optional
            Modal Damping Ratio(s). Separate multiple float values with commas.
        natural_freq_min: double, optional
            Min Frequency. For NX Nastran analysis only.
        natural_freq_min_units: str, optional
            Min Frequency units. Valid values: "HZ", "KHZ", "MHZ", "GHZ".
            For NX Nastran analysis only.
        natural_freq_max: double, optional
            Max Frequency. For NX Nastran analysis only.
        natural_freq_max_units: str, optional
            Max Frequency units. Valid values: "HZ", "KHZ", "MHZ", "GHZ".
            For NX Nastran analysis only.
        analysis_temp: double, optional
            Temperature.
        analysis_temp_units: str, optional
            Temperature units. Valid values: "C", "F", "K".
        part_validation_enabled: bool, optional
            Part validation.
        force_model_rebuild: str, optional
            Model Creation. Valid values: "FORCE" or "AUTO".
        reuse_modal_analysis: bool, optional
            Reuse Natural Frequency. For NX Nastran analysis only.
        perform_nf_freq_range_check: bool, optional
            Frequency Range Check. For NX Nastran analysis only.
        require_material_assignment_enabled: bool, optional
            Require Material Assignment.
        model_source: str, required for strain map analysis
            Model source: Valid values: GENERATED, STRAIN_MAP
        strain_map_natural_freqs, str, required for strain map analysis
            Comma-separated list of natural frequencies for strain map analysis

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
            analysis_temp_units="C"
        )

        """
        if self.FREQ_UNIT_LIST is None:
            self._init_freq_units()
        if self.TEMP_UNIT_LIST is None:
            self._init_temp_units()
        try:
            if project == "":
                raise SherlockUpdateRandomVibePropsError(message="Invalid project name")
            if cca_name == "":
                raise SherlockUpdateRandomVibePropsError(message="Invalid cca name")
            if random_vibe_damping is not None:
                for value in random_vibe_damping.split(","):
                    try:
                        float(value.strip())
                    except ValueError:
                        raise SherlockUpdateRandomVibePropsError(
                            message="Invalid random vibe damping value: " + value.strip()
                        )
            if (
                (self.FREQ_UNIT_LIST is not None)
                and (natural_freq_min_units is not None)
                and (natural_freq_min_units not in self.FREQ_UNIT_LIST)
            ):
                raise SherlockUpdateRandomVibePropsError(
                    message="Invalid min natural freq unit specified: " + natural_freq_min_units
                )

            if (
                (self.FREQ_UNIT_LIST is not None)
                and (natural_freq_max_units is not None)
                and (natural_freq_max_units not in self.FREQ_UNIT_LIST)
            ):
                raise SherlockUpdateRandomVibePropsError(
                    message="Invalid max natural freq unit specified: " + natural_freq_max_units
                )

            if (
                (self.TEMP_UNIT_LIST is not None)
                and (analysis_temp_units is not None)
                and (analysis_temp_units not in self.TEMP_UNIT_LIST)
            ):
                raise SherlockUpdateRandomVibePropsError(
                    message="Invalid analysis temperature unit specified: " + analysis_temp_units
                )

            if model_source is None or model_source == "GENERATED":
                model_source = SherlockAnalysisService_pb2.ModelSource.GENERATED
            elif model_source == "STRAIN_MAP":
                model_source = SherlockAnalysisService_pb2.ModelSource.STRAIN_MAP
            else:
                raise SherlockUpdateRandomVibePropsError(
                    message=f"Invalid model source {model_source} specified"
                )

            if model_source == SherlockAnalysisService_pb2.ModelSource.STRAIN_MAP and (
                strain_map_natural_freqs is None or strain_map_natural_freqs == ""
            ):
                raise SherlockUpdateRandomVibePropsError(
                    message=f"No natural frequenices defined for strain map analysis"
                )

        except SherlockUpdateRandomVibePropsError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
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
                return
        except SherlockUpdateRandomVibePropsError as e:
            LOG.error(str(e))
            raise e

    def get_natural_frequency_input_fields(self):
        """Return the list of valid Natural Frequency property fields based on user configuration.

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
            LOG.error("Not connected to a gRPC service.")
            return

        message = SherlockAnalysisService_pb2.GetNaturalFrequencyInputFieldsRequest()
        response = self.stub.getNaturalFrequencyInputFields(message)
        LOG.info(self._translate_field_names(response.fieldName))

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
        """Update the properties for Natural Frequency analysis.

        Parameters
        ----------
        project : str, required
            Sherlock project name
        cca_name : str, required
            The cca name
        natural_freq_count: int
            NF Result Count.
        natural_freq_min: double
            Min Frequency.
        natural_freq_min_units: str
            Min Frequency units. Valid values: "HZ", "KHZ", "MHZ", "GHZ".
        natural_freq_max: double
            Max Frequency.
        natural_freq_max_units: str
            Max Frequency units. Valid values: "HZ", "KHZ", "MHZ", "GHZ".
        part_validation_enabled: bool
            Part validation.
        require_material_assignment_enabled: bool
            Require Material Assignment.
        analysis_temp: double, optional
            Temperature.
        analysis_temp_units: str, optional
            Temperature units. Valid values: "C", "F", "K".


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
        if self.FREQ_UNIT_LIST is None:
            self._init_freq_units()
        if self.TEMP_UNIT_LIST is None:
            self._init_temp_units()
        try:
            if project == "":
                raise SherlockUpdateNaturalFrequencyPropsError(message="Invalid project name")
            if cca_name == "":
                raise SherlockUpdateNaturalFrequencyPropsError(message="Invalid cca name")
            if (self.FREQ_UNIT_LIST is not None) and (
                natural_freq_min_units not in self.FREQ_UNIT_LIST
            ):
                raise SherlockUpdateNaturalFrequencyPropsError(
                    message="Invalid min natural freq unit specified: " + natural_freq_min_units
                )
            if (self.FREQ_UNIT_LIST is not None) and (
                natural_freq_max_units not in self.FREQ_UNIT_LIST
            ):
                raise SherlockUpdateNaturalFrequencyPropsError(
                    message="Invalid max natural freq unit specified: " + natural_freq_max_units
                )
            if (self.TEMP_UNIT_LIST is not None) and (
                analysis_temp_units not in self.TEMP_UNIT_LIST
            ):
                raise SherlockUpdateNaturalFrequencyPropsError(
                    message="Invalid analysis temperature unit specified: " + analysis_temp_units
                )
        except SherlockUpdateNaturalFrequencyPropsError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
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

        response = self.stub.updateNaturalFreqencyProps(request)

        try:
            if response.value == -1:
                raise SherlockUpdateNaturalFrequencyPropsError(response.message)
            else:
                LOG.info(response.message)
                return
        except SherlockUpdateNaturalFrequencyPropsError as e:
            LOG.error(str(e))
            raise e

    def run_strain_map_analysis(
        self,
        project,
        cca_name,
        strain_map_analyses,
    ):
        """Run one or more Sherlock strain map analysis.

        Parameters
        ----------
        project : str, required
            Sherlock project name
        cca_name : str, required
            The cca name of the main CCA for the analysis.
        analyses : List of (analysis_type, event_strain_maps), required
            analysis_type : str, required
                The type of analysis performed. Valid values are: RANDOMVIBE
            event_strain_maps : List of (phase_name, event_name, pcb_side, strain_map, \
            sub_assembly_name), required
                The strain maps assigned to the desired life cycle events for a given PCB side.
            phase_name : str, required
                Life cycle phase name for the strain map assignment.
            event_name : str, required
                Life cycle event name for the strain map assignment.
            pcb_side : str, required
                PCB side for the strain map. Valid values are: TOP, BOTTOM
            strain_map : str, required
                The name of the strain map assigned to the life cycle event.
            sub_assembly_name : str, optional
                The name of the sub-assembly CCA to be assigned the strain map.
        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> analysis.run_strain_map_analysis(
                "AssemblyTutorial",
                "Main Board",
                [[
                    "RANDOMVIBE",
                    [["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                     ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                     ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"]],
                ]]
            )
        """
        try:
            if project == "":
                raise SherlockRunStrainMapAnalysisError(message="Invalid project name specified")

            if cca_name == "":
                raise SherlockRunStrainMapAnalysisError(message="Invalid CCA name specified")

            if not isinstance(strain_map_analyses, list):
                raise SherlockRunStrainMapAnalysisError("Invalid analyses argument")

            if len(strain_map_analyses) == 0:
                raise SherlockRunStrainMapAnalysisError("Missing one or more analyses")

            request = SherlockAnalysisService_pb2.RunStrainMapAnalysisRequest(
                project=project,
                ccaName=cca_name,
            )

            for i, analysis in enumerate(strain_map_analyses):
                if not isinstance(analysis, list):
                    raise SherlockRunStrainMapAnalysisError(
                        f"Invalid analysis argument for strain map analysis {i}"
                    )

                if len(analysis) != 2:
                    raise SherlockRunStrainMapAnalysisError(
                        f"Wrong number of args {str(len(analysis))} for strain map analysis {i}"
                    )

                analysis_type = analysis[0].upper()
                if analysis_type == "":
                    raise SherlockRunStrainMapAnalysisError(
                        f"Missing analysis type for strain map analysis {i}"
                    )
                elif analysis_type == "RANDOMVIBE":
                    analysis_type = (
                        SherlockAnalysisService_pb2.RunStrainMapAnalysisRequest.StrainMapAnalysis.AnalysisType.RandomVibe  # noqa: E501
                    )
                else:
                    raise SherlockRunStrainMapAnalysisError(
                        f"Invalid analysis type {analysis_type} for strain map analysis {i}"
                    )

                strain_map_analysis_request = request.strainMapAnalyses.add()
                strain_map_analysis_request.type = analysis_type

                if len(analysis[1]) == 0:
                    raise SherlockRunStrainMapAnalysisError(
                        f"Missing one or more event strain maps for strain map analysis {i}"
                    )

                for j, event_strain_map in enumerate(analysis[1]):
                    if not isinstance(event_strain_map, list):
                        raise SherlockRunStrainMapAnalysisError(
                            f"Invalid event strain map argument for strain map analysis {i}"
                        )
                    elif len(event_strain_map) < 4:
                        raise SherlockRunStrainMapAnalysisError(
                            f"Wrong number of args {str(len(event_strain_map))} for event strain "
                            f"map {j} for strain map analysis {i}"
                        )
                    elif event_strain_map[0] == "":
                        raise SherlockRunStrainMapAnalysisError(
                            f"Missing life phase for event strain map {j} for strain "
                            f"map analysis {i}"
                        )
                    elif event_strain_map[1] == "":
                        raise SherlockRunStrainMapAnalysisError(
                            f"Missing event name for event strain map {j} for strain "
                            f"map analysis {i}"
                        )
                    elif event_strain_map[2] == "":
                        raise SherlockRunStrainMapAnalysisError(
                            f"Missing PCB side for event strain map {j} for strain map analysis {i}"
                        )
                    elif event_strain_map[3] == "":
                        raise SherlockRunStrainMapAnalysisError(
                            f"Missing strain map name for event strain map {j} for strain "
                            f"map analysis {i}"
                        )

                    event_strain_map_request = strain_map_analysis_request.eventStrainMaps.add()
                    event_strain_map_request.phaseName = event_strain_map[0]
                    event_strain_map_request.eventName = event_strain_map[1]
                    event_strain_map_request.pcbSide = event_strain_map[2]
                    event_strain_map_request.strainMap = event_strain_map[3]

                    if len(event_strain_map) == 5:
                        event_strain_map_request.subAssemblyName = event_strain_map[4]

            if not self._is_connection_up():
                LOG.error("Not connected to a gRPC service.")
                return

            response = self.stub.runStrainMapAnalysis(request)

            if response.value == -1:
                if response.message == "":
                    raise SherlockRunStrainMapAnalysisError(error_array=response.errors)

                raise SherlockRunStrainMapAnalysisError(message=response.message)

        except SherlockRunStrainMapAnalysisError as e:
            LOG.error(str(e))
            raise e
