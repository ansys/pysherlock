# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

"""Module containing all analysis capabilities."""
from typing import Optional

import grpc

from ansys.sherlock.core.types.analysis_types import (
    ElementOrder,
    ModelSource,
    RunAnalysisRequestAnalysisType,
    RunStrainMapAnalysisRequestAnalysisType,
    UpdatePcbModelingPropsRequestAnalysisType,
    UpdatePcbModelingPropsRequestPcbMaterialModel,
    UpdatePcbModelingPropsRequestPcbModelType,
)

try:
    import SherlockAnalysisService_pb2
    import SherlockAnalysisService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2
    from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import (
    SherlockGetPartsListValidationAnalysisPropsError,
    SherlockNoGrpcConnectionException,
    SherlockRunAnalysisError,
    SherlockRunStrainMapAnalysisError,
    SherlockUpdateHarmonicVibePropsError,
    SherlockUpdateICTAnalysisPropsError,
    SherlockUpdateMechanicalShockPropsError,
    SherlockUpdateNaturalFrequencyPropsError,
    SherlockUpdatePartListValidationAnalysisPropsError,
    SherlockUpdatePartModelingPropsError,
    SherlockUpdatePcbModelingPropsError,
    SherlockUpdateRandomVibePropsError,
    SherlockUpdateSolderFatiguePropsError,
)
from ansys.sherlock.core.grpc_stub import GrpcStub
from ansys.sherlock.core.utils.version_check import require_version


class Analysis(GrpcStub):
    """Contains all analysis capabilities."""

    def __init__(self, channel: grpc.Channel, server_version: int):
        """Initialize a gRPC stub for the Sherlock Analysis service."""
        super().__init__(channel, server_version)
        self.stub = SherlockAnalysisService_pb2_grpc.SherlockAnalysisServiceStub(channel)
        self.FIELD_NAMES = {
            "analysisTemp": "analysis_temp",
            "analysisTemp (optional)": "analysis_temp",
            "analysisTempUnits": "analysis_temp_units",
            "analysisTempUnits (optional)": "analysis_temp_units",
            "criticalStrainShock": "critical_strain_shock",
            "criticalStrainShockUnits": "critical_strain_shock_units",
            "filterByEventFrequency": "filter_by_event_frequency",
            "forceModelRebuild": "force_model_rebuild",
            "harmonicVibeDamping": "harmonic_vibe_damping",
            "harmonicVibeCount": "harmonic_vibe_count",
            "ictApplicationTime": "ict_application_time",
            "ictApplicationTimeUnits": "ict_application_time_units",
            "ictNumberOfEvents": "ict_number_of_events",
            "ictResultCount": "ict_result_count",
            "modelSource": "model_source",
            "naturalFreqCount": "natural_freq_count",
            "naturalFreqMin": "natural_freq_min",
            "naturalFreqMinUnits": "natural_freq_min_units",
            "naturalFreqMax": "natural_freq_max",
            "naturalFreqMaxUnits": "natural_freq_max_units",
            "partTemp": "part_temp",
            "partTempUnits": "part_temp_units",
            "partValidationEnabled": "part_validation_enabled",
            "performNFFreqRangeCheck": "perform_nf_freq_range_check",
            "randomVibeDamping": "random_vibe_damping",
            "requireMaterialAssignmentEnabled": "require_material_assignment_enabled",
            "reuseModalAnalysis": "reuse_modal_analysis",
            "shockResultCount": "shock_result_count",
            "solderMaterial": "solder_material",
            "strainMapNaturalFreqs": "strain_map_natural_freqs",
            "usePartTempRiseMin": "use_part_temp_rise_min",
        }

    def _translate_field_names(self, names_list: list[str]) -> list[str]:
        names = []
        for name in list(names_list):
            names.append(self.FIELD_NAMES.get(name))

        return names

    @staticmethod
    def _add_analyses(
        request: SherlockAnalysisService_pb2.RunAnalysisRequest,
        analyses: list[tuple[RunAnalysisRequestAnalysisType, tuple[str, str]]],
    ):
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

    @require_version()
    def run_analysis(
        self,
        project: str,
        cca_name: str,
        analyses: list[tuple[RunAnalysisRequestAnalysisType, tuple[str, str]]],
    ) -> int:
        """Run one or more Sherlock analyses.

        Available Since: 2021R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        analyses: list of ``elements``

            - elements: list[tuple[RunAnalysisRequestAnalysisType, tuple[str, str]]]
                Tuples (``type``, ``event``)

                - analysis_type: RunAnalysisRequestAnalysisType
                    Type of analysis to run.

                - event: list[tuple[str, str]]
                    Tuples (``phase_name``, ``event_name``)

                    - phase_name: str
                        Name of the life cycle phase.
                    - event_name: str
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
                (RunAnalysisRequestAnalysisType.NATURAL_FREQ,
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
            raise SherlockNoGrpcConnectionException()

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

    @require_version()
    def get_harmonic_vibe_input_fields(
        self, model_source: Optional[ModelSource] = None
    ) -> list[str]:
        """Get harmonic vibe property fields based on the user configuration.

        Available Since: 2024R1

        Parameters
        ----------
        model_source: ModelSource, optional
            Model source to get the harmonic vibe property fields from.
            The default is ``None``.

        Returns
        -------
        list[str]
            Harmonic vibe property fields based on the user configuration.

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
        >>> sherlock.analysis.get_harmonic_vibe_input_fields(ModelSource.GENERATED)
        """
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        message = SherlockAnalysisService_pb2.GetHarmonicVibeInputFieldsRequest(
            modelSource=model_source
        )
        response = self.stub.getHarmonicVibeInputFields(message)

        fields = self._translate_field_names(response.fieldName)
        return fields

    @require_version()
    def update_harmonic_vibe_props(
        self,
        project: str,
        harmonic_vibe_properties: list[dict[str, bool | int | float | str]],
    ) -> int:
        """Update properties for a harmonic vibe analysis.

        Available Since: 2024R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        harmonic_vibe_properties: list[dict[str, bool | int | float | str]]
            Harmonic vibe properties for a CCA consisting of these properties:

            - cca_name: str
                Name of the CCA.
            - model_source: ModelSource
                Model source. The default is ``None``.
            - harmonic_vibe_count: int
                Number of harmonic vibe result layers to generate. The default is ``None``.
            - harmonic_vibe_damping: str
                One or more modal damping ratios. The default is ``None``.
                Separate multiple float values with commas.
            - part_validation_enabled: bool
                Whether to enable part validation. The default is ``None``.
            - require_material_assignment_enabled: bool
                Whether to require material assignment. The default is ``None``.
            - analysis_temp: float
                Temperature. The default is ``None``.
            - analysis_temp_units: str
                Temperature units. The default is ``None``.
                Options are ``"C"``, ``"F"``, and ``"K"``.
            - force_model_rebuild: str
                How to handle rebuilding of the model. The default is ``None``.
                Options are ``"FORCE"`` and ``"AUTO"``.
            - filter_by_event_frequency: bool
                Indicates if harmonic results outside analysis event range are included.
                This parameter is not used for NX Nastran analysis.
            - natural_freq_min: int
                Minimum frequency. The default is ``None``.
                This parameter is for NX Nastran analysis only.
            - natural_freq_min_units: str
                Minimum frequency units. The default is ``None``.
                Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
                This parameter is for NX Nastran analysis only.
            - natural_freq_max: int
                Maximum frequency. The default is ``None``.
                This parameter is for NX Nastran analysis only.
            - natural_freq_max_units: str
                Maximum frequency units. The default is ``None``.
                Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
                This parameter is for NX Nastran analysis only.
            - reuse_modal_analysis: bool
                Whether to reuse the natural frequency for modal analysis. The
                default is ``None``. This parameter is for NX Nastran analysis only.
            - strain_map_natural_freq: double
                Natural frequency for strain map analysis.

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
        >>> sherlock.analysis.update_harmonic_vibe_props(
            "Test",
            [{
                "cca_name": "Card",
                "model_source": ModelSource.GENERATED,
                "harmonic_vibe_count": 2,
                "harmonic_vibe_damping": "0.01, 0.05",
                "part_validation_enabled": False,
                "require_material_assignment_enabled": False,
                "analysis_temp": 20,
                "analysis_temp_units": "C",
                "force_model_rebuild": "AUTO",
                "filter_by_event_frequency": False,
                "natural_freq_min": 10,
                "natural_freq_min_units": "Hz",
                "natural_freq_max": 1000,
                "natural_freq_max_units": "KHz",
                "reuse_modal_analysis": True,
                "strain_map_natural_freq": 100.13,
            },
            ]
        )

        """
        try:
            if project == "":
                raise SherlockUpdateHarmonicVibePropsError(message="Project name is invalid.")

            if not isinstance(harmonic_vibe_properties, list):
                raise SherlockUpdateHarmonicVibePropsError(
                    message="Harmonic vibe properties argument is invalid."
                )

            if len(harmonic_vibe_properties) == 0:
                raise SherlockUpdateHarmonicVibePropsError(
                    message="One or more harmonic vibe properties are required."
                )

            request = SherlockAnalysisService_pb2.UpdateHarmonicVibePropsRequest(project=project)

            self._set_update_harmonic_vibe_props_request_properties(
                request, harmonic_vibe_properties
            )
        except SherlockUpdateHarmonicVibePropsError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        response = self.stub.updateHarmonicVibeProps(request)

        try:
            if response.value == -1:
                raise SherlockUpdateHarmonicVibePropsError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockUpdateHarmonicVibePropsError as e:
            LOG.error(str(e))
            raise e

    @staticmethod
    def _set_update_harmonic_vibe_props_request_properties(request, harmonic_vibe_properties):
        for i, harmonic_vibe_props in enumerate(harmonic_vibe_properties):
            if not isinstance(harmonic_vibe_props, dict):
                raise SherlockUpdateHarmonicVibePropsError(
                    f"Harmonic vibe props argument is invalid for harmonic vibe properties {i}."
                )

            if "cca_name" not in harmonic_vibe_props.keys():
                raise SherlockUpdateHarmonicVibePropsError(
                    message=f"CCA name is missing for harmonic vibe properties {i}."
                )

            cca_name = harmonic_vibe_props["cca_name"]
            if cca_name == "":
                raise SherlockUpdateHarmonicVibePropsError(
                    message=f"CCA name is invalid for harmonic vibe properties {i}."
                )

            if "model_source" in harmonic_vibe_props.keys():
                model_source = harmonic_vibe_props["model_source"]
            else:
                model_source = None

            if "harmonic_vibe_count" in harmonic_vibe_props.keys():
                harmonic_vibe_count = harmonic_vibe_props["harmonic_vibe_count"]
            else:
                harmonic_vibe_count = None

            if "harmonic_vibe_damping" in harmonic_vibe_props.keys():
                harmonic_vibe_damping = harmonic_vibe_props["harmonic_vibe_damping"]
                if harmonic_vibe_damping is not None:
                    for value in harmonic_vibe_damping.split(","):
                        try:
                            float(value.strip())
                        except ValueError:
                            raise SherlockUpdateHarmonicVibePropsError(
                                message=f"Harmonic vibe damping value is invalid"
                                f" for harmonic vibe properties {i}: " + value.strip()
                            )
            else:
                harmonic_vibe_damping = None

            if "part_validation_enabled" in harmonic_vibe_props.keys():
                part_validation_enabled = harmonic_vibe_props["part_validation_enabled"]
            else:
                part_validation_enabled = None

            if "require_material_assignment_enabled" in harmonic_vibe_props.keys():
                require_material_assignment_enabled = harmonic_vibe_props[
                    "require_material_assignment_enabled"
                ]
            else:
                require_material_assignment_enabled = None

            if "analysis_temp" in harmonic_vibe_props.keys():
                analysis_temp = harmonic_vibe_props["analysis_temp"]
            else:
                analysis_temp = None

            if "analysis_temp_units" in harmonic_vibe_props.keys():
                analysis_temp_units = harmonic_vibe_props["analysis_temp_units"]
            else:
                analysis_temp_units = None

            if "force_model_rebuild" in harmonic_vibe_props.keys():
                force_model_rebuild = harmonic_vibe_props["force_model_rebuild"]
            else:
                force_model_rebuild = None

            if "filter_by_event_frequency" in harmonic_vibe_props.keys():
                filter_by_event_frequency = harmonic_vibe_props["filter_by_event_frequency"]
            else:
                filter_by_event_frequency = None

            if "natural_freq_min" in harmonic_vibe_props.keys():
                natural_freq_min = harmonic_vibe_props["natural_freq_min"]
            else:
                natural_freq_min = None

            if "natural_freq_min_units" in harmonic_vibe_props.keys():
                natural_freq_min_units = harmonic_vibe_props["natural_freq_min_units"]
            else:
                natural_freq_min_units = None

            if "natural_freq_max" in harmonic_vibe_props.keys():
                natural_freq_max = harmonic_vibe_props["natural_freq_max"]
            else:
                natural_freq_max = None

            if "natural_freq_max_units" in harmonic_vibe_props.keys():
                natural_freq_max_units = harmonic_vibe_props["natural_freq_max_units"]
            else:
                natural_freq_max_units = None

            if "reuse_modal_analysis" in harmonic_vibe_props.keys():
                reuse_modal_analysis = harmonic_vibe_props["reuse_modal_analysis"]
            else:
                reuse_modal_analysis = None

            if "strain_map_natural_freq" in harmonic_vibe_props.keys():
                strain_map_natural_freq = harmonic_vibe_props["strain_map_natural_freq"]
            else:
                strain_map_natural_freq = None

            props_request = request.harmonicVibeProperties.add()
            props_request.ccaName = cca_name

            if model_source is not None:
                props_request.modelSource = model_source

            if harmonic_vibe_count is not None:
                props_request.harmonicVibeCount = harmonic_vibe_count

            if harmonic_vibe_damping is not None:
                props_request.harmonicVibeDamping = harmonic_vibe_damping

            if part_validation_enabled is not None:
                props_request.partValidationEnabled = part_validation_enabled

            if require_material_assignment_enabled is not None:
                props_request.requireMaterialAssignmentEnabled = require_material_assignment_enabled

            if analysis_temp is not None:
                props_request.analysisTemp = analysis_temp

            if analysis_temp_units is not None:
                props_request.analysisTempUnits = analysis_temp_units

            if force_model_rebuild is not None:
                props_request.forceModelRebuild = force_model_rebuild

            if filter_by_event_frequency is not None:
                props_request.filterByEventFrequency = filter_by_event_frequency

            if natural_freq_min is not None:
                props_request.naturalFreqMin = natural_freq_min

            if natural_freq_min_units is not None:
                props_request.naturalFreqMinUnits = natural_freq_min_units

            if natural_freq_max is not None:
                props_request.naturalFreqMax = natural_freq_max

            if natural_freq_max_units is not None:
                props_request.naturalFreqMaxUnits = natural_freq_max_units

            if reuse_modal_analysis is not None:
                props_request.reuseModalAnalysis = reuse_modal_analysis

            if strain_map_natural_freq is not None:
                props_request.strainMapNaturalFreq = strain_map_natural_freq

    @require_version(241)
    def get_ict_analysis_input_fields(self) -> list[str]:
        """Get ICT analysis property fields based on the user configuration.

        Available Since: 2024R1

        Returns
        -------
        list[str]
            ICT analysis property fields based on the user configuration.
            ``None`` if not connected to Sherlock.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> sherlock = launch_sherlock()
        >>> sherlock.analysis.get_ict_analysis_input_fields()
        """
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        message = SherlockAnalysisService_pb2.GetICTAnalysisInputFieldsRequest()
        response = self.stub.getICTAnalysisInputFields(message)

        fields = self._translate_field_names(response.fieldName)
        LOG.info(fields)

        return fields

    @require_version(241)
    def update_ict_analysis_props(
        self,
        project: str,
        ict_analysis_properties: list[dict[str, bool | float | int | str]],
    ) -> int:
        """Update properties for an ICT analysis.

        Available Since: 2024R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        ict_analysis_properties: list[dict[str, bool | float | int | str]]
            ICT analysis properties for a CCA consisting of these properties:

            - cca_name: str
                Name of the CCA.
            - ict_application_time: float
                Specifies the amount of time to complete one ICT event.
            - ict_application_time_units: str
                Application time units.
                Options are ``"ms"``, ``"sec"``, ``"min"``, ``"hr"``, ``"day"``, ``"year"``.
            - ict_number_of_events: int
                Specifies the number of events to apply to the application time when computing
                the time to failure for a component.
            - part_validation_enabled: bool
                Whether to enable part validation. The default is ``None``.
            - require_material_assignment_enabled: bool
                Whether to require material assignment. The default is ``None``.
            - ict_result_count: int
                The number of ICT result layers to generate. This parameter is for use with
                thermal analysis.

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
        >>> sherlock.analysis.update_ict_analysis_props(
            "Test",
            [{
                "cca_name": "Card",
                "ict_application_time": 2,
                "ict_application_time_units": "sec",
                "ict_number_of_events": 10,
                "part_validation_enabled": False,
                "require_material_assignment_enabled": False,
            },
            ]
        )

        """
        try:
            if project == "":
                raise SherlockUpdateICTAnalysisPropsError(message="Project name is invalid.")

            if not isinstance(ict_analysis_properties, list):
                raise SherlockUpdateICTAnalysisPropsError(
                    message="ICT analysis properties argument is invalid."
                )

            if len(ict_analysis_properties) == 0:
                raise SherlockUpdateICTAnalysisPropsError(
                    message="One or more ICT analysis properties are required."
                )

            request = SherlockAnalysisService_pb2.UpdateICTAnalysisPropsRequest(project=project)

            for i, ict_analysis_props in enumerate(ict_analysis_properties):
                if not isinstance(ict_analysis_props, dict):
                    raise SherlockUpdateICTAnalysisPropsError(
                        f"ICT analysis props argument is invalid for ICT analysis properties {i}."
                    )

                if "cca_name" not in ict_analysis_props.keys():
                    raise SherlockUpdateICTAnalysisPropsError(
                        message=f"CCA name is missing for ICT analysis properties {i}."
                    )

                cca_name = ict_analysis_props["cca_name"]
                if cca_name == "":
                    raise SherlockUpdateICTAnalysisPropsError(
                        message=f"CCA name is invalid for ICT analysis properties {i}."
                    )

                props_request = request.ictAnalysisProperties.add()
                props_request.ccaName = cca_name

                if "ict_analysis_count" in ict_analysis_props.keys():
                    props_request.ictAnalysisCount = ict_analysis_props["ict_analysis_count"]

                if "ict_application_time" in ict_analysis_props.keys():
                    props_request.applicationTime = ict_analysis_props["ict_application_time"]

                if "ict_application_time_units" in ict_analysis_props.keys():
                    props_request.applicationTimeUnits = ict_analysis_props[
                        "ict_application_time_units"
                    ]

                if "ict_number_of_events" in ict_analysis_props.keys():
                    props_request.numberOfEvents = ict_analysis_props["ict_number_of_events"]

                if "part_validation_enabled" in ict_analysis_props.keys():
                    props_request.partValidationEnabled = ict_analysis_props[
                        "part_validation_enabled"
                    ]

                if "require_material_assignment_enabled" in ict_analysis_props.keys():
                    props_request.requireMaterialAssignmentEnabled = ict_analysis_props[
                        "require_material_assignment_enabled"
                    ]

                if "force_model_rebuild" in ict_analysis_props.keys():
                    props_request.forceModelRebuild = ict_analysis_props["force_model_rebuild"]

        except SherlockUpdateICTAnalysisPropsError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        response = self.stub.updateICTAnalysisProps(request)

        try:
            if response.value == -1:
                raise SherlockUpdateICTAnalysisPropsError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockUpdateICTAnalysisPropsError as e:
            LOG.error(str(e))
            raise e

    @require_version(241)
    def get_mechanical_shock_input_fields(
        self, model_source: Optional[ModelSource] = None
    ) -> list[str]:
        """Get mechanical shock property fields based on the user configuration.

        Available Since: 2024R1

        Parameters
        ----------
        model_source: ModelSource, optional
            Model source to get the random vibe property fields from.
            Only GENERATED is supported.
            Default is ``None``.

        Returns
        -------
        list[str]
            Mechanical shock property fields based on the user configuration.

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
        >>> sherlock.analysis.get_mechanical_shock_input_fields(ModelSource.GENERATED)
        """
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        message = SherlockAnalysisService_pb2.GetMechanicalShockInputFieldsRequest(
            modelSource=model_source
        )
        response = self.stub.getMechanicalShockInputFields(message)

        fields = self._translate_field_names(response.fieldName)
        LOG.info(fields)

        return fields

    @require_version(241)
    def update_mechanical_shock_props(
        self,
        project: str,
        mechanical_shock_properties: list[dict[str, bool | float | int | str]],
    ) -> int:
        """Update properties for a mechanical shock analysis.

        Available Since: 2024R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        mechanical_shock_properties: list[dict[str, bool | float | int | str]]
            Mechanical shock properties for a CCA consisting of these properties:

            - cca_name: str
                Name of the CCA.
            - model_source: ModelSource, optional
                Model source. The default is ``None``.
            - shock_result_count : int
                Number of mechanical shock result layers to generate.
            - critical_shock_strain: float
                Critical shock strain. The default is ``None``.
            - critical_shock_strain_units: str
                Critical shock strain units. The default is ``None``.
                Options are ``"strain"``, ``"ε"``, and ``"µε"``.
            - part_validation_enabled: bool
                Whether to enable part validation. The default is ``None``.
            - require_material_assignment_enabled: bool
                Whether to require material assignment. The default is ``None``.
            - force_model_rebuild: str
                How to handle rebuilding of the model. The default is ``None``.
                Options are ``"FORCE"`` and ``"AUTO"``.
            - natural_freq_min: int
                Minimum frequency. The default is ``None``.
            - natural_freq_min_units: str
                Minimum frequency units. The default is ``None``.
                Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            - natural_freq_max: int
                Maximum frequency. The default is ``None``.
            - natural_freq_max_units: str
                Maximum frequency units. The default is ``None``.
                Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            - analysis_temp: float
                Temperature. The default is ``None``.
            - analysis_temp_units: str
                Temperature units. The default is ``None``.
                Options are ``"C"``, ``"F"``, and ``"K"``.

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
        >>> sherlock.analysis.update_mechanical_shock_props(
            "Test",
            [{
                "cca_name": "Card",
                "model_source": ModelSource.GENERATED,
                "shock_result_count": 2,
                "critical_shock_strain": 10,
                "critical_shock_strain_units": "strain",
                "part_validation_enabled": True,
                "require_material_assignment_enabled": False,
                "force_model_rebuild": "AUTO",
                "natural_freq_min": 10,
                "natural_freq_min_units": "Hz",
                "natural_freq_max": 100,
                "natural_freq_max_units": "KHz",
                "analysis_temp": 20,
                "analysis_temp_units": "F",
            },
            ]
        )

        """
        try:
            if project == "":
                raise SherlockUpdateMechanicalShockPropsError(message="Project name is invalid.")

            if not isinstance(mechanical_shock_properties, list):
                raise SherlockUpdateMechanicalShockPropsError(
                    message="Mechanical shock properties argument is invalid."
                )

            if len(mechanical_shock_properties) == 0:
                raise SherlockUpdateMechanicalShockPropsError(
                    message="One or more mechanical shock properties are required."
                )

            request = SherlockAnalysisService_pb2.UpdateMechanicalShockPropsRequest(project=project)

            for i, mechanical_shock_props in enumerate(mechanical_shock_properties):
                if not isinstance(mechanical_shock_props, dict):
                    raise SherlockUpdateMechanicalShockPropsError(
                        f"Mechanical shock props argument is "
                        f"invalid for mechanical shock properties {i}."
                    )

                if "cca_name" not in mechanical_shock_props.keys():
                    raise SherlockUpdateMechanicalShockPropsError(
                        message=f"CCA name is missing for mechanical shock properties {i}."
                    )

                cca_name = mechanical_shock_props["cca_name"]
                if cca_name == "":
                    raise SherlockUpdateMechanicalShockPropsError(
                        message=f"CCA name is invalid for mechanical shock properties {i}."
                    )

                model_source = mechanical_shock_props.get("model_source", None)
                shock_result_count = mechanical_shock_props.get("shock_result_count", None)
                critical_shock_strain = mechanical_shock_props.get("critical_shock_strain", None)
                critical_shock_strain_units = mechanical_shock_props.get(
                    "critical_shock_strain_units", None
                )
                part_validation_enabled = mechanical_shock_props.get(
                    "part_validation_enabled", None
                )
                require_material_assignment_enabled = mechanical_shock_props.get(
                    "require_material_assignment_enabled", None
                )
                force_model_rebuild = mechanical_shock_props.get("force_model_rebuild", None)
                natural_freq_min = mechanical_shock_props.get("natural_freq_min", None)
                natural_freq_min_units = mechanical_shock_props.get("natural_freq_min_units", None)
                natural_freq_max = mechanical_shock_props.get("natural_freq_max", None)
                natural_freq_max_units = mechanical_shock_props.get("natural_freq_max_units", None)
                analysis_temp = mechanical_shock_props.get("analysis_temp", None)
                analysis_temp_units = mechanical_shock_props.get("analysis_temp_units", None)

                props_request = request.mechanicalShockProperties.add()
                props_request.ccaName = cca_name
                props_request.modelSource = model_source

                if shock_result_count is not None:
                    props_request.shockResultCount = shock_result_count

                if critical_shock_strain is not None:
                    props_request.criticalShockStrain = critical_shock_strain

                if critical_shock_strain_units is not None:
                    props_request.criticalShockStrainUnits = critical_shock_strain_units

                if part_validation_enabled is not None:
                    props_request.partValidationEnabled = part_validation_enabled

                if require_material_assignment_enabled is not None:
                    props_request.requireMaterialAssignmentEnabled = (
                        require_material_assignment_enabled
                    )

                if force_model_rebuild is not None:
                    props_request.forceModelRebuild = force_model_rebuild

                if natural_freq_min is not None:
                    props_request.naturalFreqMin = natural_freq_min

                if natural_freq_min_units is not None:
                    props_request.naturalFreqMinUnits = natural_freq_min_units

                if natural_freq_max is not None:
                    props_request.naturalFreqMax = natural_freq_max

                if natural_freq_max_units is not None:
                    props_request.naturalFreqMaxUnits = natural_freq_max_units

                if analysis_temp is not None:
                    props_request.analysisTemp = analysis_temp

                if analysis_temp_units is not None:
                    props_request.analysisTempUnits = analysis_temp_units

        except SherlockUpdateMechanicalShockPropsError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        response = self.stub.updateMechanicalShockProps(request)

        try:
            if response.value == -1:
                raise SherlockUpdateMechanicalShockPropsError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockUpdateMechanicalShockPropsError as e:
            LOG.error(str(e))
            raise e

    @require_version(241)
    def get_solder_fatigue_input_fields(self) -> list[str]:
        """Get solder fatigue property fields based on the user configuration.

        Available Since: 2024R1

        Returns
        -------
        list[str]
            Solder fatigue property fields based on the user configuration.

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
        >>> sherlock.analysis.get_solder_fatigue_input_fields()
        """
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        message = SherlockAnalysisService_pb2.GetSolderFatigueInputFieldsRequest()
        response = self.stub.getSolderFatigueInputFields(message)

        fields = self._translate_field_names(response.fieldName)
        return fields

    @require_version(241)
    def update_solder_fatigue_props(
        self,
        project: str,
        solder_fatigue_properties: list[dict[str, bool | float | str]],
    ) -> int:
        """Update properties for a solder fatigue analysis.

        Available Since: 2024R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        solder_fatigue_properties: list[dict[str, bool | float | str]]
            Mechanical shock properties for a CCA consisting of these properties:

            - cca_name: str
                Name of the CCA.
            - solder_material: str
                Solder material. The default is ``None``.
            - part_temp: float
                Part temperature. The default is ``None``.
            - part_temp_units: str
                Part temperature units. The default is ``None``.
            - use_part_temp_rise_min: bool
                whether to apply min temp rise. The default is ``None``.
            - part_validation_enabled: bool
                Whether to enable part validation. The default is ``None``.

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
        >>> sherlock.analysis.update_solder_fatigue_props(
            "Test",
            [{
                "cca_name": "Card",
                "solder_material": "TIN-LEAD (63SN37PB)",
                "part_temp": 70,
                "part_temp_units": "F",
                "use_part_temp_rise_min": True,
                "part_validation_enabled": True
            },
            ]
        )

        """
        try:
            if project == "":
                raise SherlockUpdateSolderFatiguePropsError(message="Project name is invalid.")

            if not isinstance(solder_fatigue_properties, list):
                raise SherlockUpdateSolderFatiguePropsError(
                    message="Solder fatigue properties argument is invalid."
                )

            if len(solder_fatigue_properties) == 0:
                raise SherlockUpdateSolderFatiguePropsError(
                    message="One or more solder fatigue properties are required."
                )

            request = SherlockAnalysisService_pb2.UpdateSolderFatiguePropsRequest(project=project)

            for i, solder_fatigue_props in enumerate(solder_fatigue_properties):
                if not isinstance(solder_fatigue_props, dict):
                    raise SherlockUpdateSolderFatiguePropsError(
                        f"Solder fatigue props argument is invalid "
                        f"for solder fatigue properties {i}."
                    )

                if "cca_name" not in solder_fatigue_props.keys():
                    raise SherlockUpdateSolderFatiguePropsError(
                        message=f"CCA name is missing for solder fatigue properties {i}."
                    )

                cca_name = solder_fatigue_props["cca_name"]
                if cca_name == "":
                    raise SherlockUpdateSolderFatiguePropsError(
                        message=f"CCA name is invalid for solder fatigue properties {i}."
                    )

                solder_material = solder_fatigue_props.get("solder_material", None)
                part_temp = solder_fatigue_props.get("part_temp", None)
                part_temp_units = solder_fatigue_props.get("part_temp_units", None)
                use_part_temp_rise_min = solder_fatigue_props.get("use_part_temp_rise_min", None)
                part_validation_enabled = solder_fatigue_props.get("part_validation_enabled", None)

                props_request = request.solderFatigueProperties.add()
                props_request.ccaName = cca_name

                if solder_material is not None:
                    props_request.solderMaterial = solder_material

                if part_temp is not None:
                    props_request.partTemp = part_temp

                if part_temp_units is not None:
                    props_request.partTempUnits = part_temp_units

                if use_part_temp_rise_min is not None:
                    props_request.partTempRiseMinEnabled = use_part_temp_rise_min

                if part_validation_enabled is not None:
                    props_request.partValidationEnabled = part_validation_enabled

        except SherlockUpdateSolderFatiguePropsError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        response = self.stub.updateSolderFatigueProps(request)

        try:
            if response.value == -1:
                raise SherlockUpdateSolderFatiguePropsError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockUpdateSolderFatiguePropsError as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def get_random_vibe_input_fields(self, model_source: Optional[ModelSource] = None) -> list[str]:
        """Get random vibe property fields based on the user configuration.

        Available Since: 2023R2

        Parameters
        ----------
        model_source: ModelSource, optional
            Model source to get the random vibe property fields from.
            The default is ``None``.

        Returns
        -------
        list[str]
            Random vibe input field property names based on the user configuration.

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
        >>> sherlock.analysis.get_random_vibe_input_fields(ModelSource.STRAIN_MAP)
        """
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        message = SherlockAnalysisService_pb2.GetRandomVibeInputFieldsRequest(
            modelSource=model_source
        )
        response = self.stub.getRandomVibeInputFields(message)

        fields = self._translate_field_names(response.fieldName)
        return fields

    @require_version()
    def update_random_vibe_props(
        self,
        project: str,
        cca_name: str,
        random_vibe_damping: Optional[str] = None,
        natural_freq_min: Optional[float] = None,
        natural_freq_min_units: Optional[str] = None,
        natural_freq_max: Optional[float] = None,
        natural_freq_max_units: Optional[str] = None,
        analysis_temp: Optional[float] = None,
        analysis_temp_units: Optional[str] = None,
        part_validation_enabled: Optional[bool] = None,
        force_model_rebuild: Optional[str] = None,
        reuse_modal_analysis: Optional[bool] = None,
        perform_nf_freq_range_check: Optional[bool] = None,
        require_material_assignment_enabled: Optional[bool] = None,
        model_source: Optional[ModelSource] = None,
        strain_map_natural_freqs: Optional[str] = None,
    ) -> int:
        """Update properties for a random vibe analysis.

        Available Since: 2024R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        random_vibe_damping: str, optional
            One or more modal damping ratios. The default is ``None``.
            Separate multiple float values with commas.
        natural_freq_min: float, optional
            Minimum frequency. The default is ``None``.
            This parameter is for NX Nastran analysis only.
        natural_freq_min_units: str, optional
            Minimum frequency units. The default is ``None``.
            Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            This parameter is for NX Nastran analysis only.
        natural_freq_max: float, optional
            Maximum frequency. The default is ``None``.
            This parameter is for NX Nastran analysis only.
        natural_freq_max_units: str, optional
            Maximum frequency units. The default is ``None``.
            Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            This parameter is for NX Nastran analysis only.
        analysis_temp: float, optional
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
            Model source. The default is ``None``.
            This parameter is required for strain map analysis.
        strain_map_natural_freqs: str, optional
            Comma-separated list of natural frequencies. The default is ``None``.
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
            model_source=ModelSource.STRAIN_MAP
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
            raise SherlockNoGrpcConnectionException()

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

    @require_version()
    def get_natural_frequency_input_fields(self) -> list[str]:
        """Get natural frequency property fields based on the user configuration.

        Available Since: 2023R2

        Returns
        -------
        list[str]
            Matural frequency property fields based on the user configuration.

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
            >>> sherlock.analysis.get_natural_frequency_input_fields()
        """
        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        message = SherlockAnalysisService_pb2.GetNaturalFrequencyInputFieldsRequest()
        response = self.stub.getNaturalFrequencyInputFields(message)

        fields = self._translate_field_names(response.fieldName)
        return fields

    @require_version()
    def update_natural_frequency_props(
        self,
        project: str,
        cca_name: str,
        natural_freq_count: int,
        natural_freq_min: int,
        natural_freq_min_units: str,
        natural_freq_max: int,
        natural_freq_max_units: str,
        part_validation_enabled: bool,
        require_material_assignment_enabled: bool,
        analysis_temp: Optional[float] = None,
        analysis_temp_units: Optional[str] = None,
    ) -> int:
        """Update properties for a natural frequency analysis.

        Available Since:2023R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.
        natural_freq_count: int
            Natural frequency result count.
        natural_freq_min: int, optional
            Minimum frequency. This parameter is for NX Nastran analysis only.
        natural_freq_min_units: str, optional
            Minimum frequency units. Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            This parameter is for NX Nastran analysis only.
        natural_freq_max: int, optional
            Maximum frequency. This parameter is for NX Nastran analysis only.
        natural_freq_max_units: str, optional
            Maximum frequency units. Options are ``"HZ"``, ``"KHZ"``, ``"MHZ"``, and ``"GHZ"``.
            This parameter is for NX Nastran analysis only.
        part_validation_enabled: bool
            Whether part validation is enabled.
        require_material_assignment_enabled: bool
            Whether to require material assignment.
        analysis_temp: float, optional
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
            raise SherlockNoGrpcConnectionException()

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

    @require_version()
    def run_strain_map_analysis(
        self,
        project: str,
        cca_name: str,
        strain_map_analyses: list[list[RunStrainMapAnalysisRequestAnalysisType | list[list[str]]]],
    ) -> int:
        """Run one or more strain map analyses.

        Available Since: 2023R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the main CCA for the analysis.
        strain_map_analyses: list[list[RunStrainMapAnalysisRequestAnalysisType | list[list[str]]]]
            Analyses consisting of these properties:

            - analysis_type: RunStrainMapAnalysisRequestAnalysisType
                Type of analysis to run.
            - event_strain_maps: list
                Strain maps assigned to the desired life cycle events for
                a given PCB side. The list consists of these properties:

              - phase_name: str
                  Life cycle phase name for the strain map assignment.
              - event_name: str
                  Life cycle event name for the strain map assignment.
              - pcb_side: str
                  PCB side for the strain map. Options are ``"TOP"`` and ``"BOTTOM"``.
              - strain_map: str
                  Name of the strain map assigned to the life cycle event.
              - sub_assembly_name: str, optional
                  Name of the subassembly CCA to assign the strain map to.

        Returns
        -------
        int
            Status code of the response. 0 for success.

        Examples
        --------
        >>> from ansys.sherlock.core.launcher import launch_sherlock
        >>> from ansys.sherlock.core.types.analysis_types import (
        >>>     RunStrainMapAnalysisRequestAnalysisType
        >>> )
        >>> sherlock = launch_sherlock()
        >>> analysis_request = SherlockAnalysisService_pb2.RunStrainMapAnalysisRequest
        >>> sherlock.analysis.run_strain_map_analysis(
                "AssemblyTutorial",
                "Main Board",
                [[
                    RunStrainMapAnalysisRequestAnalysisType.RANDOM_VIBE,
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
        except SherlockRunStrainMapAnalysisError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        response = self.stub.runStrainMapAnalysis(request)

        try:
            if response.value == -1:
                raise SherlockRunStrainMapAnalysisError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockRunStrainMapAnalysisError as e:
            LOG.error(str(e))
            raise e

    @require_version()
    def update_pcb_modeling_props(
        self,
        project: str,
        cca_names: list[str],
        analyses: list[
            tuple[
                bool
                | float
                | str
                | UpdatePcbModelingPropsRequestAnalysisType
                | UpdatePcbModelingPropsRequestPcbModelType
                | UpdatePcbModelingPropsRequestPcbMaterialModel
                | ElementOrder,
                ...,
            ]
        ],
    ) -> int:
        """Update FEA PCB Modeling properties for one or more CCAs.

        Available Since: 2023R2

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_names: list
            Names of the CCAs to be used for the analysis.
        analyses: list[tuple[bool | float | str | UpdatePcbModelingPropsRequestAnalysisType\
                | UpdatePcbModelingPropsRequestPcbModelType\
                | UpdatePcbModelingPropsRequestPcbMaterialModel\
                | ElementOrder, ...]]
            Elements consisting of the following properties:

            - analysis_type: UpdatePcbModelingPropsRequestAnalysisType
                Type of analysis applied.
            - pcb_model_type: UpdatePcbModelingPropsRequestPcbModelType
                The PCB modeling mesh type.
            - modeling_region_enabled: bool
                Indicates if modeling regions are enabled.
            - pcb_material_model: UpdatePcbModelingPropsRequestPcbMaterialModel
                The PCB modeling PCB model type.
            - pcb_max_materials: Optional[int]
                The number of PCB materials for Uniform Elements and Layered Elements PCB model
                types. Not applicable if PCB model is Uniform or Layered.
            - pcb_elem_order: ElementOrder
                The element order for PCB elements.
            - pcb_max_edge_length: float
                The maximum mesh size for PCB elements.
            - pcb_max_edge_length_units: str
                The length units for the maximum mesh size.
            - pcb_max_vertical: float
                The maximum vertical mesh size for PCB elements.
            - pcb_max_vertical_units: str
                The length units for the maximum vertical mesh size.
            - quads_preferred: bool
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
                    UpdatePcbModelingPropsRequestAnalysisType.HARMONIC_VIBE,
                    UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                    True,
                    UpdatePcbModelingPropsRequestPcbMaterialModel.UNIFORM,
                    ElementOrder.SOLID_SHELL,
                    6,
                    "mm",
                    3,
                    "mm",
                    True,
                )
            ]
        )
        """
        try:
            if project == "":
                raise SherlockUpdatePcbModelingPropsError(message="Project name is invalid.")
            if not cca_names:
                raise SherlockUpdatePcbModelingPropsError(message="CCA names are invalid.")
            if not analyses:
                raise SherlockUpdatePcbModelingPropsError(message="Analysis input(s) are invalid.")
        except SherlockUpdatePcbModelingPropsError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        request = SherlockAnalysisService_pb2.UpdatePcbModelingPropsRequest(
            project=project,
            ccaNames=cca_names,
        )

        """Add PCB Modeling Props to Request"""
        _analysis = SherlockAnalysisService_pb2.UpdatePcbModelingPropsRequest.Analysis
        uniform = _analysis.PcbMaterialModel.Uniform
        layered = _analysis.PcbMaterialModel.Layered

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

        try:
            if response.value == -1:
                raise SherlockUpdatePcbModelingPropsError(response.message)
            return response.value
        except SherlockUpdatePcbModelingPropsError as e:
            LOG.error(str(e))
            raise e

    @require_version(241)
    def update_part_modeling_props(
        self, project: str, part_modeling_props: dict[str, bool | float | str]
    ) -> int:
        """Update part modeling properties for a given project's CCA.

        Available Since: 2024R1

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        part_modeling_props: dict[str, bool | float | str]
            Part modeling properties for a CCA consisting of these properties:

            - cca_name: str
                Name of the CCA.
            - part_enabled: bool
                Whether to enable part modeling. All other fields are ignored if disabled.
            - part_min_size: float, optional
                Minimum part size.
            - part_min_size_units: str, optional
                Minimum part size units.
            - part_elem_order: str, optional
                Part element order.
                Options are ``"First Order (Linear)"``, ``"Second Order (Quadratic)"``,
                or ``"Solid Shell"``.
            - part_max_edge_length: float, optional
                Part max edge length.
            - part_max_edge_length_units: str, optional
                Part max edge length units.
            - part_max_vertical: float, optional
                Part max vertical.
            - part_max_vertical_units: str, optional
                Part max vertical units.
            - part_results_filtered: bool, optional
                Whether to enable filtered part results.

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
        >>> sherlock.analysis.update_part_modeling_props(
            "Test",
            {
                "cca_name": "Card",
                "part_enabled": True,
                "part_min_size": 1,
                "part_min_size_units": "in",
                "part_elem_order": "First Order (Linear)",
                "part_max_edge_length": 1,
                "part_max_edge_length_units": "in",
                "part_max_vertical": 1,
                "part_max_vertical_units": "in",
                "part_results_filtered": True
            }
        )

        """
        try:
            if project == "":
                raise SherlockUpdatePartModelingPropsError(message="Project name is invalid.")

            if not isinstance(part_modeling_props, dict):
                raise SherlockUpdatePartModelingPropsError(
                    message="Part modeling props argument is invalid."
                )

            if "cca_name" not in part_modeling_props.keys():
                raise SherlockUpdatePartModelingPropsError(message="CCA name is missing.")
            if "part_enabled" not in part_modeling_props.keys():
                raise SherlockUpdatePartModelingPropsError(message="Part enabled is missing.")

            request = SherlockAnalysisService_pb2.UpdatePartModelingRequest(project=project)
            request.ccaName = part_modeling_props["cca_name"]

            if request.ccaName == "":
                raise SherlockUpdatePartModelingPropsError(message="CCA name is invalid.")

            request.partEnabled = part_modeling_props["part_enabled"]

            if request.partEnabled:
                if "part_min_size" in part_modeling_props.keys():
                    request.partMinSize = part_modeling_props["part_min_size"]
                if "part_min_size_units" in part_modeling_props.keys():
                    request.partMinSizeUnits = part_modeling_props["part_min_size_units"]
                if "part_elem_order" in part_modeling_props.keys():
                    request.partElemOrder = part_modeling_props["part_elem_order"]
                if "part_max_edge_length" in part_modeling_props.keys():
                    request.partMaxEdgeLength = part_modeling_props["part_max_edge_length"]
                if "part_max_edge_length_units" in part_modeling_props.keys():
                    request.partMaxEdgeLengthUnits = part_modeling_props[
                        "part_max_edge_length_units"
                    ]
                if "part_max_vertical" in part_modeling_props.keys():
                    request.partMaxVertical = part_modeling_props["part_max_vertical"]
                if "part_max_vertical_units" in part_modeling_props.keys():
                    request.partMaxVerticalUnits = part_modeling_props["part_max_vertical_units"]
                if "part_results_filtered" in part_modeling_props.keys():
                    request.partResultsFiltered = part_modeling_props["part_results_filtered"]

        except SherlockUpdatePartModelingPropsError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        response = self.stub.updatePartModelingProperties(request)

        try:
            if response.value == -1:
                raise SherlockUpdatePartModelingPropsError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockUpdatePartModelingPropsError as e:
            LOG.error(str(e))
            raise e

    @require_version(251)
    def update_part_list_validation_analysis_props(
        self,
        project: str,
        properties_per_cca: list[dict[str, bool | str]],
    ) -> int:
        """Update properties for a Part List Validation analysis.

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        properties_per_cca: list[dict[str, bool | str]]
            Part List Validation analysis properties for each CCA consisting of these properties:

            - cca_name: str
                Name of the CCA.
            - process_use_avl: bool
                Whether to use AVL.
            - process_use_wizard: bool
                Whether to use the wizard.
            - process_check_confirmed_properties: bool
                Whether to check confirmed properties.
            - process_check_part_numbers: bool
                Whether to check part numbers.
            - matching_mode: str
                Matching type.
            - avl_require_internal_part_number: bool
                Whether to require an internal part number.
            - avl_require_approved_description: bool
                Whether to require an approved description.
            - avl_require_approved_manufacturer: bool
                Whether to require an approved manufacturer.

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
        >>> sherlock.analysis.update_part_list_validation_analysis_props(
            "Test",
            [{
                "cca_name": "Card",
                "process_use_avl": True,
                "process_use_wizard": False,
                "process_check_confirmed_properties": True,
                "process_check_part_numbers": True,
                "matching_mode": "Part",
                "avl_require_internal_part_number": True,
                "avl_require_approved_description": False,
                "avl_require_approved_manufacturer": True,
            },
            ]
        )
        """
        try:
            if not isinstance(properties_per_cca, list):
                raise SherlockUpdatePartListValidationAnalysisPropsError(
                    message="Properties per CCA argument is invalid."
                )

            if len(properties_per_cca) == 0:
                raise SherlockUpdatePartListValidationAnalysisPropsError(
                    message="One or more analysis properties are required."
                )

            request = SherlockAnalysisService_pb2.UpdatePartsListValidationPropsRequest(
                project=project
            )

            for i, analysis_properties in enumerate(properties_per_cca):
                if not isinstance(analysis_properties, dict):
                    raise SherlockUpdatePartListValidationAnalysisPropsError(
                        f"Analysis properties is invalid for index {i}."
                    )

                if "cca_name" not in analysis_properties.keys():
                    raise SherlockUpdatePartListValidationAnalysisPropsError(
                        message=f"CCA name is missing for analysis properties {i}."
                    )

                cca_name = analysis_properties["cca_name"]
                if cca_name == "":
                    raise SherlockUpdatePartListValidationAnalysisPropsError(
                        message=f"CCA name is invalid for analysis properties {i}."
                    )

                request.partsListValidationProperties.add(
                    ccaName=cca_name,
                    processUseAVL=analysis_properties.get("process_use_avl", False),
                    processUseWizard=analysis_properties.get("process_use_wizard", False),
                    processCheckConfirmedProperties=analysis_properties.get(
                        "process_check_confirmed_properties", False
                    ),
                    processCheckPartNumbers=analysis_properties.get(
                        "process_check_part_numbers", False
                    ),
                    matching=analysis_properties.get("matching_mode", "Both"),
                    avlRequireInternalPartNumber=analysis_properties.get(
                        "avl_require_internal_part_number", False
                    ),
                    avlRequireApprovedDescription=analysis_properties.get(
                        "avl_require_approved_description", False
                    ),
                    avlRequireApprovedManufacturer=analysis_properties.get(
                        "avl_require_approved_manufacturer", False
                    ),
                )
        except SherlockUpdatePartListValidationAnalysisPropsError as e:
            LOG.error(str(e))
            raise e

        if not self._is_connection_up():
            raise SherlockNoGrpcConnectionException()

        response = self.stub.updatePartsListValidationProps(request)

        try:
            if response.value == -1:
                raise SherlockUpdatePartListValidationAnalysisPropsError(response.message)
            else:
                LOG.info(response.message)
                return response.value
        except SherlockUpdatePartListValidationAnalysisPropsError as e:
            LOG.error(str(e))
            raise e

    @require_version(251)
    def get_parts_list_validation_analysis_props(
        self,
        project: str,
        cca_name: str,
    ) -> SherlockAnalysisService_pb2.PartsListValidationPropsResponse:
        """Get properties for a Part List Validation analysis.

        Parameters
        ----------
        project: str
            Name of the Sherlock project.
        cca_name: str
            Name of the CCA.

        Returns
        -------
        PartsListValidationPropsResponse
            - returnCode: ReturnCode
                - value: int
                    Status code of the response. 0 for success.
                - message: str
                    indicates general errors that occurred while attempting to update parts
            - partLibrary: str
                Part library name
            - processUseAVL: bool
                Process option to use AVL
            - processUseWizard: bool
                Process option to use wizard
            - processCheckConfirmedProperties: bool
                Process option to check confirmed properties
            - processCheckPartNumbers: bool
                Process option to check part numbers
            - matching: MatchingMode
                Matching type
            - avlRequireInternalPartNumber: bool
                AVL option to require internal part number
            - avlRequireApprovedDescription: bool
                AVL option to require approved description
            - avlRequireApprovedManufacturer: bool
                AVL option to require approved manufacturer

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
        >>> analysis_props = sherlock.analysis.get_parts_list_validation_analysis_props(
            "Test", "Card"
        )
        """
        try:
            if project == "":
                raise SherlockGetPartsListValidationAnalysisPropsError(
                    message="Project name is invalid."
                )
            if cca_name == "":
                raise SherlockGetPartsListValidationAnalysisPropsError(
                    message="CCA name is invalid."
                )

            request = SherlockAnalysisService_pb2.GetPartsListValidationPropsRequest(
                project=project, ccaName=cca_name
            )

            if not self._is_connection_up():
                raise SherlockNoGrpcConnectionException()

            response = self.stub.getPartsListValidationProps(request)

            return_code = response.returnCode

            if return_code.value == -1:
                raise SherlockGetPartsListValidationAnalysisPropsError(return_code.message)

            return response
        except SherlockGetPartsListValidationAnalysisPropsError as e:
            LOG.error(str(e))
            raise e
