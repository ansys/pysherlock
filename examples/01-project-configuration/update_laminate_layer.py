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

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportODBError, SherlockUpdateLaminateLayerError

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "242"
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
# Update Laminate Layer Properties
# =================================
# Update the laminate layer properties for the "Card" of the "Test" project.

try:
    sherlock.stackup.update_laminate_layer(
        project_name="Test",
        cca_name="Card",
        layer_number="2",
        layer_material="Generic",
        layer_type="FR-4",
        layer_material_name="Generic FR-4",
        layer_thickness=0.015,
        layer_thickness_unit="in",
        layer_glass_styles=[("106", 68.0, 0.015, "in")],
        dielectric_material="E-GLASS",
        conductive_material="COPPER",
        conductive_thickness="0.0",
    )
    print("Laminate layer properties updated successfully.")
except SherlockUpdateLaminateLayerError as e:
    print(f"Error updating laminate layer properties: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
