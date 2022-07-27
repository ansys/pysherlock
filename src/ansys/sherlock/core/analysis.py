"""Module for analysis services on client-side."""

import SherlockAnalysisService_pb2
import SherlockAnalysisService_pb2_grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockInvalidPhaseError, SherlockRunAnalysisError
from ansys.sherlock.core.grpc_stub import GrpcStub


class Analysis(GrpcStub):
    """Contains methods from the Sherlock Analysis Service."""

    def __init__(self, channel):
        """Initialize a gRPC stub for SherlockAnalysisService."""
        self.channel = channel
        self.stub = SherlockAnalysisService_pb2_grpc.SherlockAnalysisServiceStub(channel)
        self.ANALYSIS_TYPES = {
            "UNKNOWN": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.UNKNOWN,
            "NATURALFREQ": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.NaturalFreq,
            "HARMONICVIBE": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.HarmonicVibe,
            "ICTANALYSIS": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.ICTAnalysis,
            "MECHANICALSHOCK": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.MechanicalShock,
            "RANDOMVIBE": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.RandomVibe,
            "HOLETOHOLECAF": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.HoleToHoleCAF,
            "COMPONENTFAILUREMODE": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.ComponentFailureMode,
            "DFMEAMODULE": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.DFMEAModule,
            "PTHFATIGUE": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.PTHFatigue,
            "PARTVALIDATION": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.PartValidation,
            "SEMICONDUCTORWEAROUT": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.SemiconductorWearout,
            "SOLDERJOINTFATIGUE": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.SolderJointFatigue,
            "THERMALDERATING": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.ThermalDerating,
            "THERMALMECH": SherlockAnalysisService_pb2.RunAnalysisRequest.Analysis.ThermalMech,
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
            "MECHANICALSHOCK", "RANDOMVIBE", "HOLETOHOLECAF", "COMPONENTFAILUREMODE",
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
