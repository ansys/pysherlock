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
.. _ref_sherlock_export_mount_points:

==========================
Export All Mount Points
==========================

This example demonstrates how to launch the Sherlock gRPC service, import a project zip archive,
and export all mount points for a printed circuit board (PCB).

Description
-----------
Sherlock's gRPC API allows users to automate various workflows, including exporting all
 mount points for a PCB.
This script demonstrates how to:

- Launch the Sherlock service.
- Import a tutorial project.
- Export all mount points to a CSV file.
- Properly close the gRPC connection.

The exported mount points can be used for further analysis or design purposes.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_export_mount_points_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockExportAllMountPoints,
    SherlockImportProjectZipArchiveError,
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
    project_zip_path = os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "Tutorial Project.zip")
    sherlock.project.import_project_zip_archive(
        project="Tutorial Project", category="Demos", archive_file=project_zip_path
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project zip archive: {str(e)}")

###############################################################################
# Export All Mount Points
# ========================
# Export all mount points for the "Main Board" to a CSV file.

try:
    mount_points_export_path = os.path.join(os.getcwd(), "MountPointsExport.csv")
    sherlock.layer.export_all_mount_points(
        project="Tutorial Project",
        cca_name="Main Board",
        export_file=mount_points_export_path,
        units="DEFAULT",
    )
    print(f"All mount points exported successfully to: {mount_points_export_path}")
except SherlockExportAllMountPoints as e:
    print(f"Error exporting all mount points: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
