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
.. _ref_sherlock_run_strain_map_analysis:

=======================
Run Strain Map Analysis
=======================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
add strain maps, and run strain map analysis, including harmonic vibration analysis.

Description
-----------
Sherlock allows you to perform strain map analysis, which can be applied in various contexts,
such as harmonic vibration analysis on PCB strain maps.
This script performs the following steps:
- Connect to the Sherlock service.
- Import a project.
- Add a strain map file to the project.
- Configure the analysis properties for harmonic vibration.
- Execute strain map analysis based on the configured properties.

For further details, refer to the official documentation on strain map analysis in Sherlock.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_run_strain_map_analysis_example.png'

import os

from ansys.api.sherlock.v0.SherlockAnalysisService_pb2 import RunStrainMapAnalysisRequest
from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockAddStrainMapsError,
    SherlockImportProjectZipArchiveError,
    SherlockRunStrainMapAnalysisError,
    SherlockUpdateHarmonicVibePropsError,
)
from ansys.sherlock.core.types.analysis_types import ModelSource
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
# =======================
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
# Update Harmonic Vibration Properties
# ====================================
# Configure properties for harmonic vibration analysis using strain maps.

try:
    # Update properties for harmonic vibration analysis
    sherlock.analysis.update_harmonic_vibe_props(
        project="Test",
        harmonic_vibe_properties=[
            {
                "cca_name": "Main Board",
                "model_source": ModelSource.STRAIN_MAP,
                "harmonic_vibe_count": 1,
                "harmonic_vibe_damping": "0.01",
                "part_validation_enabled": False,
                "require_material_assignment_enabled": True,
                "analysis_temp": 20,
                "analysis_temp_units": "C",
                "force_model_rebuild": "AUTO",
                "filter_by_event_frequency": False,
                "natural_freq_min": 1,
                "natural_freq_min_units": "Hz",
                "natural_freq_max": 1000,
                "natural_freq_max_units": "KHz",
                "reuse_modal_analysis": True,
                "strain_map_natural_freq": 500,
            }
        ],
    )
    print("Harmonic vibration properties updated successfully.")
except SherlockUpdateHarmonicVibePropsError as e:
    print(f"Error updating harmonic vibe properties: {e}")

###############################################################################
# Run Strain Map Analysis
# =======================
# Run the strain map analysis, including harmonic vibration and other analysis types.

try:
    sherlock.analysis.run_strain_map_analysis(
        project="Test",
        cca_name="Main Board",
        strain_map_analyses=[
            [
                RunStrainMapAnalysisRequest.StrainMapAnalysis.AnalysisType.HarmonicVibe,
                [
                    ["On The Road", "5 - Harmonic Vibe", "TOP", "StrainMap - Top"],
                    ["On The Road", "5 - Harmonic Vibe", "BOTTOM", "StrainMap - Bottom"],
                ],
            ]
        ],
    )
    print("Strain map analysis completed successfully.")
except SherlockRunStrainMapAnalysisError as e:
    print(f"Error running strain map analysis: {e}")
