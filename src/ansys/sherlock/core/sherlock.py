"""Module for the gRPC connection object."""
from ansys.sherlock.core.common import Common
from ansys.sherlock.core.lifecycle import Lifecycle
from ansys.sherlock.core.model import Model


class Sherlock:
    """Sherlock gRPC connection object."""

    def __init__(self, channel):
        """Initialize Sherlock gRPC connection object."""
        self.common = Common(channel)
        self.model = Model(channel)
        self.lifecycle = Lifecycle(channel)
