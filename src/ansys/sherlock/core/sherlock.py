# © 2023 ANSYS, Inc. All rights reserved

"""Module for the gRPC connection object."""
from ansys.sherlock.core.analysis import Analysis
from ansys.sherlock.core.common import Common
from ansys.sherlock.core.layer import Layer
from ansys.sherlock.core.lifecycle import Lifecycle
from ansys.sherlock.core.model import Model
from ansys.sherlock.core.parts import Parts
from ansys.sherlock.core.project import Project
from ansys.sherlock.core.stackup import Stackup


class Sherlock:
    """Sherlock gRPC connection object."""

    def __init__(self, channel):
        """Initialize Sherlock gRPC connection object."""
        self.common = Common(channel)
        self.model = Model(channel)
        self.project = Project(channel)
        self.lifecycle = Lifecycle(channel)
        self.layer = Layer(channel)
        self.stackup = Stackup(channel)
        self.parts = Parts(channel)
        self.analysis = Analysis(channel)
