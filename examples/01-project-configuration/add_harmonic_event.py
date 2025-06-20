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
.. _ref_add_harmonic_event:

=====================================
Add Harmonic Event to Lifecycle Phase
=====================================

This example demonstrates how to launch the Sherlock gRPC service, import a project,
create a lifecycle phase, and add a harmonic event to the phase, then properly close the connection.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as creating lifecycle phases
and adding harmonic events.
This script demonstrates how to:
- Connect to the Sherlock service.
- Import a project.
- Create a lifecycle phase.
- Add a harmonic event to the lifecycle phase.

The harmonic event can be used for thermal analysis and helps in simulating the effects
of various conditions on the board.
"""

# sphinx_gallery_thumbnail_path = './images/add_harmonic_event_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import LOG, launcher
from ansys.sherlock.core.errors import (
    SherlockAddHarmonicEventError,
    SherlockCreateLifePhaseError,
    SherlockImportProjectZipArchiveError,
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
    LOG.info("Project deleted successfully.")
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
        archive_file=os.path.join(get_sherlock_tutorial_path(), "Auto Relay Project.zip"),
    )
    LOG.info("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    LOG.error(f"Error importing project zip archive: {e}")

phase_name = "Life Phase Example"

###############################################################################
# Create Lifecycle Phase
# ======================
# Create a new lifecycle phase called "Example" in the "Test" project.

try:
    sherlock.lifecycle.create_life_phase(
        project="Test",
        phase_name=phase_name,
        duration=1.5,
        duration_units="sec",
        num_of_cycles=4.0,
        cycle_type="COUNT",
        description="Example phase",
    )
    LOG.info("Lifecycle phase 'Example' created successfully.")
except SherlockCreateLifePhaseError as e:
    LOG.error(f"Error creating lifecycle phase: {e}")

###############################################################################
# Add Harmonic Event to Lifecycle Phase
# =====================================
# Add a harmonic event to the "Example" lifecycle phase.

try:
    sherlock.lifecycle.add_harmonic_event(
        project="Test",
        phase_name=phase_name,
        event_name="Event1",
        duration=1.5,
        duration_units="sec",
        num_of_cycles=4.0,
        cycle_type="PER MIN",
        sweep_rate=5,
        orientation="23.45, 34.56",
        profile_type="Uniaxial",
        load_direction="2,4,5",
        description="Harmonic Event Example",
    )
    LOG.info("Harmonic event 'Event1' added successfully.")
except SherlockAddHarmonicEventError as e:
    LOG.error(f"Error adding harmonic event: {str(e)}")
