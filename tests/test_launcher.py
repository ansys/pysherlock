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
    )
    @patch("os.path.isdir")
    def test_base_ansys(self, mock_os_path_isdir):
        mock_os_path_isdir.return_value = True
        self.assertEqual("C:\\Program Files\\ANSYS Inc\\v223", launcher._get_base_ansys())

    def test_get_ansys_version_from_awp_root(self):
        self.assertEqual(223, launcher._get_ansys_version_from_awp_root("AWP_ROOT223"))
        self.assertEqual("", launcher._get_ansys_version_from_awp_root("AWPROOT223"))

    @patch("ansys.sherlock.core.launcher._get_base_ansys")
    def test_get_sherlock_exe_path(self, mock_get_base_ansys):
        mock_get_base_ansys.return_value = "base_ansys_path"
        self.assertEqual(
            os.path.join("base_ansys_path", "sherlock", "SherlockClient.exe"),
            launcher._get_sherlock_exe_path(),
        )


if __name__ == "__main__":
    unittest.main()
