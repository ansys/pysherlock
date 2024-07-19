# © 2024 ANSYS, Inc. All rights reserved.

"""Module containing types for the Common Service."""

try:
    import SherlockCommonService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2


class ListUnitsRequestUnitType:
    """Constants for Unit Type in the List Units request."""

    ACCEL_DENSITY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.ACCEL_DENSITY
    "ACCEL_DENSITY"
    ACCELERATION = SherlockCommonService_pb2.ListUnitsRequest.UnitType.ACCELERATION
    "ACCELERATION"
    AREA = SherlockCommonService_pb2.ListUnitsRequest.UnitType.AREA
    "AREA"
    BANDWIDTH = SherlockCommonService_pb2.ListUnitsRequest.UnitType.BANDWIDTH
    "BANDWIDTH"
    CAPACITANCE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.CAPACITANCE
    "CAPACITANCE"
    CTE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.CTE
    "CTE"
    CURRENT = SherlockCommonService_pb2.ListUnitsRequest.UnitType.CURRENT
    "CURRENT"
    DENSITY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.DENSITY
    "DENSITY"
    DISP_DENSITY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.DISP_DENSITY
    "DISP_DENSITY"
    FORCE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.FORCE
    "FORCE"
    FREQUENCY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.FREQUENCY
    "FREQUENCY"
    INDUCTANCE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.INDUCTANCE
    "INDUCTANCE"
    LENGTH = SherlockCommonService_pb2.ListUnitsRequest.UnitType.LENGTH
    "LENGTH"
    POWER = SherlockCommonService_pb2.ListUnitsRequest.UnitType.POWER
    "POWER"
    RESISTANCE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.RESISTANCE
    "RESISTANCE"
    SIZE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.SIZE
    "SIZE"
    SPECIFIC_HEAT = SherlockCommonService_pb2.ListUnitsRequest.UnitType.SPECIFIC_HEAT
    "SPECIFIC_HEAT"
    STRAIN = SherlockCommonService_pb2.ListUnitsRequest.UnitType.STRAIN
    "STRAIN"
    STRESS = SherlockCommonService_pb2.ListUnitsRequest.UnitType.STRESS
    "STRESS"
    TEMPERATURE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.TEMPERATURE
    "TEMPERATURE"
    THERMAL_CONDUCTIVITY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.THERMAL_CONDUCTIVITY
    "THERMAL_CONDUCTIVITY"
    THERMAL_RESISTANCE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.THERMAL_RESISTANCE
    "THERMAL_RESISTANCE"
    TIME = SherlockCommonService_pb2.ListUnitsRequest.UnitType.TIME
    "TIME"
    VELOCITY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.VELOCITY
    "VELOCITY"
    VELOCITY_DENSITY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.VELOCITY_DENSITY
    "VELOCITY_DENSITY"
    VOLTAGE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.VOLTAGE
    "VOLTAGE"
    VOLUME = SherlockCommonService_pb2.ListUnitsRequest.UnitType.VOLUME
    "VOLUME"
    WEIGHT = SherlockCommonService_pb2.ListUnitsRequest.UnitType.WEIGHT
    "WEIGHT"


class TableDelimiter:
    """Types of delimiters that can be used for exporting tables."""

    COMMA = SherlockCommonService_pb2.TableDelimiter.COMMA
    """COMMA"""
    SPACE = SherlockCommonService_pb2.TableDelimiter.SPACE
    """SPACE"""
    TAB = SherlockCommonService_pb2.TableDelimiter.TAB
    """TAB"""
    SEMICOLON = SherlockCommonService_pb2.TableDelimiter.SEMICOLON
    """SEMICOLON"""


class Measurement:
    """Contains the properties of the measurement."""

    def __init__(self, value, unit):
        """Initialize the measurement properties."""
        self.value = value
        """value : float"""
        self.unit = unit
        """unit : string"""
