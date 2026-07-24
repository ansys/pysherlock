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
.. _ref_add_potting_region:

====================================
Add Potting Regions for PCB Analysis
====================================

This example demonstrates how to use the Sherlock gRPC service to:
- Import a project.
- Add potting regions to a PCB model.
- Define potting shapes and properties.

Description
-----------
This script connects to the Sherlock gRPC service, imports a project,
and creates potting regions.

"""

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockAddPottingRegionError,
    SherlockImportProjectZipArchiveError,
)
from ansys.sherlock.core.types.layer_types import PolygonalShape

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
# Add Potting Region
# ==================
# Define a polygonal shape and add it as a potting region to the PCB.

try:
    # Define the polygonal shape for the potting region
    polygonal_shape = PolygonalShape(points=[(0, 0), (0, 6.35), (9.77, 0)], rotation=87.8)

    # Add the potting region
    sherlock.layer.add_potting_region(
        project="Test",
        potting_regions=[
            {
                "cca_name": "Auto Relay",
                "potting_id": "Test Region",
                "side": "TOP",
                "material": "epoxyencapsulant",
                "potting_units": "in",
                "thickness": 0.1,
                "standoff": 0.2,
                "shape": polygonal_shape,
            }
        ],
    )
    print("Potting region added successfully.")
except SherlockAddPottingRegionError as e:
    print(f"Error adding potting region: {e}")
