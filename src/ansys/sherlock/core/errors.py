"""pysherlock specific errors."""

from builtins import Exception

LOCALHOST = "127.0.0.1"
SHERLOCK_DEFAULT_PORT = 9090


class SherlockCannotUsePortError(Exception):
    """Raised when the specified gRPC port cannot be used."""

    def __init__(self, port, error):
        """Initialize error message."""
        self.port = port
        self.error = error

    def __str__(self):
        """Format error message."""
        return f"Specified gRPC port {self.port} cannot be used: {self.error}"


class SherlockConnectionError(Exception):
    """Raised when the Sherlock gRPC channel has not been established."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"gRPC connection error: {self.message}"


class SherlockDeleteProjectError(Exception):
    """Raised when deleting a project results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Delete project error: {self.message}"


class SherlockImportODBError(Exception):
    """Raised when importing ODB archive results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Import ODB error: {self.message}"


class SherlockImportIpc2581Error(Exception):
    """Raised when importing IPC2581 archive results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Import IPC2581 error: {self.message}"


class SherlockListCCAsError(Exception):
    """Raised when listing project CCAs results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"List CCAs error: {self.message}"


class SherlockListConductorLayersError(Exception):
    """Raised when listing project conductor layers results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"List conductor layer error: {self.message}"


class SherlockAddStrainMapsError(Exception):
    """Raised when adding strain maps for a project results in an error."""

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
    """Raised when listing strain maps for a project results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"List strain maps error: {self.message}"


class SherlockGenerateProjectReportError(Exception):
    """Raised when generating a project report results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Generate project report error: {self.message}"


class SherlockCreateLifePhaseError(Exception):
    """Raised when creating a life phase results in an error."""

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
    """Raised when adding a random vibe event results in an error."""

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
    """Raised when adding random vibe profiles results in an error."""

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
    """Raised when adding a thermal event results in an error."""

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
    """Raised when adding thermal profiles results in an error."""

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
    """Raised when adding a harmonic event results in an error."""

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
    """Raised when adding harmonic vibe profiles results in an error."""

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
    """Raised when adding a shock event results in an error."""

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
    """Raised when adding shock profiles results in an error."""

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


class SherlockUpdateMountPointsByFileError(Exception):
    """Raised when updating mount points results in an error."""

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
    """Raised when generating a stackup resulted in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Generate stackup error: {self.message}"


class SherlockUpdateConductorLayerError(Exception):
    """Raised when updating a conductor layer resulted in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update conductor layer error: {self.message}"


class SherlockUpdateLaminateLayerError(Exception):
    """Raised when updating a laminate layer resulted in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update laminate layer error: {self.message}"


class SherlockUpdatePartsListError(Exception):
    """Raised when updating a parts list results in an error."""

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
    """Raised when updating parts locations results in an error."""

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
    """Raised when updating parts locations by file results in an error."""

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
    """Raised when importing a parts list resulted in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Import parts list error: {self.message}"


class SherlockExportPartsListError(Exception):
    """Raised when exporting a parts list resulted in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Export parts list error: {self.message}"


class SherlockEnableLeadModelingError(Exception):
    """Raised when enabling lead modeling resulted in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Enable lead modeling error: {self.message}"


class SherlockRunAnalysisError(Exception):
    """Raised when running an analysis results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Run analysis error: {self.message}"


class SherlockRunStrainMapAnalysisError(Exception):
    """Raised when running a strain map analysis results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Run strain map analysis error: {self.message}"


class SherlockGetRandomVibeInputFieldsError(Exception):
    """Raised when getting the random vibe input fields results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Get random vibe input fields error: {self.message}"


class SherlockUpdateRandomVibePropsError(Exception):
    """Raised when updating the analysis properties for random vibe results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update random vibe properties error: {self.message}"


class SherlockUpdateNaturalFrequencyPropsError(Exception):
    """Raised when updating the analysis properties for natural frequency results in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Update natural frequency properties error: {self.message}"


class SherlockCommonServiceError(Exception):
    """Raised when executing an API in the common service resulted in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Sherlock common service error: {self.message}"


class SherlockModelServiceError(Exception):
    """Raised when executing an API in the model service resulted in an error."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return f"Sherlock model service error: {self.message}"


class SherlockInvalidLoadDirectionError(Exception):
    """Raised when an invalid load direction string is inputted."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidOrientationError(Exception):
    """Raised when an invalid orientation string is inputted."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidRandomVibeProfileEntriesError(Exception):
    """Raised when an invalid random vibe profile entry is inputted."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidThermalProfileEntriesError(Exception):
    """Raised when an invalid thermal profile entry is inputted."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidHarmonicProfileEntriesError(Exception):
    """Raised when an invalid harmonic profile entry is inputted."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidShockProfileEntriesError(Exception):
    """Raised when an invalid shock profile entry is inputted."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidLayerIDError(Exception):
    """Raised when an invalid layer ID is provided."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidMaterialError(Exception):
    """Raised when an invalid manufacturer/grade/material is provided."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidConductorPercentError(Exception):
    """Raised when an invalid conductor percent is provided."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidThicknessArgumentError(Exception):
    """Raised when invalid thickness arguments are provided."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidGlassConstructionError(Exception):
    """Raised when invalid glass construction arguments are provided."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message


class SherlockInvalidPhaseError(Exception):
    """Raised when invalid phase arguments are provided."""

    def __init__(self, message):
        """Initialize error message."""
        self.message = message

    def __str__(self):
        """Format error message."""
        return self.message
