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

    @patch("subprocess.Popen")
    @patch.dict(
        os.environ,
        {
            "AWP_ROOT242": "C:\\Program Files\\ANSYS Inc\\v242",
        },
        clear=True,
    )
    def test_launch_sherlock_with_version(self, mock_popen):
        mock_popen.return_value.communicate.return_value = (b"", b"")
        mock_popen.return_value.returncode = 0

        year = 24
        release_number = 2
        project_path = "D:\\Sherlock\\Projects\\Assembly Tutorial"
        sherlock = launcher.launch_sherlock(
            port=9090, single_project_path=project_path, year=year, release_number=release_number
        )

        mock_popen.assert_called_once_with(
            [
                "C:\\Program Files\\ANSYS Inc\\v242\\sherlock\\SherlockClient.exe",
                "-grpcPort=9090",
                "-singleProject",
                project_path,
            ]
        )


if __name__ == "__main__":
    unittest.main()
