# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

"""Module for the gRPC connection object."""

import grpc

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

    def __init__(self, channel: grpc.Channel, server_version: int):
        """Initialize Sherlock gRPC connection object."""
        self.common = Common(channel, server_version)
        self.model = Model(channel, server_version)
        self.project = Project(channel, server_version)
        self.lifecycle = Lifecycle(channel, server_version)
        self.layer = Layer(channel, server_version)
        self.stackup = Stackup(channel, server_version)
        self.parts = Parts(channel, server_version)
        self.analysis = Analysis(channel, server_version)
