# Copyright (C) 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
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

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockUpdatePcbModelingPropsError,
)
from ansys.sherlock.core.types.analysis_types import (
    ElementOrder,
    UpdatePcbModelingPropsRequestAnalysisType,
    UpdatePcbModelingPropsRequestPcbMaterialModel,
    UpdatePcbModelingPropsRequestPcbModelType,
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
    sherlock.analysis.update_pcb_modeling_props(
        project="Test",
        cca_names=["Auto Relay"],
        analyses=[
            (
                UpdatePcbModelingPropsRequestAnalysisType.HARMONIC_VIBE,
                UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                True,
                UpdatePcbModelingPropsRequestPcbMaterialModel.UNIFORM,
                ElementOrder.SOLID_SHELL,
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
                UpdatePcbModelingPropsRequestAnalysisType.NATURAL_FREQUENCY,
                UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                True,
                UpdatePcbModelingPropsRequestPcbMaterialModel.UNIFORM,
                ElementOrder.SOLID_SHELL,
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
                UpdatePcbModelingPropsRequestAnalysisType.ICT,
                UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                True,
                UpdatePcbModelingPropsRequestPcbMaterialModel.UNIFORM,
                ElementOrder.SOLID_SHELL,
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
                UpdatePcbModelingPropsRequestAnalysisType.MECHANICAL_SHOCK,
                UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                True,
                UpdatePcbModelingPropsRequestPcbMaterialModel.LAYERED,
                ElementOrder.SOLID_SHELL,
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
                UpdatePcbModelingPropsRequestAnalysisType.RANDOM_VIBE,
                UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                True,
                UpdatePcbModelingPropsRequestPcbMaterialModel.LAYERED_ELEMENTS,
                5,
                ElementOrder.SOLID_SHELL,
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
                UpdatePcbModelingPropsRequestAnalysisType.THERMAL_MECH,
                UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                True,
                UpdatePcbModelingPropsRequestPcbMaterialModel.UNIFORM_ELEMENTS,
                5,
                ElementOrder.SOLID_SHELL,
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
