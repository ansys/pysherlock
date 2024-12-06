# © 2023 ANSYS, Inc. All rights reserved

import os
import unittest
from unittest.mock import patch

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


if __name__ == "__main__":
    unittest.main()
