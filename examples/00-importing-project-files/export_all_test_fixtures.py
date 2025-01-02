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
.. _ref_sherlock_export_test_fixtures:

==========================
Export All Test Fixtures
==========================

This example demonstrates how to launch the Sherlock gRPC service, import a project zip archive,
and export all test fixtures for a printed circuit board (PCB).

Description
-----------
Sherlock's gRPC API enables users to automate various workflows, including exporting all
test fixtures for a PCB.
This script covers:

- Launching the Sherlock service.
- Importing a tutorial project.
- Exporting all test fixtures to a CSV file.
- Properly closing the gRPC connection.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_export_test_fixtures_example.png'

import os
import time

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockExportAllTestFixtures,
    SherlockImportProjectZipArchiveError,
)

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service using the default port and wait for initialization.

VERSION = "252"
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
# Export All Test Fixtures
# =========================
# Export all test fixtures for the "Main Board" to a CSV file.

time.sleep(10)  # Allow time for the project to load completely

try:
    test_fixtures_export_path = os.path.join(os.getcwd(), "TestFixturesExport.csv")
    sherlock.layer.export_all_test_fixtures(
        project="Tutorial Project",
        cca_name="Main Board",
        file_path=test_fixtures_export_path,
        units="DEFAULT",
    )
    print(f"All test fixtures exported successfully to: {test_fixtures_export_path}")
except SherlockExportAllTestFixtures as e:
    print(f"Error exporting all test fixtures: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
