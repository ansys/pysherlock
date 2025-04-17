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
.. _ref_update_laminate_layer:

================================
Update Laminate Layer Properties
================================

This example demonstrates how to launch the Sherlock gRPC service, import an ODB++ archive,
update laminate layer properties, and properly close the connection.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as updating laminate layer
properties for printed circuit boards (PCBs). This script shows how to:

- Launch the Sherlock service.
- Import an ODB++ archive.
- Update laminate layer properties.
- Properly close the gRPC connection.

The updated properties can be used for further design validation and optimization.
"""

# sphinx_gallery_thumbnail_path = './images/update_laminate_layer_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockUpdateLaminateLayerError,
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
# Update Laminate Layer Properties
# ================================
# Update the laminate layer properties for the "Main Board" of the "Test" project.

try:
    sherlock.stackup.update_laminate_layer(
        project="Test",
        cca_name="Main Board",
        layer="2",
        manufacturer="Generic",
        grade="Cyanate Ester",
        material="Generic CE Quartz",
        thickness=0.015,
        thickness_unit="in",
        construction_style="106",
        glass_construction=[("106", 71.0, 0.015, "in")],
        fiber_material="QUARTZ",
        conductor_material="GOLD",
        conductor_percent="10.0",
    )

    print("Laminate layer properties updated successfully.")
except SherlockUpdateLaminateLayerError as e:
    print(f"Error updating laminate layer properties: {e}")
