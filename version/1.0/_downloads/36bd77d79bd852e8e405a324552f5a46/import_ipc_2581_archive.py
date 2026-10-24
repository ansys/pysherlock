# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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
.. _ref_import_ipc2581:

=======================
Import IPC-2581 Archive
=======================

This example demonstrates how to connect to the Sherlock gRPC service and import an
IPC-2581 project,

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as importing IPC-2581 archives.
This script demonstrates how to:
- Connect to the Sherlock service.
- Import an IPC-2581 archive without specifying a project or CCA name.

This functionality is useful for initializing projects with IPC-2581 data for further
analysis and workflows.
"""

# sphinx_gallery_thumbnail_path = './images/import_ipc2581_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportIpc2581Error,
    SherlockImportProjectZipArchiveError,
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
# Import a sample project ZIP archive provided with the Sherlock installation.

try:
    sherlock.project.import_project_zip_archive(
        project="Test",
        category="Demos",
        archive_file=os.path.join(get_sherlock_tutorial_path(), "Tutorial Project.zip"),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project: {e}")

###############################################################################
# Import IPC-2581 Archive
# =======================
# Import an IPC-2581 archive without specifying a project or CCA name.

try:
    ipc2581_path = os.path.join(os.getcwd(), "IPC2581A-TestCase2.cvg")
    sherlock.project.import_ipc2581_archive(
        archive_file=ipc2581_path,
        include_other_layers=True,
        guess_part_properties=True,
        project="Test",
        cca_name=None,
        polyline_simplification=False,
        polyline_tolerance=0.1,
        polyline_tolerance_units="mm",
    )
    print("IPC-2581 archive imported successfully.")
except SherlockImportIpc2581Error as e:
    print(f"Error importing IPC-2581 archive: {e}")
