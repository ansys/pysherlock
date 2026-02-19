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
.. _ref_sherlock_run_random_vibe_analysis:

=============================
Run Random Vibration Analysis
=============================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
add strain maps, and run random vibration analysis.

Description
-----------
Sherlock allows you to perform random vibration analysis using strain maps.
This script performs the following steps:
- Connect to the Sherlock service.
- Import a project.
- Add a strain map file to the project.
- Configure the properties for random vibration analysis.
- Execute random vibration analysis based on the configured properties.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_run_random_vibe_analysis_example.png'

import os

from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2
from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockAddStrainMapsError,
    SherlockImportProjectZipArchiveError,
    SherlockRunStrainMapAnalysisError,
)
from ansys.sherlock.core.types.analysis_types import (
    ModelSource,
    RunStrainMapAnalysisRequestAnalysisType,
)
from ansys.sherlock.core.types.project_types import StrainMapsFileType

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
# ========================
# Import the tutorial project zip archive from the Sherlock tutorial directory.

try:
    sherlock.project.import_project_zip_archive(
        project="Test",
        category="Demos",
        archive_file=os.path.join(get_sherlock_tutorial_path(), "Tutorial Project.zip"),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project zip archive: {e}")

###############################################################################
# Add Strain Map
# ==============
# Add a strain map to the project.

try:
    strain_map_path = os.path.join(get_sherlock_tutorial_path(), "StrainMaps", "StrainMap.csv")
    sherlock.project.add_strain_maps(
        project="Test",
        strain_maps=[
            (
                strain_map_path,
                "This is the strain map file for the project",
                StrainMapsFileType.CSV,
                0,
                "SolidID",
                "PCB Strain",
                "µε",
                ["Main Board"],
            )
        ],
    )
    print("Strain maps added successfully.")
except SherlockAddStrainMapsError as e:
    print(f"Error adding strain maps: {e}")

###############################################################################
# Update Random Vibration Properties
# ==================================
# Configure properties for random vibration analysis using strain maps.

try:
    sherlock.analysis.update_random_vibe_props(
        project="Test",
        cca_name="Main Board",
        model_source=ModelSource.STRAIN_MAP,
        random_vibe_damping="0.01",
        part_validation_enabled=False,
        require_material_assignment_enabled=True,
        analysis_temp=20,
        analysis_temp_units="C",
        force_model_rebuild="AUTO",
        natural_freq_min=10,
        natural_freq_min_units="Hz",
        natural_freq_max=1000,
        natural_freq_max_units="KHz",
        reuse_modal_analysis=True,
        strain_map_natural_freqs="100, 200, 300",
    )
except SherlockRunStrainMapAnalysisError as e:
    print(f"Error updating random vibration properties: {e}")

###############################################################################
# Run Random Vibration Analysis
# =============================
# Run the random vibration analysis, including specified parameters.

try:
    analysis_request = SherlockAnalysisService_pb2.RunStrainMapAnalysisRequest
    sherlock.analysis.run_strain_map_analysis(
        project="Test",
        cca_name="Main Board",
        strain_map_analyses=[
            [
                RunStrainMapAnalysisRequestAnalysisType.RANDOM_VIBE,
                [
                    ["On The Road", "1 - Vibration", "TOP", "StrainMap - Top"],
                    ["On The Road", "1 - Vibration", "BOTTOM", "StrainMap - Bottom"],
                ],
            ]
        ],
    )
except SherlockRunStrainMapAnalysisError as e:
    print(f"Error running random vibration analysis: {e}")
