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
.. _ref_update_potting_region:

==============================
Add and Update Potting Regions
==============================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
add potting regions, update existing potting regions, and properly close the connection.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as adding and updating potting
regions for CCAs.
This script demonstrates how to:
- Connect to the Sherlock service.
- Import a project.
- Add a potting region.
- Update an existing potting region.
"""

# sphinx_gallery_thumbnail_path = './images/update_potting_region_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockAddPottingRegionError,
    SherlockImportProjectZipArchiveError,
)
from ansys.sherlock.core.types.layer_types import (
    PolygonalShape,
    PottingRegion,
    PottingRegionUpdateData,
    UpdatePottingRegionRequest,
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

potting_region_id = "Test Region"

###############################################################################
# Add Potting Region
# ==================
# Add a new potting region to a CCA.

try:
    polygonal_shape = PolygonalShape(
        points=[
            (0, 0),
            (0, 6.35),
            (9.77, 0),
        ],
        rotation=87.8,
    )
    sherlock.layer.add_potting_region(
        project="Test",
        potting_regions=[
            {
                "cca_name": "Auto Relay",
                "potting_id": potting_region_id,
                "side": "TOP",
                "material": "epoxyencapsulant",
                "potting_units": "in",
                "thickness": 0.1,
                "standoff": 0.2,
                "shape": polygonal_shape,
            },
        ],
    )
    print("Potting region added successfully.")
except SherlockAddPottingRegionError as e:
    print(f"Error adding potting region: {e}")

###############################################################################
# Update Potting Region
# =====================
# Update an existing potting region.

update_data = PottingRegionUpdateData(
    potting_region_id_to_update=potting_region_id,
    potting_region=PottingRegion(
        cca_name="Main Board",
        potting_id="Updated Test Region",
        potting_side="BOT",
        potting_material="epoxyencapsulant",
        potting_units="mm",
        potting_thickness=0.3,
        potting_standoff=0.1,
        shape=PolygonalShape(
            points=[(0, 1), (5, 1), (5, 5), (1, 5)],
            rotation=45.0,
        ),
    ),
)

try:
    update_request = UpdatePottingRegionRequest(
        project="Test",
        update_potting_regions=[update_data],
    )
    sherlock.layer.update_potting_region(update_request)
    print("Potting region updated successfully.")
except Exception as e:
    print(f"Error updating potting region: {e}")
