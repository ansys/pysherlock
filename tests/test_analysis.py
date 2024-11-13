# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

try:
    import SherlockAnalysisService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2

from unittest.mock import Mock

import grpc
import pytest

from ansys.sherlock.core.analysis import Analysis
from ansys.sherlock.core.errors import (
    SherlockGetPartsListValidationAnalysisPropsError,
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
from ansys.sherlock.core.types.analysis_types import (
    ElementOrder,
    ModelSource,
    RunAnalysisRequestAnalysisType,
    UpdatePcbModelingPropsRequestAnalysisType,
    UpdatePcbModelingPropsRequestPcbMaterialModel,
    UpdatePcbModelingPropsRequestPcbModelType,
)
from ansys.sherlock.core.utils.version_check import SKIP_VERSION_CHECK


def test_all():
    """Test all life cycle APIs."""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    analysis = Analysis(channel, SKIP_VERSION_CHECK)
    helper_test_run_analysis(analysis)
    helper_test_run_strain_map_analysis(analysis)
    helper_test_get_harmonic_vibe_input_fields(analysis)
    helper_test_get_ict_analysis_input_fields(analysis)
    helper_test_get_mechanical_shock_input_fields(analysis)
    helper_test_get_solder_fatigue_input_fields(analysis)
    helper_test_get_random_vibe_input_fields(analysis)
    helper_test_translate_field_names(analysis)
    helper_test_update_harmonic_vibe_props(analysis)
    helper_test_set_update_harmonic_vibe_props_request_properties(analysis)
    helper_test_update_ict_analysis_props(analysis)
    helper_test_update_mechanical_shock_props(analysis)
    helper_test_update_solder_fatigue_props(analysis)
    helper_test_update_random_vibe_props(analysis)
    helper_test_get_natural_frequency_input_fields(analysis)
    helper_test_update_natural_frequency_props(analysis)
    helper_test_update_pcb_modeling_props(analysis)
    helper_test_update_part_modeling_props(analysis)
    helper_test_update_parts_list_validation_props(analysis)
    helper_test_get_parts_list_validation_analysis_props(analysis)


def helper_test_run_analysis(analysis):
    """Test run_analysis API."""
    natural_frequency_analysis_type = RunAnalysisRequestAnalysisType.NATURAL_FREQ

    if analysis._is_connection_up():
        try:
            analysis.run_analysis(
                "AssemblyTutorial",
                "Invalid CCA",
                [(natural_frequency_analysis_type, [("Phase 1", ["Harmonic Vibe"])])],
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockRunAnalysisError

        try:
            result = analysis.run_analysis(
                "AssemblyTutorial",
                "Main Board",
                [(natural_frequency_analysis_type, [("Phase 1", ["Harmonic Vibe"])])],
            )
            assert result == 0
        except SherlockRunAnalysisError as e:
            pytest.fail(e.message)

    try:
        analysis.run_analysis(
            "", "Main Board", [(natural_frequency_analysis_type, [("Phase 1", ["Harmonic Vibe"])])]
        ),
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Project name is invalid."

    try:
        analysis.run_analysis(
            "AssemblyTutorial",
            "",
            [(natural_frequency_analysis_type, [("Phase 1", ["Harmonic Vibe"])])],
        ),
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: CCA name is invalid."

    try:
        analysis.run_analysis("AssemblyTutorial", "Main Board", "Not a list")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Analyses argument is invalid."

    try:
        analysis.run_analysis("Test", "Card", [])
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: One or more analyses are missing."


def helper_test_run_strain_map_analysis(analysis):
    """Test run_strain_map_analysis API."""
    analysis_type_enum = (
        SherlockAnalysisService_pb2.RunStrainMapAnalysisRequest.StrainMapAnalysis.AnalysisType
    )
    random_vibe_analysis_type = analysis_type_enum.RandomVibe
    if analysis._is_connection_up():
        try:
            analysis.run_strain_map_analysis(
                "AssemblyTutorial",
                "Invalid CCA",
                [
                    [
                        random_vibe_analysis_type,
                        [
                            ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                            ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                            [
                                "Phase 1",
                                "Random Vibe",
                                "TOP",
                                "MemoryCard1Strain",
                                "Memory Card 1",
                            ],
                        ],
                    ]
                ],
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockRunStrainMapAnalysisError

        try:
            result = analysis.run_strain_map_analysis(
                "AssemblyTutorial",
                "Main Board",
                [
                    [
                        random_vibe_analysis_type,
                        [
                            ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                            ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                            [
                                "Phase 1",
                                "Random Vibe",
                                "TOP",
                                "MemoryCard1Strain",
                                "Memory Card 1",
                            ],
                        ],
                    ]
                ],
            )
            assert result == 0
        except SherlockRunStrainMapAnalysisError as e:
            pytest.fail(e.message)

        try:
            result = analysis.run_strain_map_analysis(
                "AssemblyTutorial",
                "Main Board",
                [
                    [
                        analysis_type_enum.HarmonicVibe,
                        [
                            ["Phase 1", "Harmonic Vibe", "TOP", "MainBoardStrain - Top"],
                            ["Phase 1", "Harmonic Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                            [
                                "Phase 1",
                                "Harmonic Vibe",
                                "TOP",
                                "MemoryCard1Strain",
                                "Memory Card 1",
                            ],
                        ],
                    ]
                ],
            )
            assert result == 0
        except SherlockRunStrainMapAnalysisError as e:
            pytest.fail(e.message)

    try:
        analysis.run_strain_map_analysis(
            "",
            "Main Board",
            [
                [
                    random_vibe_analysis_type,
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert str(e) == "Run strain map analysis error: Project name is invalid."

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "",
            [
                [
                    random_vibe_analysis_type,
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert str(e) == "Run strain map analysis error: CCA name is invalid."

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            "Invalid analyses",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert str(e) == "Run strain map analysis error: Analyses argument is invalid."

    try:
        analyses = []
        analysis.run_strain_map_analysis("AssemblyTutorial", "Main Board", analyses)
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert str(e) == "Run strain map analysis error: One or more analyses are missing."

    try:
        analyses = ["INVALID"]
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            analyses,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Analyses argument is invalid for strain "
            "map analysis 0."
        )

    try:
        analyses = [["INVALID"]]
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            analyses,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e)
            == "Run strain map analysis error: Number of elements (1) is wrong for strain map "
            "analysis 0."
        )

    try:
        analysis_type = ""
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    analysis_type,
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Analysis type is missing for strain map "
            "analysis 0."
        )

    try:
        event_strain_maps = []
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    random_vibe_analysis_type,
                    event_strain_maps,
                ]
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: One or more event strain maps are "
            "missing for strain map analysis 0."
        )

    try:
        event_strain_maps = ["INVALID"]
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    random_vibe_analysis_type,
                    event_strain_maps,
                ]
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Event strain maps argument is invalid for "
            "strain map analysis 0."
        )

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    random_vibe_analysis_type,
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Number of elements (3) is wrong for event "
            "strain map 1 for strain map analysis 0."
        )

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    random_vibe_analysis_type,
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Life phase is missing for event strain map 1 "
            "for strain map analysis 0."
        )

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    random_vibe_analysis_type,
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Event name is missing for event strain map 2 "
            "for strain map analysis 0."
        )

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    random_vibe_analysis_type,
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ],
                [
                    random_vibe_analysis_type,
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ],
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e)
            == "Run strain map analysis error: PCB side is missing for event strain map 2 for "
            "strain map analysis 1."
        )

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    random_vibe_analysis_type,
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "", "Memory Card 1"],
                    ],
                ]
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Strain map name is missing for event strain "
            "map 2 for strain map analysis 0."
        )


def helper_test_get_harmonic_vibe_input_fields(analysis):
    if analysis._is_connection_up():
        fields = analysis.get_harmonic_vibe_input_fields()
        assert "harmonic_vibe_count" in fields
        assert "harmonic_vibe_damping" in fields
        assert "part_validation_enabled" in fields
        assert "require_material_assignment_enabled" in fields
        assert "model_source" not in fields

        fields = analysis.get_harmonic_vibe_input_fields(ModelSource.GENERATED)
        assert "harmonic_vibe_count" in fields
        assert "harmonic_vibe_damping" in fields
        assert "model_source" in fields
        assert "part_validation_enabled" in fields
        assert "require_material_assignment_enabled" in fields


def helper_test_get_ict_analysis_input_fields(analysis):
    if analysis._is_connection_up():
        fields = analysis.get_ict_analysis_input_fields()
        assert "ict_application_time" in fields
        assert "ict_application_time_units" in fields
        assert "ict_number_of_events" in fields
        assert "require_material_assignment_enabled" in fields
        assert "model_source" not in fields


def helper_test_get_mechanical_shock_input_fields(analysis):
    if analysis._is_connection_up():
        fields = analysis.get_mechanical_shock_input_fields()
        assert "shock_result_count" in fields
        assert "critical_strain_shock" in fields
        assert "critical_strain_shock_units" in fields
        assert "part_validation_enabled" in fields
        assert "require_material_assignment_enabled" in fields
        assert "natural_freq_min" in fields
        assert "natural_freq_min_units" in fields
        assert "natural_freq_max" in fields
        assert "natural_freq_max_units" in fields
        assert "model_source" not in fields

        fields = analysis.get_mechanical_shock_input_fields(ModelSource.GENERATED)
        assert "shock_result_count" in fields
        assert "critical_strain_shock" in fields
        assert "critical_strain_shock_units" in fields
        assert "model_source" in fields
        assert "part_validation_enabled" in fields
        assert "require_material_assignment_enabled" in fields
        assert "natural_freq_min" in fields
        assert "natural_freq_min_units" in fields
        assert "natural_freq_max" in fields
        assert "natural_freq_max_units" in fields


def helper_test_get_solder_fatigue_input_fields(analysis):
    if analysis._is_connection_up():
        fields = analysis.get_solder_fatigue_input_fields()
        assert "solder_material" in fields
        assert "part_temp" in fields
        assert "part_temp_units" in fields
        assert "use_part_temp_rise_min" in fields
        assert "part_validation_enabled" in fields


def helper_test_get_random_vibe_input_fields(analysis):
    if analysis._is_connection_up():
        fields = analysis.get_random_vibe_input_fields()
        assert "part_validation_enabled" in fields
        assert "random_vibe_damping" in fields
        assert "require_material_assignment_enabled" in fields
        assert "model_source" not in fields

        fields = analysis.get_random_vibe_input_fields(ModelSource.GENERATED)
        assert "model_source" in fields
        assert "part_validation_enabled" in fields
        assert "random_vibe_damping" in fields
        assert "require_material_assignment_enabled" in fields

        fields = analysis.get_random_vibe_input_fields(ModelSource.STRAIN_MAP)
        assert "model_source" in fields
        assert "part_validation_enabled" in fields
        assert "random_vibe_damping" in fields
        assert "require_material_assignment_enabled" in fields
        assert "strain_map_natural_freqs" in fields


def helper_test_translate_field_names(analysis):
    """Test translating the analysis field names."""

    results = analysis._translate_field_names(
        [
            "analysisTemp",
            "analysisTemp (optional)",
            "analysisTempUnits",
            "analysisTempUnits (optional)",
            "filterByEventFrequency",
            "forceModelRebuild",
            "harmonicVibeDamping",
            "harmonicVibeCount",
            "ictApplicationTime",
            "ictApplicationTimeUnits",
            "ictNumberOfEvents",
            "ictResultCount",
            "modelSource",
            "naturalFreqCount",
            "naturalFreqMin",
            "naturalFreqMinUnits",
            "naturalFreqMax",
            "naturalFreqMaxUnits",
            "partValidationEnabled",
            "performNFFreqRangeCheck",
            "randomVibeDamping",
            "requireMaterialAssignmentEnabled",
            "reuseModalAnalysis",
            "strainMapNaturalFreqs",
        ]
    )

    expected = [
        "analysis_temp",
        "analysis_temp",
        "analysis_temp_units",
        "analysis_temp_units",
        "filter_by_event_frequency",
        "force_model_rebuild",
        "harmonic_vibe_damping",
        "harmonic_vibe_count",
        "ict_application_time",
        "ict_application_time_units",
        "ict_number_of_events",
        "ict_result_count",
        "model_source",
        "natural_freq_count",
        "natural_freq_min",
        "natural_freq_min_units",
        "natural_freq_max",
        "natural_freq_max_units",
        "part_validation_enabled",
        "perform_nf_freq_range_check",
        "random_vibe_damping",
        "require_material_assignment_enabled",
        "reuse_modal_analysis",
        "strain_map_natural_freqs",
    ]

    assert results == expected


def helper_test_update_harmonic_vibe_props(analysis):
    try:
        analysis.update_harmonic_vibe_props(
            "",
            [
                {
                    "cca_name": "Card",
                    "model_source": ModelSource.STRAIN_MAP,
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
                    "natural_freq_max_units": "Hz",
                    "reuse_modal_analysis": False,
                    "strain_map_natural_freq": 100.13,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateHarmonicVibePropsError as e:
        assert str(e) == "Update harmonic vibe properties error: Project name is invalid."

    try:
        analysis.update_harmonic_vibe_props("Test", "Card")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateHarmonicVibePropsError as e:
        assert (
            str(e) == "Update harmonic vibe properties error: "
            "Harmonic vibe properties argument is invalid."
        )

    try:
        analysis.update_harmonic_vibe_props("Test", [])
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateHarmonicVibePropsError as e:
        assert (
            str(e) == "Update harmonic vibe properties error: "
            "One or more harmonic vibe properties are required."
        )

    try:
        analysis.update_harmonic_vibe_props("Test", ["Card"])
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateHarmonicVibePropsError as e:
        assert (
            str(e) == "Update harmonic vibe properties error: "
            "Harmonic vibe props argument is invalid for harmonic vibe properties 0."
        )

    try:
        analysis.update_harmonic_vibe_props(
            "Test",
            [
                {
                    "model_source": ModelSource.STRAIN_MAP,
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
                    "natural_freq_max_units": "Hz",
                    "reuse_modal_analysis": False,
                    "strain_map_natural_freq": 100.13,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateHarmonicVibePropsError as e:
        assert (
            str(e) == "Update harmonic vibe properties error: "
            "CCA name is missing for harmonic vibe properties 0."
        )

    try:
        analysis.update_harmonic_vibe_props(
            "Test",
            [
                {
                    "cca_name": "",
                    "model_source": ModelSource.STRAIN_MAP,
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
                    "natural_freq_max_units": "Hz",
                    "reuse_modal_analysis": False,
                    "strain_map_natural_freq": 100.13,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateHarmonicVibePropsError as e:
        assert (
            str(e) == "Update harmonic vibe properties error: "
            "CCA name is invalid for harmonic vibe properties 0."
        )

    try:
        analysis.update_harmonic_vibe_props(
            "Test",
            [
                {
                    "cca_name": "Card",
                    "model_source": ModelSource.STRAIN_MAP,
                    "harmonic_vibe_count": 2,
                    "harmonic_vibe_damping": "0.01, foo",
                    "part_validation_enabled": False,
                    "require_material_assignment_enabled": False,
                    "analysis_temp": 20,
                    "analysis_temp_units": "C",
                    "force_model_rebuild": "AUTO",
                    "filter_by_event_frequency": False,
                    "natural_freq_min": 10,
                    "natural_freq_min_units": "Hz",
                    "natural_freq_max": 1000,
                    "natural_freq_max_units": "Hz",
                    "reuse_modal_analysis": False,
                    "strain_map_natural_freq": 100.13,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateHarmonicVibePropsError as e:
        assert (
            str(e) == "Update harmonic vibe properties error: "
            "Harmonic vibe damping value is invalid for harmonic vibe properties 0: foo"
        )

    if analysis._is_connection_up():
        try:
            analysis.update_harmonic_vibe_props(
                "Tutorial Project",
                [
                    {
                        "cca_name": "Main Board",
                        "model_source": ModelSource.STRAIN_MAP,
                        "harmonic_vibe_count": 2,
                        "harmonic_vibe_damping": "0.01, 0.02",
                        "part_validation_enabled": False,
                        "require_material_assignment_enabled": False,
                        "analysis_temp": 20,
                        "analysis_temp_units": "foo",
                        "force_model_rebuild": "AUTO",
                        "filter_by_event_frequency": False,
                        "natural_freq_min": 10,
                        "natural_freq_min_units": "Hz",
                        "natural_freq_max": 1000,
                        "natural_freq_max_units": "Hz",
                        "reuse_modal_analysis": False,
                        "strain_map_natural_freq": 100.13,
                    },
                ],
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdateHarmonicVibePropsError

        try:
            result = analysis.update_harmonic_vibe_props(
                "Tutorial Project",
                [
                    {
                        "cca_name": "Main Board",
                        "model_source": ModelSource.STRAIN_MAP,
                        "harmonic_vibe_count": 4,
                        "harmonic_vibe_damping": "0.015, 0.025",
                        "part_validation_enabled": True,
                        "require_material_assignment_enabled": True,
                        "analysis_temp": 30,
                        "analysis_temp_units": "F",
                        "force_model_rebuild": "FORCE",
                        "filter_by_event_frequency": True,
                        "natural_freq_min": 50,
                        "natural_freq_min_units": "Hz",
                        "natural_freq_max": 1000,
                        "natural_freq_max_units": "Hz",
                        "reuse_modal_analysis": True,
                        "strain_map_natural_freq": 222.45,
                    },
                ],
            )
            assert result == 0
        except SherlockUpdateHarmonicVibePropsError as e:
            pytest.fail(str(e))


def helper_test_set_update_harmonic_vibe_props_request_properties(analysis):
    properties = [
        {
            "cca_name": "Main Board",
            "model_source": ModelSource.STRAIN_MAP,
            "harmonic_vibe_count": 4,
            "harmonic_vibe_damping": "0.015, 0.025",
            "part_validation_enabled": True,
            "require_material_assignment_enabled": True,
            "analysis_temp": 30,
            "analysis_temp_units": "F",
            "force_model_rebuild": "FORCE",
            "filter_by_event_frequency": True,
            "natural_freq_min": 50,
            "natural_freq_min_units": "Hz",
            "natural_freq_max": 1000,
            "natural_freq_max_units": "Hz",
            "reuse_modal_analysis": True,
            "strain_map_natural_freq": 222.45,
        },
    ]
    mockRequest = Mock()
    mockHvProperties = Mock()
    mockRequest.harmonicVibeProperties.add.return_value = mockHvProperties

    analysis._set_update_harmonic_vibe_props_request_properties(mockRequest, properties)

    assert mockHvProperties.ccaName == "Main Board"
    assert mockHvProperties.modelSource == ModelSource.STRAIN_MAP
    assert mockHvProperties.harmonicVibeCount == 4
    assert mockHvProperties.harmonicVibeDamping == "0.015, 0.025"
    assert mockHvProperties.partValidationEnabled == True
    assert mockHvProperties.requireMaterialAssignmentEnabled == True
    assert mockHvProperties.analysisTemp == 30
    assert mockHvProperties.analysisTempUnits == "F"
    assert mockHvProperties.forceModelRebuild == "FORCE"
    assert mockHvProperties.filterByEventFrequency == True
    assert mockHvProperties.naturalFreqMin == 50
    assert mockHvProperties.naturalFreqMinUnits == "Hz"
    assert mockHvProperties.naturalFreqMax == 1000
    assert mockHvProperties.naturalFreqMaxUnits == "Hz"
    assert mockHvProperties.reuseModalAnalysis == True
    assert mockHvProperties.strainMapNaturalFreq == 222.45


def helper_test_update_ict_analysis_props(analysis):
    try:
        analysis.update_ict_analysis_props(
            "",
            [
                {
                    "cca_name": "Main Board",
                    "application_time": 0.22,
                    "application_time_units": "min",
                    "ict_number_of_events": 19,
                    "part_validation_enabled": False,
                    "require_material_assignment_enabled": False,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateICTAnalysisPropsError as e:
        assert str(e) == "Update ICT analysis properties error: Project name is invalid."

    try:
        analysis.update_ict_analysis_props("Tutorial Project", "Main Board")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateICTAnalysisPropsError as e:
        assert (
            str(e) == "Update ICT analysis properties error: "
            "ICT analysis properties argument is invalid."
        )

    try:
        analysis.update_ict_analysis_props("Tutorial Project", [])
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateICTAnalysisPropsError as e:
        assert (
            str(e) == "Update ICT analysis properties error: "
            "One or more ICT analysis properties are required."
        )

    try:
        analysis.update_ict_analysis_props("Tutorial Project", ["INVALID"])
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateICTAnalysisPropsError as e:
        assert (
            str(e) == "Update ICT analysis properties error: "
            "ICT analysis props argument is invalid for ICT analysis properties 0."
        )

    try:
        analysis.update_ict_analysis_props(
            "Tutorial Project",
            [
                {
                    "ict_application_time": 2,
                    "ict_application_time_units": "sec",
                    "ict_number_of_events": 5,
                    "part_validation_enabled": False,
                    "require_material_assignment_enabled": False,
                    "force_model_rebuild": "AUTO",
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateICTAnalysisPropsError as e:
        assert (
            str(e) == "Update ICT analysis properties error: "
            "CCA name is missing for ICT analysis properties 0."
        )

    try:
        analysis.update_ict_analysis_props(
            "Tutorial Project",
            [
                {
                    "cca_name": "",
                    "ict_application_time": 2,
                    "ict_application_time_units": "sec",
                    "ict_number_of_events": 5,
                    "part_validation_enabled": False,
                    "require_material_assignment_enabled": False,
                    "force_model_rebuild": "AUTO",
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateICTAnalysisPropsError as e:
        assert (
            str(e) == "Update ICT analysis properties error: "
            "CCA name is invalid for ICT analysis properties 0."
        )

    if analysis._is_connection_up():
        try:
            analysis.update_ict_analysis_props(
                "Tutorial Project",
                [
                    {
                        "cca_name": "Main Board",
                        "ict_application_time": -2,
                        "ict_application_time_units": "sec",
                        "ict_number_of_events": 5,
                        "part_validation_enabled": False,
                        "require_material_assignment_enabled": False,
                        "force_model_rebuild": "AUTO",
                    },
                ],
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdateICTAnalysisPropsError

        try:
            result = analysis.update_ict_analysis_props(
                "Tutorial Project",
                [
                    {
                        "cca_name": "Main Board",
                        "ict_application_time": 2,
                        "ict_application_time_units": "sec",
                        "ict_number_of_events": 5,
                        "part_validation_enabled": False,
                        "require_material_assignment_enabled": False,
                        "force_model_rebuild": "AUTO",
                    },
                ],
            )
            assert result == 0
        except SherlockUpdateICTAnalysisPropsError as e:
            pytest.fail(str(e))


def helper_test_update_mechanical_shock_props(analysis):
    try:
        analysis.update_mechanical_shock_props(
            "",
            [
                {
                    "cca_name": "Main Board",
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
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateMechanicalShockPropsError as e:
        assert str(e) == "Update mechanical shock properties error: Project name is invalid."

    try:
        analysis.update_mechanical_shock_props("Test", "INVALID_TYPE")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateMechanicalShockPropsError as e:
        assert (
            str(e) == "Update mechanical shock properties error: "
            "Mechanical shock properties argument is invalid."
        )

    try:
        analysis.update_mechanical_shock_props("Test", [])
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateMechanicalShockPropsError as e:
        assert (
            str(e) == "Update mechanical shock properties error: "
            "One or more mechanical shock properties are required."
        )

    try:
        analysis.update_mechanical_shock_props("Test", ["INVALID"])
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateMechanicalShockPropsError as e:
        assert (
            str(e) == "Update mechanical shock properties error: "
            "Mechanical shock props argument is invalid for mechanical shock properties 0."
        )

    try:
        analysis.update_mechanical_shock_props(
            "Tutorial Project",
            [
                {
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
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateMechanicalShockPropsError as e:
        assert (
            str(e) == "Update mechanical shock properties error: "
            "CCA name is missing for mechanical shock properties 0."
        )

    try:
        analysis.update_mechanical_shock_props(
            "Tutorial Project",
            [
                {
                    "cca_name": "",
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
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateMechanicalShockPropsError as e:
        assert (
            str(e) == "Update mechanical shock properties error: "
            "CCA name is invalid for mechanical shock properties 0."
        )

    if not analysis._is_connection_up():
        return

    try:
        analysis.update_mechanical_shock_props(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "model_source": SherlockAnalysisService_pb2.ModelSource.GENERATED,
                    "shock_result_count": 2,
                    "critical_shock_strain": 10,
                    "critical_shock_strain_units": "INVALID",
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
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert type(e) == SherlockUpdateMechanicalShockPropsError

    try:
        result = analysis.update_mechanical_shock_props(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "model_source": SherlockAnalysisService_pb2.ModelSource.GENERATED,
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
            ],
        )
        assert result == 0
    except SherlockUpdateMechanicalShockPropsError as e:
        pytest.fail(str(e))


def helper_test_update_solder_fatigue_props(analysis):
    try:
        analysis.update_solder_fatigue_props(
            "",
            [
                {
                    "cca_name": "Card",
                    "solder_material": "63SN37PB",
                    "part_temp": 70,
                    "part_temp_units": "F",
                    "use_part_temp_rise_min": True,
                    "part_validation_enabled": True,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateSolderFatiguePropsError as e:
        assert str(e) == "Update solder fatigue properties error: Project name is invalid."

    try:
        analysis.update_solder_fatigue_props("Test", "INVALID_TYPE")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateSolderFatiguePropsError as e:
        assert (
            str(e) == "Update solder fatigue properties error: "
            "Solder fatigue properties argument is invalid."
        )

    try:
        analysis.update_solder_fatigue_props("Test", [])
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateSolderFatiguePropsError as e:
        assert (
            str(e) == "Update solder fatigue properties error: "
            "One or more solder fatigue properties are required."
        )

    try:
        analysis.update_solder_fatigue_props("Test", ["INVALID"])
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateSolderFatiguePropsError as e:
        assert (
            str(e) == "Update solder fatigue properties error: "
            "Solder fatigue props argument is invalid for solder fatigue properties 0."
        )

    try:
        analysis.update_solder_fatigue_props(
            "Tutorial Project",
            [
                {
                    "solder_material": "63SN37PB",
                    "part_temp": 70,
                    "part_temp_units": "F",
                    "use_part_temp_rise_min": True,
                    "part_validation_enabled": True,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateSolderFatiguePropsError as e:
        assert (
            str(e) == "Update solder fatigue properties error: "
            "CCA name is missing for solder fatigue properties 0."
        )

    try:
        analysis.update_solder_fatigue_props(
            "Tutorial Project",
            [
                {
                    "cca_name": "",
                    "solder_material": "63SN37PB",
                    "part_temp": 70,
                    "part_temp_units": "F",
                    "use_part_temp_rise_min": True,
                    "part_validation_enabled": True,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateSolderFatiguePropsError as e:
        assert (
            str(e) == "Update solder fatigue properties error: "
            "CCA name is invalid for solder fatigue properties 0."
        )

    if not analysis._is_connection_up():
        return

    try:
        analysis.update_solder_fatigue_props(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "solder_material": "63SN37PB",
                    "part_temp": 70,
                    "part_temp_units": "INVALID",
                    "use_part_temp_rise_min": True,
                    "part_validation_enabled": True,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert type(e) == SherlockUpdateSolderFatiguePropsError

    try:
        result = analysis.update_solder_fatigue_props(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "solder_material": "TIN-LEAD (63SN37PB)",
                    "part_temp": 70,
                    "part_temp_units": "F",
                    "use_part_temp_rise_min": True,
                    "part_validation_enabled": True,
                },
            ],
        )
        assert result == 0
    except SherlockUpdateSolderFatiguePropsError as e:
        pytest.fail(str(e))


def helper_test_update_random_vibe_props(analysis):
    try:
        analysis.update_random_vibe_props(
            "", "Card", random_vibe_damping="0.01, 0.05", analysis_temp=20, analysis_temp_units="C"
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateRandomVibePropsError as e:
        assert str(e) == "Update random vibe properties error: Project name is invalid."

    try:
        analysis.update_random_vibe_props(
            "Test", "", random_vibe_damping="0.01, 0.05", analysis_temp=20, analysis_temp_units="C"
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateRandomVibePropsError as e:
        assert str(e) == "Update random vibe properties error: CCA name is invalid."

    try:
        analysis.update_random_vibe_props("Tutorial Project", "Main Board", random_vibe_damping="")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateRandomVibePropsError as e:
        assert (
            str(e) == "Update random vibe properties error: Random vibe damping value is invalid."
        )

    try:
        analysis.update_random_vibe_props(
            "Test",
            "Card",
            random_vibe_damping="0.01, 0.02",
            model_source=ModelSource.STRAIN_MAP,
            strain_map_natural_freqs=None,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateRandomVibePropsError as e:
        assert str(e) == "Update random vibe properties error: Natural frequencies are invalid."

    if analysis._is_connection_up():
        try:
            invalid_strain_map_natural_freqs = "BAD, FREQS"
            analysis.update_random_vibe_props(
                "Tutorial Project",
                "Main Board",
                random_vibe_damping="0.01, 0.02",
                part_validation_enabled=True,
                require_material_assignment_enabled=False,
                model_source=ModelSource.STRAIN_MAP,
                strain_map_natural_freqs=invalid_strain_map_natural_freqs,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdateRandomVibePropsError

        try:
            result = analysis.update_random_vibe_props(
                "Tutorial Project",
                "Main Board",
                random_vibe_damping="0.01, 0.02",
                part_validation_enabled=True,
                require_material_assignment_enabled=False,
                model_source=ModelSource.GENERATED,
                strain_map_natural_freqs="101, 201, 501, 1001",
            )
            assert result == 0
        except SherlockUpdateRandomVibePropsError as e:
            pytest.fail(e.message)


def helper_test_get_natural_frequency_input_fields(analysis):
    if analysis._is_connection_up():
        fields = analysis.get_natural_frequency_input_fields()
        assert "natural_freq_count" in fields
        assert "natural_freq_max" in fields
        assert "natural_freq_max_units" in fields
        assert "natural_freq_min" in fields
        assert "natural_freq_min_units" in fields
        assert "part_validation_enabled" in fields
        assert "require_material_assignment_enabled" in fields


def helper_test_update_natural_frequency_props(analysis):
    try:
        analysis.update_natural_frequency_props(
            "",
            "Card",
            natural_freq_count=2,
            natural_freq_min=10,
            natural_freq_min_units="HZ",
            natural_freq_max=100,
            natural_freq_max_units="HZ",
            part_validation_enabled=True,
            require_material_assignment_enabled=False,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateNaturalFrequencyPropsError as e:
        assert str(e) == "Update natural frequency properties error: Project name is invalid."

    try:
        analysis.update_natural_frequency_props(
            "Test",
            "",
            natural_freq_count=2,
            natural_freq_min=10,
            natural_freq_min_units="HZ",
            natural_freq_max=100,
            natural_freq_max_units="HZ",
            part_validation_enabled=True,
            require_material_assignment_enabled=False,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdateNaturalFrequencyPropsError as e:
        assert str(e) == "Update natural frequency properties error: CCA name is invalid."

    if analysis._is_connection_up():
        try:
            invalid_natural_freq_count = -1
            analysis.update_natural_frequency_props(
                "AssemblyTutorial",
                "Main Board",
                natural_freq_count=invalid_natural_freq_count,
                natural_freq_min=10,
                natural_freq_min_units="HZ",
                natural_freq_max=100,
                natural_freq_max_units="HZ",
                part_validation_enabled=True,
                require_material_assignment_enabled=False,
                analysis_temp=25,
                analysis_temp_units="C",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdateNaturalFrequencyPropsError

        try:
            result = analysis.update_natural_frequency_props(
                "AssemblyTutorial",
                "Main Board",
                natural_freq_count=2,
                natural_freq_min=10,
                natural_freq_min_units="HZ",
                natural_freq_max=100,
                natural_freq_max_units="HZ",
                part_validation_enabled=True,
                require_material_assignment_enabled=False,
                analysis_temp=25,
                analysis_temp_units="C",
            )
            assert result == 0
        except SherlockUpdateNaturalFrequencyPropsError as e:
            pytest.fail(e.message)


def helper_test_update_pcb_modeling_props(analysis):
    try:
        analysis.update_pcb_modeling_props(
            "",
            ["Main Board"],
            [
                (
                    "NaturalFreq",
                    "Bonded",
                    True,
                    "Uniform",
                    "SolidShell",
                    6,
                    "mm",
                    3,
                    "mm",
                    True,
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePcbModelingPropsError as e:
        assert str(e) == "Update PCB Modeling Error: Project name is invalid."

    try:
        analysis.update_pcb_modeling_props(
            "Tutorial Project",
            [],
            [
                (
                    "NaturalFreq",
                    "Bonded",
                    True,
                    "Uniform",
                    "SolidShell",
                    6,
                    "mm",
                    3,
                    "mm",
                    True,
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePcbModelingPropsError as e:
        assert str(e) == "Update PCB Modeling Error: CCA names are invalid."

    try:
        analysis.update_pcb_modeling_props(
            "Tutorial Project",
            ["Main Board"],
            [],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePcbModelingPropsError as e:
        assert str(e) == "Update PCB Modeling Error: Analysis input(s) are invalid."

    if analysis._is_connection_up():
        try:
            analysis.update_pcb_modeling_props(
                "Tutorial Project",
                ["Invalid CCA"],
                [
                    (
                        UpdatePcbModelingPropsRequestAnalysisType.NATURAL_FREQUENCY,
                        UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                        True,
                        UpdatePcbModelingPropsRequestPcbMaterialModel.LAYERED,
                        ElementOrder.SOLID_SHELL,
                        6,
                        "mm",
                        3,
                        "mm",
                        True,
                    )
                ],
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            print(str(e))
            assert type(e) == SherlockUpdatePcbModelingPropsError

        try:
            result1 = analysis.update_pcb_modeling_props(
                "Tutorial Project",
                ["Main Board"],
                [
                    (
                        UpdatePcbModelingPropsRequestAnalysisType.NATURAL_FREQUENCY,
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
                ],
            )
            assert result1 == 0
        except SherlockUpdatePcbModelingPropsError as e:
            assert pytest.fail(e.message)

        try:
            result1 = analysis.update_pcb_modeling_props(
                "Tutorial Project",
                ["Main Board"],
                [
                    (
                        UpdatePcbModelingPropsRequestAnalysisType.NATURAL_FREQUENCY,
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
                ],
            )
            assert result1 == 0
        except SherlockUpdatePcbModelingPropsError as e:
            assert pytest.fail(e.message)

        try:
            result2 = analysis.update_pcb_modeling_props(
                "Tutorial Project",
                ["Main Board"],
                [
                    (
                        UpdatePcbModelingPropsRequestAnalysisType.NATURAL_FREQUENCY,
                        UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                        True,
                        UpdatePcbModelingPropsRequestPcbMaterialModel.LAYERED,
                        ElementOrder.SOLID_SHELL,
                        6,
                        "mm",
                        3,
                        "mm",
                        True,
                    )
                ],
            )
            assert result2 == 0
        except SherlockUpdatePcbModelingPropsError as e:
            assert pytest.fail(e.message)

        try:
            result3 = analysis.update_pcb_modeling_props(
                "Tutorial Project",
                ["Main Board"],
                [
                    (
                        UpdatePcbModelingPropsRequestAnalysisType.NATURAL_FREQUENCY,
                        UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                        True,
                        UpdatePcbModelingPropsRequestPcbMaterialModel.UNIFORM_ELEMENTS,
                        94,
                        ElementOrder.SOLID_SHELL,
                        6,
                        "mm",
                        3,
                        "mm",
                        True,
                    )
                ],
            )
            assert result3 == 0
        except SherlockUpdatePcbModelingPropsError as e:
            assert pytest.fail(e.message)

        try:
            result4 = analysis.update_pcb_modeling_props(
                "Tutorial Project",
                ["Main Board"],
                [
                    (
                        UpdatePcbModelingPropsRequestAnalysisType.NATURAL_FREQUENCY,
                        UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                        True,
                        UpdatePcbModelingPropsRequestPcbMaterialModel.LAYERED_ELEMENTS,
                        94,
                        ElementOrder.SOLID_SHELL,
                        6,
                        "mm",
                        3,
                        "mm",
                        True,
                    )
                ],
            )
            assert result4 == 0
        except SherlockUpdatePcbModelingPropsError as e:
            assert pytest.fail(e.message)


def helper_test_update_part_modeling_props(analysis):
    try:
        analysis.update_part_modeling_props(
            "",
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
                "part_results_filtered": True,
            },
        )
        pytest.fail("No exception thrown when project is the empty string.")
    except SherlockUpdatePartModelingPropsError as e:
        assert str(e) == "Update part modeling props error: Project name is invalid."

    try:
        analysis.update_part_modeling_props(
            "Test",
            {
                "cca_name": "",
                "part_enabled": True,
                "part_min_size": 1,
                "part_min_size_units": "in",
                "part_elem_order": "First Order (Linear)",
                "part_max_edge_length": 1,
                "part_max_edge_length_units": "in",
                "part_max_vertical": 1,
                "part_max_vertical_units": "in",
                "part_results_filtered": True,
            },
        )
        pytest.fail("No exception thrown when cca name is the empty string.")
    except SherlockUpdatePartModelingPropsError as e:
        assert str(e) == "Update part modeling props error: CCA name is invalid."

    try:
        analysis.update_part_modeling_props("Test", "INVALID")
        pytest.fail("No exception thrown when part modeling props is incorrect type.")
    except SherlockUpdatePartModelingPropsError as e:
        assert (
            str(e) == "Update part modeling props error: "
            "Part modeling props argument is invalid."
        )

    try:
        analysis.update_part_modeling_props(
            "Test",
            {
                "part_enabled": True,
                "part_min_size": 1,
                "part_min_size_units": "in",
                "part_elem_order": "First Order (Linear)",
                "part_max_edge_length": 1,
                "part_max_edge_length_units": "in",
                "part_max_vertical": 1,
                "part_max_vertical_units": "in",
                "part_results_filtered": True,
            },
        )
        pytest.fail("No exception thrown when CCA name is missing.")
    except SherlockUpdatePartModelingPropsError as e:
        assert str(e) == "Update part modeling props error: CCA name is missing."

    try:
        analysis.update_part_modeling_props(
            "Test",
            {
                "cca_name": "",
                "part_enabled": True,
                "part_min_size": 1,
                "part_min_size_units": "in",
                "part_elem_order": "First Order (Linear)",
                "part_max_edge_length": 1,
                "part_max_edge_length_units": "in",
                "part_max_vertical": 1,
                "part_max_vertical_units": "in",
                "part_results_filtered": True,
            },
        )
        pytest.fail("No exception thrown when CCA name is empty.")
    except SherlockUpdatePartModelingPropsError as e:
        assert str(e) == "Update part modeling props error: CCA name is invalid."

    try:
        analysis.update_part_modeling_props(
            "Test",
            {
                "cca_name": "Card",
                "part_min_size": 1,
                "part_min_size_units": "in",
                "part_elem_order": "First Order (Linear)",
                "part_max_edge_length": 1,
                "part_max_edge_length_units": "in",
                "part_max_vertical": 1,
                "part_max_vertical_units": "in",
                "part_results_filtered": True,
            },
        )
        pytest.fail("No exception thrown when part enabled is missing.")
    except SherlockUpdatePartModelingPropsError as e:
        assert str(e) == "Update part modeling props error: Part enabled is missing."

    if not analysis._is_connection_up():
        return

    try:
        analysis.update_part_modeling_props(
            "Tutorial Project",
            {
                "cca_name": "Main Board",
                "part_enabled": True,
                "part_min_size": 1,
                "part_min_size_units": "in",
                "part_elem_order": "INVALID",
                "part_max_edge_length": 1,
                "part_max_edge_length_units": "in",
                "part_max_vertical": 1,
                "part_max_vertical_units": "in",
                "part_results_filtered": True,
            },
        )
        pytest.fail("No exception raised when using an invalid parameter.")
    except Exception as e:
        assert type(e) == SherlockUpdatePartModelingPropsError

    try:
        result = analysis.update_part_modeling_props(
            "Tutorial Project",
            {
                "cca_name": "Main Board",
                "part_enabled": False,
            },
        )
        assert result == 0
    except SherlockUpdatePartModelingPropsError as e:
        pytest.fail(str(e))


def helper_test_update_parts_list_validation_props(analysis):
    try:
        analysis.update_part_list_validation_analysis_props("Tutorial Project", "Main Board")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartListValidationAnalysisPropsError as e:
        assert (
            str(e) == "Update part list validation analysis properties error: "
            "Properties per CCA argument is invalid."
        )

    try:
        analysis.update_part_list_validation_analysis_props("Tutorial Project", [])
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartListValidationAnalysisPropsError as e:
        assert e.message == "One or more analysis properties are required."

    try:
        analysis.update_part_list_validation_analysis_props(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "process_use_avl": True,
                    "process_use_wizard": False,
                    "process_check_confirmed_properties": True,
                    "process_check_part_numbers": True,
                    "matching_mode": "Part",
                    "avl_require_internal_part_number": True,
                    "avl_require_approved_description": True,
                    "avl_require_approved_manufacturer": True,
                },
                {
                    "process_use_avl": True,
                    "process_use_wizard": False,
                    "process_check_confirmed_properties": True,
                    "process_check_part_numbers": True,
                    "matching_mode": "Part",
                    "avl_require_internal_part_number": True,
                    "avl_require_approved_description": True,
                    "avl_require_approved_manufacturer": True,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartListValidationAnalysisPropsError as e:
        assert e.message == "CCA name is missing for analysis properties 1."

    try:
        analysis.update_part_list_validation_analysis_props(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "process_use_avl": True,
                    "process_use_wizard": False,
                    "process_check_confirmed_properties": True,
                    "process_check_part_numbers": True,
                    "matching_mode": "Part",
                    "avl_require_internal_part_number": True,
                    "avl_require_approved_description": True,
                    "avl_require_approved_manufacturer": True,
                },
                {
                    "cca_name": "",
                    "process_use_avl": True,
                    "process_use_wizard": False,
                    "process_check_confirmed_properties": True,
                    "process_check_part_numbers": True,
                    "matching_mode": "Part",
                    "avl_require_internal_part_number": True,
                    "avl_require_approved_description": True,
                    "avl_require_approved_manufacturer": True,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartListValidationAnalysisPropsError as e:
        assert e.message == "CCA name is invalid for analysis properties 1."

    if not analysis._is_connection_up():
        return

    try:
        analysis.update_part_list_validation_analysis_props(
            "",
            [
                {
                    "cca_name": "Main Board",
                    "process_use_avl": True,
                    "process_use_wizard": False,
                    "process_check_confirmed_properties": True,
                    "process_check_part_numbers": True,
                    "matching_mode": "Part",
                    "avl_require_internal_part_number": True,
                    "avl_require_approved_description": True,
                    "avl_require_approved_manufacturer": True,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert type(e) == SherlockUpdatePartListValidationAnalysisPropsError

    try:
        result = analysis.update_part_list_validation_analysis_props(
            "Tutorial Project",
            [
                {
                    "cca_name": "Main Board",
                    "process_use_avl": True,
                    "process_use_wizard": False,
                    "process_check_confirmed_properties": True,
                    "process_check_part_numbers": False,
                    "matching_mode": "Part",
                    "avl_require_internal_part_number": True,
                    "avl_require_approved_description": False,
                    "avl_require_approved_manufacturer": True,
                },
            ],
        )
        assert result == 0
    except SherlockUpdatePartListValidationAnalysisPropsError as e:
        pytest.fail(str(e))


def helper_test_get_parts_list_validation_analysis_props(analysis):
    try:
        analysis.get_parts_list_validation_analysis_props("", "Main Board")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetPartsListValidationAnalysisPropsError as e:
        assert (
            str(e)
            == "Get parts list validation analysis properties error: Project name is invalid."
        )

    if analysis._is_connection_up():
        try:
            analysis.get_parts_list_validation_analysis_props(
                "Tutorial Project",
                "Invalid CCA name",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockGetPartsListValidationAnalysisPropsError

        try:
            response = analysis.get_parts_list_validation_analysis_props(
                "Tutorial Project",
                "Main Board",
            )
            assert response is not None
            assert response.partLibrary is not None
            assert response.processUseAVL is not None
            assert response.processUseWizard is not None
            assert response.processCheckConfirmedProperties is not None
            assert response.processCheckPartNumbers is not None
            assert response.matching is not None
            assert response.avlRequireInternalPartNumber is not None
            assert response.avlRequireApprovedDescription is not None
            assert response.avlRequireApprovedManufacturer is not None
        except SherlockGetPartsListValidationAnalysisPropsError as e:
            pytest.fail(str(e))


if __name__ == "__main__":
    test_all()
