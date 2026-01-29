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

import grpc
import pytest

from ansys.sherlock.core.common import Common
from ansys.sherlock.core.errors import SherlockVersionError


def test_all():
    test_version_check()


def test_version_check():
    try:
        channel_param = "127.0.0.1:9090"
        channel = grpc.insecure_channel(channel_param)
        # Set Sherlock version to 24R2 which is before 25R1, when
        # "get_sherlock_version" was added to PySherlock / Sherlock.
        common = Common(channel, 242)
        # This should fail since it did not exist in 242
        common.get_sherlock_info()
        pytest.fail("Sherlock version should be too low to launch this method")
    except Exception as e:
        if not isinstance(e, SherlockVersionError):
            pytest.fail("Unexpected exception " + str(e))


def assert_float_equals(expected, actual):
    assert pytest.approx(actual, abs=1e-14) == pytest.approx(expected, abs=1e-14)


if __name__ == "__main__":
    test_all()
