# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
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
import time

from SherlockAnalysisService_pb2 import RunStrainMapAnalysisRequest

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockAddStrainMapsError,
    SherlockImportODBError,
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
# Import ODB Archive and Strain Maps
# ===================================
# Import a project and add strain maps to the Sherlock project.

try:
    # Import ODB++ archive into the project
    sherlock.project.import_odb_archive(
        ANSYS_ROOT
        + os.path.sep
        + "sherlock"
        + os.path.sep
        + "tutorial"
        + os.path.sep
        + "ODB++ Tutorial.tgz",
        True,
        True,
        True,
        True,
        project="Test",
        cca_name="Card",
    )
except SherlockImportODBError as e:
    print(f"Error importing ODB archive: {str(e)}")

try:
    # Add strain maps to the project
    strain_map_path = (
        ANSYS_ROOT
        + os.path.sep
        + "sherlock"
        + os.path.sep
        + "tutorial"
        + os.path.sep
        + "StrainMaps"
        + os.path.sep
        + "StrainMap.csv"
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
                "\u03bc\u03b5",
                ["Card"],
            )
        ],
    )
except SherlockAddStrainMapsError as e:
    print(f"Error adding strain maps: {str(e)}")

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
                "cca_name": "Card",
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
except SherlockRunStrainMapAnalysisError as e:
    print(f"Error updating mechanical shock properties: {str(e)}")

###############################################################################
# Run Mechanical Shock Analysis
# ==============================
# Execute the mechanical shock analysis based on strain maps.

try:
    sherlock.analysis.run_strain_map_analysis(
        "Test",
        "Card",
        [
            [
                RunStrainMapAnalysisRequest.StrainMapAnalysis.AnalysisType.MechanicalShock,
                [
                    ["Phase 1", "Shock Event", "TOP", "StrainMap - Top"],
                    ["Phase 1", "Shock Event", "BOTTOM", "StrainMap - Bottom"],
                ],
            ]
        ],
    )
except SherlockRunStrainMapAnalysisError as e:
    print(f"Error running mechanical shock analysis: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

time.sleep(5)
sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
