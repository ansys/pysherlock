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
.. _ref_update_part_location:

================================
Update Part Locations
================================

This example demonstrates how to launch the Sherlock gRPC service, import an ODB++ archive,
update part locations, and properly close the connection.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as updating part
locations for printed circuit boards (PCBs). This script shows how to:

- Launch the Sherlock service.
- Import an ODB++ archive.
- Update part locations.
- Properly close the gRPC connection.

The updated part locations can be used for accurate placement validation and optimization.
"""

# sphinx_gallery_thumbnail_path = './images/update_part_location_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportODBError, SherlockUpdatePartsLocationsError

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "252"
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
        project="Test",
        cca_name="Card",
    )
    print("ODB++ archive imported successfully.")
except SherlockImportODBError as e:
    print(f"Error importing ODB++ archive: {str(e)}")

###############################################################################
# Update Part Locations
# ======================
# Update the part locations for the "Card" of the "Test" project.

try:
    part_locations = [
        ("C1", "-2.7", "-1.65", "0", "in", "TOP", "False"),
        ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
    ]
    sherlock.parts.update_parts_locations(
        project_name="Test",
        cca_name="Card",
        parts_data=part_locations,
    )
    print("Part locations updated successfully.")
except SherlockUpdatePartsLocationsError as e:
    print(f"Error updating part locations: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
