# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
.. _ref_setup:

=====
Setup
=====

This prepares the environment for running the examples.

Description
-----------
Perform the following steps to set up the environment.
"""

import os
import sys
from time import monotonic, sleep

# Add the 'examples' directory to the Python path to allow importing files in that directory.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(os.getcwd()))))

from examples.examples_globals import (
    SHERLOCK_COMMAND_ARGS,
    SHERLOCK_CONNECT_TIMEOUT,
    SHERLOCK_LAUNCH_AND_CONNECT_TIMEOUT,
    SHERLOCK_PORT,
    SHERLOCK_TRANSPORT_MODE,
    store_sherlock_tutorial_path,
)

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockCannotUsePortError, SherlockConnectionError

# attempt to exit Sherlock in case a previous run was not properly terminated
try:
    sherlock = launcher.connect(
        port=SHERLOCK_PORT, timeout=SHERLOCK_CONNECT_TIMEOUT, transport_mode=SHERLOCK_TRANSPORT_MODE
    )

    print(f"Exiting Sherlock that is running on port {SHERLOCK_PORT}.")
    sherlock.common.exit(True)
    EXIT_TIMEOUT = 30
    start_time = monotonic()
    while True:
        try:
            launcher._is_port_available(port=SHERLOCK_PORT)
            break
        except SherlockCannotUsePortError as error:
            if monotonic() - start_time >= EXIT_TIMEOUT:
                raise TimeoutError(
                    f"Sherlock did not release port {SHERLOCK_PORT} "
                    f"within {EXIT_TIMEOUT} seconds."
                ) from error
            sleep(0.5)
    print("Sherlock exited successfully.")
except SherlockConnectionError:
    # Sherlock is not running
    pass


###############################################################################
# Launch Sherlock
# ===============
# Launch Sherlock on Windows in headless mode using Windows Named User Authentication for the gRPC
# transport mode.
# See the API reference for how to launch Sherlock on Linux or Windows using other options.

sherlock, ansys_install_path = launcher.launch_and_connect(
    port=SHERLOCK_PORT,
    timeout=SHERLOCK_LAUNCH_AND_CONNECT_TIMEOUT,
    transport_mode=SHERLOCK_TRANSPORT_MODE,
    sherlock_command_args=SHERLOCK_COMMAND_ARGS,
)

# store the path to the Sherlock tutorial directory in a shared data file for use by other examples
store_sherlock_tutorial_path(ansys_install_path)
