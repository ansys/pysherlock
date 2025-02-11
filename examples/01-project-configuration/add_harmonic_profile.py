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
.. _ref_add_harmonic_vibe_profiles:

=========================================
Add Harmonic Vibration Profiles
=========================================

This example demonstrates how to launch the Sherlock gRPC service, import an ODB++ archive,
create a lifecycle phase, add a harmonic event to the phase, and then add harmonic
vibration profiles.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as adding harmonic vibration profiles
to lifecycle phases. This script shows how to:

- Launch the Sherlock service.
- Import an ODB++ archive.
- Create a lifecycle phase.
- Add a harmonic event to the lifecycle phase.
- Add vibration profiles to the harmonic event.
- Properly close the gRPC connection.

The harmonic vibration profiles simulate the effects of vibration conditions on the board.

"""

# sphinx_gallery_thumbnail_path = './images/add_harmonic_vibe_profiles_example.png'

import os
import time

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockAddHarmonicVibeProfilesError, SherlockImportODBError

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "242"
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
        project="Tutorial",
        cca_name="Card",
    )
    print("ODB++ archive imported successfully.")
except SherlockImportODBError as e:
    print(f"Error importing ODB++ archive: {str(e)}")

###############################################################################
# Create Lifecycle Phase and Add Harmonic Event
# ==============================================
# Create a new lifecycle phase and add a harmonic event to it.

try:
    # Create lifecycle phase
    sherlock.lifecycle.create_life_phase(
        project="Test",
        phase_name="Example",
        time_duration=1.5,
        time_units="sec",
        cycle_count=4.0,
        cycle_units="COUNT",
    )
    print("Lifecycle phase 'Example' created successfully.")

    # Add harmonic event to lifecycle phase
    sherlock.lifecycle.add_harmonic_event(
        project="Test",
        phase_name="Example",
        event_name="Event1",
        time_duration=1.5,
        time_units="sec",
        cycle_count=4.0,
        cycle_units="PER MIN",
        frequency=5,
        direction="45,45",
        load_type="Uniaxial",
        components="2,4,5",
    )
    print("Harmonic event 'Event1' added successfully.")

except SherlockAddHarmonicVibeProfilesError as e:
    print(f"Error adding harmonic event: {str(e)}")

###############################################################################
# Add Harmonic Vibration Profiles
# ===============================
# Add harmonic vibration profiles to the lifecycle phase.

try:
    sherlock.lifecycle.add_harmonic_vibe_profiles(
        project="Test",
        profiles=[("Example", "Event1", "Profile1", "HZ", "G", [(10, 1), (1000, 1)], "")],
    )
    print("Harmonic vibration profiles added successfully.")
except SherlockAddHarmonicVibeProfilesError as e:
    print(f"Error adding harmonic vibration profiles: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
