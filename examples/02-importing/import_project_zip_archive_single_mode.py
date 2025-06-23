# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

======================================
Sherlock Project Import in Single Mode
======================================

This example demonstrates how to launch the Sherlock gRPC service in single-project mode,
import a project, and handle common exceptions during the import process.

Description
Sherlock's gRPC API enables automation of various workflows, including project management.
This script demonstrates how to:
- Connect to the Sherlock service in single-project mode.
- Import a sample project archive.
- Handle import errors gracefully.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_import_single_mode_example.png'

import os

from examples.examples_globals import (
    get_sherlock_tutorial_path,
    get_temp_dir,
    store_sherlock_tutorial_path,
)

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportProjectZipArchiveSingleModeError

###############################################################################
# Launch PySherlock service in single-project mode
# ================================================
# Launch the Sherlock service using the specified project path and wait for initialization.

sherlock, ansys_install_path = launcher.launch_and_connect(
    port=9093,
    single_project_path=os.getcwd(),
    # sherlock_command_args="-noGUI",
)
store_sherlock_tutorial_path(ansys_install_path)

###############################################################################
# Import Sherlock Project in Single Mode
# ======================================
# Import a tutorial project ZIP archive provided with the Sherlock installation.

try:
    sherlock.project.import_project_zip_archive_single_mode(
        project="Test",
        category="Demos",
        archive_file=os.path.join(get_sherlock_tutorial_path(), "Auto Relay Project.zip"),
        destination_file_directory=get_temp_dir(),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveSingleModeError as e:
    print(f"Error importing project: {e}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
