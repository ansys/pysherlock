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
.. _ref_import_ipc2581:

===============================
Import IPC-2581 Archive
===============================

This example demonstrates how to launch the Sherlock gRPC service, import an IPC-2581 archive,
and properly close the connection.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as importing IPC-2581 archives.
This script shows how to:

- Launch the Sherlock service.
- Import an IPC-2581 archive without specifying a project or CCA name.
- Properly close the gRPC connection.

This functionality is useful for initializing projects with IPC-2581 data for further
analysis and workflows.

.. todo::
    Before running this script, download the file **IPC2581A-TestCase2.cvg** from the repository
    `Importing Project and Files`_.
"""

# sphinx_gallery_thumbnail_path = './images/import_ipc2581_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportIpc2581Error,
    SherlockImportProjectZipArchiveError,
)

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

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
# Import a sample project ZIP archive provided with the Sherlock installation.

try:
    sherlock.project.import_project_zip_archive(
        project="Test",
        category="Demos",
        archive_file=(os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "Tutorial Project.zip")),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project: {e}")

###############################################################################
# Import IPC-2581 Archive
# ========================
# Import an IPC-2581 archive without specifying a project or CCA name.

try:
    ipc2581_path = os.path.join(os.getcwd(), "IPC2581A-TestCase2.cvg")
    sherlock.project.import_ipc2581_archive(
        archive_file=ipc2581_path,
        include_other_layers=True,
        guess_part_properties=True,
        project="Test",
        cca_name=None,
        polyline_simplification=False,
        polyline_tolerance=0.1,
        polyline_tolerance_units="mm",
    )
    print("IPC-2581 archive imported successfully.")
except SherlockImportIpc2581Error as e:
    print(f"Error importing IPC-2581 archive: {e}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
