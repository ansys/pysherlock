# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

"""pysherlock specific errors."""

from builtins import Exception

LOCALHOST = "127.0.0.1"
SHERLOCK_DEFAULT_PORT = 9090


class SherlockCannotUsePortError(Exception):
    """Contains the error raised when the specified gRPC port cannot be used."""

    def __init__(self, port, error):
        """Initialize error message."""
        self.port = port
        self.error = error

    def __str__(self):
        """Format error message."""
        return f"Specified gRPC port {self.port} cannot be used: {self.error}"


class SherlockConnectionError(Exception):
    """Contains the error raised when the Sherlock gRPC channel has not been established."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"gRPC connection error: {self.message}"


class SherlockDeleteProjectError(Exception):
    """Contains the error raised when a project cannot be deleted."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Delete project error: {self.message}"


class SherlockImportODBError(Exception):
    """Contains the error raised when an ODB archive cannot be imported."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Import ODB error: {self.message}"


class SherlockImportIpc2581Error(Exception):
    """Contains the error raised when an IPC2581 archive cannot be imported."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Import IPC2581 error: {self.message}"


class SherlockListCCAsError(Exception):
    """Contains the error raised when a project's CCAs results cannot be listed."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"List CCAs error: {self.message}"


class SherlockListConductorLayersError(Exception):
    """Contains the error raised when a project's conductor layers cannot be listed."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"List conductor layer error: {self.message}"


class SherlockListLaminateLayersError(Exception):
    """Contains the error raised when a project's laminate layers cannot be listed."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"List laminate layer error: {self.message}"


class SherlockGetStackupPropsError(Exception):
    """Raised when getting stackup properties results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Get stackup prop error: {self.message}"


class SherlockGetLayerCountError(Exception):
    """Raised when getting layer count results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Get layer count error: {self.message}"


class SherlockGetLayerCountError(Exception):
    """Raised when getting layer count results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Get layer count error: {self.message}"


class SherlockGetTotalConductorThicknessError(Exception):
    """Raised when getting total conductor thickness results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Get total conductor thickness error: {self.message}"


class SherlockAddStrainMapsError(Exception):
    """Contains the error raised when strain maps cannot be added to the project."""

    def __init__(self, message=None, error_array=None):
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
    """Provides the error raised when strain maps for a project cannot be listed."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"List strain maps error: {self.message}"


class SherlockGenerateProjectReportError(Exception):
    """Contains the error raised when project report cannot be generated."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Generate project report error: {self.message}"


class SherlockCreateLifePhaseError(Exception):
    """Contains the error raised when a life phase cannot be created."""

    def __init__(self, message=None, error_array=None):
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
    """Contains the error raised when a random vibe event cannot be added."""

    def __init__(self, message=None, error_array=None):
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
    """Contains the error raised when random vibe profiles cannot be added."""

    def __init__(self, message=None, error_array=None):
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
    """Contains the error raised when a thermal event cannot be added."""

    def __init__(self, message=None, error_array=None):
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
    """Creates the error raised when thermal profiles cannot be added."""

    def __init__(self, message=None, error_array=None):
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
    """Contains the error raised when a harmonic event cannot be added."""

    def __init__(self, message=None, error_array=None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Create life phase error: {error}" for error in self.error_array]

        assert self.error_array is None
        return [f"Add harmonic event error: {self.message}"]


class SherlockAddHarmonicVibeProfilesError(Exception):
    """Contains the error raised when harmonic vibe profiles cannot be added."""

    def __init__(self, message=None, error_array=None):
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
    """Contains the error raised when a shock event cannot be added."""

    def __init__(self, message=None, error_array=None):
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
    """Contains the error raised when shock profiles cannot be added."""

    def __init__(self, message=None, error_array=None):
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
    """Raised when loading random vibe properties results in an error."""

    def __init__(self, message):
        """Initialize Error Message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Load random vibe profile error: {self.message}"


class SherlockLoadHarmonicProfileError(Exception):
    """Raised when loading a harmonic profile results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format Error Message."""
        return f"Load Harmonic profile error: {self.message}"


class SherlockUpdateMountPointsByFileError(Exception):
    """Contains the error raised when mount points cannot be updated."""

    def __init__(self, message=None, error_array=None):
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

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Generate stackup error: {self.message}"


class SherlockUpdateConductorLayerError(Exception):
    """Contains the error raised when a conductor layer cannot be updated."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update conductor layer error: {self.message}"


class SherlockUpdateLaminateLayerError(Exception):
    """Contains the error raised when a laminate layer cannot be updated."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update laminate layer error: {self.message}"


class SherlockUpdatePartsListError(Exception):
    """Contains the error raised when a parts list cannot be updated."""

    def __init__(self, message=None, error_array=None):
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
    """Contains the error raised when part locations cannot be updated."""

    def __init__(self, message=None, error_array=None):
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
    """Contains the error raised when part locations cannot be updated by file results."""

    def __init__(self, message=None, error_array=None):
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

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Import parts list error: {self.message}"


class SherlockExportPartsListError(Exception):
    """Contains the error raised when a parts list cannot be exported."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Export parts list error: {self.message}"


class SherlockEnableLeadModelingError(Exception):
    """Contains the error raised when lead modeling cannot be enabled."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Enable lead modeling error: {self.message}"


class SherlockGetPartLocationError(Exception):
    """Raised when getting part location results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Get part location error: {self.message}"


class SherlockLoadThermalProfileError(Exception):
    """Raised when loading thermal profile results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Load thermal profile error: {self.message}"


class SherlockRunAnalysisError(Exception):
    """Contains the error raised when an analysis cannot be run."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Run analysis error: {self.message}"


class SherlockRunStrainMapAnalysisError(Exception):
    """Contains the error raised when a strain map analysis cannot be run."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Run strain map analysis error: {self.message}"


class SherlockGetRandomVibeInputFieldsError(Exception):
    """Contains the error raised when random vibe input fields cannot be returned."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Get random vibe input fields error: {self.message}"


class SherlockUpdateRandomVibePropsError(Exception):
    """Contains the error raised when properties for random vibe results cannot be updated."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update random vibe properties error: {self.message}"


class SherlockLoadShockProfileDatasetError(Exception):
    """Raised when loading shock profile dataset results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Initialize error message."""
        return f"Load shock profile dataset error: {self.message}"


class SherlockUpdateNaturalFrequencyPropsError(Exception):
    """Contains the error raised when properties for natural frequency results cannot be updated."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update natural frequency properties error: {self.message}"


class SherlockCommonServiceError(Exception):
    """Contains the error raised when an API in the common service cannot be executed."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Sherlock common service error: {self.message}"


class SherlockModelServiceError(Exception):
    """Contains the error raised when an API in the model service cannot be executed."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Sherlock model service error: {self.message}"


class SherlockInvalidLoadDirectionError(Exception):
    """Contains the error raised when the load direction string is invalid."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidOrientationError(Exception):
    """Contains the error raised when an orientation string is invalid."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidRandomVibeProfileEntriesError(Exception):
    """Contains the error raised when an random vibe profile is invalid."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidThermalProfileEntriesError(Exception):
    """Contains the error raised when a thermal profile entry is invalid."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidHarmonicProfileEntriesError(Exception):
    """Contains the error raised when an harmonic profile entry is invalid."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidShockProfileEntriesError(Exception):
    """Contains the error raised when a shock profile entry is invalid."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidLayerIDError(Exception):
    """Contains the error raised when an layer ID is invalid."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidMaterialError(Exception):
    """Contains the error raised when a manufacturer/grade/material are invalid."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidConductorPercentError(Exception):
    """Contains the error raised when a conductor percent is invalid."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidThicknessArgumentError(Exception):
    """Contains the error raised when thickness arguments are invalid."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidGlassConstructionError(Exception):
    """Contains the argument raised when glass construction arguments are invalid."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidPhaseError(Exception):
    """Contains the error raised when phase arguments are invalid."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message
