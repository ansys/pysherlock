# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.

"""Module containing types for the Analysis Service."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator

from ansys.sherlock.core.types.common_types import basic_str_validator

try:
    import SherlockAnalysisService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2

analysis_service = SherlockAnalysisService_pb2


class ElementOrder:
    """Constants for Element Order."""

    LINEAR = analysis_service.ElementOrder.Linear
    "LINEAR"
    QUADRATIC = analysis_service.ElementOrder.Quadratic
    "QUADRATIC"
    SOLID_SHELL = analysis_service.ElementOrder.SolidShell
    "SOLID_SHELL"


class ModelSource:
    """Constants for Model Source."""

    GENERATED = analysis_service.ModelSource.GENERATED
    "GENERATED"
    STRAIN_MAP = analysis_service.ModelSource.STRAIN_MAP
    "STRAIN_MAP"


class RunAnalysisRequestAnalysisType:
    """Constants for type of analysis in the Run Analysis request."""

    __analysis_type = analysis_service.RunAnalysisRequest.Analysis.AnalysisType
    NATURAL_FREQ = __analysis_type.NaturalFreq
    "NATURAL_FREQ"
    HARMONIC_VIBE = __analysis_type.HarmonicVibe
    "HARMONIC_VIBE"
    ICT = __analysis_type.ICTAnalysis
    "ICT"
    MECHANICAL_SHOCK = __analysis_type.MechanicalShock
    "MECHANICAL_SHOCK"
    RANDOM_VIBE = __analysis_type.RandomVibe
    "RANDOM_VIBE"
    COMPONENT_FAILURE_MODE = __analysis_type.ComponentFailureMode
    "COMPONENT_FAILURE_MODE"
    DFMEA = __analysis_type.DFMEAModule
    "DFMEA"
    PTH_FATIQUE = __analysis_type.PTHFatigue
    "PTH_FATIQUE"
    PART_VALIDATION = __analysis_type.PartValidation
    "PART_VALIDATION"
    SEMICINDUCTOR_WEAROUT = __analysis_type.SemiconductorWearout
    "SEMICINDUCTOR_WEAROUT"
    SOLDER_JOINT_FATIGUE = __analysis_type.SolderJointFatigue
    "SOLDER_JOINT_FATIGUE"
    THERMAL_DERATING = __analysis_type.ThermalDerating
    "THERMAL_DERATING"
    THERMAL_MECH = __analysis_type.ThermalMech
    "THERMAL_MECH"


class RunStrainMapAnalysisRequestAnalysisType:
    """Constants for type of analysis in the Run Strain Map Analysis request."""

    __analysis_type = analysis_service.RunStrainMapAnalysisRequest.StrainMapAnalysis.AnalysisType
    HARMONIC_VIBE = __analysis_type.HarmonicVibe
    "HARMONIC_VIBE"

    MECHANICAL_SHOCK = __analysis_type.MechanicalShock
    "MECHANICAL_SHOCK"

    RANDOM_VIBE = __analysis_type.RandomVibe
    "RANDOM_VIBE"


class UpdatePcbModelingPropsRequestAnalysisType:
    """Constants for type of analysis in the Update PCB Modeling Properties Analysis request."""

    __analysis_type = analysis_service.UpdatePcbModelingPropsRequest.Analysis.AnalysisType
    HARMONIC_VIBE = __analysis_type.HarmonicVibe
    "HARMONIC_VIBE"
    ICT = __analysis_type.ICTAnalysis
    "ICT"
    MECHANICAL_SHOCK = __analysis_type.MechanicalShock
    "MECHANICAL_SHOCK"
    NATURAL_FREQUENCY = __analysis_type.NaturalFreq
    "NATURAL_FREQUENCY"
    RANDOM_VIBE = __analysis_type.RandomVibe
    "RANDOM_VIBE"
    THERMAL_MECH = __analysis_type.ThermalMech
    "THERMAL_MECH"


class UpdatePcbModelingPropsRequestPcbMaterialModel:
    """Constants for PCB Material Model in the Update PCB Modeling Properties Analysis request."""

    __material_model = analysis_service.UpdatePcbModelingPropsRequest.Analysis.PcbMaterialModel
    UNIFORM = __material_model.Uniform
    "UNIFORM"
    LAYERED = __material_model.Layered
    "LAYERED"
    UNIFORM_ELEMENTS = __material_model.UniformElements
    "UNIFORM_ELEMENTS"
    LAYERED_ELEMENTS = __material_model.LayeredElements
    "LAYERED_ELEMENTS"


class UpdatePcbModelingPropsRequestPcbModelType:
    """Constants for PCB Model Type in the Update PCB Modeling Properties Analysis request."""

    __model_type = analysis_service.UpdatePcbModelingPropsRequest.Analysis.PcbModelType
    BONDED = __model_type.Bonded
    "BONDED"


class ComponentFailureMechanism(BaseModel):
    """Contains the properties of a component failure mechanism update request."""

    cca_name: str
    """Name of the CCA."""
    default_part_temp_rise: float
    """Default part temperature rise."""
    default_part_temp_rise_units: str
    """Default part temperature rise units."""
    part_temp_rise_min_enabled: bool
    """Whether part temperature rise value is applied to the minimum temperature defined in the
    thermal cycle."""
    part_validation_enabled: bool
    """Whether part validation should be performed."""

    def _convert_to_grpc(
        self,
    ) -> analysis_service.UpdateComponentFailureMechanismPropsRequest.ComponentFailureMechanism:

        grpc_data = (
            analysis_service.UpdateComponentFailureMechanismPropsRequest.ComponentFailureMechanism()
        )

        grpc_data.ccaName = self.cca_name
        grpc_data.defaultPartTempRise = self.default_part_temp_rise
        grpc_data.defaultPartTempRiseUnits = self.default_part_temp_rise_units
        grpc_data.partTempRiseMinEnabled = self.part_temp_rise_min_enabled
        grpc_data.partValidationEnabled = self.part_validation_enabled
        return grpc_data

    @field_validator("cca_name")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)


class UpdateComponentFailureMechanismPropsRequest(BaseModel):
    """Contains the properties of a component failure mechanism update per project."""

    project: str
    """Name of the Sherlock project."""
    component_failure_mechanism_properties_per_cca: list[ComponentFailureMechanism]
    """List of potting region data to update."""

    @field_validator("project")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(
        self,
    ) -> analysis_service.UpdateComponentFailureMechanismPropsRequest:
        request = analysis_service.UpdateComponentFailureMechanismPropsRequest()
        request.project = self.project
        for properties in self.component_failure_mechanism_properties_per_cca:
            request.componentFailureMechanismProperties.append(properties._convert_to_grpc())
        return request


class SemiconductorWearoutAnalysis(BaseModel):
    """Contains the properties of a semiconductor wearout analysis update request."""

    cca_name: str
    """Name of the CCA."""
    max_feature_size: float
    """Maximum feature size."""
    max_feature_size_units: str
    """Units of the maximum feature size."""
    part_temp_rise: float
    """Part temperature rise."""
    part_temp_rise_units: str
    """Units of the part temperature rise."""
    part_temp_rise_min_enabled: bool
    """Whether part temperature rise value is applied to the minimum temperature defined in the
    thermal cycle."""
    part_validation_enabled: bool
    """Whether part validation should be performed."""

    def _convert_to_grpc(
        self,
    ) -> (
        analysis_service.UpdateSemiconductorWearoutAnalysisPropsRequest.SemiconductorWearoutAnalysis
    ):

        request_class = analysis_service.UpdateSemiconductorWearoutAnalysisPropsRequest
        semiconductor_wearout_analysis = request_class.SemiconductorWearoutAnalysis
        grpc_data = semiconductor_wearout_analysis()

        grpc_data.ccaName = self.cca_name
        grpc_data.maxFeatureSize = self.max_feature_size
        grpc_data.maxFeatureSizeUnits = self.max_feature_size_units
        grpc_data.partTempRise = self.part_temp_rise
        grpc_data.partTempRiseUnits = self.part_temp_rise_units
        grpc_data.partTempRiseMinEnabled = self.part_temp_rise_min_enabled
        grpc_data.partValidationEnabled = self.part_validation_enabled
        return grpc_data

    @field_validator("cca_name", "max_feature_size_units", "part_temp_rise_units")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)


class UpdateSemiconductorWearoutAnalysisPropsRequest(BaseModel):
    """Contains the properties of a semiconductor wearout analysis update per project."""

    project: str
    """Name of the Sherlock project."""
    semiconductor_wearout_analysis_properties: list[SemiconductorWearoutAnalysis]
    """List of semiconductor wearout analysis properties to update."""

    @field_validator("project")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(
        self,
    ) -> analysis_service.UpdateSemiconductorWearoutAnalysisPropsRequest:
        request = analysis_service.UpdateSemiconductorWearoutAnalysisPropsRequest()
        request.project = self.project
        for properties in self.semiconductor_wearout_analysis_properties:
            request.semiconductorWearoutAnalysisProperties.append(properties._convert_to_grpc())
        return request


class UpdatePTHFatiguePropsRequestAnalysisType(Enum):
    """Constants for qualification choices in the Update PTH Fatigue Properties request."""

    __qualification = analysis_service.UpdatePTHFatiguePropsRequest.PTHFatigueAnalysis.Qualification
    NONE = __qualification.NONE
    "NONE"
    PER_LOT = __qualification.PER_LOT
    "PER_LOT"
    PRODUCT = __qualification.PRODUCT
    "PRODUCT"
    SUPPLIER = __qualification.SUPPLIER
    "SUPPLIER"


class PTHFatiguePropsAnalysis(BaseModel):
    """Contains the properties of a PTH fatigue analysis update request."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    cca_name: str
    """Name of the CCA."""
    qualification: Optional[UpdatePTHFatiguePropsRequestAnalysisType] = None
    """Qualification choice for IST/HATS."""  # noqa: E501
    pth_quality_factor: Optional[str] = None
    """Quality factor for PTH."""
    pth_wall_thickness: Optional[float] = None
    """Wall thickness of PTH."""
    pth_wall_thickness_units: Optional[str] = None
    """Units for PTH wall thickness."""
    min_hole_size: Optional[float] = None
    """Minimum hole size."""
    min_hole_size_units: Optional[str] = None
    """Units for minimum hole size."""
    max_hole_size: Optional[float] = None
    """Maximum hole size."""
    max_hole_size_units: Optional[str] = None
    """Units for maximum hole size."""

    def _convert_to_grpc(
        self,
    ) -> analysis_service.UpdatePTHFatiguePropsRequest.PTHFatigueAnalysis:
        grpc_data = analysis_service.UpdatePTHFatiguePropsRequest.PTHFatigueAnalysis()

        grpc_data.ccaName = self.cca_name
        if self.qualification is not None:
            grpc_data.qualification = self.qualification.value
        if self.pth_quality_factor is not None:
            grpc_data.pthQualityFactor = self.pth_quality_factor
        if self.pth_wall_thickness is not None:
            grpc_data.pthWallThickness = self.pth_wall_thickness
        if self.pth_wall_thickness_units is not None:
            grpc_data.pthWallThicknessUnits = self.pth_wall_thickness_units
        if self.min_hole_size is not None:
            grpc_data.minHoleSize = self.min_hole_size
        if self.min_hole_size_units is not None:
            grpc_data.minHoleSizeUnits = self.min_hole_size_units
        if self.max_hole_size is not None:
            grpc_data.maxHoleSize = self.max_hole_size
        if self.max_hole_size_units is not None:
            grpc_data.maxHoleSizeUnits = self.max_hole_size_units

        return grpc_data

    @field_validator(
        "cca_name",
        "pth_quality_factor",
        "pth_wall_thickness_units",
        "min_hole_size_units",
        "max_hole_size_units",
    )
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)


class UpdatePTHFatiguePropsRequest(BaseModel):
    """Contains the properties of a PTH fatigue analysis update per project."""

    project: str
    """Name of the Sherlock project."""
    pth_fatigue_analysis_properties: list[PTHFatiguePropsAnalysis]
    """List of PTH fatigue analysis properties to update."""

    @field_validator("project")
    @classmethod
    def str_validation(cls, value: str, info: ValidationInfo):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(
        self,
    ) -> analysis_service.UpdatePTHFatiguePropsRequest:
        request = analysis_service.UpdatePTHFatiguePropsRequest()
        request.project = self.project
        for properties in self.pth_fatigue_analysis_properties:
            request.pthFatigueAnalysisProperties.append(properties._convert_to_grpc())
        return request
