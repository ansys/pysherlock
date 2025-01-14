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
.. _ref_sherlock_update_part_list_validation_analysis:

=====================================
Update Part List Validation Analysis
=====================================

This example demonstrates how to launch the Sherlock gRPC service, import an ODB++ archive,
update part list validation analysis properties, and retrieve those properties.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as validating and updating part list
analysis properties for printed circuit boards (PCBs). This script shows how to:

- Launch the Sherlock service.
- Import an ODB++ archive.
- Update the part list validation analysis properties.
- Retrieve and print the updated part list validation analysis properties.
- Properly close the gRPC connection.

The retrieved analysis properties can be used for further validation or integration
with other software tools.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_update_part_list_valid_analysis_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockGetPartsListValidationAnalysisPropsError,
    SherlockImportProjectZipArchiveError,
    SherlockUpdatePartListValidationAnalysisPropsError,
)

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
# Update Part List Validation Analysis Properties
# =================================================
# Update the part list validation analysis properties for the "Card" of the "Test" project.

try:
    update_props = [
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
    ]
    sherlock.analysis.update_part_list_validation_analysis_props(
        project="Test",
        properties_per_cca=update_props,
    )
    print("Part list validation analysis properties updated successfully.")
except SherlockUpdatePartListValidationAnalysisPropsError as e:
    print(f"Error updating part list validation analysis properties: {e}")

###############################################################################
# Get Part List Validation Analysis Properties
# ============================================
# Retrieve the updated part list validation analysis properties.

try:
    response = sherlock.analysis.get_parts_list_validation_analysis_props(
        project="Test",
        cca_name="Main Board",
    )
    print("Retrieved part list validation analysis properties:")
    print(f"Response: {response}")
except SherlockGetPartsListValidationAnalysisPropsError as e:
    print(f"Error retrieving part list validation analysis properties: {e}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
