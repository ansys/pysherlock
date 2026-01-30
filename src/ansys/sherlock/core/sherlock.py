# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
