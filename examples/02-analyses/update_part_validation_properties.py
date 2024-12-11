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
.. _ref_sherlock_run_part_list_validation_analysis:

===========================================
Run Part List Validation Analysis
===========================================

This example demonstrates how to launch the Sherlock gRPC service, import project data,
and configure part list validation analysis properties.

Description
-----------
Sherlock allows you to perform part list validation analysis. This script includes the following steps:

- Launch the Sherlock service.
- Import ODB++ archive into the project.
- Configure the properties for part list validation analysis.
- Exit the gRPC connection after the configuration.

For further details, refer to the official documentation on part list validation analysis in Sherlock.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_run_part_list_validation_analysis_example.png'

import os
import time
from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockUpdatePartListValidationAnalysisPropsError, SherlockImportODBError

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = '252'
ANSYS_ROOT = os.getenv('AWP_ROOT' + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import ODB Archive
# ==================
# Import a project into the Sherlock environment.

try:
    # Import ODB++ archive into the project
    sherlock.project.import_odb_archive(
        ANSYS_ROOT + os.path.sep + 'sherlock' + os.path.sep + 'tutorial' + os.path.sep + 'ODB++ Tutorial.tgz',
        True, True, True, True, project="Test", cca_name="Card"
    )
except SherlockImportODBError as e:
    print(f"Error importing ODB archive: {str(e)}")

###############################################################################
# Update Part List Validation Properties
# ======================================
# Configure properties for part list validation analysis.

try:
    # Update properties for part list validation analysis
    sherlock.analysis.update_part_list_validation_analysis_props(
        "Test",
        [{
            "cca_name": "Card",
            "process_use_avl": True,
            "process_use_wizard": True,
            "process_check_confirmed_properties": False,
            "process_check_part_numbers": False,
            "matching_mode": "Part",
            "avl_require_internal_part_number": False,
            "avl_require_approved_description": True,
            "avl_require_approved_manufacturer": False,
        }]
    )
except SherlockUpdatePartListValidationAnalysisPropsError as e:
    print(f"Error updating part list validation analysis properties: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")