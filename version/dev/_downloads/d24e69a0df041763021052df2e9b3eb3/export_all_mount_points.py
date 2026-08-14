# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

=======================
Export All Mount Points
=======================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and export all mount points for a CCA.

Description
-----------
Sherlock's gRPC API allows users to automate various workflows, including exporting all
mount points for a PCB.
This script demonstrates how to:
- Connect to the Sherlock service.
- Import a tutorial project.
- Export all mount points to a CSV file.

The exported mount points can be used for further analysis or design purposes.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_export_mount_points_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path, get_temp_dir

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockExportAllMountPoints,
    SherlockImportProjectZipArchiveError,
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
        archive_file=os.path.join(get_sherlock_tutorial_path(), "Tutorial Project.zip"),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project zip archive: {e}")

###############################################################################
# Export All Mount Points
# =======================
# Export all mount points for the "Main Board" to a CSV file.

try:
    mount_points_export_path = os.path.join(get_temp_dir(), "MountPointsExport.csv")
    sherlock.layer.export_all_mount_points(
        project="Test",
        cca_name="Main Board",
        export_file=mount_points_export_path,
        units="DEFAULT",
    )
    print(f"All mount points exported successfully to: {mount_points_export_path}")
except SherlockExportAllMountPoints as e:
    print(f"Error exporting all mount points: {e}")
