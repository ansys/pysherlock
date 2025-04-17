# © 2023 ANSYS, Inc. All rights reserved

import os
import unittest
from unittest.mock import patch

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


if __name__ == "__main__":
    unittest.main()
