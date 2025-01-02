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
.. _ref_sherlock_export_net_list:

====================================
Export Net List
====================================

This example demonstrates how to launch the Sherlock gRPC service, import an ODB++ project archive,
and export the net list associated with the imported project.

Description
Sherlock's gRPC API enables automation of various workflows, including net list export.
This script demonstrates:

- Launching the Sherlock service.
- Importing an ODB++ archive.
- Exporting the net list from the project.
- Properly exiting the gRPC connection.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_export_net_list_example.png'

import os
import time

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockExportNetListError, SherlockImportODBError
from ansys.sherlock.core.types.common_types import TableDelimiter

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service using the default port and wait for initialization.

VERSION = "252"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

time.sleep(5)  # Allow time for environment setup

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import ODB++ Archive
# =====================
# Import an ODB++ project archive provided with the Sherlock installation.

try:
    odb_archive_path = os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "ODB++ Tutorial.tgz")
    sherlock.project.import_odb_archive(
        odb_archive_path,
        overwrite=True,
        create_project=True,
        use_guidelines=True,
        use_predefined_materials=True,
        project="Test",
        cca_name="Card",
    )
    print("ODB++ project imported successfully.")
except SherlockImportODBError as e:
    print(f"Error importing ODB++ project: {str(e)}")

###############################################################################
# Export Net List
# ================
# Export the net list from the imported project.

try:
    net_list_path = os.path.join(os.getcwd(), "exportedNetList.csv")
    sherlock.parts.export_net_list(
        "Test",
        "Card",
        net_list_path,
        col_delimiter=TableDelimiter.COMMA,
        overwrite_existing=True,
        utf8_enabled=True,
    )
    print(f"Net list exported successfully to: {net_list_path}")
except SherlockExportNetListError as e:
    print(f"Error exporting net list: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

time.sleep(5)  # Allow time for any remaining operations
sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
