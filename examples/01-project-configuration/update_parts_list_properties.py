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
.. _ref_update_parts_list_properties:

============================================
Update and Export Parts List Properties
============================================

This example demonstrates how to launch the Sherlock gRPC service, import an ODB++ archive,
update the parts list properties, export the parts list, and properly close the connection.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as updating the
parts list properties and exporting the parts list for printed circuit boards (PCBs).
This script shows how to:

- Launch the Sherlock service.
- Import an ODB++ archive.
- Update the parts list properties.
- Export the parts list.
- Properly close the gRPC connection.

The updated properties and exported list ensure consistency and provide
documentation for further use.
"""

# sphinx_gallery_thumbnail_path = './images/update_parts_list_properties_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockExportPartsListError,
    SherlockImportODBError,
    SherlockUpdatePartsListPropertiesError,
)

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
# Update Parts List Properties
# ============================
# Update the parts list properties for the "Card" of the "Test" project.

try:
    parts_properties = [
        {
            "reference_designators": ["C1"],
            "properties": [{"name": "partType", "value": "RESISTOR"}],
        },
        {
            "reference_designators": ["C2"],
            "properties": [{"name": "locX", "value": "1"}, {"name": "userNotes", "value": "test"}],
        },
        {"reference_designators": ["U6"], "properties": [{"name": "userNotes", "value": "test2"}]},
        {"reference_designators": ["U7"], "properties": [{"name": "leadBend", "value": "45"}]},
    ]
    sherlock.parts.update_parts_list_properties(
        project_name="Test",
        cca_name="Card",
        properties=parts_properties,
    )
    print("Parts list properties updated successfully.")
except SherlockUpdatePartsListPropertiesError as e:
    print(f"Error updating parts list properties: {str(e)}")

###############################################################################
# Export Parts List
# ==================
# Export the parts list for the "Card" of the "Test" project to a CSV file.

try:
    export_path = os.path.join(os.getcwd(), "exportedPartsList.csv")
    sherlock.parts.export_parts_list(
        project_name="Test",
        cca_name="Card",
        file_path=export_path,
    )
    print("Parts list exported successfully to", export_path)
except SherlockExportPartsListError as e:
    print(f"Error exporting parts list: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
