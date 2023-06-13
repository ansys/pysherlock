# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

import grpc
import pytest

from ansys.sherlock.core.common import Common
from ansys.sherlock.core.types.common_types import ListUnitsRequestUnitType


def test_all():
    """Test all common APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    common = Common(channel)
    helper_test_list_units(common)


def helper_test_list_units(common):
    """Test list_units API"""

    if not common._is_connection_up():
        return

    try:
        units = common.list_units(ListUnitsRequestUnitType.ACCEL_DENSITY)
        assert len(units) != 0
    except Exception as e:
        pytest.fail(str(e))


if __name__ == "__main__":
    test_all()
