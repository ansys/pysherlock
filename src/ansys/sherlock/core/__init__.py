"""Initialize session variables."""
from ansys.sherlock.core.logging import Logger

LOG = Logger("sherlock")
SHERLOCK = None

from ansys.sherlock.core._version import __version__
