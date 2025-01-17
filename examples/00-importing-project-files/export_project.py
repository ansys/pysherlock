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
.. _ref_sherlock_project_export:

======================================
Sherlock Project Export
======================================

This example demonstrates how to launch the Sherlock gRPC service, import a project archive,
and export the project in multiple configurations.

Description
Sherlock's gRPC API enables automation of various workflows, including project export.
This script demonstrates:

- Launching the Sherlock service.
- Importing a tutorial project ZIP archive.
- Exporting a project with different configurations.
- Properly exiting the gRPC connection.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_project_export_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockExportProjectError,
    SherlockImportProjectZipArchiveError,
)

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service using the default port and wait for initialization.

VERSION = "242"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import Tutorial Project
# ========================
# Import a sample project ZIP archive provided with the Sherlock installation.

try:
    project_zip_path = os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "Tutorial Project.zip")
    sherlock.project.import_project_zip_archive("Tutorial Project", "Demos", project_zip_path)
    print("Project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project: {str(e)}")

###############################################################################
# Export Project
# ==============
# Export the imported project with different configurations.

# Export with all options enabled
try:
    sherlock.project.export_project(
        project_name="Tutorial Project",
        export_design_files=True,
        export_result_files=True,
        export_archive_results=True,
        export_user_files=True,
        export_log_files=True,
        export_system_data=True,
        export_file_dir=os.getcwd(),
        export_file_name="Exported_Project_All.zip",
        overwrite_existing_file=True,
    )
    print("Project exported successfully with all options enabled.")
except SherlockExportProjectError as e:
    print(f"Error exporting project (all options): {str(e)}")

# Export with limited options
try:
    sherlock.project.export_project(
        project_name="Tutorial Project",
        export_design_files=True,
        export_result_files=False,
        export_archive_results=False,
        export_user_files=False,
        export_log_files=False,
        export_system_data=False,
        export_file_dir=os.getcwd(),
        export_file_name="Exported_Project_Limited.zip",
        overwrite_existing_file=True,
    )
    print("Project exported successfully with limited options.")
except SherlockExportProjectError as e:
    print(f"Error exporting project (limited options): {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
