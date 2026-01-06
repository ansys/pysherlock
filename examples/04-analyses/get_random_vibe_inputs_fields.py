# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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
.. _ref_sherlock_run_analysis:

====================================
Get Random Vibration Analysis inputs
====================================

This example demonstrates how to connect to the Sherlock gRPC service, import a project,
and retrieve the analysis input fields.

Description
-----------
Sherlock provides the ability to run a random vibration analysis using its gRPC interface.
This script demonstrates how to:
- Connect to the Sherlock service.
- Retrieve the input fields required for random vibration analysis.

This example assumes you have already set up Sherlock and the necessary environment.

For more details on vibration analysis in Sherlock, refer to the official documentation.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_run_analysis_example.png'


from ansys.sherlock.core import launcher

###############################################################################
# Connect to Sherlock
# ===================
# Connect to the Sherlock service and ensure proper initialization.

sherlock = launcher.connect(port=9092, timeout=10)

###############################################################################
# Get Random Vibration Input Fields
# =================================
# Retrieve the list of input fields for the random vibration analysis.

try:
    random_vibe_input_fields = sherlock.analysis.get_random_vibe_input_fields()
    print("Random vibration analysis input fields:")
    print(random_vibe_input_fields)
except Exception as e:
    print(f"Error retrieving random vibration input fields: {e}")
