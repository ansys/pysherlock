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
.. _ref_sherlock_run_mechanical_shock_analysis:

=========================================
Run Mechanical Shock Analysis
=========================================

This example demonstrates how to launch the Sherlock gRPC service, import project data,
and configure mechanical shock analysis properties.

Description
-----------
Sherlock allows you to perform mechanical shock analysis. This script includes the following steps:

- Launch the Sherlock service.
- Import ODB++ archive into the project.
- Configure the properties for mechanical shock analysis.
- Exit the gRPC connection after the configuration.

For further details, refer to the official documentation on mechanical shock analysis in Sherlock.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_run_mechanical_shock_analysis_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportODBError,
    SherlockUpdateMechanicalShockPropsError,
)
from ansys.sherlock.core.types.analysis_types import ModelSource

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
# Update Mechanical Shock Properties
# ==================================
# Configure properties for mechanical shock analysis.

try:
    # Update properties for mechanical shock analysis
    sherlock.analysis.update_mechanical_shock_props(
        "Test",
        [
            {
                "cca_name": "Card",
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
except SherlockUpdateMechanicalShockPropsError as e:
    print(f"Error updating mechanical shock properties: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
