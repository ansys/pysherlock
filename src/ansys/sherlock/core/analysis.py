"""Module containing all the analysis capabilities."""

try:
    import SherlockAnalysisService_pb2
    import SherlockAnalysisService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2
    from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockInvalidPhaseError, SherlockRunAnalysisError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Analysis(GrpcStub):
    """Module containing all the analysis capabilities."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockAnalysisService."""
        self.channel = channel
        self.stub = SherlockAnalysisService_pb2_grpc.SherlockAnalysisServiceStub(channel)
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
        events : str list
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
