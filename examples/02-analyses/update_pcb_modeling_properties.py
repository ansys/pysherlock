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
.. _ref_sherlock_update_pcb_modeling_props:

===========================================
Update PCB Modeling Properties
===========================================

This example demonstrates how to launch the Sherlock gRPC service, import project data,
and configure PCB modeling properties for various analysis types.

Description
-----------
Sherlock allows you to configure PCB modeling properties for multiple analysis types. This script
includes the following steps:

- Launch the Sherlock service.
- Import ODB++ archive into the project.
- Configure PCB modeling properties for several analysis types.
- Exit the gRPC connection after the configuration.

For further details, refer to the official documentation on PCB modeling properties in Sherlock.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_update_pcb_modeling_props_example.png'

import os

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportODBError, SherlockUpdatePcbModelingPropsError
from ansys.sherlock.core.types.analysis_types import (
    ElementOrder,
    UpdatePcbModelingPropsRequestAnalysisType,
    UpdatePcbModelingPropsRequestPcbMaterialModel,
    UpdatePcbModelingPropsRequestPcbModelType,
)

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
# Update PCB Modeling Properties
# ===============================
# Configure PCB modeling properties for various analysis types.

try:
    sherlock.analysis.update_pcb_modeling_props(
        "Test",
        ["Card"],
        [
            (
                UpdatePcbModelingPropsRequestAnalysisType.HARMONIC_VIBE,
                UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                True,
                UpdatePcbModelingPropsRequestPcbMaterialModel.UNIFORM,
                ElementOrder.SOLID_SHELL,
                6,
                "mm",
                3,
                "mm",
                True,
            )
        ],
    )
    sherlock.analysis.update_pcb_modeling_props(
        "Test",
        ["Card"],
        [
            (
                UpdatePcbModelingPropsRequestAnalysisType.NATURAL_FREQUENCY,
                UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                True,
                UpdatePcbModelingPropsRequestPcbMaterialModel.UNIFORM,
                ElementOrder.SOLID_SHELL,
                6,
                "mm",
                3,
                "mm",
                True,
            )
        ],
    )
    sherlock.analysis.update_pcb_modeling_props(
        "Test",
        ["Card"],
        [
            (
                UpdatePcbModelingPropsRequestAnalysisType.ICT,
                UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                True,
                UpdatePcbModelingPropsRequestPcbMaterialModel.UNIFORM,
                ElementOrder.SOLID_SHELL,
                6,
                "mm",
                3,
                "mm",
                True,
            )
        ],
    )
    sherlock.analysis.update_pcb_modeling_props(
        "Test",
        ["Card"],
        [
            (
                UpdatePcbModelingPropsRequestAnalysisType.MECHANICAL_SHOCK,
                UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                True,
                UpdatePcbModelingPropsRequestPcbMaterialModel.LAYERED,
                ElementOrder.SOLID_SHELL,
                6,
                "mm",
                3,
                "mm",
                True,
            )
        ],
    )
    sherlock.analysis.update_pcb_modeling_props(
        "Test",
        ["Card"],
        [
            (
                UpdatePcbModelingPropsRequestAnalysisType.RANDOM_VIBE,
                UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                True,
                UpdatePcbModelingPropsRequestPcbMaterialModel.LAYERED_ELEMENTS,
                5,
                ElementOrder.SOLID_SHELL,
                6,
                "mm",
                3,
                "mm",
                True,
            )
        ],
    )
    sherlock.analysis.update_pcb_modeling_props(
        "Test",
        ["Card"],
        [
            (
                UpdatePcbModelingPropsRequestAnalysisType.THERMAL_MECH,
                UpdatePcbModelingPropsRequestPcbModelType.BONDED,
                True,
                UpdatePcbModelingPropsRequestPcbMaterialModel.UNIFORM_ELEMENTS,
                5,
                ElementOrder.SOLID_SHELL,
                6,
                "mm",
                3,
                "mm",
                True,
            )
        ],
    )
except SherlockUpdatePcbModelingPropsError as e:
    print(f"Error updating PCB modeling properties: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
