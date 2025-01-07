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
.. _ref_sherlock_run_random_vibe_analysis:

=============================
Run Random Vibration Analysis
=============================

This example demonstrates how to launch the Sherlock gRPC service, import project data,
add strain maps, and run random vibration analysis.

Description
-----------
Sherlock allows you to perform random vibration analysis using strain maps.
This script includes the following steps:

- Launch the Sherlock service.
- Import ODB++ archive and strain map files into the project.
- Configure the properties for random vibration analysis.
- Execute random vibration analysis based on the configured properties.
- Exit the gRPC connection after the analysis is complete.

For further details, refer to the official documentation on random vibration analysis in Sherlock.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_run_random_vibe_analysis_example.png'

import os
import time

from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockAddStrainMapsError,
    SherlockImportODBError,
    SherlockRunStrainMapAnalysisError,
)
from ansys.sherlock.core.types.analysis_types import (
    ModelSource,
    RunStrainMapAnalysisRequestAnalysisType,
)
from ansys.sherlock.core.types.project_types import StrainMapsFileType

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "251"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import ODB Archive and Strain Maps
# ==================================
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
                "µε",
                ["Card"],
            )
        ],
    )
except SherlockAddStrainMapsError as e:
    print(f"Error adding strain maps: {str(e)}")

###############################################################################
# Update Random Vibration Properties
# ==================================
# Configure properties for random vibration analysis using strain maps.

try:
    # Update properties for random vibration analysis
    sherlock.analysis.update_random_vibe_props(
        project="Test",
        cca_name="Card",
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
    print(f"Error updating random vibration properties: {str(e)}")

###############################################################################
# Run Random Vibration Analysis
# =============================
# Run the random vibration analysis, including specified parameters.

try:
    analysis_request = SherlockAnalysisService_pb2.RunStrainMapAnalysisRequest
    sherlock.analysis.run_strain_map_analysis(
        "Test",
        "Card",
        [
            [
                RunStrainMapAnalysisRequestAnalysisType.RANDOM_VIBE,
                [
                    ["Phase 1", "Random Event", "TOP", "StrainMap - Top"],
                    ["Phase 1", "Random Event", "BOTTOM", "StrainMap - Bottom"],
                ],
            ]
        ],
    )
except SherlockRunStrainMapAnalysisError as e:
    print(f"Error running random vibration analysis: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

time.sleep(5)
sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
