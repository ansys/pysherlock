import unittest
from unittest.mock import patch

from ansys.sherlock.core import model
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

    def test_set_trace_param(self):
        str_obj = "wrong object type"
        try:
            model.set_trace_parameter(str_obj)
        except Exception as e:
            error_msg = (
                "Sherlock model service error: trace_param object is not of type "
                "SherlockModelService_pb2.ExportTraceReinforcementModelRequest.TraceParam."
            )
            assert str(e) == error_msg

    def test_set_trace_drill_hole_param(self):
        str_obj = "wrong object type"
        try:
            model.set_trace_drill_hole_parameter(str_obj)
        except Exception as e:
            error_msg = (
                "Sherlock model service error: trace_drill_hole_param object is not of type "
                "SherlockModelService_pb2.ExportTraceReinforcementModelRequest.TraceDrillHoleParam."
            )
            assert str(e) == error_msg


if __name__ == "__main__":
    unittest.main()
