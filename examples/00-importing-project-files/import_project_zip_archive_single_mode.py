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
.. _ref_sherlock_project_import_single_mode:

=======================================
Sherlock Project Import in Single Mode
=======================================

This example demonstrates how to launch the Sherlock gRPC service in single-project mode,
import a project archive, and handle common exceptions during the import process.

Description
Sherlock's gRPC API enables automation of various workflows, including project management.
This script demonstrates:

- Launching the Sherlock service in single-project mode.
- Importing a sample project archive.
- Handling import errors gracefully.
- Properly exiting the gRPC connection.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_import_single_mode_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportProjectZipArchiveSingleModeError

###############################################################################
# Launch PySherlock service in single-project mode
# ================================================
# Launch the Sherlock service using the specified project path and wait for initialization.

VERSION = "242"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092, single_project_path=os.getcwd())

###############################################################################
# Import Sherlock Project in Single Mode
# =======================================
# Import a tutorial project ZIP archive provided with the Sherlock installation.

try:
    sherlock.project.import_project_zip_archive_single_mode(
        project="Test",
        category="Demos",
        archive_file=(os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "Tutorial Project.zip")),
        destination_file_directory=os.getcwd(),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveSingleModeError as e:
    print(f"Error importing project: {e}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
