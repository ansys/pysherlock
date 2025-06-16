# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.

import os
import platform
import unittest

import grpc
import pytest

from ansys.sherlock.core.errors import (
    SherlockExportAEDBError,
    SherlockExportFEAModelError,
    SherlockModelServiceError,
)
from ansys.sherlock.core.model import Model
from ansys.sherlock.core.types.common_types import Measurement
from ansys.sherlock.core.utils.version_check import SKIP_VERSION_CHECK


class TestModel(unittest.TestCase):
    def test_model_export_trace_reinforcement_model(self):
        channel_param = "127.0.0.1:9090"
        channel = grpc.insecure_channel(channel_param)
        model = Model(channel, SKIP_VERSION_CHECK)

        if platform.system() == "Windows":
            temp_dir = os.environ.get("TEMP", "C:\\TEMP")
        else:
            temp_dir = os.environ.get("TEMP", "/tmp")
        path = os.path.join(temp_dir, "export.wbjn")

        if model._is_connection_up():
            try:
                invalid_cca = "Invalid CCA"
                model.export_trace_reinforcement_model("Tutorial Project", invalid_cca, path)
                pytest.fail("No exception raised when using an invalid parameter")
            except Exception as e:
                assert type(e) is SherlockModelServiceError

            try:
                result = model.export_trace_reinforcement_model(
                    "Tutorial Project", "Main Board", path
                )
                assert result == 0
            except SherlockModelServiceError as e:
                pytest.fail(str(e))

        try:
            model.export_trace_reinforcement_model("", "Main Board", path)
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Project name is invalid."

        try:
            model.export_trace_reinforcement_model("Tutorial Project", "", path)
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: CCA name is invalid."

        try:
            model.export_trace_reinforcement_model("Tutorial Project", "Main Board", export_file="")
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Export file path is invalid."

        missing_file_path = "missing\\file\\path\\"
        try:
            model.export_trace_reinforcement_model(
                "Tutorial Project", "Main Board", missing_file_path
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockModelServiceError as e:
            assert (
                str(e) == "Model service error: Export file directory"
                ' "' + missing_file_path + '" does not exist.'
            )

    def test_model_generate_trace_model(self):
        channel_param = "127.0.0.1:9090"
        channel = grpc.insecure_channel(channel_param)
        model = Model(channel, SKIP_VERSION_CHECK)

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
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Project name is invalid."

        if model._is_connection_up():
            try:
                invalid_cca_name = "Invalid CCA"
                model.generate_trace_model(
                    project_name=project_name,
                    cca_name=invalid_cca_name,
                    copper_layer_name=copper_layer_name,
                    max_arc_segment=max_arc_segment,
                )
                pytest.fail("No exception raised when using an invalid parameter")
            except Exception as e:
                assert type(e) is SherlockModelServiceError

            try:
                result = model.generate_trace_model(
                    project_name,
                    cca_name,
                    copper_layer_name,
                    max_arc_segment,
                )
                assert result == 0
            except SherlockModelServiceError as e:
                pytest.fail(str(e))

    def test_model_export_aedb(self):
        channel_param = "127.0.0.1:9090"
        channel = grpc.insecure_channel(channel_param)
        model = Model(channel, SKIP_VERSION_CHECK)

        project_name = "Tutorial Project"
        cca_name = "Main Board"
        export_file = "test_aedb_export"
        try:
            model.export_aedb(
                project_name="",
                cca_name=cca_name,
                export_file=export_file,
                overwrite=True,
                display_model=False,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockExportAEDBError as e:
            assert str(e) == "Export AEDB error: Project name is invalid."

        try:
            model.export_aedb(
                project_name=project_name,
                cca_name="",
                export_file=export_file,
                overwrite=True,
                display_model=False,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockExportAEDBError as e:
            assert str(e) == "Export AEDB error: CCA name is invalid."

        try:
            model.export_aedb(
                project_name=project_name,
                cca_name=cca_name,
                export_file="",
                overwrite=True,
                display_model=False,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockExportAEDBError as e:
            assert str(e) == "Export AEDB error: Export filepath is required."

        if model._is_connection_up():
            try:
                invalid_cca_name = "Invalid CCA"
                model.export_aedb(
                    project_name=project_name,
                    cca_name=invalid_cca_name,
                    export_file=export_file,
                    overwrite=True,
                    display_model=False,
                )
                pytest.fail("No exception raised when using an invalid parameter")
            except Exception as e:
                assert type(e) is SherlockExportAEDBError

            try:
                result = model.export_aedb(
                    project_name=project_name,
                    cca_name=cca_name,
                    export_file=export_file,
                    overwrite=True,
                    display_model=False,
                )
                assert result == 0
            except SherlockExportAEDBError as e:
                pytest.fail(str(e))

    def test_model_export_trace_model(self):
        channel_param = "127.0.0.1:9090"
        channel = grpc.insecure_channel(channel_param)
        model = Model(channel, SKIP_VERSION_CHECK)

        project_name = "Tutorial Project"
        cca_name = "Main Board"
        output_file_path = ".\\outputFile.stp"
        copper_layer_name = "copper-01.odb"

        try:
            model.exportTraceModel(
                [
                    model.createExportTraceCopperLayerParams(
                        project_name="",
                        cca_name=cca_name,
                        output_file_path=output_file_path,
                        copper_layer=copper_layer_name,
                        overwrite=True,
                    )
                ]
            )
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Project name is invalid."

        try:
            model.exportTraceModel(
                [
                    model.createExportTraceCopperLayerParams(
                        project_name=project_name,
                        cca_name="",
                        output_file_path=output_file_path,
                        copper_layer=copper_layer_name,
                        overwrite=True,
                    )
                ]
            )
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: CCA name is invalid."

        try:
            model.exportTraceModel(
                [
                    model.createExportTraceCopperLayerParams(
                        project_name=project_name,
                        cca_name=cca_name,
                        output_file_path="",
                        copper_layer=copper_layer_name,
                        overwrite=True,
                    )
                ]
            )
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Output File path is required"

        try:
            model.exportTraceModel(
                [
                    model.createExportTraceCopperLayerParams(
                        project_name=project_name,
                        cca_name=cca_name,
                        output_file_path=output_file_path,
                        copper_layer="",
                        overwrite=True,
                    )
                ]
            )
        except SherlockModelServiceError as e:
            assert str(e) == "Model service error: Copper layer name is required."

        if model._is_connection_up():
            try:
                result = model.exportTraceModel(
                    [
                        model.createExportTraceCopperLayerParams(
                            project_name=project_name,
                            cca_name=cca_name,
                            output_file_path=output_file_path,
                            copper_layer=copper_layer_name,
                            overwrite=True,
                        )
                    ]
                )
                assert result == 0
            except SherlockModelServiceError as e:
                pytest.fail(str(e))

    def test_export_FEA_model(self):
        channel_param = "127.0.0.1:9090"
        channel = grpc.insecure_channel(channel_param)
        model = Model(channel, SKIP_VERSION_CHECK)

        if platform.system() == "Windows":
            temp_dir = os.environ.get("TEMP", "C:\\TEMP")
        else:
            temp_dir = os.environ.get("TEMP", "/tmp")
        path = os.path.join(temp_dir, "export.wbjn")

        try:
            model.export_FEA_model(
                project="",
                cca_name="Main Board",
                export_file=path,
                analysis="NaturalFreq",
                drill_hole_parameters=[
                    {
                        "drill_hole_modeling": "ENABLED",
                        "min_hole_diameter": Measurement(value=0.5, unit="mm"),
                        "max_edge_length": Measurement(value=1.0, unit="mm"),
                    }
                ],
                detect_lead_modeling="ENABLED",
                lead_model_parameters=[
                    {
                        "lead_modeling": "ENABLED",
                        "lead_element_order": "First Order (Linear)",
                        "max_mesh_size": Measurement(value=0.5, unit="mm"),
                        "vertical_mesh_size": Measurement(value=0.1, unit="mm"),
                        "thicknessCount": 3,
                        "aspectRatio": 2,
                    }
                ],
                display_model=True,
                clear_FEA_database=True,
                use_FEA_model_id=True,
                coordinate_units="mm",
            )
            pytest.fail("No exception raised for invalid project name")
        except SherlockExportFEAModelError as e:
            assert str(e) == "Export FEA model error: Project name is invalid."

        try:
            model.export_FEA_model(
                project="Tutorial Project",
                cca_name="",
                export_file=path,
                analysis="NaturalFreq",
                drill_hole_parameters=[
                    {
                        "drill_hole_modeling": "ENABLED",
                        "min_hole_diameter": Measurement(value=0.5, unit="mm"),
                        "max_edge_length": Measurement(value=1.0, unit="mm"),
                    }
                ],
                detect_lead_modeling="ENABLED",
                lead_model_parameters=[
                    {
                        "lead_modeling": "ENABLED",
                        "lead_element_order": "First Order (Linear)",
                        "max_mesh_size": Measurement(value=0.5, unit="mm"),
                        "vertical_mesh_size": Measurement(value=0.1, unit="mm"),
                        "thicknessCount": 3,
                        "aspectRatio": 2,
                    }
                ],
                display_model=True,
                clear_FEA_database=True,
                use_FEA_model_id=True,
                coordinate_units="mm",
            )
            pytest.fail("No exception raised for invalid project name")
        except SherlockExportFEAModelError as e:
            assert str(e) == "Export FEA model error: CCA name is invalid."

        try:
            model.export_FEA_model(
                project="Tutorial Project",
                cca_name="Main Board",
                export_file="",
                analysis="NaturalFreq",
                drill_hole_parameters=[
                    {
                        "drill_hole_modeling": "ENABLED",
                        "min_hole_diameter": Measurement(value=0.5, unit="mm"),
                        "max_edge_length": Measurement(value=1.0, unit="mm"),
                    }
                ],
                detect_lead_modeling="ENABLED",
                lead_model_parameters=[
                    {
                        "lead_modeling": "ENABLED",
                        "lead_element_order": "First Order (Linear)",
                        "max_mesh_size": Measurement(value=0.5, unit="mm"),
                        "vertical_mesh_size": Measurement(value=0.1, unit="mm"),
                        "thicknessCount": 3,
                        "aspectRatio": 2,
                    }
                ],
                display_model=True,
                clear_FEA_database=True,
                use_FEA_model_id=True,
                coordinate_units="mm",
            )
            pytest.fail("No exception raised for invalid project name")
        except SherlockExportFEAModelError as e:
            assert str(e) == "Export FEA model error: Export file path is invalid."

        try:
            model.export_FEA_model(
                project="Tutorial Project",
                cca_name="Main Board",
                export_file="test",
                analysis="NaturalFreq",
                drill_hole_parameters=[
                    {
                        "drill_hole_modeling": "ENABLED",
                        "min_hole_diameter": Measurement(value=0.5, unit="mm"),
                        "max_edge_length": Measurement(value=1.0, unit="mm"),
                    }
                ],
                detect_lead_modeling="ENABLED",
                lead_model_parameters=[
                    {
                        "lead_modeling": "ENABLED",
                        "lead_element_order": "First Order (Linear)",
                        "max_mesh_size": Measurement(value=0.5, unit="mm"),
                        "vertical_mesh_size": Measurement(value=0.1, unit="mm"),
                        "thicknessCount": 3,
                        "aspectRatio": 2,
                    }
                ],
                display_model=True,
                clear_FEA_database=True,
                use_FEA_model_id=True,
                coordinate_units="mm",
            )
            pytest.fail("No exception raised for invalid project name")
        except SherlockExportFEAModelError as e:
            assert str(e) == f'Export FEA model error: Export file directory "test" does not exist.'

        try:
            model.export_FEA_model(
                project="Tutorial Project",
                cca_name="Main Board",
                export_file=path,
                analysis="NaturalFreq",
                drill_hole_parameters=[
                    {
                        "drill_hole_modeling": "ENABLED",
                        "min_hole_diameter": 0,
                        "max_edge_length": Measurement(value=1.0, unit="mm"),
                    }
                ],
                detect_lead_modeling="ENABLED",
                lead_model_parameters=[
                    {
                        "lead_modeling": "ENABLED",
                        "lead_element_order": "First Order (Linear)",
                        "max_mesh_size": Measurement(value=0.5, unit="mm"),
                        "vertical_mesh_size": Measurement(value=0.1, unit="mm"),
                        "thicknessCount": 3,
                        "aspectRatio": 2,
                    }
                ],
                display_model=True,
                clear_FEA_database=True,
                use_FEA_model_id=True,
                coordinate_units="mm",
            )
            pytest.fail("No exception raised for invalid project name")
        except SherlockExportFEAModelError as e:
            assert str(e) == "Export FEA model error: Minimum hole diameter is invalid."

        try:
            model.export_FEA_model(
                project="Tutorial Project",
                cca_name="Main Board",
                export_file=path,
                analysis="NaturalFreq",
                drill_hole_parameters=[
                    {
                        "drill_hole_modeling": "ENABLED",
                        "min_hole_diameter": Measurement(value=0.5, unit="mm"),
                        "max_edge_length": 0,
                    }
                ],
                detect_lead_modeling="ENABLED",
                lead_model_parameters=[
                    {
                        "lead_modeling": "ENABLED",
                        "lead_element_order": "First Order (Linear)",
                        "max_mesh_size": Measurement(value=0.5, unit="mm"),
                        "vertical_mesh_size": Measurement(value=0.1, unit="mm"),
                        "thicknessCount": 3,
                        "aspectRatio": 2,
                    }
                ],
                display_model=True,
                clear_FEA_database=True,
                use_FEA_model_id=True,
                coordinate_units="mm",
            )
            pytest.fail("No exception raised for invalid project name")
        except SherlockExportFEAModelError as e:
            assert str(e) == "Export FEA model error: Maximum edge length is invalid."

        try:
            model.export_FEA_model(
                project="Tutorial Project",
                cca_name="Main Board",
                export_file=path,
                analysis="NaturalFreq",
                drill_hole_parameters=[
                    {
                        "drill_hole_modeling": "ENABLED",
                        "min_hole_diameter": Measurement(value=0.5, unit="mm"),
                        "max_edge_length": Measurement(value=1.0, unit="mm"),
                    }
                ],
                detect_lead_modeling="ENABLED",
                lead_model_parameters=[
                    {
                        "lead_modeling": "ENABLED",
                        "lead_element_order": "First Order (Linear)",
                        "max_mesh_size": 0,
                        "vertical_mesh_size": Measurement(value=0.1, unit="mm"),
                        "thicknessCount": 3,
                        "aspectRatio": 2,
                    }
                ],
                display_model=True,
                clear_FEA_database=True,
                use_FEA_model_id=True,
                coordinate_units="mm",
            )
            pytest.fail("No exception raised for invalid project name")
        except SherlockExportFEAModelError as e:
            assert str(e) == "Export FEA model error: Maximum mesh size is invalid."

        try:
            model.export_FEA_model(
                project="Tutorial Project",
                cca_name="Main Board",
                export_file=path,
                analysis="NaturalFreq",
                drill_hole_parameters=[
                    {
                        "drill_hole_modeling": "ENABLED",
                        "min_hole_diameter": Measurement(value=0.5, unit="mm"),
                        "max_edge_length": Measurement(value=1.0, unit="mm"),
                    }
                ],
                detect_lead_modeling="ENABLED",
                lead_model_parameters=[
                    {
                        "lead_modeling": "ENABLED",
                        "lead_element_order": "First Order (Linear)",
                        "max_mesh_size": Measurement(value=0.5, unit="mm"),
                        "vertical_mesh_size": 0,
                        "thicknessCount": 3,
                        "aspectRatio": 2,
                    }
                ],
                display_model=True,
                clear_FEA_database=True,
                use_FEA_model_id=True,
                coordinate_units="mm",
            )
            pytest.fail("No exception raised for invalid project name")
        except SherlockExportFEAModelError as e:
            assert str(e) == "Export FEA model error: Vertical mesh size is invalid."

        if model._is_connection_up():
            try:
                model.export_FEA_model(
                    project="Tutorial Project",
                    cca_name="Invalid CCA",
                    export_file=path,
                    analysis="NaturalFreq",
                    drill_hole_parameters=[
                        {
                            "drill_hole_modeling": "ENABLED",
                            "min_hole_diameter": Measurement(value=0.5, unit="mm"),
                            "max_edge_length": Measurement(value=1.0, unit="mm"),
                        }
                    ],
                    detect_lead_modeling="ENABLED",
                    lead_model_parameters=[
                        {
                            "lead_modeling": "ENABLED",
                            "lead_element_order": "First Order (Linear)",
                            "max_mesh_size": Measurement(value=0.5, unit="mm"),
                            "vertical_mesh_size": Measurement(value=0.1, unit="mm"),
                            "thicknessCount": 3,
                            "aspectRatio": 2,
                        }
                    ],
                    display_model=True,
                    clear_FEA_database=True,
                    use_FEA_model_id=True,
                    coordinate_units="mm",
                )
                pytest.fail("No exception raised for invalid project name")
            except Exception as e:
                assert type(e) == SherlockExportFEAModelError

            try:
                result = model.export_FEA_model(
                    project="Tutorial Project",
                    cca_name="Main Board",
                    export_file=path,
                    analysis="NaturalFreq",
                    drill_hole_parameters=[
                        {
                            "drill_hole_modeling": "ENABLED",
                            "min_hole_diameter": Measurement(value=0.5, unit="mm"),
                            "max_edge_length": Measurement(value=1.0, unit="mm"),
                        }
                    ],
                    detect_lead_modeling="ENABLED",
                    lead_model_parameters=[
                        {
                            "lead_modeling": "ENABLED",
                            "lead_element_order": "First Order (Linear)",
                            "max_mesh_size": Measurement(value=0.5, unit="mm"),
                            "vertical_mesh_size": Measurement(value=0.1, unit="mm"),
                            "thicknessCount": 3,
                            "aspectRatio": 2,
                        }
                    ],
                    display_model=False,
                    clear_FEA_database=False,
                    use_FEA_model_id=False,
                    coordinate_units="mm",
                )
                assert result == 0

            except SherlockExportFEAModelError as e:
                pytest.fail(str(e))
            finally:
                # Clean up file
                if os.path.exists(path):
                    os.remove(path)


if __name__ == "__main__":
    unittest.main()
