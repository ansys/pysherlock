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
.. _ref_import_odb_archive:

====================
Import ODB++ Archive
====================

This example demonstrates how to launch the Sherlock gRPC service, import an ODB++ archive,
and handle common exceptions during the import process.

Description
Sherlock's gRPC API enables automation of various workflows, including importing ODB++ archives.
This script demonstrates how to:
- Connect to the Sherlock service.
- Import an ODB++ archive.
- Handle import errors gracefully.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_odb_import_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportODBError

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
# Import ODB++ Archive
# ====================
# Import an ODB++ archive provided with the Sherlock installation.

try:
    odb_path = os.path.join(get_sherlock_tutorial_path(), "ODB++ Tutorial.tgz")
    sherlock.project.import_odb_archive(
        archive_file=odb_path,
        process_layer_thickness=True,
        include_other_layers=True,
        process_cutout_file=True,
        guess_part_properties=True,
        ims_stackup=True,
        project="Test",
        cca_name="Card",
    )
    print("ODB++ archive imported successfully.")
except SherlockImportODBError as e:
    print(f"Error importing ODB++ archive: {e}")
