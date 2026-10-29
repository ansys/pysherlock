# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

from pathlib import Path
import runpy
import sys
from types import ModuleType
import unittest
from unittest.mock import Mock, patch


class TestExampleSetup(unittest.TestCase):
    def setUp(self):
        self.launcher = Mock()
        self.launcher.launch_and_connect.return_value = (Mock(), "installation")
        core = ModuleType("ansys.sherlock.core")
        core.launcher = self.launcher
        errors = ModuleType("ansys.sherlock.core.errors")
        errors.SherlockCannotUsePortError = OSError
        errors.SherlockConnectionError = ConnectionError
        globals_module = ModuleType("examples.examples_globals")
        globals_module.SHERLOCK_CONNECT_TIMEOUT = 2
        globals_module.SHERLOCK_LAUNCH_AND_CONNECT_TIMEOUT = 10
        globals_module.store_sherlock_tutorial_path = Mock()
        self.modules = {
            "ansys.sherlock.core": core,
            "ansys.sherlock.core.errors": errors,
            "examples.examples_globals": globals_module,
        }
        self.elapsed = 0

    def sleep(self, duration):
        self.elapsed += duration

    def run_setup(self):
        path = Path(__file__).resolve().parents[1] / "examples" / "00-setup" / "setup.py"
        with (
            patch.dict(sys.modules, self.modules),
            patch.object(sys, "path", sys.path.copy()),
            patch("time.monotonic", side_effect=lambda: self.elapsed),
            patch("time.sleep", side_effect=self.sleep),
            patch("builtins.print"),
        ):
            runpy.run_path(str(path))

    def test_available_port_does_not_wait(self):
        self.run_setup()
        self.assertEqual(self.elapsed, 0)
        self.launcher._is_port_available.assert_called_once_with(port=9092)
        self.launcher.launch_and_connect.assert_called_once()

    def test_polls_until_port_is_released(self):
        self.launcher._is_port_available.side_effect = [OSError(), OSError(), True]
        self.run_setup()
        self.assertEqual(self.elapsed, 1)
        self.assertEqual(self.launcher._is_port_available.call_count, 3)
        self.launcher.launch_and_connect.assert_called_once()

    def test_busy_port_times_out_without_launching(self):
        self.launcher._is_port_available.side_effect = OSError("Port is already in use")
        with self.assertRaisesRegex(TimeoutError, "port 9092 within 30 seconds"):
            self.run_setup()
        self.assertEqual(self.elapsed, 30)
        self.launcher.launch_and_connect.assert_not_called()

    def test_no_existing_instance_launches_without_polling(self):
        self.launcher.connect.side_effect = ConnectionError()
        self.run_setup()
        self.launcher._is_port_available.assert_not_called()
        self.launcher.launch_and_connect.assert_called_once()

    def test_exit_failure_is_not_suppressed(self):
        self.launcher.connect.return_value.common.exit.side_effect = RuntimeError("Exit failed")
        with self.assertRaisesRegex(RuntimeError, "Exit failed"):
            self.run_setup()
        self.launcher.launch_and_connect.assert_not_called()
