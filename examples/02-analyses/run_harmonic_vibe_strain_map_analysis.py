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
.. _ref_sherlock_run_strain_map_analysis:

========================
Run Strain Map Analysis
========================

This example demonstrates how to launch the Sherlock gRPC service, import project data,
add strain maps, and run strain map analysis, including harmonic vibration analysis.

Description
-----------
Sherlock allows you to perform strain map analysis, which can be applied in various contexts,
such as harmonic vibration analysis on PCB strain maps. This script covers the following steps:

- Launch the Sherlock service.
- Import ODB++ archive and strain map files into the project.
- Configure the analysis properties for harmonic vibration.
- Execute strain map analysis based on the configured properties.
- Exit the gRPC connection after the analysis is complete.

For further details, refer to the official documentation on strain map analysis in Sherlock.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_run_strain_map_analysis_example.png'

import os
import time
import pandas as pd
from ansys.sherlock.core.errors import SherlockRunStrainMapAnalysisError, SherlockImportODBError, SherlockAddStrainMapsError
from ansys.sherlock.core.types.analysis_types import RunStrainMapAnalysisRequestAnalysisType, ModelSource
from ansys.sherlock.core.types.project_types import StrainMapsFileType
from ansys.api.sherlock.v0 import SherlockModelService_pb2
from ansys.sherlock.core import launcher

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = '252'
ANSYS_ROOT = os.getenv('AWP_ROOT' + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import ODB Archive and Strain Maps
# ==================================
# Import a project and add strain maps to the Sherlock project.

try:
    # Import ODB++ archive into the project
    sherlock.project.import_odb_archive(
        ANSYS_ROOT + os.path.sep + 'sherlock' + os.path.sep + 'tutorial' + os.path.sep + 'ODB++ Tutorial.tgz',
        True, True, True, True, project="Test", cca_name="Card"
    )
except SherlockImportODBError as e:
    print(f"Error importing ODB archive: {str(e)}")

try:
    # Add strain maps to the project
    strain_map_path = ANSYS_ROOT + os.path.sep + "sherlock" + os.path.sep + "tutorial" + os.path.sep + "StrainMaps" + os.path.sep + "StrainMap.csv"
    sherlock.project.add_strain_maps(
        "Test",
        [(strain_map_path, "This is the strain map file for the project", StrainMapsFileType.CSV, 0, "SolidID", "PCB Strain", "µε", ["Card"])]
    )
except SherlockAddStrainMapsError as e:
    print(f"Error adding strain maps: {str(e)}")

###############################################################################
# Update Harmonic Vibration Properties
# ====================================
# Configure properties for harmonic vibration analysis using strain maps.

try:
    # Update properties for harmonic vibration analysis
    sherlock.analysis.update_harmonic_vibe_props(
        "Test",
        [{
            "cca_name": "Card",
            "model_source": ModelSource.STRAIN_MAP,
            "harmonic_vibe_count": 1,
            "harmonic_vibe_damping": "0.01",
            "part_validation_enabled": False,
            "require_material_assignment_enabled": True,
            "analysis_temp": 20,
            "analysis_temp_units": "C",
            "force_model_rebuild": "AUTO",
            "filter_by_event_frequency": False,
            "natural_freq_min": 10,
            "natural_freq_min_units": "Hz",
            "natural_freq_max": 1000,
            "natural_freq_max_units": "KHz",
            "reuse_modal_analysis": True,
            "strain_map_natural_freq": 500,
        }]
    )
except SherlockRunStrainMapAnalysisError as e:
    print(f"Error updating harmonic vibe properties: {str(e)}")

###############################################################################
# Run Strain Map Analysis
# =======================
# Run the strain map analysis, including harmonic vibration and other analysis types.

try:
    analysis_request = SherlockModelService_pb2.RunStrainMapAnalysisRequest
    sherlock.analysis.run_strain_map_analysis(
        "Test",
        "Card",
        [[
            SherlockModelService_pb2.RunStrainMapAnalysisRequest.StrainMapAnalysis.AnalysisType.HarmonicVibe,
            [["Phase 1", "Harmonic Event", "TOP", "StrainMap - Top"],
             ["Phase 1", "Harmonic Event", "BOTTOM", "StrainMap - Bottom"]]
        ]]
    )
except SherlockRunStrainMapAnalysisError as e:
    print(f"Error running strain map analysis: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

time.sleep(5)
sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
