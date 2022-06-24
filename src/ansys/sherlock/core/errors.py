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
        else:
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
        else:
            assert self.error_array is None
            return [f"Add random vibe event error: {self.message}"]


class SherlockAddRandomVibeProfileError(Exception):
    """Raised when adding a random vibe profile results in an error."""

    def __init__(self, message=None, error_array=None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Add random vibe profile error: {error}" for error in self.error_array]
        else:
            assert self.error_array is None
            return [f"Add random vibe profile error: {self.message}"]


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
        else:
            assert self.error_array is None
            return [f"Add thermal event error: {self.message}"]


class SherlockAddThermalProfileError(Exception):
    """Raised when adding a thermal profile results in an error."""

    def __init__(self, message=None, error_array=None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Add thermal profile error: {error}" for error in self.error_array]
        else:
            assert self.error_array is None
            return [f"Add thermal profile error: {self.message}"]


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
        else:
            assert self.error_array is None
            return [f"Add harmonic event error: {self.message}"]


class SherlockAddHarmonicProfileError(Exception):
    """Raised when adding a harmonic profile results in an error."""

    def __init__(self, message=None, error_array=None):
        """Initialize error message."""
        self.message = message
        self.error_array = error_array

    def str_itr(self):
        """Create list of error messages."""
        if self.message is None:
            return [f"Add harmonic profile error: {error}" for error in self.error_array]
        else:
            assert self.error_array is None
            return [f"Add harmonic profile error: {self.message}"]


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
