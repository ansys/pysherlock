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
.. _ref_setup:

=========================================
Setup
=========================================

This prepares the environment for running the examples.

Description
-----------
Perform the following steps to set up the environment:
- Launch Sherlock.
- Store the Sherlock tutorial path.
"""

import os
import sys

# Add the 'examples' directory to the Python path to allow importing files in that directory.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))))

from examples.examples_globals import store_sherlock_tutorial_path

from ansys.sherlock.core import launcher

###############################################################################
# Launch Sherlock
# ===============
# Launch the Sherlock service and ensure proper initialization.

sherlock, ansys_install_path = launcher.launch_and_connect(
    port=9092,
    # sherlock_command_args="-noGUI",
)

store_sherlock_tutorial_path(ansys_install_path)
