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
.. _ref_update_parts_list:

=================
Update Parts List
=================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
update the parts list, and properly close the connection.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as updating the
parts list for printed circuit boards (PCBs). This script shows how to:

- Launch the Sherlock service.
- Import a project.
- Update the parts list.
- Properly close the gRPC connection.

The updated parts list ensures alignment with a specified library for consistency and accuracy.
"""

# sphinx_gallery_thumbnail_path = './images/update_parts_list_example.png'

import os

import SherlockCommonService_pb2
import SherlockPartsService_pb2
from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockUpdatePartsListError,
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
        archive_file=os.path.join(get_sherlock_tutorial_path(), "Auto Relay Project.zip"),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project zip archive: {e}")

###############################################################################
# Update Parts List
# =================
# Update the parts list for the "Auto Relay" CCA of the "Test" project.

try:
    sherlock.parts.update_parts_list(
        project="Test",
        cca_name="Auto Relay",
        part_library="Sherlock Part Library",
        matching_mode=SherlockCommonService_pb2.MatchingMode.Both,
        duplication_mode=SherlockPartsService_pb2.DuplicationMode.Error,
    )
    print("Parts list updated successfully.")
except SherlockUpdatePartsListError as e:
    print(f"Error updating parts list: {e}")
