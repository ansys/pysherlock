# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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
.. _ref_update_thermal_maps:

===================
Update Thermal Maps
===================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and update thermal maps.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as updating thermal maps for printed
circuit boards (PCBs).
This script demonstrates how to:
- Connect to the Sherlock service.
- Import a project.
- Update thermal maps.

The updated thermal maps ensure the accuracy of thermal profiles and board configurations.
"""

# sphinx_gallery_thumbnail_path = './images/update_thermal_maps_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportProjectZipArchiveError
from ansys.sherlock.core.types.project_types import (
    BoardBounds,
    ImageBounds,
    ImageFile,
    LegendBounds,
    LegendOrientation,
    ThermalBoardSide,
    ThermalMapsFileType,
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
# =======================
# Import the tutorial project zip archive from the Sherlock tutorial directory.

try:
    sherlock.project.import_project_zip_archive(
        project="Test",
        category="Demos",
        archive_file=os.path.join(get_sherlock_tutorial_path(), "Tutorial Project.zip"),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project zip archive: {e}")

###############################################################################
# Update Thermal Maps
# ===================
# Update the thermal maps for the "Tutorial Project".

try:
    thermal_map_properties = ImageFile(
        board_bounds=BoardBounds([(1.0, 2.0), (5.0, 1.0), (5.0, 5.0), (1.0, 5.0)]),
        coordinate_units="mm",
        image_bounds=ImageBounds(-95, -57, 114, 290),
        legend_bounds=LegendBounds(1.0, 2.0, 4.0, 2.0),
        legend_orientation=LegendOrientation.VERTICAL,
        min_temperature=17.0,
        min_temperature_units="C",
        max_temperature=90.0,
        max_temperature_units="C",
    )

    add_thermal_map_files = [
        {
            "thermal_map_file": os.path.join(
                get_sherlock_tutorial_path(), "ThermalMaps", "Thermal Image.jpg"
            ),
            "thermal_map_file_properties": [
                {
                    "file_name": "Thermal Image.jpg",
                    "file_type": ThermalMapsFileType.IMAGE,
                    "file_comment": "Update thermal map",
                    "thermal_board_side": ThermalBoardSide.BOTH,
                    "file_data": thermal_map_properties,
                    "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                    "cca_names": ["Main Board"],
                },
            ],
        }
    ]
    sherlock.project.add_thermal_maps(
        project="Test",
        add_thermal_map_files=add_thermal_map_files,
    )

    thermal_map_files = [
        {
            "file_name": "Thermal Image.jpg",
            "file_type": ThermalMapsFileType.IMAGE,
            "file_comment": "Update thermal map",
            "thermal_board_side": ThermalBoardSide.TOP,
            "file_data": thermal_map_properties,
            "thermal_profiles": ["Environmental/1 - Temp Cycle - Max"],
            "cca_names": ["Main Board"],
        },
    ]
    sherlock.project.update_thermal_maps(
        project="Test",
        thermal_map_files=thermal_map_files,
    )

    print("Thermal maps updated successfully.")
except Exception as e:
    print(f"Error adding or updating thermal maps")
