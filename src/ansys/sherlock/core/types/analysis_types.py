# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# © 2023 - 2024 ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module containing types for the Analysis Service."""

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
