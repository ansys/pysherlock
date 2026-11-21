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
.. _ref_update_part_modeling_props:

===============================
Update Part Modeling Properties
===============================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and update part modeling properties.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as updating part
modeling properties for printed circuit boards (PCBs).
This script demonstrates how to:
- Connect to the Sherlock service.
- Import a project.
- Update part modeling properties.

The updated properties ensure accurate simulation results for mechanical and thermal analyses.
"""

# sphinx_gallery_thumbnail_path = './images/update_part_modeling_props_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockUpdatePartModelingPropsError,
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
# Import the tutorial project zip archive from the Sherlock tutorial directory.

try:
    sherlock.project.import_project_zip_archive(
        project="Test",
        category="Demos",
        archive_file=os.path.join(get_sherlock_tutorial_path(), "Tutorial Project.zip"),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project zip archive: {e}")

###############################################################################
# Update Part Modeling Properties
# ===============================
# Update the part modeling properties for the "Card" of the "Test" project.

try:
    modeling_props = {
        "cca_name": "Main Board",
        "part_enabled": True,
        "part_min_size": 1,
        "part_min_size_units": "in",
        "part_elem_order": "First Order (Linear)",
        "part_max_edge_length": 1,
        "part_max_edge_length_units": "in",
        "part_max_vertical": 1,
        "part_max_vertical_units": "in",
        "part_results_filtered": True,
    }
    sherlock.analysis.update_part_modeling_props(
        project="Test",
        part_modeling_props=modeling_props,
    )
    print("Part modeling properties updated successfully.")
except SherlockUpdatePartModelingPropsError as e:
    print(f"Error updating part modeling properties: {e}")
