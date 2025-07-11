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
.. _ref_add_harmonic_vibe_profiles:

===============================
Add Harmonic Vibration Profiles
===============================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
create a lifecycle phase, add a harmonic event to the phase, and add harmonic
vibration profiles.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as adding harmonic vibration profiles
to lifecycle phases.
This script demonstrates how to:
- Connect to the Sherlock service.
- Import a project.
- Create a lifecycle phase.
- Add a harmonic event to the lifecycle phase.
- Add vibration profiles to the harmonic event.

The harmonic vibration profiles simulate the effects of vibration conditions on the board.

"""

# sphinx_gallery_thumbnail_path = './images/add_harmonic_vibe_profiles_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportProjectZipArchiveError

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
        archive_file=os.path.join(get_sherlock_tutorial_path(), "Auto Relay Project.zip"),
    )
    print("Tutorial project imported successfully.")
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project zip archive: {e}")

###############################################################################
# Create Lifecycle Phase and Add Harmonic Event
# =============================================
# Create a new lifecycle phase and add a harmonic event to it.

try:
    phase_name = "Life Phase Example"
    event_name = "Example Harmonic Event"

    # Create lifecycle phase
    sherlock.lifecycle.create_life_phase(
        project="Test",
        phase_name=phase_name,
        duration=1.5,
        duration_units="sec",
        num_of_cycles=4.0,
        cycle_type="COUNT",
        description="Example lifecycle phase.",
    )
    print(f"Lifecycle phase '{phase_name}' created successfully.")

    # Add harmonic event to lifecycle phase
    sherlock.lifecycle.add_harmonic_event(
        project="Test",
        phase_name=phase_name,
        event_name=event_name,
        duration=1.5,
        duration_units="sec",
        num_of_cycles=4.0,
        cycle_type="PER MIN",
        sweep_rate=5,
        orientation="45,45",
        profile_type="Triaxial",
        load_direction="2,4,5",
        description="Example harmonic event.",
    )
    print(f"Harmonic event '{event_name}' added successfully.")

    # Add harmonic vibration profiles to the lifecycle phase.
    sherlock.lifecycle.add_harmonic_vibe_profiles(
        project="Test",
        harmonic_vibe_profiles=[
            (phase_name, event_name, "Profile z axis", "HZ", "G", [(10, 1), (1000, 1)], "z")
        ],
    )
    print("Harmonic vibration profile added successfully.")

except Exception as e:
    print(f"Error creating life phase, harmonic event, or harmonic vibe profiles. {e}")
