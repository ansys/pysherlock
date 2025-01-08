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
.. _ref_update_mount_points:

=================================
Update Mount Points by File
=================================

This example demonstrates how to launch the Sherlock gRPC service, import an ODB++ archive,
update mount points using a file, and properly close the connection.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as updating mount points
for printed circuit boards (PCBs) using a CSV file. This script shows how to:

- Launch the Sherlock service.
- Import an ODB++ archive.
- Update mount points using a CSV file.
- Properly close the gRPC connection.

The updated mount points can be used for further structural analysis and validation.

.. todo::
    Before running this script, download the file **updateMountPoints.csv** from the repository
    `Project Configuration`_.
"""

# sphinx_gallery_thumbnail_path = './images/update_mount_points_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportODBError, SherlockUpdateMountPointsByFileError

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "242"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import ODB++ Archive
# =====================
# Import the ODB++ archive from the Sherlock tutorial directory.

try:
    odb_archive_path = os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "ODB++ Tutorial.tgz")
    sherlock.project.import_odb_archive(
        file_path=odb_archive_path,
        allow_subdirectories=True,
        include_layers=True,
        use_stackup=True,
        project="Tutorial",
        cca_name="Card",
    )
    print("ODB++ archive imported successfully.")
except SherlockImportODBError as e:
    print(f"Error importing ODB++ archive: {str(e)}")

###############################################################################
# Update Mount Points by File
# ============================
# Update the mount points for the "Card" of the "Tutorial" project using a CSV file.

csv_file_path = os.path.join(os.getcwd(), "updateMountPoints.csv")

try:
    sherlock.layer.update_mount_points_by_file(
        project_name="Tutorial",
        cca_name="Card",
        file_path=csv_file_path,
    )
    print("Mount points updated successfully using the CSV file.")
except SherlockUpdateMountPointsByFileError as e:
    print(f"Error updating mount points by file: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
