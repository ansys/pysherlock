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
.. _ref_sherlock_export_aedb:

==========================
Export AEDB
==========================

This example demonstrates how to launch the Sherlock gRPC service, import an ODB++ archive,
and export an AEDB file for a printed circuit board (PCB).

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as exporting an AEDB file for a PCB.
This script demonstrates how to:

- Launch the Sherlock service.
- Import an ODB++ archive.
- Export an AEDB file.
- Properly close the gRPC connection.

The exported AEDB file can be used for further analysis or integration with other software tools.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_export_aedb_example.png'

import os
import time

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockExportAEDBError, SherlockImportODBError

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "242"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

time.sleep(5)  # Allow time for environment setup

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
# Export AEDB File
# =================
# Export the AEDB file for the "Card" of the "Test" project to the specified path.

time.sleep(5)  # Allow time for the project to load completely

try:
    aedb_export_path = os.path.join(os.getcwd(), "test.aedb")
    sherlock.model.export_aedb(
        project="Test",
        cca_name="Card",
        export_file=aedb_export_path,
        include_geometry=True,
        include_annotations=False,
    )
    print(f"AEDB file exported successfully to: {aedb_export_path}")
except SherlockExportAEDBError as e:
    print(f"Error exporting AEDB: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
