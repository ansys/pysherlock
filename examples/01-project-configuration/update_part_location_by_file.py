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
.. _ref_update_part_location_file:

=============================
Update Part Locations by File
=============================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and update part locations using a CSV file.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as updating part
locations for printed circuit boards (PCBs) using a CSV file.
This script demonstrates how to:
- Connect to the Sherlock service.
- Import a project.
- Update part locations using a CSV file.

The updated part locations can ensure consistency across various PCB designs.
"""

# sphinx_gallery_thumbnail_path = './images/update_part_location_file_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockUpdatePartsLocationsByFileError,
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
# Update Part Locations by File
# =============================
# Update the part locations for the "Card" of the "Test" project using a CSV file.

csv_file_path = os.path.join(os.getcwd(), "partslist.csv")

try:
    sherlock.parts.update_parts_locations_by_file(
        project="Test",
        cca_name="Main Board",
        file_path=csv_file_path,
        numeric_format="JAPANESE",
    )
    print("Part locations updated successfully using the CSV file.")
except SherlockUpdatePartsLocationsByFileError as e:
    print(f"Error updating part locations by file: {e}")
