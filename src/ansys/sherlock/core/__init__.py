"""Initialize session variables."""
from ansys.sherlock.core.logging import Logger
from ansys.sherlock.core.sherlock import Sherlock

LOG = Logger("sherlock")
SHERLOCK = None

from ansys.sherlock.core._version import __version__

