# Copyright (C) 2024 ANSYS, Inc. and/or its affiliates.
"""Module for version check done on api methods."""
import functools

from ansys.sherlock.core.errors import SherlockVersionError

_EARLIEST_SUPPORTED_VERSION = 211

# Used in testing. Set this as the version and all version checks will be skipped.
SKIP_VERSION_CHECK = "SKIP"

# PySherlock release version to the best Sherlock counterpart version
#  0.2.0 : 24R1
#  0.3.0 : 24R1
#  0.4.0 : 24R1
#  0.5.0 : 24R2
#  0.6.0 : 24R2
#  0.7.0 : 25R1


def require_version(min_version: int = _EARLIEST_SUPPORTED_VERSION, max_version: int = None):
    """Check version of server against expected version."""

    def decorate(func) -> callable:
        """Return wrapped function."""

        @functools.wraps(func)
        # Use functools to keep the doc string associated with the wrapped function, for Sphinx.
        def wrapper(self, *args, **kwargs) -> callable:
            """Wrap outer function."""
            if not hasattr(self, "_server_version") or self._server_version is None:
                raise SherlockVersionError(
                    "Unable to detect which version of sherlock was launched."
                )

            if self._server_version == SKIP_VERSION_CHECK:
                return func(self, *args, **kwargs)

            cur_version = int(self._server_version)
            nonlocal min_version
            nonlocal max_version

            if max_version is not None and min_version > max_version:
                raise ValueError("min_version is > max_version in version decorator")
            if cur_version < min_version:
                raise SherlockVersionError(
                    "Sherlock version "
                    + str(cur_version)
                    + " too old to use function "
                    + func.__name__
                    + " update server to at least version "
                    + str(min_version)
                )
            if max_version is not None and cur_version > max_version:
                raise SherlockVersionError(
                    "Sherlock version "
                    + str(cur_version)
                    + " is too new. This function "
                    + func.__name__
                    + " deprecated after version "
                    + str(max_version)
                )

            # If no issues have been raised call the wrapped function
            return func(self, *args, **kwargs)

        return wrapper

    return decorate
