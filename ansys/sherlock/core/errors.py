"""pysherlock specific errors"""

from builtins import Exception

LOCALHOST = "127.0.0.1"
SHERLOCK_DEFAULT_PORT = 9090


class SherlockCannotUsePortError(Exception):
    """Raised when the specified gRPC port cannot be used"""
    def __init__(self, port, error):
        self.port = port
        self.error = error

    def __str__(self):
        return f"Specified gRPC port {self.port} cannot be used: {self.error}"
