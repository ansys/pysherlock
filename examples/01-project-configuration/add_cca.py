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
.. _ref_add_cca_and_import_odb:

=========================
Add Circuit Card Assembly
=========================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and add a CCA (Circuit Card Assembly) to a project.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as adding CCAs to a project
and importing ODB++ archives.
This script demonstrates how to:
- Connect to the Sherlock service.
- Import a project.
- Add CCAs to the project.

The added CCAs allow for proper circuit analysis and component tracking within the project.
"""

# sphinx_gallery_thumbnail_path = './images/add_cca_and_import_odb_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockAddCCAError, SherlockImportProjectZipArchiveError

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
    print(f"Error importing project: {str(e)}")

###############################################################################
# Add CCA to Project
# ===================
# Add a CCA to a project.

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
except SherlockAddCCAError as e:
    print(f"Error adding CCA: {str(e)}")
