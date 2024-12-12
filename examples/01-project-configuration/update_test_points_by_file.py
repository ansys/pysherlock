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
.. _ref_update_test_points:

=================================
Update Test Points by File
=================================

This example demonstrates how to launch the Sherlock gRPC service, import a project zip archive, 
update test points using a CSV file, and properly close the connection.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as updating test 
points for printed circuit boards (PCBs) using a CSV file. This script shows how to:

- Launch the Sherlock service.
- Import a project zip archive.
- Update test points using a CSV file.
- Properly close the gRPC connection.

The updated test points ensure accurate validation during the testing phase.
"""

# sphinx_gallery_thumbnail_path = './images/update_test_points_example.png'

import os
import time
from ansys.sherlock.core.errors import (
    SherlockUpdateTestPointsByFileError,
    SherlockImportProjectZipArchiveError,
)
from ansys.sherlock.core import launcher

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = '252'
ANSYS_ROOT = os.getenv('AWP_ROOT' + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import Project Zip Archive
# ===========================
# Import the project zip archive from the Sherlock tutorial directory.

try:
    project_zip_path = os.path.join(
        ANSYS_ROOT, "sherlock", "tutorial", "Tutorial Project.zip"
    )
    sherlock.project.import_project_zip_archive(
        project_name="Tutorial Project",
        project_dir="Demos",
        zip_file_path=project_zip_path,
    )
    print("Project zip archive imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project zip archive: {str(e)}")

###############################################################################
# Update Test Points by File
# ===========================
# Update the test points for the "Main Board" of the "Tutorial Project" using a CSV file.

csv_file_path = os.path.join(
    os.getenv('PARTSDIR'), "AM", "SHERLOCK", "TestPoints.csv"
)

try:
    sherlock.layer.update_test_points_by_file(
        project_name="Tutorial Project",
        cca_name="Main Board",
        file_path=csv_file_path,
    )
    print("Test points updated successfully using the CSV file.")
except SherlockUpdateTestPointsByFileError as e:
    print(f"Error updating test points by file: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
