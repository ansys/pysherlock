# © 2023-2025 ANSYS, Inc. All rights reserved

import os
import unittest
from unittest.mock import MagicMock, patch

from ansys.sherlock.core import launcher


class TestLauncher(unittest.TestCase):
    @patch("os.path.isfile")
    @patch.dict(
        os.environ,
        {
            "AWP_ROOT223": "C:\\Program Files\\ANSYS Inc\\v223",
            "AWP_ROOT222": "C:\\Program Files\\ANSYS Inc\\v222",
            "AWP_ROOT102": "C:\\Program Files\\ANSYS Inc\\v102",
        },
        clear=True,
    )
    def test_base_ansys(self, mock_os_path_isfile):
        mock_os_path_isfile.return_value = True
        self.assertEqual("C:\\Program Files\\ANSYS Inc\\v223", launcher._get_base_ansys()[0])

    def test_get_ansys_version_from_awp_root(self):
        self.assertEqual(223, launcher._get_ansys_version_from_awp_root("AWP_ROOT223"))
        self.assertEqual(0, launcher._get_ansys_version_from_awp_root("AWPROOT223"))

    @patch("ansys.sherlock.core.launcher._get_base_ansys")
    def test_get_sherlock_exe_path(self, mock_get_base_ansys):
        install_path = "C:\\Program Files\\ANSYS Inc\\v223"
        mock_get_base_ansys.return_value = (install_path, 223)
        sherlock_path, version, ansys_install_path = launcher._get_sherlock_exe_path()
        self.assertEqual(
            os.path.join(install_path, "sherlock", "SherlockClient.exe"),
            sherlock_path,
        )
        self.assertEqual(223, version)
        self.assertEqual(install_path, ansys_install_path)

    def test_extract_sherlock_version_year_with_three_digits(self):
        with self.assertRaises(ValueError) as context:
            launcher._extract_sherlock_version_year(999)
        self.assertEqual(str(context.exception), "Year must be a 4-digit integer.")

    def test_extract_sherlock_version_year_with_four_digits(self):
        self.assertEqual(24, launcher._extract_sherlock_version_year(2024))

    @patch("os.path.isfile")
    @patch("ansys.sherlock.core.launcher._extract_sherlock_version_year")
    @patch.dict(
        os.environ,
        {
            "AWP_ROOT241": "C:\\Program Files\\ANSYS Inc\\v241",
            "AWP_ROOT232": "C:\\Program Files\\ANSYS Inc\\v232",
        },
        clear=True,
    )
    def test_get_base_ansys_calls_extract_sherlock_version_year(
        self, mock_extract_year, mock_os_path_isfile
    ):
        mock_extract_year.return_value = 24
        mock_os_path_isfile.return_value = True

        launcher._get_base_ansys(year=2024, release_number=1)

        mock_os_path_isfile.assert_any_call(
            os.path.join("C:\\Program Files\\ANSYS Inc\\v241", "sherlock", "SherlockClient.exe")
        )
        mock_os_path_isfile.assert_any_call(
            os.path.join("C:\\Program Files\\ANSYS Inc\\v232", "sherlock", "SherlockClient.exe")
        )
        mock_extract_year.assert_called_once_with(2024)

    def test_convert_to_server_version(self):
        self.assertEqual(
            241, launcher._convert_to_server_version(sherlock_release_version="2024 R1")
        )

    def test_convert_to_server_version_fails_for_two_digit_year(self):
        try:
            launcher._convert_to_server_version(sherlock_release_version="24 R1")
            self.fail("Expected ValueError to be raised.")
        except ValueError as e:
            self.assertEqual("Year must be a 4-digit integer.", str(e))

    def test_convert_to_server_version_fails_for_invalid_version(self):
        version = "INVALID"
        try:
            launcher._convert_to_server_version(sherlock_release_version=version)
            self.fail("Expected exception to be raised.")
        except Exception as e:
            self.assertEqual(f"invalid literal for int() with base 10: '{version}'", str(e))


class TestLauncherTransportModes(unittest.TestCase):
    def setUp(self):
        self.mock_sherlock_info = MagicMock()
        self.mock_sherlock_info.releaseVersion = "2025 R2"
        self.mock_channel = MagicMock()
        self.mock_channel.unary_unary.return_value.return_value = self.mock_sherlock_info

    # ----------------
    # Tests: launch
    # ----------------
    @patch("ansys.sherlock.core.launcher._is_port_available")
    @patch("ansys.sherlock.core.launcher.subprocess.Popen")
    def test_launch_insecure(self, mock_popen, mock_port_available):
        mock_port_available.return_value = True
        mock_popen.return_value = MagicMock()

        result = launcher.launch(
            host="127.0.0.1",
            port=9090,
            transport_mode="insecure",
        )

        self.assertIsNotNone(result)
        mock_popen.assert_called_once()
        self.assertIn("--transport-mode=insecure", mock_popen.call_args[0][0])
        self.assertIn("--grpcHost=127.0.0.1", mock_popen.call_args[0][0])
        self.assertIn("--grpcPort=9090", mock_popen.call_args[0][0])

    @patch("ansys.sherlock.core.launcher._is_port_available")
    @patch("ansys.sherlock.core.launcher.subprocess.Popen")
    def test_launch_mtls(self, mock_popen, mock_port_available):
        mock_port_available.return_value = True
        mock_popen.return_value = MagicMock()

        certs_dir = "./test_certs"
        result = launcher.launch(
            host="127.0.0.1",
            port=9090,
            transport_mode="mtls",
            certs_dir=certs_dir,
        )

        self.assertIsNotNone(result)
        mock_popen.assert_called_once()
        self.assertIn("--transport-mode=mtls", mock_popen.call_args[0][0])
        self.assertIn("--grpcHost=127.0.0.1", mock_popen.call_args[0][0])
        self.assertIn("--grpcPort=9090", mock_popen.call_args[0][0])
        self.assertIn(f"--certs-dir={certs_dir}", mock_popen.call_args[0][0])

    @patch("ansys.sherlock.core.launcher._is_port_available")
    @patch("ansys.sherlock.core.launcher.subprocess.Popen")
    def test_launch_uds(self, mock_popen, mock_port_available):
        mock_port_available.return_value = True
        mock_popen.return_value = MagicMock()

        uds_dir = "/tmp/test_uds"
        uds_id = "test_id"
        result = launcher.launch(
            transport_mode="uds",
            uds_dir=uds_dir,
            uds_id=uds_id,
        )

        self.assertIsNotNone(result)
        mock_popen.assert_called_once()
        self.assertIn("--transport-mode=uds", mock_popen.call_args[0][0])
        self.assertIn(f"--uds-dir={uds_dir}", mock_popen.call_args[0][0])
        self.assertIn(f"--uds-id={uds_id}", mock_popen.call_args[0][0])

    @patch("ansys.sherlock.core.launcher._is_port_available")
    @patch("ansys.sherlock.core.launcher.subprocess.Popen")
    def test_launch_wnua(self, mock_popen, mock_port_available):
        mock_port_available.return_value = True
        mock_popen.return_value = MagicMock()

        result = launcher.launch(
            host="127.0.0.1",
            port=9090,
            transport_mode="wnua",
        )

        self.assertIsNotNone(result)
        mock_popen.assert_called_once()
        self.assertIn("--transport-mode=wnua", mock_popen.call_args[0][0])
        self.assertIn("--grpcHost=127.0.0.1", mock_popen.call_args[0][0])
        self.assertIn("--grpcPort=9090", mock_popen.call_args[0][0])

    # ----------------
    # Tests: connect
    # ----------------
    @patch("ansys.sherlock.core.launcher._connect_grpc_channel")
    @patch("ansys.sherlock.core.launcher._wait_for_sherlock_grpc_ready")
    def test_connect_insecure(self, mock_wait_ready, mock_connect_channel):
        mock_connect_channel.return_value = self.mock_channel
        mock_wait_ready.return_value = None

        sherlock = launcher.connect(
            port=9090,
            transport_mode="insecure",
        )

        self.assertIsNotNone(sherlock)
        mock_connect_channel.assert_called_once_with(
            host="127.0.0.1",
            port=9090,
            uds_dir=None,
            uds_id=None,
            transport_mode="insecure",
            certs_dir=None,
        )
        mock_wait_ready.assert_called_once_with(self.mock_channel, 120)

    @patch("ansys.sherlock.core.launcher._connect_grpc_channel")
    @patch("ansys.sherlock.core.launcher._wait_for_sherlock_grpc_ready")
    def test_connect_mtls(self, mock_wait_ready, mock_connect_channel):
        mock_connect_channel.return_value = self.mock_channel
        mock_wait_ready.return_value = None

        certs_dir = "./test_certs"
        sherlock = launcher.connect(
            port=9090,
            transport_mode="mtls",
            certs_dir=certs_dir,
        )

        self.assertIsNotNone(sherlock)
        mock_connect_channel.assert_called_once_with(
            host="127.0.0.1",
            port=9090,
            uds_dir=None,
            uds_id=None,
            transport_mode="mtls",
            certs_dir=certs_dir,
        )
        mock_wait_ready.assert_called_once_with(self.mock_channel, 120)

    @patch("ansys.sherlock.core.launcher._connect_grpc_channel")
    @patch("ansys.sherlock.core.launcher._wait_for_sherlock_grpc_ready")
    def test_connect_uds(self, mock_wait_ready, mock_connect_channel):
        mock_connect_channel.return_value = self.mock_channel
        mock_wait_ready.return_value = None

        uds_dir = "/tmp/test_uds"
        uds_id = "test_id"
        sherlock = launcher.connect(
            transport_mode="uds",
            uds_dir=uds_dir,
            uds_id=uds_id,
        )

        self.assertIsNotNone(sherlock)
        mock_connect_channel.assert_called_once_with(
            host="127.0.0.1",
            port=9090,
            uds_dir=uds_dir,
            uds_id=uds_id,
            transport_mode="uds",
            certs_dir=None,
        )
        mock_wait_ready.assert_called_once_with(self.mock_channel, 120)


if __name__ == "__main__":
    unittest.main()
