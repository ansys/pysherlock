# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

"""Module containing types for the Analysis Service."""

try:
    import SherlockAnalysisService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2

analysis_service = SherlockAnalysisService_pb2


class ElementOrder:
    """Values for Element Order."""

    LINEAR = analysis_service.ElementOrder.Linear
    QUADRATIC = analysis_service.ElementOrder.Quadratic
    SOLID_SHELL = analysis_service.ElementOrder.SolidShell


class ModelSource:
    """Values for Model Source."""

    GENERATED = analysis_service.ModelSource.GENERATED
    STRAIN_MAP = analysis_service.ModelSource.STRAIN_MAP


class RunAnalysisRequestAnalysisType:
    """Values for type of analysis in the Run Analysis request."""

    __analysis_type = analysis_service.RunAnalysisRequest.Analysis.AnalysisType
    NATURAL_FREQ = __analysis_type.NaturalFreq
    HARMONIC_VIBE = __analysis_type.HarmonicVibe
    ICT = __analysis_type.ICTAnalysis
    MECHANICAL_SHOCK = __analysis_type.MechanicalShock
    RANDOM_VIBE = __analysis_type.RandomVibe
    COMPONENT_FAILURE_MODE = __analysis_type.ComponentFailureMode
    DFMEA = __analysis_type.DFMEAModule
    PTH_FATIQUE = __analysis_type.PTHFatigue
    PART_VALIDATION = __analysis_type.PartValidation
    SEMICINDUCTOR_WEAROUT = __analysis_type.SemiconductorWearout
    SOLDER_JOINT_FATIGUE = __analysis_type.SolderJointFatigue
    THERMAL_DERATING = __analysis_type.ThermalDerating
    THERMAL_MECH = __analysis_type.ThermalMech


class RunStrainMapAnalysisRequestAnalysisType:
    """Values for type of analysis in the Run Strain Map Analysis request."""

    __analysis_type = analysis_service.RunStrainMapAnalysisRequest.StrainMapAnalysis.AnalysisType
    RANDOM_VIBE = __analysis_type.RandomVibe


class UpdatePcbModelingPropsRequestAnalysisType:
    """Values for type of analysis in the Update PCB Modeling Properties Analysis request."""

    __analysis_type = analysis_service.UpdatePcbModelingPropsRequest.Analysis.AnalysisType
    HARMONIC_VIBE = __analysis_type.HarmonicVibe
    ICT = __analysis_type.ICTAnalysis
    MECHANICAL_SHOCK = __analysis_type.MechanicalShock
    NATURAL_FREQUENCY = __analysis_type.NaturalFreq
    RANDOM_VIBE = __analysis_type.RandomVibe
    THERMAL_MECH = __analysis_type.ThermalMech


class UpdatePcbModelingPropsRequestPcbMaterialModel:
    """Values for PCB Material Model in the Update PCB Modeling Properties Analysis request."""

    __material_model = analysis_service.UpdatePcbModelingPropsRequest.Analysis.PcbMaterialModel
    UNIFORM = __material_model.Uniform
    LAYERED = __material_model.Layered
    UNIFORM_ELEMENTS = __material_model.UniformElements
    LAYERED_ELEMENTS = __material_model.LayeredElements


class UpdatePcbModelingPropsRequestPcbModelType:
    """Values for PCB Model Type in the Update PCB Modeling Properties Analysis request."""

    __model_type = analysis_service.UpdatePcbModelingPropsRequest.Analysis.PcbModelType
    BONDED = __model_type.Bonded
