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
.. _ref_sherlock_update_mechanical_shock_props:

=============================
Run Mechanical Shock Analysis
=============================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and configure mechanical shock analysis properties.

Description
-----------
Sherlock allows you to perform mechanical shock analysis.
This script performs the following steps:
- Connect to the Sherlock service.
- Import a project.
- Configure the properties for mechanical shock analysis.
"""

"""
sphinx_gallery_thumbnail_path =
'./images/sherlock_update_mechanical_shock_analysis_props_example.png'
"""

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockUpdateMechanicalShockPropsError,
)
from ansys.sherlock.core.types.analysis_types import ModelSource

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
# ========================
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
# Update Mechanical Shock Properties
# ==================================
# Configure properties for mechanical shock analysis.

try:
    # Update properties for mechanical shock analysis
    sherlock.analysis.update_mechanical_shock_props(
        project="Test",
        mechanical_shock_properties=[
            {
                "cca_name": "Auto Relay",
                "model_source": ModelSource.GENERATED,
                "shock_result_count": 3,
                "critical_shock_strain": 5,
                "critical_shock_strain_units": "strain",
                "part_validation_enabled": True,
                "require_material_assignment_enabled": False,
                "force_model_rebuild": "AUTO",
                "natural_freq_min": 5,
                "natural_freq_min_units": "Hz",
                "natural_freq_max": 50,
                "natural_freq_max_units": "KHz",
                "analysis_temp": 100,
                "analysis_temp_units": "F",
            }
        ],
    )
    print("Mechanical shock properties updated successfully.")
except SherlockUpdateMechanicalShockPropsError as e:
    print(f"Error updating mechanical shock properties: {e}")
