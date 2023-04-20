# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

"""Initialize session variables."""
from ansys.sherlock.core._version import __version__
from ansys.sherlock.core.logging import Logger

LOG = Logger("sherlock")
SHERLOCK = None
