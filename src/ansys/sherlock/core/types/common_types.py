# © 2024 ANSYS, Inc. All rights reserved.

"""Module containing types for the Common Service."""

try:
    import SherlockCommonService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2


def basic_str_validator(value: str, field_name: str):
    """Apply basic string validation."""
    if value is None or value == "":
        raise ValueError(field_name + " is invalid because it is None or empty.")
    return value


class ListUnitsRequestUnitType:
    """Constants for Unit Type in the List Units request."""

    __unit_type = SherlockCommonService_pb2.ListUnitsRequest.UnitType
    ACCEL_DENSITY = __unit_type.ACCEL_DENSITY
    "ACCEL_DENSITY"
    ACCELERATION = __unit_type.ACCELERATION
    "ACCELERATION"
    AREA = __unit_type.AREA
    "AREA"
    BANDWIDTH = __unit_type.BANDWIDTH
    "BANDWIDTH"
    CAPACITANCE = __unit_type.CAPACITANCE
    "CAPACITANCE"
    CTE = __unit_type.CTE
    "CTE"
    CURRENT = __unit_type.CURRENT
    "CURRENT"
    DENSITY = __unit_type.DENSITY
    "DENSITY"
    DISP_DENSITY = __unit_type.DISP_DENSITY
    "DISP_DENSITY"
    FORCE = __unit_type.FORCE
    "FORCE"
    FREQUENCY = __unit_type.FREQUENCY
    "FREQUENCY"
    INDUCTANCE = __unit_type.INDUCTANCE
    "INDUCTANCE"
    LENGTH = __unit_type.LENGTH
    "LENGTH"
    POWER = __unit_type.POWER
    "POWER"
    RESISTANCE = __unit_type.RESISTANCE
    "RESISTANCE"
    SIZE = __unit_type.SIZE
    "SIZE"
    SPECIFIC_HEAT = __unit_type.SPECIFIC_HEAT
    "SPECIFIC_HEAT"
    STRAIN = __unit_type.STRAIN
    "STRAIN"
    STRESS = __unit_type.STRESS
    "STRESS"
    TEMPERATURE = __unit_type.TEMPERATURE
    "TEMPERATURE"
    THERMAL_CONDUCTIVITY = __unit_type.THERMAL_CONDUCTIVITY
    "THERMAL_CONDUCTIVITY"
    THERMAL_RESISTANCE = __unit_type.THERMAL_RESISTANCE
    "THERMAL_RESISTANCE"
    TIME = __unit_type.TIME
    "TIME"
    VELOCITY = __unit_type.VELOCITY
    "VELOCITY"
    VELOCITY_DENSITY = __unit_type.VELOCITY_DENSITY
    "VELOCITY_DENSITY"
    VOLTAGE = __unit_type.VOLTAGE
    "VOLTAGE"
    VOLUME = __unit_type.VOLUME
    "VOLUME"
    WEIGHT = __unit_type.WEIGHT
    "WEIGHT"


class TableDelimiter:
    """Types of delimiters that can be used for exporting tables."""

    __table_delimiter = SherlockCommonService_pb2.TableDelimiter

    COMMA = __table_delimiter.COMMA
    "COMMA"
    SPACE = __table_delimiter.SPACE
    "SPACE"
    TAB = __table_delimiter.TAB
    "TAB"
    SEMICOLON = __table_delimiter.SEMICOLON
    "SEMICOLON"


class Measurement:
    """Contains the properties of the measurement."""

    def __init__(self, value: float, unit: str):
        """Initialize the measurement properties."""
        self.value = value
        """float: measurement value"""
        self.unit = unit
        """str: measurement units"""
