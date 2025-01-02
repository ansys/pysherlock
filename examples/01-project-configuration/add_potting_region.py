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
.. _ref_add_potting_region:

==========================================
Add Potting Regions for PCB Analysis
==========================================

This example demonstrates how to use the Sherlock gRPC service to:

- Import an ODB++ archive.
- Add potting regions to a PCB model.
- Define potting shapes and properties for simulation.

Description
-----------
In this script, we launch the Sherlock gRPC service, import an ODB++ archive,
and create potting regions with specified shapes and properties for a PCB analysis.

"""

import os
import time

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockAddPottingRegionError, SherlockImportODBError
from ansys.sherlock.core.types.layer_types import PolygonalShape

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "252"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

# Wait for service to initialize
time.sleep(5)

###############################################################################
# Import ODB++ Archive
# =====================
# Import the ODB++ archive from the Sherlock tutorial directory.

try:
    sherlock.project.import_odb_archive(
        file_path=os.path.join(ANSYS_ROOT, "sherlock", "tutorial", "ODB++ Tutorial.tgz"),
        allow_subdirectories=True,
        include_layers=True,
        use_stackup=True,
        project="Test",
        cca_name="Card",
    )
    print("ODB++ archive imported successfully.")
except SherlockImportODBError as e:
    print(f"Error importing ODB++ archive: {str(e)}")

###############################################################################
# Add Potting Region
# ===================
# Define a polygonal shape and add it as a potting region to the PCB.

try:
    # Define the polygonal shape for the potting region
    polygonal_shape = PolygonalShape(points=[(0, 0), (0, 6.35), (9.77, 0)], rotation=87.8)

    # Add the potting region
    sherlock.layer.add_potting_region(
        "Test",
        [
            {
                "cca_name": "Card",
                "potting_id": "Test Region",
                "side": "TOP",
                "material": "epoxyencapsulant",
                "potting_units": "in",
                "thickness": 0.1,
                "standoff": 0.2,
                "shape": polygonal_shape,
            }
        ],
    )
    print("Potting region added successfully.")
except SherlockAddPottingRegionError as e:
    print(f"Error adding potting region: {str(e)}")

###############################################################################
# Exit Sherlock
# ==============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
