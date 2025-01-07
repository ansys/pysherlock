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
.. _ref_sherlock_export_fea_model:

=================================
Export FEA Model
=================================

This example demonstrates how to launch the Sherlock gRPC service, import a project zip archive,
and export a Finite Element Analysis (FEA) model.

Description
Sherlock's gRPC API enables automation of various workflows, including exporting FEA models.
This script demonstrates:

- Launching the Sherlock service.
- Importing a tutorial project.
- Exporting an FEA model with specific parameters.
- Properly exiting the gRPC connection.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_export_fea_model_example.png'

import os
import time

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockExportFEAModelError,
    SherlockImportProjectZipArchiveError,
)
from ansys.sherlock.core.types.common_types import Measurement

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service using the default port and wait for initialization.

VERSION = "251"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

time.sleep(5)  # Allow time for environment setup

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import Tutorial Project
# ========================
# Import the tutorial project zip archive provided with the Sherlock installation.

try:
    project_zip_path = os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "Tutorial Project.zip")
    sherlock.project.import_project_zip_archive(
        project="Tutorial Project", description="Demos", file_path=project_zip_path
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project zip archive: {str(e)}")

###############################################################################
# Export FEA Model
# =================
# Export the FEA model with customized parameters.

try:
    fea_export_path = os.path.join(os.getcwd(), "export.wbjn")
    sherlock.model.export_FEA_model(
        project="Tutorial Project",
        cca_name="Main Board",
        export_file=fea_export_path,
        analysis="NaturalFreq",
        drill_hole_parameters=[
            {
                "drill_hole_modeling": "ENABLED",
                "min_hole_diameter": Measurement(value=0.5, unit="mm"),
                "max_edge_length": Measurement(value=1.0, unit="mm"),
            }
        ],
        detect_lead_modeling="ENABLED",
        lead_model_parameters=[
            {
                "lead_modeling": "ENABLED",
                "lead_element_order": "First Order (Linear)",
                "max_mesh_size": Measurement(value=0.5, unit="mm"),
                "vertical_mesh_size": Measurement(value=0.1, unit="mm"),
                "thicknessCount": 3,
                "aspectRatio": 2,
            }
        ],
        display_model=True,
        clear_FEA_database=True,
        use_FEA_model_id=True,
        coordinate_units="mm",
    )
    print(f"FEA model exported successfully to: {fea_export_path}")
except SherlockExportFEAModelError as e:
    print(f"Error exporting FEA model: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

time.sleep(120)  # Allow time for processing and export
sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
