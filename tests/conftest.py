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

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-behavioral",
        action="store_true",
        default=False,
        help="Run behavioral tests that require Sherlock/real process launches.",
    )


def pytest_configure(config):
    config.addinivalue_line("markers", "behavioral: mark a test as behavioral/integration")
    config.addinivalue_line("markers", "requires_sherlock: test requires local Sherlock")


def pytest_collection_modifyitems(config, items):
    run_behavioral = config.getoption("--run-behavioral")
    skip_behavioral = pytest.mark.skip(reason="skipped by default (need --run-behavioral)")

    for item in items:
        if "behavioral" in item.keywords:
            if not run_behavioral:
                item.add_marker(skip_behavioral)
