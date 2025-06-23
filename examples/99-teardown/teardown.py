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
.. _ref_teardown:

=========================================
Teardown
=========================================

This restores the environment after running the examples.

Description
-----------
Perform the following steps to set up the environment:
- Connect to Sherlock
- Exit Sherlock
- Delete temp files
"""

import shutil

from examples.examples_globals import get_temp_dir

from ansys.sherlock.core import LOG, launcher

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

LOG.info("Teardown: connect to and exit Sherlock")
try:
    sherlock = launcher.connect(port=9092, timeout=2)
    sherlock.common.exit(True)
    LOG.info("Sherlock exited successfully.")
except Exception as e:
    LOG.error(f"Error exiting Sherlock: {e}")

###############################################################################
# Clean temporary directory
# =========================
# Delete the directory for storing temp files.

try:
    shutil.rmtree(get_temp_dir(), ignore_errors=True)
except Exception as e:
    LOG.error(f"Error deleting temporary directory: {e}")
