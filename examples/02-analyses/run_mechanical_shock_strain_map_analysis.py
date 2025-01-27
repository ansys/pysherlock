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
.. _ref_sherlock_run_mechanical_shock_analysis:

=====================================
Run Mechanical Shock Analysis Example
=====================================

This example demonstrates how to launch the Sherlock gRPC service, import project data,
add strain maps, and run a mechanical shock analysis based on strain maps.

Description
-----------
Sherlock provides tools to perform mechanical shock analysis using strain maps.
This script includes the following steps:

- Launch the Sherlock service.
- Import ODB++ archive and strain map files into the project.
- Configure the analysis properties for mechanical shock.
- Execute the mechanical shock analysis.
- Exit the gRPC connection after the analysis is complete.

For further details, refer to the official documentation on mechanical shock analysis in Sherlock.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_run_mechanical_shock_analysis_example.png'

import os

from SherlockAnalysisService_pb2 import RunStrainMapAnalysisRequest

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockAddStrainMapsError,
    SherlockImportProjectZipArchiveError,
    SherlockRunStrainMapAnalysisError,
)
from ansys.sherlock.core.types.analysis_types import ModelSource
from ansys.sherlock.core.types.project_types import StrainMapsFileType

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "242"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import Tutorial Project
# ========================
# Import the tutorial project zip archive from the Sherlock tutorial directory.

try:
    sherlock.project.import_project_zip_archive(
        project="Test",
        category="Demos",
        archive_file=(os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "Tutorial Project.zip")),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project zip archive: {e}")

###############################################################################
# Add Strain Map
# ====================================
# Add a strain map to the project.

try:
    strain_map_path = os.path.join(
        ANSYS_ROOT, "sherlock", "tutorial", "StrainMaps", "StrainMap.csv"
    )
    sherlock.project.add_strain_maps(
        "Test",
        [
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
# Update Mechanical Shock Properties
# ===================================
# Configure properties for mechanical shock analysis using strain maps.

try:
    # Update properties for mechanical shock analysis
    sherlock.analysis.update_mechanical_shock_props(
        "Test",
        [
            {
                "cca_name": "Main Board",
                "model_source": ModelSource.STRAIN_MAP,
                "shock_result_count": 1,
                "part_validation_enabled": False,
                "require_material_assignment_enabled": True,
                "force_model_rebuild": "AUTO",
                "natural_freq_min": 10,
                "natural_freq_min_units": "Hz",
                "natural_freq_max": 100,
                "natural_freq_max_units": "KHz",
                "analysis_temp": 20,
                "analysis_temp_units": "C",
            }
        ],
    )
    print("Mechanical shock properties updated successfully.")
except SherlockRunStrainMapAnalysisError as e:
    print(f"Error updating mechanical shock properties: {e}")

###############################################################################
# Run Mechanical Shock Analysis
# ==============================
# Execute the mechanical shock analysis based on strain maps.

try:
    sherlock.analysis.run_strain_map_analysis(
        "Test",
        "Main Board",
        [
            [
                RunStrainMapAnalysisRequest.StrainMapAnalysis.AnalysisType.MechanicalShock,
                [
                    ["On The Road", "2 - Pothole", "TOP", "StrainMap - Top"],
                    ["On The Road", "3 - Collision", "BOTTOM", "StrainMap - Bottom"],
                ],
            ]
        ],
    )
    print("Mechanical shock analysis executed successfully.")
except SherlockRunStrainMapAnalysisError as e:
    print(f"Error running mechanical shock analysis: {e}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
