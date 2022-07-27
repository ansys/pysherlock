import grpc

from ansys.sherlock.core.analysis import Analysis
from ansys.sherlock.core.errors import SherlockRunAnalysisError


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    analysis = Analysis(channel)

    helper_test_run_analysis(analysis)


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


if __name__ == "__main__":
    test_all()
