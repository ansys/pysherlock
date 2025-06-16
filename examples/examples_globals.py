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

import json
import os


def get_temp_dir() -> str:
    return os.path.join(os.path.dirname(os.getcwd()), "Temp")


def _make_temp_dir() -> None:
    """Create a temporary directory for storing files."""
    os.makedirs(get_temp_dir(), exist_ok=True)


def _get_shared_data_file() -> str:
    return os.path.join(get_temp_dir(), "pysherlock_examples_shared_data.json")


def store_sherlock_tutorial_path(ansys_install_path: str) -> None:
    """Store the Sherlock tutorial path in a shared data file."""
    _make_temp_dir()
    data = {"sherlock_tutorial_path": os.path.join(ansys_install_path, "sherlock", "tutorial")}
    with open(_get_shared_data_file(), "w") as file:
        json.dump(data, file)


def get_sherlock_tutorial_path() -> str:
    """Retrieve the Sherlock tutorial path from the shared data file."""
    with open(_get_shared_data_file(), "r") as file:
        data = json.load(file)
    return data.get("sherlock_tutorial_path", "Not set")
