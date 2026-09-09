# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
.. _ref_sherlock_update_pcb_modeling_props:

==============================
Update PCB Modeling Properties
==============================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and configure PCB modeling properties for various analysis types.

Description
-----------
Sherlock allows you to configure PCB modeling properties for multiple analysis types.
This script performs the following steps:
- Connect to the Sherlock service.
- Import a project.
- Configure PCB modeling properties for several analysis types.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_update_pcb_modeling_props_example.png'

import os

from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2
from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockUpdatePcbModelingPropsError,
)

PcbAnalysisType = (
    SherlockAnalysisService_pb2.UpdatePcbModelingPropsRequest.Analysis.AnalysisType.ValueType
)
PcbModelType = (
    SherlockAnalysisService_pb2.UpdatePcbModelingPropsRequest.Analysis.PcbModelType.ValueType
)
PcbMaterialModel = (
    SherlockAnalysisService_pb2.UpdatePcbModelingPropsRequest.Analysis.PcbMaterialModel.ValueType
)

###############################################################################
# Connect to Sherlock
# ===================
# Connect to the Sherlock service and ensure proper initialization.

sherlock = launcher.connect(port=9092, timeout=10)

###############################################################################
# Delete Project
# ==============
# Delete the project if it already exists.

try:
    sherlock.project.delete_project("Test")
    print("Project deleted successfully.")
except Exception:
    pass

###############################################################################
# Import Tutorial Project
# =======================
# Import the tutorial project zip archive from the Sherlock tutorial directory.

try:
    sherlock.project.import_project_zip_archive(
        project="Test",
        category="Demos",
        archive_file=os.path.join(get_sherlock_tutorial_path(), "Auto Relay Project.zip"),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project zip archive: {e}")

###############################################################################
# Update PCB Modeling Properties
# ==============================
# Configure PCB modeling properties for various analysis types.

try:
    analysis_type = SherlockAnalysisService_pb2.UpdatePcbModelingPropsRequest.Analysis.AnalysisType
    material_model = (
        SherlockAnalysisService_pb2.UpdatePcbModelingPropsRequest.Analysis.PcbMaterialModel
    )
    pcb_model_type = SherlockAnalysisService_pb2.UpdatePcbModelingPropsRequest.Analysis.PcbModelType

    harmonic_vibe = analysis_type.HarmonicVibe
    natural_freq = analysis_type.NaturalFreq
    ict_analysis = analysis_type.ICTAnalysis
    mechanical_shock = analysis_type.MechanicalShock
    random_vibe = analysis_type.RandomVibe
    thermal_mech = analysis_type.ThermalMech
    bonded = pcb_model_type.Bonded
    uniform = material_model.Uniform
    layered = material_model.Layered
    layered_elements = material_model.LayeredElements
    uniform_elements = material_model.UniformElements
    solid_shell = SherlockAnalysisService_pb2.ElementOrder.SolidShell

    sherlock.analysis.update_pcb_modeling_props(
        project="Test",
        cca_names=["Auto Relay"],
        analyses=[(harmonic_vibe, bonded, True, uniform, solid_shell, 6, "mm", 3, "mm", True)],
    )
    sherlock.analysis.update_pcb_modeling_props(
        project="Test",
        cca_names=["Auto Relay"],
        analyses=[(natural_freq, bonded, True, uniform, solid_shell, 6, "mm", 3, "mm", True)],
    )
    sherlock.analysis.update_pcb_modeling_props(
        project="Test",
        cca_names=["Auto Relay"],
        analyses=[(ict_analysis, bonded, True, uniform, solid_shell, 6, "mm", 3, "mm", True)],
    )
    sherlock.analysis.update_pcb_modeling_props(
        project="Test",
        cca_names=["Auto Relay"],
        analyses=[(mechanical_shock, bonded, True, layered, solid_shell, 6, "mm", 3, "mm", True)],
    )
    sherlock.analysis.update_pcb_modeling_props(
        project="Test",
        cca_names=["Auto Relay"],
        analyses=[
            (
                random_vibe,
                bonded,
                True,
                layered_elements,
                5,
                solid_shell,
                6,
                "mm",
                3,
                "mm",
                True,
            )
        ],
    )
    sherlock.analysis.update_pcb_modeling_props(
        project="Test",
        cca_names=["Auto Relay"],
        analyses=[
            (
                thermal_mech,
                bonded,
                True,
                uniform_elements,
                5,
                solid_shell,
                6,
                "mm",
                3,
                "mm",
                True,
            )
        ],
    )
    print("PCB modeling properties updated successfully.")
except SherlockUpdatePcbModelingPropsError as e:
    print(f"Error updating PCB modeling properties: {e}")
