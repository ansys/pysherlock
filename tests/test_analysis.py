import grpc

from ansys.sherlock.core.analysis import Analysis
from ansys.sherlock.core.errors import SherlockRunAnalysisError, SherlockUpdateRandomVibePropsError


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    analysis = Analysis(channel)

    helper_test_run_analysis(analysis)
    helper_test_translate_random_vibe_field_names(analysis)
    helper_test_update_random_vibe_props(analysis)


def helper_test_run_analysis(analysis):
    """Test run_analysis API."""

    try:
        analysis.run_analysis("", "Card", [("NATURALFREQ", [("Phase 1", ["Harmonic Event"])])])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Invalid project name"

    try:
        analysis.run_analysis("Test", "", [("NATURALFREQ", [("Phase 1", ["Harmonic Event"])])])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Invalid cca name"

    try:
        analysis.run_analysis(
            "Test",
            "Card",
            "Invalid",
        )
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Invalid analyses argument"

    try:
        analysis.run_analysis(
            "Test",
            "Card",
            [],
        )
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Missing one or more analyses"

    try:
        analysis.run_analysis("Test", "Card", [("Invalid", [("Phase 1", ["Harmonic Event"])])])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Invalid analysis 0: Invalid analysis provided"

    try:
        analysis.run_analysis("Test", "Card", [("NATURALFREQ", [("", ["Harmonic Event"])])])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == (
            "Run analysis error: Invalid analysis 0:" " Invalid phase 0: Invalid phase name"
        )

    try:
        analysis.run_analysis("Test", "Card", [("NATURALFREQ", "Invalid")])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == "Run analysis error: Invalid analysis 0: Invalid phases argument"

    try:
        analysis.run_analysis("Test", "Card", [("NATURALFREQ", [("Phase 1", "Invalid")])])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == (
            "Run analysis error: Invalid analysis 0:" " Invalid phase 0: Invalid events argument"
        )

    try:
        analysis.run_analysis("Test", "Card", [("NATURALFREQ", [("Phase 1", [""])])])
        assert False
    except SherlockRunAnalysisError as e:
        assert str(e) == (
            "Run analysis error: Invalid analysis 0:" " Invalid phase 0: Invalid event(s) name"
        )

def helper_test_translate_random_vibe_field_names(analysis):
    """Test translating the random vibe field names."""

    results = analysis._translate_random_vibe_field_names([
        "randomVibeDamping", "naturalFreqMin", "naturalFreqMinUnits",
        "naturalFreqMax", "naturalFreqMaxUnits", "analysisTemp",
        "analysisTempUnits", "partValidationEnabled", "forceModelRebuild",
        "reuseModalAnalysis", "performNFFreqRangeCheck", "requireMaterialAssignmentEnabled"
    ])

    expected = """
random_vibe_damping
natural_freq_min
natural_freq_min_units
natural_freq_max
natural_freq_max_units
analysis_temp
analysis_temp_units
part_validation_enabled
force_model_rebuild
reuse_modal_analysis
perform_nf_freq_range_check
require_material_assignment_enabled"""

    assert results == expected

def helper_test_update_random_vibe_props(analysis):
    try:
        analysis.update_random_vibe_props("", "Card", random_vibe_damping="0.01, 0.05",
                                          analysis_temp=20, analysis_temp_units="C")
        assert False
    except SherlockUpdateRandomVibePropsError as e:
        assert str(e) == "Update random vibe properties error: Invalid project name"

    try:
        analysis.update_random_vibe_props("Test", "", random_vibe_damping="0.01, 0.05",
                                          analysis_temp=20, analysis_temp_units="C")
        assert False
    except SherlockUpdateRandomVibePropsError as e:
        assert str(e) == "Update random vibe properties error: Invalid cca name"

    try:
        analysis.update_random_vibe_props("Test", "Card", random_vibe_damping="0.01, foo")
        assert False
    except SherlockUpdateRandomVibePropsError as e:
        assert str(e) == \
               "Update random vibe properties error: Invalid random vibe damping value: foo"

    if analysis._is_connection_up():
        try:
            analysis.update_random_vibe_props("Test", "Card",
                                              random_vibe_damping="0.01, 0.02",
                                              natural_freq_min=10,
                                              natural_freq_min_units="foo",
                                              natural_freq_max=100,
                                              natural_freq_max_units="HZ")
            assert False
        except SherlockUpdateRandomVibePropsError as e:
            assert str(e) == \
                   "Update random vibe properties error: Invalid min natural freq unit specified: foo"

        try:
            analysis.update_random_vibe_props("Test", "Card",
                                              random_vibe_damping="0.01, 0.02",
                                              natural_freq_min=10,
                                              natural_freq_min_units="HZ",
                                              natural_freq_max=100,
                                              natural_freq_max_units="foo")
            assert False
        except SherlockUpdateRandomVibePropsError as e:
            assert str(e) == \
                   "Update random vibe properties error: Invalid max natural freq unit specified: foo"

        try:
            analysis.update_random_vibe_props("Test", "Card",
                                              random_vibe_damping="0.01, 0.02",
                                              natural_freq_min=10,
                                              natural_freq_min_units="HZ",
                                              natural_freq_max=100,
                                              natural_freq_max_units="HZ",
                                              analysis_temp_units="foo")
            assert False
        except SherlockUpdateRandomVibePropsError as e:
            assert str(e) == \
                   "Update random vibe properties error: Invalid analysis " \
                "temperature unit specified: foo"

if __name__ == "__main__":
    test_all()
