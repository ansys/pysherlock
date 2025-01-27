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
.. _ref_add_cca_and_import_odb:

==================================
Add Component Circuits Assemblies
==================================

This example demonstrates how to launch the Sherlock gRPC service, import an ODB++ archive,
add CCAs (Component Circuits Assemblies) to a project, and properly close the connection.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as adding CCAs to a project
and importing ODB++ archives. This script shows how to:

- Launch the Sherlock service.
- Import an ODB++ archive.
- Add CCAs to the project.
- Properly close the gRPC connection.

The added CCAs allow for proper circuit analysis and component tracking within the project.
"""

# sphinx_gallery_thumbnail_path = './images/add_cca_and_import_odb_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockAddCCAError, SherlockImportProjectZipArchiveError

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "242"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import Tutorial Project
# ========================
# Import the tutorial project zip archive from the Sherlock tutorial directory.

try:
    sherlock.project.import_project_zip_archive(
        project="Test",
        category="Demos",
        archive_file=(os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "Tutorial Project.zip")),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing ODB++ archive: {str(e)}")

###############################################################################
# Add CCAs to Project
# ===================
# Add two CCAs ("Card 2" and "Card 3") to the "Test" project.

try:
    sherlock.project.add_cca(
        project="Test",
        cca_properties=[
            {
                "cca_name": "Card 2",
                "description": "Second CCA",
                "default_solder_type": "SAC305",
                "default_stencil_thickness": 10,
                "default_stencil_thickness_units": "mm",
                "default_part_temp_rise": 20,
                "default_part_temp_rise_units": "C",
                "guess_part_properties_enabled": False,
            }
        ],
    )
    print("Card 2 added successfully.")

    sherlock.project.add_cca(
        project="Test",
        cca_properties=[
            {
                "cca_name": "Card 3",
                "description": "Third CCA",
                "default_solder_type": "SAC305",
                "default_stencil_thickness": 5,
                "default_stencil_thickness_units": "in",
                "default_part_temp_rise": 20,
                "default_part_temp_rise_units": "K",
                "guess_part_properties_enabled": False,
            }
        ],
    )
    print("Card 3 added successfully.")
except SherlockAddCCAError as e:
    print(f"Error adding CCA: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
