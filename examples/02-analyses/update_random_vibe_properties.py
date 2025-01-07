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
.. _ref_sherlock_update_random_vibe_props:

=========================================
Update Random Vibration Properties
=========================================

This example demonstrates how to launch the Sherlock gRPC service, import project data,
and update random vibration properties.

Description
-----------
Sherlock allows you to configure random vibration properties for specific PCBs. This script includes
the following steps:

- Launch the Sherlock service.
- Import ODB++ archive into the project.
- Update random vibration properties.
- Exit the gRPC connection after the configuration.

For further details, refer to the official documentation on random vibration properties in Sherlock.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_update_random_vibe_props_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportODBError, SherlockUpdateRandomVibePropsError

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "251"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import ODB Archive
# ==================
# Import a project into the Sherlock environment.

try:
    # Import ODB++ archive into the project
    sherlock.project.import_odb_archive(
        ANSYS_ROOT
        + os.path.sep
        + "sherlock"
        + os.path.sep
        + "tutorial"
        + os.path.sep
        + "ODB++ Tutorial.tgz",
        True,
        True,
        True,
        True,
        project="Test",
        cca_name="Card",
    )
except SherlockImportODBError as e:
    print(f"Error importing ODB archive: {str(e)}")

###############################################################################
# Update Random Vibration Properties
# ===================================
# Configure random vibration properties for the PCB.

try:
    sherlock.analysis.update_random_vibe_props(
        "Test",
        "Card",
        random_vibe_damping="0.01, 0.03",
        part_validation_enabled=False,
        require_material_assignment_enabled=False,
        model_source="GENERATED",
    )
except SherlockUpdateRandomVibePropsError as e:
    print(f"Error updating random vibration properties: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
