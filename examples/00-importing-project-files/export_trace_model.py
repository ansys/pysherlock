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
.. _ref_sherlock_trace_model_export:

===================================== 
Sherlock Trace Model Export 
=====================================

This example demonstrates how to launch the Sherlock gRPC service, import a project archive, 
generate export parameters for copper layers, and export a trace model.

Description
Sherlock's gRPC API enables automation of various workflows, including trace model exports.
This script demonstrates:

- Launching the Sherlock service.
- Importing a tutorial project ZIP archive.
- Generating copper layer parameters for trace model export.
- Exporting a trace model with multiple copper layers.
- Properly exiting the gRPC connection.
"""

#sphinx_gallery_thumbnail_path = './images/sherlock_trace_model_export_example.png'

import os
import time
from ansys.sherlock.core.errors import (
    SherlockModelServiceError,
    SherlockImportProjectZipArchiveError,
)
from ansys.api.sherlock.v0 import SherlockAnalysisService_pb2
from ansys.api.sherlock.v0 import SherlockModelService_pb2
from ansys.sherlock.core import launcher

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service using the default port and wait for initialization.

VERSION = '252'
ANSYS_ROOT = os.getenv('AWP_ROOT' + VERSION)
TESTDIR = os.getcwd()

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import Tutorial Project
# ========================
# Import a sample project ZIP archive provided with the Sherlock installation.

try:
    project_zip_path = os.path.join(
        ANSYS_ROOT, "sherlock", "tutorial", "Tutorial Project.zip"
    )
    sherlock.project.import_project_zip_archive(
        "Tutorial Project", "Demos", project_zip_path
    )
    print("Project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project: {str(e)}")

###############################################################################
# Export Trace Model
# ===================
# Generate copper layer parameters and export a trace model.

try:
    copper_1_layer = sherlock.model.createExportTraceCopperLayerParams(
        project_name="Tutorial Project",
        assembly_name="Main Board",
        output_file_path=os.path.join(TESTDIR, "outputfile_path.stp"),
        odb_file="copper-01.odb",
        include_pins=True,
        include_nets=False,
        include_components=False,
        include_drcs=False,
        length_unit="mm",
        mesh_type=SherlockModelService_pb2.MeshType.NONE,
        include_solder_pads=False,
        trace_output_type=SherlockModelService_pb2.TraceOutputType.ALL_REGIONS,
        element_order=SherlockAnalysisService_pb2.ElementOrder.Linear,
        trace_thickness=1.0,
        trace_thickness_unit="mm",
        trace_simplification_factor=2,
        include_vias=False,
        via_diameter=1.0,
        via_diameter_unit="mm",
        via_height=1.0,
    )
    copper_2_layer = sherlock.model.createExportTraceCopperLayerParams(
        project_name="Tutorial Project",
        assembly_name="Main Board",
        output_file_path=os.path.join(TESTDIR, "outputfile_path2.stp"),
        odb_file="copper-02.odb",
        include_pins=True,
        include_nets=False,
        include_components=False,
        include_drcs=False,
        length_unit="mm",
        mesh_type=SherlockModelService_pb2.MeshType.NONE,
        include_solder_pads=False,
        trace_output_type=SherlockModelService_pb2.TraceOutputType.ALL_REGIONS,
        element_order=SherlockAnalysisService_pb2.ElementOrder.Linear,
        trace_thickness=1.0,
        trace_thickness_unit="mm",
        trace_simplification_factor=2,
        include_vias=False,
        via_diameter=1.0,
        via_diameter_unit="mm",
        via_height=1.0,
    )
    sherlock.model.exportTraceModel([copper_1_layer, copper_2_layer])
    print("Trace model exported successfully.")
except SherlockModelServiceError as e:
    print(f"Error exporting trace model: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

time.sleep(5)  # Allow time for any remaining operations
sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
