# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# © 2023 - 2024 ANSYS, Inc. All rights reserved
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
from ansys.sherlock.core.errors import SherlockCommonServiceError
from ansys.sherlock.core.types.common_types import ListUnitsRequestUnitType
from ansys.sherlock.core.utils.version_check import SKIP_VERSION_CHECK


def test_all():
    """Test all common APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    common = Common(channel, SKIP_VERSION_CHECK)
    helper_test_list_units(common)
    helper_test_get_solders(common)
    helper_test_get_sherlock_info(common)
    helper_test_get_solder_info(common)


def helper_test_list_units(common: Common):
    """Test list_units API"""

    if common._is_connection_up():
        try:
            common.list_units(ListUnitsRequestUnitType.WEIGHT + 10000)
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockCommonServiceError

        try:
            units = common.list_units(ListUnitsRequestUnitType.ACCEL_DENSITY)
            assert len(units) != 0
        except SherlockCommonServiceError as e:
            pytest.fail(str(e))


def helper_test_get_solders(common: Common):
    """Test get_solders API"""

    if common._is_connection_up():
        try:
            solders = common.list_solder_materials()
            assert len(solders) != 0
        except SherlockCommonServiceError as e:
            pytest.fail(str(e))


def helper_test_get_sherlock_info(common: Common):
    """Test get_sherlock_info API"""

    if common._is_connection_up():
        try:
            sherlock_info_response = common.get_sherlock_info()
            assert sherlock_info_response is not None
        except Exception as e:
            pytest.fail(str(e))


def helper_test_get_solder_info(common: Common):
    """Test get_solder_info"""

    if common._is_connection_up():
        try:
            response = common.get_solder_info()
            assert len(response.solders) > 0
        except Exception as e:
            pytest.fail(str(e))


if __name__ == "__main__":
    test_all()
