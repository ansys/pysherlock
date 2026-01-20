# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# © 2023 - 2025 ANSYS, Inc. All rights reserved
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

import os
import unittest
from unittest.mock import MagicMock, patch

from ansys.sherlock.core import launcher


class TestLauncher(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "AWP_ROOT223": "C:\\Program Files\\ANSYS Inc\\v223",
            "AWP_ROOT222": "C:\\Program Files\\ANSYS Inc\\v222",
            "AWP_ROOT102": "C:\\Program Files\\ANSYS Inc\\v102",
        },
        clear=True,
    )
    @patch("os.path.isdir")
    def test_base_ansys(self, mock_os_path_isdir):
        mock_os_path_isdir.return_value = True
        self.assertEqual("C:\\Program Files\\ANSYS Inc\\v223", launcher._get_base_ansys()[0])

    def test_get_ansys_version_from_awp_root(self):
        self.assertEqual(223, launcher._get_ansys_version_from_awp_root("AWP_ROOT223"))
        self.assertEqual("", launcher._get_ansys_version_from_awp_root("AWPROOT223"))

    @patch("ansys.sherlock.core.launcher._get_base_ansys")
    def test_get_sherlock_exe_path(self, mock_get_base_ansys):
        mock_get_base_ansys.return_value = ("base_ansys_path", 223)
        sherlock_path, version = launcher._get_sherlock_exe_path()
        self.assertEqual(
            os.path.join("base_ansys_path", "sherlock", "SherlockClient.exe"),
            sherlock_path,
        )

    def test_extract_sherlock_version_year_with_two_digits(self):
        with self.assertRaises(ValueError) as context:
            launcher._extract_sherlock_version_year(999)
        self.assertEqual(str(context.exception), "Year must be a 4-digit integer.")

    def test_extract_sherlock_version_year_with_four_digits(self):
        self.assertEqual(24, launcher._extract_sherlock_version_year(2024))

    @patch.dict(
        os.environ,
        {
            "AWP_ROOT241": "C:\\Program Files\\ANSYS Inc\\v241",
            "AWP_ROOT232": "C:\\Program Files\\ANSYS Inc\\v232",
        },
        clear=True,
    )
    @patch("os.path.isdir")
    @patch("ansys.sherlock.core.launcher._extract_sherlock_version_year")
    def test_get_base_ansys_calls_extract_sherlock_version_year(
        self, mock_extract_year, mock_os_path_isdir
    ):
        mock_os_path_isdir.return_value = True
        mock_extract_year.return_value = 24
        launcher._get_base_ansys(year=2024, release_number=1)
        mock_extract_year.assert_called_once_with(2024)


class TestLauncherTransportModes(unittest.TestCase):
    @patch("ansys.sherlock.core.launcher.Sherlock")
    @patch("ansys.sherlock.core.launcher._is_port_available")
    @patch("ansys.sherlock.core.launcher.subprocess.Popen")
    def test_launch_sherlock_insecure(self, mock_popen, mock_port_available, mock_sherlock):
        mock_port_available.return_value = True
        mock_popen.return_value = MagicMock()
        mock_sherlock_instance = MagicMock()
        mock_sherlock.return_value = mock_sherlock_instance
        mock_sherlock_instance.common.check.return_value = True
        mock_sherlock_instance.common.is_sherlock_client_loading.return_value = True

        result = launcher.launch_sherlock(
            host="127.0.0.1",
            port=9090,
            transport_mode="insecure",
        )

        self.assertIsNotNone(result)
        mock_popen.assert_called_once()
        self.assertIn("--transport-mode=insecure", mock_popen.call_args[0][0])
        self.assertIn("-grpcHost=127.0.0.1", mock_popen.call_args[0][0])
        self.assertIn("-grpcPort=9090", mock_popen.call_args[0][0])

    @patch("ansys.sherlock.core.launcher.connect_grpc_channel")
    @patch("ansys.sherlock.core.launcher._is_port_available")
    @patch("ansys.sherlock.core.launcher.subprocess.Popen")
    def test_launch_sherlock_mtls(self, mock_popen, mock_port_available, mock_connect_grpc):
        mock_port_available.return_value = True
        mock_popen.return_value = MagicMock()
        mock_connect_grpc.return_value = MagicMock()  # Simulate a successful connection

        certs_dir = "./test_certs"
        result = launcher.launch_sherlock(
            host="127.0.0.1",
            port=9090,
            transport_mode="mtls",
            certs_dir=certs_dir,
        )

        self.assertIsNotNone(result)
        mock_popen.assert_called_once()
        self.assertIn("--transport-mode=mtls", mock_popen.call_args[0][0])
        self.assertIn("-grpcHost=127.0.0.1", mock_popen.call_args[0][0])
        self.assertIn("-grpcPort=9090", mock_popen.call_args[0][0])
        self.assertIn(f"--certs-dir={certs_dir}", mock_popen.call_args[0][0])

    @patch("ansys.sherlock.core.launcher.connect_grpc_channel")
    @patch("ansys.sherlock.core.launcher._is_port_available")
    @patch("ansys.sherlock.core.launcher.subprocess.Popen")
    def test_launch_sherlock_uds(self, mock_popen, mock_port_available, mock_connect_grpc):
        mock_port_available.return_value = True
        mock_popen.return_value = MagicMock()
        mock_connect_grpc.return_value = MagicMock()  # Simulate a successful connection

        uds_dir = "/tmp/test_uds"
        uds_id = "test_id"
        result = launcher.launch_sherlock(
            transport_mode="uds",
            uds_dir=uds_dir,
            uds_id=uds_id,
        )

        self.assertIsNotNone(result)
        mock_popen.assert_called_once()
        self.assertIn("--transport-mode=uds", mock_popen.call_args[0][0])
        self.assertIn(f"--uds-dir={uds_dir}", mock_popen.call_args[0][0])
        self.assertIn(f"--uds-id={uds_id}", mock_popen.call_args[0][0])

    @patch("ansys.sherlock.core.launcher.connect_grpc_channel")
    @patch("ansys.sherlock.core.launcher._is_port_available")
    @patch("ansys.sherlock.core.launcher.subprocess.Popen")
    def test_launch_sherlock_wnua(self, mock_popen, mock_port_available, mock_connect_grpc):
        mock_port_available.return_value = True
        mock_popen.return_value = MagicMock()
        mock_connect_grpc.return_value = MagicMock()  # Simulate a successful connection

        result = launcher.launch_sherlock(
            host="127.0.0.1",
            port=9090,
            transport_mode="wnua",
        )

        self.assertIsNotNone(result)
        mock_popen.assert_called_once()
        self.assertIn("--transport-mode=wnua", mock_popen.call_args[0][0])
        self.assertIn("-grpcHost=127.0.0.1", mock_popen.call_args[0][0])
        self.assertIn("-grpcPort=9090", mock_popen.call_args[0][0])


if __name__ == "__main__":
    unittest.main()
