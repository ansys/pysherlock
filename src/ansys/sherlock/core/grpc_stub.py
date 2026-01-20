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

"""Module for shared methods for the gRPC stubs."""
try:
    import SherlockCommonService_pb2
    import SherlockCommonService_pb2_grpc
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2_grpc
import grpc


class GrpcStub:
    """Provides the gRPC stub."""

    def __init__(self, channel: grpc.Channel, server_version: int):
        """Initialize the gRPC stub."""
        self.channel = channel
        self._server_version = server_version

    def _is_connection_up(self):
        try:
            stub = SherlockCommonService_pb2_grpc.SherlockCommonServiceStub(self.channel)
            stub.check(SherlockCommonService_pb2.HealthCheckRequest())
            return True
        except grpc.RpcError:
            return False
