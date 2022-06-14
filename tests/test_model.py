import unittest
from unittest.mock import patch

from ansys.sherlock.core.model import Model


class TestModel(unittest.TestCase):
    def test_model_export_file_directory(self):
        with patch.object(Model, "__init__", lambda a, b, c, d: None):
            instance = Model(None, None, None)

            try:
                instance.export_trace_reinforcement_model(
                    "Tutorial Project", "Main Board", "C:\\Temp2\\export.wbjn"
                )
            except Exception as e:
                assert (
                    str(e) == "Sherlock model service error: Export file directory "
                    "(C:\Temp2) does not exist"
                )


if __name__ == "__main__":
    unittest.main()
