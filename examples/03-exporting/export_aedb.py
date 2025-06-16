# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

===========
Export AEDB
===========

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and export an AEDB file for a CCA.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as exporting an AEDB file for a CCA.
This script demonstrates how to:

- Connect to the Sherlock service.
- Import a project.
- Export an AEDB file.

The exported AEDB file can be used for further analysis or integration with other software tools.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_export_aedb_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path, get_temp_dir

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockExportAEDBError, SherlockImportProjectZipArchiveError

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
# Export AEDB File
# =================
# Export the AEDB file for the "Card" of the "Test" project to the specified path.

try:
    aedb_export_path = os.path.join(get_temp_dir(), "test.aedb")
    sherlock.model.export_aedb(
        project_name="Test",
        cca_name="Auto Relay",
        export_file=aedb_export_path,
    )
    print(f"AEDB file exported successfully to: {aedb_export_path}")
except SherlockExportAEDBError as e:
    print(f"Error exporting AEDB: {e}")
