# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

================
Export FEA Model
================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and export a Finite Element Analysis (FEA) model.

Description
Sherlock's gRPC API enables automation of various workflows, including exporting FEA models.
This script demonstrates how to:
- Connect to the Sherlock service.
- Import a tutorial project.
- Export an FEA model with specific parameters.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_export_fea_model_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path, get_temp_dir

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockExportFEAModelError,
    SherlockImportProjectZipArchiveError,
)
from ansys.sherlock.core.types.common_types import Measurement

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
# Import the tutorial project zip archive provided with the Sherlock installation.

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
# Export FEA Model
# ================
# Export the FEA model with customized parameters.

try:
    fea_export_path = os.path.join(get_temp_dir(), "export.wbjn")
    sherlock.model.export_FEA_model(
        project="Test",
        cca_name="Main Board",
        export_file=fea_export_path,
        analysis="NaturalFreq",
        drill_hole_parameters=[
            {
                "drill_hole_modeling": "ENABLED",
                "min_hole_diameter": Measurement(value=1.0, unit="mm"),
                "max_edge_length": Measurement(value=1.0, unit="mm"),
            }
        ],
        detect_lead_modeling="ENABLED",
        lead_model_parameters=[
            {
                "lead_modeling": "ENABLED",
                "lead_element_order": "First Order (Linear)",
                "max_mesh_size": Measurement(value=1.0, unit="mm"),
                "vertical_mesh_size": Measurement(value=0.5, unit="mm"),
                "thicknessCount": 3,
                "aspectRatio": 2,
            }
        ],
        display_model=False,
        clear_FEA_database=True,
        use_FEA_model_id=True,
        coordinate_units="mm",
    )
    print(f"FEA model exported successfully to: {fea_export_path}")
except SherlockExportFEAModelError as e:
    print(f"Error exporting FEA model: {e}")
