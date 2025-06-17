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
.. _ref_sherlock_update_harmonic_vibe_props:

=============================================
Update Harmonic Vibration Analysis properties
=============================================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and configure harmonic vibration analysis properties.

Description
-----------
Sherlock allows you to perform harmonic vibration analysis.
This script performs the following steps:
- Connect to the Sherlock service.
- Import a project.
- Configure the properties for harmonic vibration analysis.
"""

"""
 sphinx_gallery_thumbnail_path =
 './images/sherlock_update_harmonic_vibe_analysis_props_example.png'
"""

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockUpdateHarmonicVibePropsError,
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
        archive_file=os.path.join(get_sherlock_tutorial_path(), "Auto Relay Project.zip"),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project zip archive: {e}")

###############################################################################
# Update Harmonic Vibration Properties
# ====================================
# Configure properties for harmonic vibration analysis.

try:
    # Update properties for harmonic vibration analysis
    sherlock.analysis.update_harmonic_vibe_props(
        project="Test",
        harmonic_vibe_properties=[
            {
                "cca_name": "Auto Relay",
                "harmonic_vibe_count": 2,
                "harmonic_vibe_damping": "0.01, 0.05",
                "part_validation_enabled": False,
                "require_material_assignment_enabled": False,
                "analysis_temp": 23.8,
                "analysis_temp_units": "C",
                "filter_by_event_frequency": False,
            }
        ],
    )
    print("Harmonic vibration properties updated successfully.")
except SherlockUpdateHarmonicVibePropsError as e:
    print(f"Error updating harmonic vibration properties: {e}")
