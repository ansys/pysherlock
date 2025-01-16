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
.. _ref_sherlock_export_aedb:

==========================
Export AEDB
==========================

This example demonstrates how to launch the Sherlock gRPC service, import an ODB++ archive,
and export an AEDB file for a printed circuit board (PCB).

Description
-----------
Sherlock's gRPC API allows users to automate workflows such as exporting an AEDB file for a PCB.
This script demonstrates how to:

- Launch the Sherlock service.
- Import an ODB++ archive.
- Export an AEDB file.
- Properly close the gRPC connection.

The exported AEDB file can be used for further analysis or integration with other software tools.
"""

# sphinx_gallery_thumbnail_path = './images/sherlock_export_aedb_example.png'

# import os
import time

from ansys.sherlock.core import LOG, launcher

# from ansys.sherlock.core.errors import SherlockExportAEDBError, SherlockImportODBError

###############################################################################
# Launch PySherlock service
# ==========================
# Launch the Sherlock service and ensure proper initialization.

LOG.info("******************** export_aedb.py ************************")

# VERSION = "242"
# ANSYS_ROOT = os.getenv("AWP_ROOT" + VERSION)

sherlock = launcher.launch_sherlock(port=9090)

# ------------ do this if Sherlock is already running and listening to port 9090 -------------
# To launch sherlock to listen to port 9090, add the following command line option:
# -grpcPort=9090

# VERSION = "252"
# sherlock = launcher.connect_grpc_channel(port=9090, server_version=VERSION)
#
# count = 0
# while sherlock.common.check() is False and count < 30:
#     time.sleep(1)
#     count = count + 1
#
# count = 0
# while sherlock.common.is_sherlock_client_loading() is False and count < 5:
#     time.sleep(1)
#     count = count + 1
#
# sherlock.common.channel.close()

time.sleep(1)
sherlock.common.exit(True)
LOG.info("Sherlock gRPC connection closed successfully.")
