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
.. _ref_sherlock_run_harmonic_vibe_analysis:

=================================
Run Harmonic Vibration Analysis
=================================

This example demonstrates how to launch the Sherlock gRPC service, import project data,
and configure harmonic vibration analysis properties.

Description
-----------
Sherlock allows you to perform harmonic vibration analysis. This script includes
the following steps:

- Launch the Sherlock service.
- Import ODB++ archive into the project.
- Configure the properties for harmonic vibration analysis.
- Exit the gRPC connection after the configuration.

For further details, refer to the official documentation on harmonic vibration analysis in Sherlock.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_run_harmonic_vibe_analysis_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockUpdateHarmonicVibePropsError,
)

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "251"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

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
        archive_file=(os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "Tutorial Project.zip")),
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
                "cca_name": "Main Board",
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

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
