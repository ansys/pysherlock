# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

import os
import platform
import unittest

import grpc
from ansys.sherlock.core.errors import SherlockModelServiceError

from ansys.sherlock.core.model import Model


class TestModel(unittest.TestCase):
    def test_model_export_trace_reinforcement_model(self):
        channel_param = "127.0.0.1:9090"
        channel = grpc.insecure_channel(channel_param)
        model = Model(channel)

        if platform.system() == "Windows":
            temp_dir = os.environ.get("TEMP", "C:\\TEMP")
        else:
            temp_dir = os.environ.get("TEMP", "/tmp")
        path = os.path.join(temp_dir, "export.wbjn")

        if model._is_connection_up():
            result = model.export_trace_reinforcement_model("Tutorial Project", "Main Board", path)
            assert result[0] == 0

            try:
                invalid_cca = "Invalid CCA"
                model.export_trace_reinforcement_model("Tutorial Project", invalid_cca, path)
                assert False
            except Exception as e:
                assert type(e) == SherlockModelServiceError

        try:
            model.export_trace_reinforcement_model("", "Main Board", path)
            assert False
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Project name is invalid."

        try:
            model.export_trace_reinforcement_model("Tutorial Project", "", path)
            assert False
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: CCA name is invalid."

        try:
            model.export_trace_reinforcement_model("Tutorial Project", "Main Board", export_file="")
            assert False
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Export file path is invalid."

        missing_file_path = "missing\\file\\path\\"
        try:
            model.export_trace_reinforcement_model(
                "Tutorial Project", "Main Board", missing_file_path
            )
            assert False
        except SherlockModelServiceError as e:
            assert (
                str(e) == "Model service error: Export file directory"
                ' "' + missing_file_path + '" does not exist.'
            )

    def test_model_generate_trace_model(self):
        channel_param = "127.0.0.1:9090"
        channel = grpc.insecure_channel(channel_param)
        model = Model(channel)

        project_name = "Tutorial Project"
        cca_name = "Main Board"
        copper_layer_name = "copper-03.odb"
        max_arc_segment = 5
        try:
            model.generate_trace_model(
                project_name="",
                cca_name=cca_name,
                copper_layer_name=copper_layer_name,
                max_arc_segment=max_arc_segment,
            )
            assert False
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Project name is invalid."

        try:
            model.generate_trace_model(
                project_name=project_name,
                cca_name="",
                copper_layer_name=copper_layer_name,
                max_arc_segment=max_arc_segment,
            )
            assert False
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: CCA name is invalid."

        try:
            model.generate_trace_model(
                project_name=project_name,
                cca_name=cca_name,
                copper_layer_name="",
                max_arc_segment=max_arc_segment,
            )
            assert False
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Copper layer name is required."

        try:
            model.generate_trace_model(
                project_name=project_name,
                cca_name=cca_name,
                copper_layer_name=copper_layer_name,
                max_arc_segment=None,
            )
            assert False
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Maximum arc segment is required."

        try:
            model.generate_trace_model(
                project_name=project_name,
                cca_name=cca_name,
                copper_layer_name=copper_layer_name,
                max_arc_segment=max_arc_segment,
                max_arc_segment_units="",
            )
            assert False
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Maximum arc segment units are required."

        try:
            model.generate_trace_model(
                project_name=project_name,
                cca_name=cca_name,
                copper_layer_name=copper_layer_name,
                max_arc_segment=max_arc_segment,
                min_trace_area=None,
            )
            assert False
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Minimum trace area is required."

        try:
            model.generate_trace_model(
                project_name=project_name,
                cca_name=cca_name,
                copper_layer_name=copper_layer_name,
                max_arc_segment=max_arc_segment,
                min_trace_area_units="",
            )
            assert False
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Minimum trace area units are required."

        try:
            model.generate_trace_model(
                project_name=project_name,
                cca_name=cca_name,
                copper_layer_name=copper_layer_name,
                max_arc_segment=max_arc_segment,
                min_hole_area=None,
            )
            assert False
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Minimum hole area is required."

        try:
            model.generate_trace_model(
                project_name=project_name,
                cca_name=cca_name,
                copper_layer_name=copper_layer_name,
                max_arc_segment=max_arc_segment,
                min_hole_area_units="",
            )
            assert False
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Minimum hole area units are required."

        if model._is_connection_up():
            result = model.generate_trace_model(
                project_name,
                cca_name,
                copper_layer_name,
                max_arc_segment,
            )
            assert result == 0

            try:
                invalid_cca_name = "Invalid CCA"
                model.generate_trace_model(
                    project_name=project_name,
                    cca_name=invalid_cca_name,
                    copper_layer_name=copper_layer_name,
                    max_arc_segment=max_arc_segment,
                )
                assert False
            except Exception as e:
                assert type(e) == SherlockModelServiceError


if __name__ == "__main__":
    unittest.main()
