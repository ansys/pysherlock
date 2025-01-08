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
.. _ref_sherlock_update_solder_fatigue_props:

=========================================
Update Solder Fatigue Properties
=========================================

This example demonstrates how to launch the Sherlock gRPC service, import project data,
and update solder fatigue properties.

Description
-----------
This script shows how to configure solder fatigue properties for a PCB assembly. It includes the
following steps:

- Launch the Sherlock service.
- Import an ODB++ archive into the project.
- Update solder fatigue properties.
- Exit the gRPC connection after the configuration.

For further details, refer to the official documentation on solder fatigue properties in Sherlock.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_update_solder_fatigue_props_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportODBError, SherlockUpdateSolderFatiguePropsError

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "242"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import ODB Archive
# ==================
# Import a project into the Sherlock environment.

try:
    # Import ODB++ archive into the project
    odb_path = os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "ODB++ Tutorial.tgz")
    sherlock.project.import_odb_archive(
        odb_path, True, True, True, True, project="Test", cca_name="Card"
    )
except SherlockImportODBError as e:
    print(f"Error importing ODB archive: {str(e)}")

###############################################################################
# Update Solder Fatigue Properties
# ================================
# Configure solder fatigue properties for the PCB assembly.

try:
    sherlock.analysis.update_solder_fatigue_props(
        "Test",
        [
            {
                "cca_name": "Card",
                "solder_material": "TIN-LEAD (63SN37PB)",
                "part_temp": 70,
                "part_temp_units": "F",
                "use_part_temp_rise_min": True,
                "part_validation_enabled": True,
            }
        ],
    )
except SherlockUpdateSolderFatiguePropsError as e:
    print(f"Error updating solder fatigue properties: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
