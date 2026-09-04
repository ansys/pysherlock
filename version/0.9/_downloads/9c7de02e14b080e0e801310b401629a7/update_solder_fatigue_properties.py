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
.. _ref_sherlock_update_solder_fatigue_props:

================================
Update Solder Fatigue Properties
================================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and update solder fatigue properties.

Description
-----------
This script shows how to configure solder fatigue properties for a PCB assembly.
It performs the following steps:
- Connect to the Sherlock service.
- Import a project.
- Update solder fatigue properties.

For further details, refer to the official documentation on solder fatigue properties in Sherlock.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_update_solder_fatigue_props_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockUpdateSolderFatiguePropsError,
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
# Update Solder Fatigue Properties
# ================================
# Configure solder fatigue properties for the PCB assembly.

try:
    sherlock.analysis.update_solder_fatigue_props(
        project="Test",
        solder_fatigue_properties=[
            {
                "cca_name": "Auto Relay",
                "solder_material": "TIN-LEAD (63SN37PB)",
                "part_temp": 70,
                "part_temp_units": "F",
                "use_part_temp_rise_min": True,
                "part_validation_enabled": True,
            }
        ],
    )
    print("Solder fatigue properties updated successfully.")
except SherlockUpdateSolderFatiguePropsError as e:
    print(f"Error updating solder fatigue properties: {e}")
