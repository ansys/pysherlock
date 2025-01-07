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
.. _ref_sherlock_run_advanced_analysis:

========================
Run Advanced Analysis
========================

This example demonstrates how to launch the Sherlock gRPC service and run multiple analysis types
on a project, including part validation, natural frequency, thermal derating, and more.

Description
-----------
Sherlock provides the ability to perform various types of analyses on a project.
This script showcases how to:

- Launch the Sherlock service.
- Import a project into Sherlock.
- Run several types of analyses, such as part validation, mechanical shock, harmonic vibration,
and others.
- Properly close the gRPC connection after all analyses are complete.

The example assumes you have already set up Sherlock and the necessary environment.

For more details on running specific analyses, refer to the official documentation.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_run_advanced_analysis_example.png'

import os
import time

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockRunAnalysisError,
)
from ansys.sherlock.core.types.analysis_types import RunAnalysisRequestAnalysisType

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "251"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import Tutorial Project
# ========================
# Import a tutorial project to run analyses on.

try:
    sherlock.project.import_project_zip_archive(
        "Tutorial Project",
        "Demos",
        ANSYS_ROOT
        + os.path.sep
        + "sherlock"
        + os.path.sep
        + "tutorial"
        + os.path.sep
        + "Tutorial Project.zip",
    )
except SherlockImportProjectZipArchiveError as e:
    print(f"Error importing project: {str(e)}")

###############################################################################
# Run Multiple Analyses
# =====================
# Run various types of analyses on the "Main Board" in the "Tutorial Project".

try:
    # Run analyses
    analysis_types = [
        (RunAnalysisRequestAnalysisType.PART_VALIDATION, [("", [])]),
        (RunAnalysisRequestAnalysisType.NATURAL_FREQ, [("", [])]),
        (RunAnalysisRequestAnalysisType.PTH_FATIQUE, [("Environmental", ["1 - Temp Cycle"])]),
        (RunAnalysisRequestAnalysisType.ICT, [("", [])]),
        (
            RunAnalysisRequestAnalysisType.SEMICINDUCTOR_WEAROUT,
            [("Environmental", ["1 - Temp Cycle"])],
        ),
        (
            RunAnalysisRequestAnalysisType.SOLDER_JOINT_FATIGUE,
            [("Environmental", ["1 - Temp Cycle"])],
        ),
        (RunAnalysisRequestAnalysisType.THERMAL_DERATING, [("Environmental", ["1 - Temp Cycle"])]),
        (
            RunAnalysisRequestAnalysisType.COMPONENT_FAILURE_MODE,
            [("Environmental", ["1 - Temp Cycle"])],
        ),
        (RunAnalysisRequestAnalysisType.HARMONIC_VIBE, [("On The Road", ["5 - Harmonic Vibe"])]),
        (RunAnalysisRequestAnalysisType.RANDOM_VIBE, [("On The Road", ["1 - Vibration"])]),
        (
            RunAnalysisRequestAnalysisType.MECHANICAL_SHOCK,
            [("Environmental", ["2 - Shopping Cart"])],
        ),
        (RunAnalysisRequestAnalysisType.THERMAL_MECH, [("Environmental", ["1 - Temp Cycle"])]),
    ]

    for analysis_type, params in analysis_types:
        sherlock.analysis.run_analysis("Tutorial Project", "Main Board", [(analysis_type, params)])

except SherlockRunAnalysisError as e:
    print(f"Error running analysis: {str(e)}")

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

time.sleep(5)
sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
