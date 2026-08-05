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
.. _ref_sherlock_update_ict_props:

================
Run ICT Analysis
================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and configure ICT analysis properties.

Description
-----------
Sherlock allows you to perform ICT (In-Circuit Test) analysis.
This script performs the following steps:
- Connect to the Sherlock service.
- Import a project.
- Configure the properties for ICT analysis.

For further details, refer to the official documentation on ICT analysis in Sherlock.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_update_ict_analysis_props_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockUpdateICTAnalysisPropsError,
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
# ========================
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
# Update ICT Analysis Properties
# ==============================
# Configure properties for ICT analysis.

try:
    # Update properties for ICT analysis
    sherlock.analysis.update_ict_analysis_props(
        project="Test",
        ict_analysis_properties=[
            {
                "cca_name": "Auto Relay",
                "ict_application_time": 2,
                "ict_application_time_units": "sec",
                "ict_number_of_events": 10,
                "part_validation_enabled": False,
                "require_material_assignment_enabled": False,
            }
        ],
    )
    print("ICT analysis properties updated successfully.")
except SherlockUpdateICTAnalysisPropsError as e:
    print(f"Error updating ICT analysis properties: {e}")
