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


class SherlockDeleteProjectError(Exception):
    """Raised when deleting an error results in an error."""

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
