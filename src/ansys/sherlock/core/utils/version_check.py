# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Module for version check done on api methods."""
import functools

from ansys.sherlock.core.errors import SherlockVersionError

_EARLIEST_SUPPORTED_VERSION = 211

# Used in testing. Set this as the version and all version checks will be skipped.
SKIP_VERSION_CHECK = None

# PySherlock release version to the best Sherlock counterpart version
#  0.2.0 : 24R1
#  0.3.0 : 24R1
#  0.4.0 : 24R1
#  0.5.0 : 24R2
#  0.6.0 : 24R2
#  0.7.0 : 25R1
#  0.8.0 : 25R1
#  0.9.0 : 25R2


def require_version(min_version: int = _EARLIEST_SUPPORTED_VERSION, max_version: int = None):
    """Check version of server against expected version."""

    def decorate(func) -> callable:
        """Return wrapped function."""

        @functools.wraps(func)
        # Use functools to keep the doc string associated with the wrapped function, for Sphinx.
        def wrapper(self, *args, **kwargs) -> callable:
            """Wrap outer function."""
            if not hasattr(self, "_server_version"):
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
