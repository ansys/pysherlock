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
.. _ref_import_ipc2581:

===============================
Import IPC-2581 Archive
===============================

This example demonstrates how to launch the Sherlock gRPC service, import an IPC-2581 archive,
and properly close the connection.

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as importing IPC-2581 archives.
This script shows how to:

- Launch the Sherlock service.
- Import an IPC-2581 archive without specifying a project or CCA name.
- Properly close the gRPC connection.

This functionality is useful for initializing projects with IPC-2581 data for further
analysis and workflows.

.. todo::
    Before running this script, download the file **IPC2581A-TestCase2.cvg** from the repository
    `Importing Project and Files`_.
"""

# sphinx_gallery_thumbnail_path = './images/import_ipc2581_example.png'

import os
import time

from ansys.sherlock.core import launcher
from ansys.sherlock.core.errors import SherlockImportIpc2581Error

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

VERSION = "252"
ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9092)

###############################################################################
# Import IPC-2581 Archive
# ========================
# Import an IPC-2581 archive without specifying a project or CCA name.

try:
    ipc2581_path = os.path.join(os.getcwd(), "IPC2581A-TestCase2.cvg")
    sherlock.project.import_ipc2581_archive(
        file_path=ipc2581_path, allow_subdirectories=True, include_layers=True
    )
    print("IPC-2581 archive imported successfully.")
except SherlockImportIpc2581Error as e:
    print(f"Error importing IPC-2581 archive: {str(e)}")

# Wait for 30 seconds to ensure all processes are completed.
time.sleep(30)

###############################################################################
# Exit Sherlock
# =============
# Exit the gRPC connection and shut down Sherlock.

sherlock.common.exit(True)
print("Sherlock gRPC connection closed successfully.")
