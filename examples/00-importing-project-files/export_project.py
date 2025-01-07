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
import time

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockExportProjectError,
    SherlockImportProjectZipArchiveError,
)

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
        "Tutorial Project",
        export_dfr=True,
        export_pcb_layers=True,
        export_components=True,
        export_nets=True,
        export_simulations=True,
        export_settings=True,
        output_dir=os.getcwd(),
        output_file="Exported_Project_All.zip",
        overwrite=True,
    )
    print("Project exported successfully with all options enabled.")
except SherlockExportProjectError as e:
    print(f"Error exporting project (all options): {str(e)}")

# Export with limited options
try:
    sherlock.project.export_project(
        "Tutorial Project",
        export_dfr=True,
        export_pcb_layers=False,
        export_components=False,
        export_nets=False,
        export_simulations=False,
        export_settings=False,
        output_dir=os.getcwd(),
        output_file="Exported_Project_Limited.zip",
        overwrite=True,
    )
    print("Project exported successfully with limited options.")
except SherlockExportProjectError as e:
    print(f"Error exporting project (limited options): {str(e)}")

# Export only the settings
try:
    sherlock.project.export_project(
        "Tutorial Project",
        export_dfr=False,
        export_pcb_layers=False,
        export_components=False,
        export_nets=False,
        export_simulations=False,
        export_settings=True,
        output_dir=os.getcwd(),
        output_file="Exported_Project_Settings.zip",
        overwrite=True,
    )
    print("Project exported successfully with settings only.")
except SherlockExportProjectError as e:
    print(f"Error exporting project (settings only): {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

time.sleep(20)  # Allow time for any remaining operations
sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
