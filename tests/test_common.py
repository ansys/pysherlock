# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

import grpc
import pytest

from ansys.sherlock.core.common import Common
from ansys.sherlock.types.common_types import ListUnitsRequestUnitType


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

    units = common.list_units(ListUnitsRequestUnitType.ACCEL_DENSITY)
    assert len(units) == 5 and "G2/Hz" in units
    units = common.list_units(ListUnitsRequestUnitType.ACCELERATION)
    assert len(units) == 5 and "G" in units
    units = common.list_units(ListUnitsRequestUnitType.AREA)
    assert len(units) == 4 and "in2" in units
    units = common.list_units(ListUnitsRequestUnitType.BANDWIDTH)
    assert len(units) == 4 and "Bps" in units
    units = common.list_units(ListUnitsRequestUnitType.CAPACITANCE)
    assert len(units) == 10 and "pF" in units
    units = common.list_units(ListUnitsRequestUnitType.CTE)
    assert len(units) == 2 and "ppm/C" in units
    units = common.list_units(ListUnitsRequestUnitType.CURRENT)
    assert len(units) == 4 and "uA" in units
    units = common.list_units(ListUnitsRequestUnitType.DENSITY)
    assert len(units) == 15 and "g/cc" in units
    units = common.list_units(ListUnitsRequestUnitType.DISP_DENSITY)
    assert len(units) == 4 and "m2/Hz" in units
    units = common.list_units(ListUnitsRequestUnitType.FORCE)
    assert len(units) == 5 and "N" in units
    units = common.list_units(ListUnitsRequestUnitType.FREQUENCY)
    assert len(units) == 4 and "HZ" in units
    units = common.list_units(ListUnitsRequestUnitType.INDUCTANCE)
    assert len(units) == 5 and "H" in units
    units = common.list_units(ListUnitsRequestUnitType.LENGTH)
    assert len(units) == 6 and "in" in units
    units = common.list_units(ListUnitsRequestUnitType.POWER)
    assert len(units) == 12 and "pW" in units
    units = common.list_units(ListUnitsRequestUnitType.RESISTANCE)
    assert len(units) == 11 and "picoOhm" in units
    units = common.list_units(ListUnitsRequestUnitType.SIZE)
    assert len(units) == 18 and "bit" in units
    units = common.list_units(ListUnitsRequestUnitType.SPECIFIC_HEAT)
    assert len(units) == 5 and "J/kg-C" in units
    units = common.list_units(ListUnitsRequestUnitType.STRAIN)
    assert len(units) == 3 and "µε" in units
    units = common.list_units(ListUnitsRequestUnitType.STRESS)
    assert len(units) == 5 and "MPA" in units
    units = common.list_units(ListUnitsRequestUnitType.TEMPERATURE)
    assert len(units) == 3 and "C" in units
    units = common.list_units(ListUnitsRequestUnitType.THERMAL_CONDUCTIVITY)
    assert len(units) == 7 and "W/m-K" in units
    units = common.list_units(ListUnitsRequestUnitType.THERMAL_RESISTANCE)
    assert len(units) == 1 and "C/W" in units
    units = common.list_units(ListUnitsRequestUnitType.TIME)
    assert len(units) == 6 and "ms" in units
    units = common.list_units(ListUnitsRequestUnitType.VELOCITY)
    assert len(units) == 4 and "m/s" in units
    units = common.list_units(ListUnitsRequestUnitType.VELOCITY_DENSITY)
    assert len(units) == 4 and "m2/s2/Hz" in units
    units = common.list_units(ListUnitsRequestUnitType.VOLTAGE)
    assert len(units) == 11 and "pV" in units
    units = common.list_units(ListUnitsRequestUnitType.VOLUME)
    assert len(units) == 6 and "cc" in units
    units = common.list_units(ListUnitsRequestUnitType.WEIGHT)
    assert len(units) == 5 and "mg" in units
    try:
        units = common.list_units(ListUnitsRequestUnitType.ACCEL_DENSITY)
        assert len(units) != 0
    except Exception as e:
        pytest.fail(str(e))


if __name__ == "__main__":
    test_all()
