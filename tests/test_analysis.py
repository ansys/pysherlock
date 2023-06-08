# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.
import time

import SherlockAnalysisService_pb2
import grpc
import pytest

from ansys.sherlock.core.analysis import Analysis
from ansys.sherlock.core.errors import (
    SherlockGetRandomVibeInputFieldsError,
    SherlockRunAnalysisError,
    SherlockRunStrainMapAnalysisError,
    SherlockUpdateNaturalFrequencyPropsError,
    SherlockUpdatePcbModelingPropsError,
    SherlockUpdateRandomVibePropsError,
)


def test_all():
    """Test all life cycle APIs."""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    analysis = Analysis(channel)
    helper_test_run_analysis(analysis)
    time.sleep(1)
    helper_test_run_strain_map_analysis(analysis)
    helper_test_get_harmonic_vibe_input_fields(analysis)
    helper_test_get_random_vibe_input_fields(analysis)
    helper_test_translate_field_names(analysis)
    helper_test_update_random_vibe_props(analysis)
    helper_test_update_natural_frequency_props(analysis)
    helper_test_update_pcb_modeling_props(analysis)


def helper_test_run_analysis(analysis):
    """Test run_analysis API."""
    analysis_request = SherlockAnalysisService_pb2.RunAnalysisRequest
    natural_frequency_analysis_type = analysis_request.Analysis.AnalysisType.NaturalFreq

    if analysis._is_connection_up():
        result = analysis.run_analysis(
            "AssemblyTutorial",
            "Main Board",
            [(natural_frequency_analysis_type, [("Phase 1", ["Harmonic Vibe"])])],
        )
        assert result == 0

    try:
        analysis.run_analysis(
            "", "Main Board", [(natural_frequency_analysis_type, [("Phase 1", ["Harmonic Vibe"])])]
        ),
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Project name is invalid."

    try:
        analysis.run_analysis(
            "AssemblyTutorial",
            "",
            [(natural_frequency_analysis_type, [("Phase 1", ["Harmonic Vibe"])])],
        ),
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: CCA name is invalid."

    try:
        analysis.run_analysis("AssemblyTutorial", "Main Board", "Not a list")
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Analyses argument is invalid."

    try:
        analysis.run_analysis("Test", "Card", [])
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: One or more analyses are missing."


def helper_test_run_strain_map_analysis(analysis):
    """Test run_strain_map_analysis API."""
    analysis_request = SherlockAnalysisService_pb2.RunStrainMapAnalysisRequest
    random_vibe_analysis_type = analysis_request.StrainMapAnalysis.AnalysisType.RandomVibe
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
            pytest.fail("No exception thrown when using an invalid parameter")
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
        pytest.fail("No exception thrown when using an invalid parameter")
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
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert str(e) == "Run strain map analysis error: CCA name is invalid."

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            "Invalid analyses",
        )
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert str(e) == "Run strain map analysis error: Analyses argument is invalid."

    try:
        analyses = []
        analysis.run_strain_map_analysis("AssemblyTutorial", "Main Board", analyses)
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert str(e) == "Run strain map analysis error: One or more analyses are missing."

    try:
        analyses = ["INVALID"]
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            analyses,
        )
        pytest.fail("No exception thrown when using an invalid parameter")
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
        pytest.fail("No exception thrown when using an invalid parameter")
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
        pytest.fail("No exception thrown when using an invalid parameter")
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
        pytest.fail("No exception thrown when using an invalid parameter")
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
        pytest.fail("No exception thrown when using an invalid parameter")
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
        pytest.fail("No exception thrown when using an invalid parameter")
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
        pytest.fail("No exception thrown when using an invalid parameter")
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
        pytest.fail("No exception thrown when using an invalid parameter")
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
        pytest.fail("No exception thrown when using an invalid parameter")
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
        pytest.fail("No exception thrown when using an invalid parameter")
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Strain map name is missing for event strain "
            "map 2 for strain map analysis 0."
        )


def helper_test_get_harmonic_vibe_input_fields(analysis):
    if analysis._is_connection_up():
        fields = analysis.get_harmonic_vibe_input_fields()
        assert "analysis_temp" in fields
        assert "analysis_temp_units" in fields
        assert "harmonic_vibe_count" in fields
        assert "harmonic_vibe_damping" in fields
        assert "model_source" in fields
        assert "part_validation_enabled" in fields
        assert "require_material_assignment_enabled" in fields


def helper_test_get_random_vibe_input_fields(analysis):
    try:
        analysis.get_random_vibe_input_fields("BADTYPE")
        assert False
    except SherlockGetRandomVibeInputFieldsError as e:
        assert str(e) == "Get random vibe input fields error: Model source BADTYPE is invalid."

    if analysis._is_connection_up():
        try:
            fields = analysis.get_random_vibe_input_fields()
            assert "analysis_temp" in fields
            assert "analysis_temp_units" in fields
            assert "model_source" in fields
            assert "part_validation_enabled" in fields
            assert "random_vibe_damping" in fields
            assert "require_material_assignment_enabled" in fields
        except Exception as e:
            print(str(e))
            assert False

        try:
            fields = analysis.get_random_vibe_input_fields("GENERATED")
            assert "analysis_temp" in fields
            assert "analysis_temp_units" in fields
            assert "model_source" in fields
            assert "part_validation_enabled" in fields
            assert "random_vibe_damping" in fields
            assert "require_material_assignment_enabled" in fields
        except Exception as e:
            print(str(e))
            assert False

        try:
            fields = analysis.get_random_vibe_input_fields("STRAIN_MAP")
            assert "model_source" in fields
            assert "part_validation_enabled" in fields
            assert "random_vibe_damping" in fields
            assert "require_material_assignment_enabled" in fields
            assert "strain_map_natural_freqs" in fields
        except Exception as e:
            print(str(e))
            assert False


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

    expected = """
analysis_temp
analysis_temp
analysis_temp_units
analysis_temp_units
filter_by_event_frequency
force_model_rebuild
harmonic_vibe_damping
harmonic_vibe_count
model_source
natural_freq_count
natural_freq_min
natural_freq_min_units
natural_freq_max
natural_freq_max_units
part_validation_enabled
perform_nf_freq_range_check
random_vibe_damping
require_material_assignment_enabled
reuse_modal_analysis
strain_map_natural_freqs"""

    assert results == expected


def helper_test_update_random_vibe_props(analysis):
    try:
        analysis.update_random_vibe_props(
            "", "Card", random_vibe_damping="0.01, 0.05", analysis_temp=20, analysis_temp_units="C"
        )
        assert False
    except SherlockUpdateRandomVibePropsError as e:
        assert str(e) == "Update random vibe properties error: Project name is invalid."

    try:
        analysis.update_random_vibe_props(
            "Test", "", random_vibe_damping="0.01, 0.05", analysis_temp=20, analysis_temp_units="C"
        )
        assert False
    except SherlockUpdateRandomVibePropsError as e:
        assert str(e) == "Update random vibe properties error: CCA name is invalid."

    try:
        analysis.update_random_vibe_props("Test", "Card", random_vibe_damping="0.01, foo")
        assert False
    except SherlockUpdateRandomVibePropsError as e:
        assert (
            str(e)
            == "Update random vibe properties error: Random vibe damping value is invalid: foo"
        )

    try:
        analysis.update_random_vibe_props(
            "Test", "Card", random_vibe_damping="0.01, 0.02", model_source="BAD_SOURCE"
        )
        assert False
    except SherlockUpdateRandomVibePropsError as e:
        assert str(e) == "Update random vibe properties error: Model source BAD_SOURCE is invalid."

    try:
        analysis.update_random_vibe_props(
            "Test", "Card", random_vibe_damping="0.01, 0.02", model_source="STRAIN_MAP"
        )
        assert False
    except SherlockUpdateRandomVibePropsError as e:
        assert str(e) == "Update random vibe properties error: Natural frequencies are invalid."

    if analysis._is_connection_up():
        try:
            analysis.update_random_vibe_props(
                "Test",
                "Card",
                random_vibe_damping="0.01, 0.02",
                natural_freq_min=10,
                natural_freq_min_units="foo",
                natural_freq_max=100,
                natural_freq_max_units="HZ",
            )
            assert False
        except SherlockUpdateRandomVibePropsError as e:
            assert (
                str(e) == "Update random vibe properties error: Minimum "
                "natural frequency units are invalid: foo"
            )

        try:
            analysis.update_random_vibe_props(
                "Test",
                "Card",
                random_vibe_damping="0.01, 0.02",
                natural_freq_min=10,
                natural_freq_min_units="HZ",
                natural_freq_max=100,
                natural_freq_max_units="foo",
            )
            assert False
        except SherlockUpdateRandomVibePropsError as e:
            assert (
                str(e) == "Update random vibe properties error: Maximum "
                "natural frequency units are invalid: foo"
            )

        try:
            analysis.update_random_vibe_props(
                "Test",
                "Card",
                random_vibe_damping="0.01, 0.02",
                natural_freq_min=10,
                natural_freq_min_units="HZ",
                natural_freq_max=100,
                natural_freq_max_units="HZ",
                analysis_temp_units="foo",
            )
            assert False
        except SherlockUpdateRandomVibePropsError as e:
            assert (
                str(e) == "Update random vibe properties error: Analysis "
                "temperature units are invalid: foo"
            )

        result = analysis.update_random_vibe_props(
            "Tutorial Project",
            "Main Board",
            random_vibe_damping="0.01, 0.02",
            model_source="STRAIN_MAP",
            part_validation_enabled=True,
            require_material_assignment_enabled=False,
            strain_map_natural_freqs="101, 201, 501, 1001",
        )
        assert result == 0

        try:
            invalid_strain_map_natural_freqs = "BAD, FREQS"
            analysis.update_random_vibe_props(
                "Tutorial Project",
                "Main Board",
                random_vibe_damping="0.01, 0.02",
                model_source="STRAIN_MAP",
                part_validation_enabled=True,
                require_material_assignment_enabled=False,
                strain_map_natural_freqs=invalid_strain_map_natural_freqs,
            )
            assert False
        except Exception as e:
            assert type(e) == SherlockUpdateRandomVibePropsError


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
        assert False
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
        assert False
    except SherlockUpdateNaturalFrequencyPropsError as e:
        assert str(e) == "Update natural frequency properties error: CCA name is invalid."

    if analysis._is_connection_up():
        try:
            analysis.update_natural_frequency_props(
                "Test",
                "Card",
                natural_freq_count=2,
                natural_freq_min=10,
                natural_freq_min_units="foo",
                natural_freq_max=100,
                natural_freq_max_units="HZ",
                part_validation_enabled=True,
                require_material_assignment_enabled=False,
            )
            assert False
        except SherlockUpdateNaturalFrequencyPropsError as e:
            assert (
                str(e) == "Update natural frequency properties error: Minimum "
                "natural frequency units are invalid: foo"
            )

        try:
            analysis.update_natural_frequency_props(
                "Test",
                "Card",
                natural_freq_count=2,
                natural_freq_min=10,
                natural_freq_min_units="HZ",
                natural_freq_max=100,
                natural_freq_max_units="foo",
                part_validation_enabled=True,
                require_material_assignment_enabled=False,
            )
            assert False
        except SherlockUpdateNaturalFrequencyPropsError as e:
            assert (
                str(e) == "Update natural frequency properties error: Maximum "
                "natural frequency units are invalid: foo"
            )

        try:
            analysis.update_natural_frequency_props(
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
                analysis_temp_units="foo",
            )
            assert False
        except SherlockUpdateNaturalFrequencyPropsError as e:
            assert (
                str(e) == "Update natural frequency properties error: Analysis "
                "temperature units are invalid: foo"
            )

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
        except Exception as e:
            print(str(e))
            assert False

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
            assert False
        except Exception as e:
            assert type(e) == SherlockUpdateNaturalFrequencyPropsError


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
    except SherlockUpdatePcbModelingPropsError as e:
        assert str(e) == "Update PCB Modeling Error: CCA names are invalid."

    try:
        analysis.update_pcb_modeling_props(
            "Tutorial Project",
            ["Main Board"],
            [],
        )
    except SherlockUpdatePcbModelingPropsError as e:
        assert str(e) == "Update PCB Modeling Error: Analysis input(s) are invalid."

    if analysis._is_connection_up():
        try:
            result1 = analysis.update_pcb_modeling_props(
                "Tutorial Project",
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
            assert result1 == 0
        except Exception as e:
            assert False, e.message
        try:
            result1 = analysis.update_pcb_modeling_props(
                "Tutorial Project",
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
            assert result1 == 0
        except Exception as e:
            assert False, e.message

        try:
            result2 = analysis.update_pcb_modeling_props(
                "Tutorial Project",
                ["Main Board"],
                [
                    (
                        "NaturalFreq",
                        "Bonded",
                        True,
                        "Layered",
                        "SolidShell",
                        6,
                        "mm",
                        3,
                        "mm",
                        True,
                    )
                ],
            )
            assert result2 == 0
        except Exception as e:
            assert False, e.message

        try:
            result3 = analysis.update_pcb_modeling_props(
                "Tutorial Project",
                ["Main Board"],
                [
                    (
                        "NaturalFreq",
                        "Bonded",
                        True,
                        "UniformElements",
                        94,
                        "SolidShell",
                        6,
                        "mm",
                        3,
                        "mm",
                        True,
                    )
                ],
            )
            assert result3 == 0
        except Exception as e:
            assert False, e.message
        try:
            result4 = analysis.update_pcb_modeling_props(
                "Tutorial Project",
                ["Main Board"],
                [
                    (
                        "NaturalFreq",
                        "Bonded",
                        True,
                        "LayeredElements",
                        94,
                        "SolidShell",
                        6,
                        "mm",
                        3,
                        "mm",
                        True,
                    )
                ],
            )
            assert result4 == 0
        except Exception as e:
            assert False, e.message
        try:
            analysis.update_pcb_modeling_props(
                "Tutorial Project",
                ["Invalid CCA"],
                [
                    (
                        "NaturalFreq",
                        "Bonded",
                        True,
                        "Layered",
                        "SolidShell",
                        6,
                        "mm",
                        3,
                        "mm",
                        True,
                    )
                ],
            )
            assert False
        except Exception as e:
            assert type(e) == SherlockUpdatePcbModelingPropsError


if __name__ == "__main__":
    test_all()
