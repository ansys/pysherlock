# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

import grpc

from ansys.sherlock.core.analysis import Analysis
from ansys.sherlock.core.errors import (
    SherlockGetRandomVibeInputFieldsError,
    SherlockRunAnalysisError,
    SherlockRunStrainMapAnalysisError,
    SherlockUpdateNaturalFrequencyPropsError,
    SherlockUpdateRandomVibePropsError,
)


def test_all():
    """Test all life cycle APIs."""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    analysis = Analysis(channel)
    helper_test_run_strain_map_analysis(analysis)
    helper_test_run_analysis(analysis)
    helper_test_get_harmonic_vibe_input_fields(analysis)
    helper_test_get_random_vibe_input_fields(analysis)
    helper_test_translate_field_names(analysis)
    helper_test_update_random_vibe_props(analysis)
    helper_test_update_natural_frequency_props(analysis)


def helper_test_run_analysis(analysis):
    """Test run_analysis API."""

    if analysis._is_connection_up():
        result = analysis.run_analysis(
            "AssemblyTutorial",
            "Main Board",
            [("NATURALFREQ", [("Phase 1", ["Harmonic Vibe"])])],
        )
        assert result == 0

    try:
        analysis.run_analysis(
            "", "Main Board", [("NATURALFREQ", [("Phase 1", ["Harmonic Vibe"])])]
        ),
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Project name is invalid."

    try:
        analysis.run_analysis(
            "AssemblyTutorial", "", [("NATURALFREQ", [("Phase 1", ["Harmonic Vibe"])])]
        ),
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: CCA name is invalid."

    try:
        analysis.run_analysis("AssemblyTutorial", "Main Board", "Invalid")
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Analyses argument is invalid."

    try:
        analysis.run_analysis("Test", "Card", [])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: One or more analyses are missing."

    try:
        analysis.run_analysis("Test", "Card", [("Invalid", [("Phase 1", ["Harmonic Event"])])])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Invalid analysis 0: Analysis is invalid."

    try:
        analysis.run_analysis("Test", "Card", [("NATURALFREQ", [("", ["Harmonic Event"])])])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == (
            "Run analysis error: Invalid analysis 0:" " Invalid phase 0: Phase name is invalid."
        )

    try:
        analysis.run_analysis("Test", "Card", [("NATURALFREQ", "Invalid")])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Invalid analysis 0: Phases argument is invalid."

    try:
        analysis.run_analysis("Test", "Card", [("NATURALFREQ", [("Phase 1", "Invalid")])])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == (
            "Run analysis error: Invalid analysis 0:"
            " Invalid phase 0: Events argument "
            "is invalid."
        )

    try:
        analysis.run_analysis("Test", "Card", [("NATURALFREQ", [("Phase 1", [""])])])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == (
            "Run analysis error: Invalid analysis 0:"
            " Invalid phase 0: One or more event "
            "names are invalid."
        )


def helper_test_run_strain_map_analysis(analysis):
    """Test run_strain_map_analysis API."""

    if analysis._is_connection_up():
        try:
            analysis.run_strain_map_analysis(
                "AssemblyTutorial",
                "Main Board",
                [
                    [
                        "RANDOMVIBE",
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
        except Exception as e:
            print(str(e))

    try:
        analysis.run_strain_map_analysis(
            "",
            "Main Board",
            [
                [
                    "RANDOMVIBE",
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        assert False
    except SherlockRunStrainMapAnalysisError as e:
        assert str(e) == "Run strain map analysis error: Project name is invalid."

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "",
            [
                [
                    "RANDOMVIBE",
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        assert False
    except SherlockRunStrainMapAnalysisError as e:
        assert str(e) == "Run strain map analysis error: CCA name is invalid."

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            "Invalid",
        )
        assert False
    except SherlockRunStrainMapAnalysisError as e:
        assert str(e) == "Run strain map analysis error: Analyses argument is invalid."

    try:
        analysis.run_strain_map_analysis("AssemblyTutorial", "Main Board", [])
        assert False
    except SherlockRunStrainMapAnalysisError as e:
        assert str(e) == "Run strain map analysis error: One or more analyses are missing."

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            ["INVALID"],
        )
        assert False
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Analysis argument is invalid for strain "
            "map analysis 0."
        )

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [["INVALID"]],
        )
        assert False
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e)
            == "Run strain map analysis error: Number of elements (1) is wrong for strain map "
            "analysis 0."
        )

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    "",
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        assert False
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Analysis type is missing for strain map "
            "analysis 0."
        )

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    "NOTREAL",
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        assert False
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Analysis type NOTREAL is invalid for "
            "strain map analysis 0."
        )

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    "RANDOMVIBE",
                    [],
                ]
            ],
        )
        assert False
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: One or more event strain maps are "
            "missing for strain map analysis 0."
        )

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    "RANDOMVIBE",
                    ["INVALID"],
                ]
            ],
        )
        assert False
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Event strain map argument is invalid for "
            "strain map analysis 0."
        )

    try:
        analysis.run_strain_map_analysis(
            "AssemblyTutorial",
            "Main Board",
            [
                [
                    "RANDOMVIBE",
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        assert False
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
                    "RANDOMVIBE",
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        assert False
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
                    "RANDOMVIBE",
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ]
            ],
        )
        assert False
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
                    "RANDOMVIBE",
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ],
                [
                    "RANDOMVIBE",
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "", "MemoryCard1Strain", "Memory Card 1"],
                    ],
                ],
            ],
        )
        assert False
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
                    "RANDOMVIBE",
                    [
                        ["Phase 1", "Random Vibe", "TOP", "MainBoardStrain - Top"],
                        ["Phase 1", "Random Vibe", "BOTTOM", "MainBoardStrain - Bottom"],
                        ["Phase 1", "Random Vibe", "TOP", "", "Memory Card 1"],
                    ],
                ]
            ],
        )
        assert False
    except SherlockRunStrainMapAnalysisError as e:
        assert (
            str(e) == "Run strain map analysis error: Strain map name is missing for event strain "
            "map 2 for strain map analysis 0."
        )


def helper_test_get_harmonic_vibe_input_fields(analysis):
    if analysis._is_connection_up():
        try:
            fields = analysis.get_harmonic_vibe_input_fields()
            assert "analysis_temp" in fields
            assert "analysis_temp_units" in fields
            assert "harmonic_vibe_count" in fields
            assert "harmonic_vibe_damping" in fields
            assert "model_source" in fields
            assert "part_validation_enabled" in fields
            assert "require_material_assignment_enabled" in fields
        except Exception as e:
            print(str(e))


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


if __name__ == "__main__":
    test_all()
