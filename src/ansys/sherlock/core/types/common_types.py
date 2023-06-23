# © 2023 ANSYS, Inc. All rights reserved.

"""Module containing types for the Common Service."""

try:
    import SherlockCommonService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2


class ListUnitsRequestUnitType:
    """Constants for Unit Type in the List Units request."""

    ACCEL_DENSITY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.ACCEL_DENSITY
    ACCELERATION = SherlockCommonService_pb2.ListUnitsRequest.UnitType.ACCELERATION
    AREA = SherlockCommonService_pb2.ListUnitsRequest.UnitType.AREA
    BANDWIDTH = SherlockCommonService_pb2.ListUnitsRequest.UnitType.BANDWIDTH
    CAPACITANCE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.CAPACITANCE
    CTE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.CTE
    CURRENT = SherlockCommonService_pb2.ListUnitsRequest.UnitType.CURRENT
    DENSITY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.DENSITY
    DISP_DENSITY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.DISP_DENSITY
    FORCE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.FORCE
    FREQUENCY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.FREQUENCY
    INDUCTANCE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.INDUCTANCE
    LENGTH = SherlockCommonService_pb2.ListUnitsRequest.UnitType.LENGTH
    POWER = SherlockCommonService_pb2.ListUnitsRequest.UnitType.POWER
    RESISTANCE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.RESISTANCE
    SIZE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.SIZE
    SPECIFIC_HEAT = SherlockCommonService_pb2.ListUnitsRequest.UnitType.SPECIFIC_HEAT
    STRAIN = SherlockCommonService_pb2.ListUnitsRequest.UnitType.STRAIN
    STRESS = SherlockCommonService_pb2.ListUnitsRequest.UnitType.STRESS
    TEMPERATURE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.TEMPERATURE
    THERMAL_CONDUCTIVITY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.THERMAL_CONDUCTIVITY
    THERMAL_RESISTANCE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.THERMAL_RESISTANCE
    TIME = SherlockCommonService_pb2.ListUnitsRequest.UnitType.TIME
    VELOCITY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.VELOCITY
    VELOCITY_DENSITY = SherlockCommonService_pb2.ListUnitsRequest.UnitType.VELOCITY_DENSITY
    VOLTAGE = SherlockCommonService_pb2.ListUnitsRequest.UnitType.VOLTAGE
    VOLUME = SherlockCommonService_pb2.ListUnitsRequest.UnitType.VOLUME
    WEIGHT = SherlockCommonService_pb2.ListUnitsRequest.UnitType.WEIGHT
