
import grpc

from ansys.sherlock.core.errors import (
    SherlockCommonServiceError,
)
from ansys.sherlock.core.common import Common


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
        common.list_units("NOTHING")
        assert False
    except SherlockCommonServiceError as e:
        assert str(e) == "Sherlock common service error: Invalid unit type 'NOTHING' specified"

    units = common.list_units("ACCEL_DENSITY")
    assert len(units) == 5 and "G2/Hz" in units
    units = common.list_units("ACCELERATION")
    assert len(units) == 5 and "G" in units
    units = common.list_units("AREA")
    assert len(units) == 4 and "in2" in units
    units = common.list_units("BANDWIDTH")
    assert len(units) == 4 and "Bps" in units
    units = common.list_units("CAPACITANCE")
    assert len(units) == 10 and "pF" in units
    units = common.list_units("CTE")
    assert len(units) == 2 and "ppm/C" in units
    units = common.list_units("CURRENT")
    assert len(units) == 4 and "uA" in units
    units = common.list_units("DENSITY")
    assert len(units) == 15 and "g/cc" in units
    units = common.list_units("DISP_DENSITY")
    assert len(units) == 4 and "m2/Hz" in units
    units = common.list_units("FORCE")
    assert len(units) == 5 and 'N' in units
    units = common.list_units("FREQUENCY")
    assert len(units) == 4 and 'HZ' in units
    units = common.list_units("INDUCTANCE")
    assert len(units) == 5 and 'H' in units
    units = common.list_units("LENGTH")
    assert len(units) == 6 and 'in' in units
    units = common.list_units("POWER")
    assert len(units) == 12 and 'pW' in units
    units = common.list_units("RESISTANCE")
    assert len(units) == 11 and 'picoOhm' in units
    units = common.list_units("SIZE")
    assert len(units) == 18 and 'bit' in units
    units = common.list_units("SPECIFIC_HEAT")
    assert len(units) == 5 and 'J/kg-C' in units
    units = common.list_units("STRAIN")
    assert len(units) == 3 and 'µε' in units
    units = common.list_units("STRESS")
    assert len(units) == 5 and 'MPA' in units
    units = common.list_units("TEMPERATURE")
    assert len(units) == 3 and 'C' in units
    units = common.list_units("THERMAL_CONDUCTIVITY")
    assert len(units) == 7 and 'W/m-K' in units
    units = common.list_units("THERMAL_RESISTANCE")
    assert len(units) == 1 and 'C/W' in units
    units = common.list_units("TIME")
    assert len(units) == 6 and 'ms' in units
    units = common.list_units("VELOCITY")
    assert len(units) == 4 and 'm/s' in units
    units = common.list_units("VELOCITY_DENSITY")
    assert len(units) == 4 and 'm2/s2/Hz' in units
    units = common.list_units("VOLTAGE")
    assert len(units) == 11 and 'pV' in units
    units = common.list_units("VOLUME")
    assert len(units) == 6 and 'cc' in units
    units = common.list_units("WEIGHT")
    assert len(units) == 5 and 'mg' in units


if __name__ == "__main__":
    test_all()
