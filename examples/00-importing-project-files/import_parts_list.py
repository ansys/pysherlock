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
.. _ref_import_odb_and_parts_list:

=============================================
Import ODB++ Archive and Parts List
=============================================

This example demonstrates how to launch the Sherlock gRPC service, import an ODB++ archive,
import parts lists, and properly close the connection.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as importing ODB++
archives and parts lists.
This script shows how to:

- Launch the Sherlock service.
- Import an ODB++ archive with specified project and CCA names.
- Import parts lists with different settings.
- Properly close the gRPC connection.

These functionalities enable users to prepare projects with ODB++ data and associated parts lists
for further analysis.

.. todo::
    Before running this script, download the file **partslist.csv** from the repository
    `Importing Project and Files`_.
"""

# sphinx_gallery_thumbnail_path = './images/import_odb_and_parts_list_example.png'

import os
import time

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportODBError, SherlockImportPartsListError

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
# Import an ODB++ archive with specified project and CCA names.

try:
    odb_path = os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "ODB++ Tutorial.tgz")
    sherlock.project.import_odb_archive(
        file_path=odb_path,
        allow_subdirectories=True,
        include_layers=True,
        use_stackup=True,
        use_materials=True,
        project="Test",
        cca_name="Card",
    )
    print("ODB++ archive imported successfully.")
except SherlockImportODBError as e:
    print(f"Error importing ODB++ archive: {str(e)}")

###############################################################################
# Import Parts List
# ==================
# Import parts lists with different settings for the "Test" project and "Card" CCA.

try:
    parts_list_path = os.path.join(os.getcwd(), "partslist.csv")

    # Import parts list with validation enabled
    sherlock.parts.import_parts_list(
        project="Test", cca_name="Card", file_path=parts_list_path, validate=True
    )
    print("Parts list imported successfully with validation.")
except SherlockImportPartsListError as e:
    print(f"Error importing parts list with validation: {str(e)}")

try:
    # Import parts list without validation
    sherlock.parts.import_parts_list(
        project="Test", cca_name="Card", file_path=parts_list_path, validate=False
    )
    print("Parts list imported successfully without validation.")
except SherlockImportPartsListError as e:
    print(f"Error importing parts list without validation: {str(e)}")

# Wait for 5 seconds to ensure all processes are completed.
time.sleep(5)

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
