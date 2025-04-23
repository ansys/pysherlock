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
.. _ref_sherlock_run_part_list_validation_analysis:

=================================
Run Part List Validation Analysis
=================================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and configure part list validation analysis properties.

Description
-----------
Sherlock allows you to perform part list validation analysis.
This script performs the following steps:
- Connect to the Sherlock service.
- Import ODB++ archive into the project.
- Configure the properties for part list validation analysis.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_run_part_list_validation_analysis_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockUpdatePartListValidationAnalysisPropsError,
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
# Update Part List Validation Properties
# ======================================
# Configure properties for part list validation analysis.

try:
    # Update properties for part list validation analysis
    sherlock.analysis.update_part_list_validation_analysis_props(
        project="Test",
        properties_per_cca=[
            {
                "cca_name": "Main Board",
                "process_use_avl": True,
                "process_use_wizard": True,
                "process_check_confirmed_properties": False,
                "process_check_part_numbers": False,
                "matching_mode": "Part",
                "avl_require_internal_part_number": False,
                "avl_require_approved_description": True,
                "avl_require_approved_manufacturer": False,
            }
        ],
    )
    print("Part list validation analysis properties updated successfully.")
except SherlockUpdatePartListValidationAnalysisPropsError as e:
    print(f"Error updating part list validation analysis properties: {e}")
