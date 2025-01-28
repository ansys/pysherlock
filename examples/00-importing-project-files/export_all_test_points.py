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
.. _ref_sherlock_export_test_points:

========================
Export All Test Points
========================

This example demonstrates how to launch the Sherlock gRPC service, import a project zip archive,
and export all test points for a printed circuit board (PCB).

Description
-----------
Sherlock's gRPC API enables users to automate various workflows, including exporting all
test points for a PCB.
This script covers:

- Launching the Sherlock service.
- Importing a tutorial project.
- Exporting all test points to a CSV file.
- Properly closing the gRPC connection.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_export_test_points_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockExportAllTestPointsError,
    SherlockImportProjectZipArchiveError,
)

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service using the default port and wait for initialization.

VERSION = "251"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

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
# Import the tutorial project zip archive provided with the Sherlock installation.

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
# Export All Test Points
# =======================
# Export all test points for the "Main Board" to a CSV file.

try:
    test_points_export_path = os.path.join(os.getcwd(), "temp", "TestPointsExport.csv")
    sherlock.layer.export_all_test_points(
        project="Test",
        cca_name="Main Board",
        export_file=test_points_export_path,
        length_units="DEFAULT",
        displacement_units="DEFAULT",
        force_units="DEFAULT",
    )
    print(f"All test points exported successfully to: {test_points_export_path}")
except SherlockExportAllTestPointsError as e:
    print(f"Error exporting all test points: {e}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
