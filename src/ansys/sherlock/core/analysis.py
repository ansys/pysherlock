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
from ansys.sherlock.core.errors import SherlockInvalidPhaseError, SherlockRunAnalysisError, \
    SherlockUpdateRandomVibePropsError
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

    def get_random_vibe_input_fields(self):
        """Returns the list of valid Random Vibe property fields based on the user configuration.

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

        if not self._is_connection_up():
            LOG.error("Not connected to a gRPC service.")
            return

        message = SherlockAnalysisService_pb2.GetRandomVibeInputFieldsRequest()
        response = self.stub.getRandomVibeInputFields(message)

        # translates from Java gRPC field names to Python field names
        field_names = {"randomVibeDamping": "random_vibe_damping",
                       "naturalFreqMin": "natural_freq_min",
                       "naturalFreqMinUnits": "natural_freq_min_units",
                       "naturalFreqMax": "natural_freq_max",
                       "naturalFreqMaxUnits": "natural_freq_max_units",
                       "analysisTemp": "analysis_temp",
                       "analysisTempUnits": "analysis_temp_units",
                       "partValidationEnabled": "part_validation_enabled",
                       "forceModelRebuild": "force_model_rebuild",
                       "reuseModalAnalysis": "reuse_modal_analysis",
                       "performNFFreqRangeCheck": "perform_nf_freq_range_check",
                       "requireMaterialAssignmentEnabled": "require_material_assignment_enabled"
                       }

        LOG.info(self._translate_random_vibe_field_names(response.fieldName))

    def _translate_random_vibe_field_names(self, names_list):
        # translates from Java gRPC field names to Python field names
        field_names = {"randomVibeDamping": "random_vibe_damping",
                       "naturalFreqMin": "natural_freq_min",
                       "naturalFreqMinUnits": "natural_freq_min_units",
                       "naturalFreqMax": "natural_freq_max",
                       "naturalFreqMaxUnits": "natural_freq_max_units",
                       "analysisTemp": "analysis_temp",
                       "analysisTempUnits": "analysis_temp_units",
                       "partValidationEnabled": "part_validation_enabled",
                       "forceModelRebuild": "force_model_rebuild",
                       "reuseModalAnalysis": "reuse_modal_analysis",
                       "performNFFreqRangeCheck": "perform_nf_freq_range_check",
                       "requireMaterialAssignmentEnabled": "require_material_assignment_enabled"
                       }
        names = ""
        for name in list(names_list):
            names = names + '\n' + field_names.get(name)

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
            require_material_assignment_enabled=None
    ):
        """Updates the properties for Random Vibe analysis.

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
                for value in random_vibe_damping.split(','):
                    try:
                        float(value.strip())
                    except ValueError:
                        raise SherlockUpdateRandomVibePropsError(
                            message="Invalid random vibe damping value: " +
                                    value.strip())
            if (self.FREQ_UNIT_LIST is not None) and \
                    (natural_freq_min_units not in self.FREQ_UNIT_LIST):
                raise SherlockUpdateRandomVibePropsError(
                    message="Invalid min natural freq unit specified: " +
                            natural_freq_min_units)
            if (self.FREQ_UNIT_LIST is not None) and \
                    (natural_freq_max_units not in self.FREQ_UNIT_LIST):
                raise SherlockUpdateRandomVibePropsError(
                    message="Invalid max natural freq unit specified: " +
                            natural_freq_max_units)
            if (self.TEMP_UNIT_LIST is not None) and \
                    (analysis_temp_units not in self.TEMP_UNIT_LIST):
                raise SherlockUpdateRandomVibePropsError(
                    message="Invalid analysis temperature unit specified: " +
                            analysis_temp_units)
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
            requireMaterialAssignmentEnabled=require_material_assignment_enabled
        )

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