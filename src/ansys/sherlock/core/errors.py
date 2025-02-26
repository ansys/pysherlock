# © 2024 ANSYS, Inc. All rights reserved

"""pysherlock specific errors."""

from builtins import Exception
from typing import Optional

LOCALHOST = "127.0.0.1"
SHERLOCK_DEFAULT_PORT = 9090


class SherlockNoGrpcConnectionException(Exception):
    """Contains the error raised when the Sherlock gRPC channel has not been established."""

    def __init__(self):
        """Initialize error message."""
        self.message = "No connection to Sherlock gRPC server."

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockCannotUsePortError(Exception):
    """Contains the error raised when the specified gRPC port cannot be used."""

    def __init__(self, port: int, error: str):
        """Initialize error message."""
        self.port = port
        self.error = error

    def __str__(self):
        """Format error message."""
        return f"Specified gRPC port {self.port} cannot be used: {self.error}"


class SherlockConnectionError(Exception):
    """Contains the error raised when the Sherlock gRPC channel has not been established."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"gRPC connection error: {self.message}"


class SherlockDeleteProjectError(Exception):
    """Contains the error raised when a project cannot be deleted."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Delete project error: {self.message}"


class SherlockImportODBError(Exception):
    """Contains the error raised when an ODB archive cannot be imported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Import ODB error: {self.message}"


class SherlockImportIpc2581Error(Exception):
    """Contains the error raised when an IPC2581 archive cannot be imported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Import IPC2581 error: {self.message}"


class SherlockListCCAsError(Exception):
    """Contains the errors raised when a project's CCAs results cannot be listed."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"List CCAs error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"List CCAs error: {self.message}"]


class SherlockListConductorLayersError(Exception):
    """Contains the error raised when a project's conductor layers cannot be listed."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"List conductor layer error: {self.message}"


class SherlockListLaminateLayersError(Exception):
    """Contains the error raised when a project's laminate layers cannot be listed."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"List laminate layer error: {self.message}"


class SherlockGetStackupPropsError(Exception):
    """Contains the error raised when getting stackup properties."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Get stackup prop error: {self.message}"


class SherlockGetLayerCountError(Exception):
    """Contains the error raised when getting layer count."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Get layer count error: {self.message}"


class SherlockGetTotalConductorThicknessError(Exception):
    """Contains the error raised when getting total conductor thickness."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Get total conductor thickness error: {self.message}"


class SherlockAddStrainMapsError(Exception):
    """Contains the errors raised when strain maps cannot be added to the project."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Add strain maps error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Add strain maps error: {self.message}"]


class SherlockListStrainMapsError(Exception):
    """Contains the errors raised when strain maps for a project cannot be listed."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Format error message."""
        if self.message is None:
            return [f"List strain maps error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"List strain maps error: {self.message}"]


class SherlockGenerateProjectReportError(Exception):
    """Contains the error raised when project report cannot be generated."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Generate project report error: {self.message}"


class SherlockCreateLifePhaseError(Exception):
    """Contains the errors raised when a life phase cannot be created."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Create life phase error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Create life phase error: {self.message}"]


class SherlockAddRandomVibeEventError(Exception):
    """Contains the errors raised when a random vibe event cannot be added."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Add random vibe event error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Add random vibe event error: {self.message}"]


class SherlockAddRandomVibeProfilesError(Exception):
    """Contains the errors raised when random vibe profiles cannot be added."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Add random vibe profiles error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Add random vibe profiles error: {self.message}"]


class SherlockAddThermalEventError(Exception):
    """Contains the errors raised when a thermal event cannot be added."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Add thermal event error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Add thermal event error: {self.message}"]


class SherlockAddThermalProfilesError(Exception):
    """Creates the errors raised when thermal profiles cannot be added."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Add thermal profiles error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Add thermal profiles error: {self.message}"]


class SherlockAddHarmonicEventError(Exception):
    """Contains the errors raised when a harmonic event cannot be added."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Add harmonic event error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Add harmonic event error: {self.message}"]


class SherlockAddHarmonicVibeProfilesError(Exception):
    """Contains the errors raised when harmonic vibe profiles cannot be added."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Add harmonic vibe profiles error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Add harmonic vibe profiles error: {self.message}"]


class SherlockAddShockEventError(Exception):
    """Contains the errors raised when a shock event cannot be added."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Add shock event error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Add shock event error: {self.message}"]


class SherlockAddShockProfilesError(Exception):
    """Contains the errors raised when shock profiles cannot be added."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Add shock profiles error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Add shock profiles error: {self.message}"]


class SherlockLoadRandomVibeProfileError(Exception):
    """Contains the error raised when loading random vibe properties."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Load random vibe profile error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Load random vibe profile error: {self.message}"]


class SherlockLoadHarmonicProfileError(Exception):
    """Contains the error raised when loading a harmonic profile."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Load harmonic profile error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Load harmonic profile error: {self.message}"]


class SherlockUpdateMountPointsByFileError(Exception):
    """Contains the errors raised when mount points cannot be updated."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Update mount points by file error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Update mount points by file error: {self.message}"]


class SherlockGenStackupError(Exception):
    """Contains the error raised when a stackup cannot be generated."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Generate stackup error: {self.message}"


class SherlockUpdateConductorLayerError(Exception):
    """Contains the error raised when a conductor layer cannot be updated."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update conductor layer error: {self.message}"


class SherlockUpdateLaminateLayerError(Exception):
    """Contains the error raised when a laminate layer cannot be updated."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update laminate layer error: {self.message}"


class SherlockUpdatePartsListError(Exception):
    """Contains the errors raised when a parts list cannot be updated."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Update parts list error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Update parts list error: {self.message}"]


class SherlockUpdatePartsLocationsError(Exception):
    """Contains the errors raised when part locations cannot be updated."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Update parts locations error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Update parts locations error: {self.message}"]


class SherlockUpdatePartsLocationsByFileError(Exception):
    """Contains the errors raised when part locations cannot be updated by file results."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Update parts locations by file error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Update parts locations by file error: {self.message}"]


class SherlockImportPartsListError(Exception):
    """Contains the error raised when a parts list cannot be imported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Import parts list error: {self.message}"


class SherlockExportPartsListError(Exception):
    """Contains the error raised when a parts list cannot be exported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Export parts list error: {self.message}"


class SherlockEnableLeadModelingError(Exception):
    """Contains the error raised when lead modeling cannot be enabled."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Enable lead modeling error: {self.message}"


class SherlockGetPartLocationError(Exception):
    """Contains the error raised when getting part location results in an error."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Get part location error: {self.message}"


class SherlockLoadThermalProfileError(Exception):
    """Contains the error raised when loading thermal profile."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Load thermal profile error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Load thermal profile error: {self.message}"]


class SherlockRunAnalysisError(Exception):
    """Contains the error raised when an analysis cannot be run."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Run analysis error: {self.message}"


class SherlockRunStrainMapAnalysisError(Exception):
    """Contains the error raised when a strain map analysis cannot be run."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Run strain map analysis error: {self.message}"


class SherlockUpdateRandomVibePropsError(Exception):
    """Contains the error raised when properties for random vibe results cannot be updated."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update random vibe properties error: {self.message}"


class SherlockLoadShockProfileDatasetError(Exception):
    """Contains the error raised when loading shock profile dataset results in an error."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Load shock profile dataset error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Load shock profile dataset error: {self.message}"]


class SherlockUpdateNaturalFrequencyPropsError(Exception):
    """Contains the error raised when properties for natural frequency results cannot be updated."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update natural frequency properties error: {self.message}"


class SherlockCommonServiceError(Exception):
    """Contains the error raised when an API in the common service cannot be executed."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Sherlock common service error: {self.message}"


class SherlockModelServiceError(Exception):
    """Contains the error raised when an API in the model service cannot be executed."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Model service error: {self.message}"


class SherlockExportAEDBError(Exception):
    """Contains the error raised when an Electronics Desktop model cannot be exported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Export AEDB error: {self.message}"


class SherlockInvalidLoadDirectionError(Exception):
    """Contains the error raised when the load direction string is invalid."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidOrientationError(Exception):
    """Contains the error raised when an orientation string is invalid."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidRandomVibeProfileEntriesError(Exception):
    """Contains the error raised when a random vibe profile is invalid."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidThermalProfileEntriesError(Exception):
    """Contains the error raised when a thermal profile entry is invalid."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidHarmonicProfileEntriesError(Exception):
    """Contains the error raised when a harmonic profile entry is invalid."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidShockProfileEntriesError(Exception):
    """Contains the error raised when a shock profile entry is invalid."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidLayerIDError(Exception):
    """Contains the error raised when a layer ID is invalid."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidMaterialError(Exception):
    """Contains the error raised when a manufacturer/grade/material combination is invalid."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidConductorPercentError(Exception):
    """Contains the error raised when a conductor percent is invalid."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidThicknessArgumentError(Exception):
    """Contains the error raised when the thickness is invalid."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidGlassConstructionError(Exception):
    """Contains the error raised when the glass construction is invalid."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockLoadShockProfilePulsesError(Exception):
    """Contains the error raised when loading shock profile pulses."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Load shock profile pulses error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Load shock profile pulses error: {self.message}"]


class SherlockUpdatePcbModelingPropsError(Exception):
    """Contains the error raised when updating pcb modeling properties results in an error."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Initialize error message."""
        return f"Update PCB Modeling Error: {self.message}"


class SherlockUpdateHarmonicVibePropsError(Exception):
    """Contains the error raised when properties for harmonic vibe analysis cannot be updated."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update harmonic vibe properties error: {self.message}"


class SherlockUpdateICTAnalysisPropsError(Exception):
    """Contains the error raised when properties for ICT analysis cannot be updated."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update ICT analysis properties error: {self.message}"


class SherlockUpdateMechanicalShockPropsError(Exception):
    """Contains the error raised when properties for mechanical shock analysis cannot be updated."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update mechanical shock properties error: {self.message}"


class SherlockUpdatePartListValidationAnalysisPropsError(Exception):
    """Contains the error raised when part list validation analysis properties cannot be updated."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update part list validation analysis properties error: {self.message}"


class SherlockUpdateSolderFatiguePropsError(Exception):
    """Contains the error raised when properties for solder fatigue analysis cannot be updated."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update solder fatigue properties error: {self.message}"


class SherlockAddProjectError(Exception):
    """Contains the error raised when Project cannot be added."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Add project error: {self.message}"


class SherlockAddCCAError(Exception):
    """Contains the error raised when CCA cannot be added."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Add CCA error: {self.message}"


class SherlockAddPottingRegionError(Exception):
    """Contains the error raised when a potting region cannot be added."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Add potting region error: {self.message}"


class SherlockUpdatePartModelingPropsError(Exception):
    """Contains the error raised when part modeling properties cannot be updated."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update part modeling props error: {self.message}"


class SherlockUpdatePartsFromAVLError(Exception):
    """Contains the error raised when parts list cannot be updated by AVL."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Update part from AVL error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Update part from AVL error: {self.message}"]


class SherlockListThermalMapsError(Exception):
    """Contains the errors raised when thermal map files for a project cannot be listed."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Format error message."""
        if self.message is None:
            return [f"List thermal maps error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"List thermal maps error: {self.message}"]


class SherlockUpdateThermalMapsError(Exception):
    """Contains the errors raised when thermal map files for a project cannot be updated."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Format error message."""
        if self.message is None:
            return [f"Update thermal maps error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Update thermal maps error: {self.message}"]


class SherlockAddThermalMapsError(Exception):
    """Contains the errors raised when thermal map files for a project cannot be added."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Format error message."""
        if self.message is None:
            return [f"Add thermal maps error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Add thermal maps error: {self.message}"]


class SherlockImportProjectZipArchiveError(Exception):
    """Contains the error raised when a .zip project archive cannot be imported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Import zipped project archive error: {self.message}"


class SherlockImportProjectZipArchiveSingleModeError(Exception):
    """Contains the error raised when a .zip project archive cannot be imported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Import zipped project archive error: {self.message}"


class SherlockUpdatePartsListPropertiesError(Exception):
    """Contains the errors raised when a parts list properties cannot be updated."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Format error message."""
        if self.message is None:
            return [f"Update parts list properties error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Update parts list properties error: {self.message}"]


class SherlockExportNetListError(Exception):
    """Contains the error raised when a net list cannot be exported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Export net list error: {self.message}"


class SherlockExportProjectError(Exception):
    """Contains the error raised when a project cannot be exported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Export project error : {self.message}"


class SherlockDeleteAllMountPointsError(Exception):
    """Contains the error raised when the mount points cannot be deleted."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Delete mount points error: {self.message}"


class SherlockDeleteAllICTFixturesError(Exception):
    """Contains the error raised when the ICT fixtures cannot be deleted."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Delete ict fixtures error: {self.message}"


class SherlockDeleteAllTestPointsError(Exception):
    """Contains the error raised when the test points cannot be deleted."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Delete test points error: {self.message}"


class SherlockUpdateTestPointsByFileError(Exception):
    """Contains the errors raised when test points cannot be updated."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Update test points by file error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Update test points by file error: {self.message}"]


class SherlockUpdateTestFixturesByFileError(Exception):
    """Contains the errors raised when test fixtures cannot be updated."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Update test fixtures by file error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Update test fixtures by file error: {self.message}"]


class SherlockExportAllTestPointsError(Exception):
    """Contains the errors raised when test points cannot be exported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Export test points error: {self.message}"


class SherlockExportAllTestFixtures(Exception):
    """Contains the errors raised when test fixtures cannot be exported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Export test fixtures error: {self.message}"


class SherlockExportAllMountPoints(Exception):
    """Contains the errors raised when mount points cannot be exported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Export mount points error: {self.message}"


class SherlockCreateCCAFromModelingRegionError(Exception):
    """Contains the error raised when a CCA cannot be created from a modeling region."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Create CCA from modeling region error: {self.message}"


class SherlockExportFEAModelError(Exception):
    """Contains the error raised when a FEA model cannot be exported."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Export FEA model error: {self.message}"


class SherlockAddModelingRegionError(Exception):
    """Contains the errors raised when modeling regions for a project cannot be added."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Format error message."""
        if self.message is None:
            return [f"Add modeling region error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Add modeling region error: {self.message}"]


class SherlockUpdateModelingRegionError(Exception):
    """Contains the errors raised when modeling regions for a project cannot be updated."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Format error message."""
        if self.message is None:
            return [f"Update modeling region error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Update modeling region error: {self.message}"]


class SherlockCopyModelingRegionError(Exception):
    """Contains the errors raised when modeling regions for a project cannot be copied."""

    def __init__(self, message: Optional[str] = None, error_array: Optional[list[str]] = None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Format error message."""
        if self.message is None:
            return [f"Copy modeling region error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Copy modeling region error: {self.message}"]


class SherlockGetPartsListValidationAnalysisPropsError(Exception):
    """Contains the error raised when getting parts list validation properties."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Get parts list validation analysis properties error: {self.message}"


class SherlockDeleteModelingRegionError(Exception):
    """Contains the error raised when the modeling regions cannot be deleted."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Delete modeling region error: {self.message}"


class SherlockVersionError(Exception):
    """Contains the error raised when an incompatible Sherlock version is being used."""

    def __init__(self, message: str):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Sherlock Version Error: {self.message}"
