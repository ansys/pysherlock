# © 2024 ANSYS, Inc. All rights reserved.

"""Module containing types for the Model Service."""

try:
    import SherlockModelService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockModelService_pb2

model_service = SherlockModelService_pb2


class ExportFEAModelAnalysisType:
    """Constants for type of analysis in the Export FEA Model request."""

    __analysis_type = model_service.ExportFEAModelRequest.ExportAnalysis
    NATURAL_FREQUENCY = __analysis_type.NaturalFreq
    HARMONIC_VIBE = __analysis_type.HarmonicVibe
    ICT = __analysis_type.ICTAnalysis
    MECHANICAL_SHOCK = __analysis_type.MechanicalShock
    RANDOM_VIBE = __analysis_type.RandomVibe


class MinHoleDiameter:
    """Constants for minimim hole diameter in the Export FEA Model request."""

    def __init__(self, value, unit):
        """Initialize the minimum hole diameter properties."""
        self.value = value
        """value of the miminum diameter hole : float"""
        self.unit = unit
        """unit of the minimum diameter hole : string"""


class MaxEdgeLength:
    """Constants for maximum edge length in the Export FEA Model request."""

    def __init__(self, value, unit):
        """Initialize the maximum edge length properties."""
        self.value = value
        """value of the maximum edge length : float"""
        self.unit = unit
        """unit of the maximum edge length : string"""


class MaxMeshSize:
    """Constants for maximum mesh size in the Export FEA Model request."""

    def __init__(self, value, unit):
        """Initialize the maximum mesh size properties."""
        self.value = value
        """value of the maximum mesh size : float"""
        self.unit = unit
        """unit of the maximum mesh size : string"""


class VerticalMeshSize:
    """Constants for vertical mesh size in the Export FEA Model request."""

    def __init__(self, value, unit):
        """Initialize the vertical mesh size properties."""
        self.value = value
        """value of the vertical mesh size : float"""
        self.unit = unit
        """unit of the vertical mesh size : string"""
