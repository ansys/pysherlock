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

"""Module containing types for the Stackup Service."""
try:
    import SherlockStackupService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockStackupService_pb2


class StackupProperties:
    """Stackup property values."""

    def __init__(self, properties: SherlockStackupService_pb2.GetStackupPropsResponse):
        """Initialize members from the properties."""
        self.board_dimension = properties.boardDimension
        self.board_thickness = properties.boardThickness
        self.density = properties.density
        self.conductor_layers_cnt = properties.conductorLayersCnt
        self.ctexy = properties.ctExy
        self.ctez = properties.ctEz
        self.exy = properties.exy
        self.ez = properties.ez
