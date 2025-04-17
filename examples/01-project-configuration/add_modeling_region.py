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
.. _ref_add_modeling_region:

======================================
Add Modeling Regions for PCB Analysis
======================================

This example demonstrates how to use the Sherlock gRPC service to:

- Import an ODB++ archive.
- Add modeling regions to a PCB model.
- Define different region shapes like polygonal, rectangular, circular, and slot shapes.
- Configure PCB and trace model properties for simulation.

Description
-----------
In this script, we launch the Sherlock gRPC service, import an ODB++ archive,
and create modeling regions with different shapes for a PCB analysis. The script
shows how to configure the modeling region shapes, PCB properties, and trace
properties for each region.

"""

# sphinx_gallery_thumbnail_path = './images/add_modeling_region_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockAddModelingRegionError, SherlockImportODBError
from ansys.sherlock.core.types.layer_types import (
    CircularShape,
    PolygonalShape,
    RectangularShape,
    SlotShape,
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
# Import ODB++ Archive
# =====================
# Import the ODB++ archive from the Sherlock tutorial directory.

try:
    sherlock.project.import_odb_archive(
        archive_file=os.path.join(get_sherlock_tutorial_path(), "ODB++ Project.zip"),
        process_layer_thickness=True,
        include_other_layers=True,
        process_cutout_file=True,
        guess_part_properties=True,
        project="Test",
        cca_name="Card",
    )
    print("ODB++ archive imported successfully.")
except SherlockImportODBError as e:
    print(f"Error importing ODB++ archive: {e}")

###############################################################################
# Create Modeling Regions
# =======================
# Define different shapes (polygonal, rectangular, circular, and slot) for modeling regions.

try:
    # Define coordinates and dimensions
    U9_x = 0.0  # X-Coordinate in mm.
    U9_y = 19.05  # Y-Coordinate in mm.
    U9_package_length = 27.0  # Package Length in mm.
    U9_package_width = 27.0  # Package Width in mm.
    tolerance = 2.0  # Dimension Tolerance in mm.

    x_min = U9_x - (U9_package_width / 2) - tolerance
    x_max = U9_x + (U9_package_width / 2) + tolerance
    y_min = U9_y - (U9_package_length / 2) - tolerance
    y_max = U9_y + (U9_package_length / 2) + tolerance

    # Define the region shapes
    polygonal_shape = PolygonalShape(points=[(0, 0), (0, 6.35), (9.77, 0)], rotation=87.8)
    rectangular_shape = RectangularShape(
        length=U9_package_length, width=U9_package_width, center_x=U9_x, center_y=U9_y, rotation=0.0
    )
    slot_shape = SlotShape(
        length=5.0, width=5.0, node_count=6, center_x=U9_x, center_y=U9_y, rotation=0.0
    )
    circular_shape = CircularShape(
        diameter=5.0, node_count=4, center_x=0.0, center_y=0.0, rotation=30.0
    )

    # Create the modeling regions
    modeling_regions = [
        {
            "cca_name": "Card",
            "region_id": "Region001",
            "region_units": "mm",
            "model_mode": "Enabled",
            "shape": polygonal_shape,
            "pcb_model_props": {
                "export_model_type": "Sherlock",
                "elem_order": "First_Order",
                "max_mesh_size": 0.5,
                "max_mesh_size_units": "mm",
                "quads_preferred": True,
            },
            "trace_model_props": {
                "trace_model_type": "Enabled",
                "elem_order": "Second_Order",
                "trace_mesh_size": 0.3,
                "trace_mesh_size_units": "mm",
            },
        },
        {
            "cca_name": "Card",
            "region_id": "Region002",
            "region_units": "mm",
            "model_mode": "Enabled",
            "shape": rectangular_shape,
            "pcb_model_props": {
                "export_model_type": "Sherlock",
                "elem_order": "First_Order",
                "max_mesh_size": 0.5,
                "max_mesh_size_units": "mm",
                "quads_preferred": True,
            },
            "trace_model_props": {
                "trace_model_type": "Enabled",
                "elem_order": "Second_Order",
                "trace_mesh_size": 0.3,
                "trace_mesh_size_units": "mm",
            },
        },
        {
            "cca_name": "Card",
            "region_id": "Region003",
            "region_units": "mm",
            "model_mode": "Enabled",
            "shape": circular_shape,
            "pcb_model_props": {
                "export_model_type": "Sherlock",
                "elem_order": "First_Order",
                "max_mesh_size": 0.5,
                "max_mesh_size_units": "mm",
                "quads_preferred": True,
            },
            "trace_model_props": {
                "trace_model_type": "Enabled",
                "elem_order": "Second_Order",
                "trace_mesh_size": 0.3,
                "trace_mesh_size_units": "mm",
            },
        },
        {
            "cca_name": "Card",
            "region_id": "Region004",
            "region_units": "mm",
            "model_mode": "Enabled",
            "shape": slot_shape,
            "pcb_model_props": {
                "export_model_type": "Sherlock",
                "elem_order": "First_Order",
                "max_mesh_size": 0.5,
                "max_mesh_size_units": "mm",
                "quads_preferred": True,
            },
            "trace_model_props": {
                "trace_model_type": "Enabled",
                "elem_order": "Second_Order",
                "trace_mesh_size": 0.3,
                "trace_mesh_size_units": "mm",
            },
        },
    ]

    # Add modeling regions to the project
    sherlock.layer.add_modeling_region("Test", modeling_regions)
    print("Modeling regions added successfully.")
except SherlockAddModelingRegionError as e:
    print(f"Error adding modeling regions: {e}")
