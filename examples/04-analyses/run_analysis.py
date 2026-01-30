# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
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

=====================
Run Advanced Analysis
=====================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and run various analyses on a project, including part validation, natural frequency,
thermal derating, and more.

Description
-----------
Sherlock provides the ability to perform various types of analyses on a project.
This script demonstrates how to:
- Connect to the Sherlock service.
- Import a project into Sherlock.
- Run several types of analyses, such as part validation, mechanical shock, harmonic vibration,
and others.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_run_advanced_analysis_example.png'

import os

from examples.examples_globals import get_sherlock_tutorial_path

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import (
    SherlockImportProjectZipArchiveError,
    SherlockRunAnalysisError,
)
from ansys.sherlock.core.types.analysis_types import RunAnalysisRequestAnalysisType

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
# Run Multiple Analyses
# =====================
# Run various types of analyses on the "Main Board" in the "Tutorial Project".

try:
    # Run analyses

    analysis_types = [
        (RunAnalysisRequestAnalysisType.PTH_FATIQUE, [("Phase 1", ["Thermal Event"])]),
        (
            RunAnalysisRequestAnalysisType.SEMICINDUCTOR_WEAROUT,
            [("Phase 1", ["Thermal Event"])],
        ),
        (RunAnalysisRequestAnalysisType.THERMAL_DERATING, [("Phase 1", ["Thermal Event"])]),
        (
            RunAnalysisRequestAnalysisType.COMPONENT_FAILURE_MODE,
            [("Phase 1", ["Thermal Event"])],
        ),
    ]

    for analysis_type, params in analysis_types:
        sherlock.analysis.run_analysis(
            project="Test", cca_name="Auto Relay", analyses=[(analysis_type, params)]
        )

except SherlockRunAnalysisError as e:
    print(f"Error running analysis: {e}")
