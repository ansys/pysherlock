# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.

"""PySherlock client library."""

# Version
# ------------------------------------------------------------------------------

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:  # pragma: no cover
    import importlib_metadata  # type: ignore

__version__ = importlib_metadata.version(__name__.replace(".", "-"))
"""PySherlock version."""

# Ease import statements
# ------------------------------------------------------------------------------

from ansys.sherlock.core.pysherlock_logging import Logger

LOG = Logger("sherlock")
"""PySherlock logger."""
