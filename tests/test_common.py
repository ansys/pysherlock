# © 2023 ANSYS, Inc. All rights reserved

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


def helper_test_list_units(common):
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


def helper_test_get_solders(common):
    """Test get_solders API"""

    if common._is_connection_up():
        try:
            solders = common.list_solder_materials()
            assert len(solders) != 0
        except SherlockCommonServiceError as e:
            pytest.fail(str(e))


if __name__ == "__main__":
    test_all()
