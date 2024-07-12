# © 2024 ANSYS, Inc. All rights reserved

import os
import platform
import time
import uuid

import grpc
import pytest

from ansys.sherlock.core.errors import (
    SherlockAddCCAError,
    SherlockAddProjectError,
    SherlockAddStrainMapsError,
    SherlockAddThermalMapsError,
    SherlockCreateCCAFromModelingRegionError,
    SherlockDeleteProjectError,
    SherlockExportProjectError,
    SherlockGenerateProjectReportError,
    SherlockImportIpc2581Error,
    SherlockImportODBError,
    SherlockImportProjectZipArchiveError,
    SherlockImportProjectZipArchiveSingleModeError,
    SherlockListCCAsError,
    SherlockListStrainMapsError,
    SherlockListThermalMapsError,
    SherlockUpdateThermalMapsError,
)
from ansys.sherlock.core.project import Project
from ansys.sherlock.core.types.project_types import (
    BoardBounds,
    CsvExcelFile,
    ImageBounds,
    ImageFile,
    LegendBounds,
    LegendOrientation,
    StrainMapLegendOrientation,
    StrainMapsFileType,
    ThermalBoardSide,
    ThermalMapsFileType,
)

PROJECT_ADD_NAME = "Delete This After Add"


def test_all():
    """Test all project APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    project = Project(channel)

    helper_test_add_strain_maps(project)
    helper_test_delete_project(project)
    helper_test_import_odb_archive(project)
    helper_test_import_ipc2581_archive(project)
    helper_test_import_project_zip_archive(project)
    helper_test_import_project_zip_archive_single_mode(project)
    helper_test_generate_project_report(project)
    helper_test_list_ccas(project)
    helper_test_add_cca(project)
    helper_test_list_strain_maps(project)
    helper_test_add_thermal_maps(project)
    helper_test_update_thermal_maps(project)
    helper_test_list_thermal_maps(project)
    helper_test_create_cca_from_modeling_region(project)
    project_name = None
    try:
        project_name = helper_test_add_project(project)
    finally:
        clean_up_after_add(project, project_name)

    helper_test_export_project(project)


def helper_test_delete_project(project):
    """Test delete_project API"""
    try:
        project.delete_project("")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockDeleteProjectError as e:
        assert str(e) == "Delete project error: Project name is blank. Specify a project name."

    if project._is_connection_up():
        try:
            missing_project_name = "Name of project that should not exist"
            project.delete_project(missing_project_name)
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockDeleteProjectError


def helper_test_import_odb_archive(project):
    """Test import_odb_archive API"""
    try:
        project.import_odb_archive("", True, True, True, True)
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockImportODBError as e:
        assert str(e) == "Import ODB error: Archive path is required."

    if project._is_connection_up():
        try:
            missing_archive_file = "Missing ODB.tgz"
            project.import_odb_archive(missing_archive_file, True, True, True, True)
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockImportODBError


def helper_test_import_ipc2581_archive(project):
    """Test import_ipc2581_archive API"""
    try:
        project.import_ipc2581_archive("", True, True)
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockImportIpc2581Error as e:
        assert str(e) == "Import IPC2581 error: Archive file path is required."

    if project._is_connection_up():
        try:
            project.import_ipc2581_archive("Missing Archive File.zip", True, True)
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockImportIpc2581Error


def helper_test_generate_project_report(project):
    """Test generate_project_report API."""
    try:
        project.generate_project_report("", "John Doe", "Generic Co.", "C:/report.pdf")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGenerateProjectReportError as e:
        assert str(e) == "Generate project report error: Project name is invalid."

    try:
        project.generate_project_report("Test", "", "Generic Co.", "C:/report.pdf")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGenerateProjectReportError as e:
        assert str(e) == "Generate project report error: Author name is invalid."

    try:
        project.generate_project_report("Test", "John Doe", "", "C:/report.pdf")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGenerateProjectReportError as e:
        assert str(e) == "Generate project report error: Company name is invalid."

    try:
        project.generate_project_report("Test", "John Doe", "Generic Co.", "")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGenerateProjectReportError as e:
        assert str(e) == "Generate project report error: Report path is required."

    if project._is_connection_up():
        if platform.system() == "Windows":
            temp_dir = os.environ.get("TEMP", "C:\\TEMP")
        else:
            temp_dir = os.environ.get("TEMP", "/tmp")
        report_file = os.path.join(temp_dir, "PySherlock unit test project report.pdf")

        result = project.generate_project_report(
            "AssemblyTutorial", "Author", "Company", report_file
        )
        assert result == 0
        assert os.path.exists(report_file)

        os.remove(report_file)

        report_file = "invalid/invalid"
        try:
            project.generate_project_report("Test", "John Doe", "Generic Co.", report_file)
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockGenerateProjectReportError


def helper_test_list_ccas(project):
    """Test list_ccas API"""

    try:
        project.list_ccas("")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockListCCAsError as e:
        assert str(e.str_itr()) == "['List CCAs error: Project name is invalid.']"

    try:
        project.list_ccas("Tutorial Project", "CCA names that is not a list")
        assert False
    except SherlockListCCAsError as e:
        assert str(e.str_itr()) == "['List CCAs error: cca_names is not a list.']"

    if project._is_connection_up():
        try:
            project.list_ccas("Project that doesn't exist")
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockListCCAsError

        try:
            ccas = project.list_ccas("AssemblyTutorial")
            assert len(ccas) == 4
            assert ccas[0].ccaName == "Main Board"
            assert ccas[1].ccaName == "Memory Card 1"
            assert ccas[2].ccaName == "Memory Card 2"
            assert ccas[3].ccaName == "Power Module"

            cca_names = ["Memory Card 2"]
            ccas = project.list_ccas("AssemblyTutorial", cca_names)
            assert len(ccas) == 1
            assert ccas[0].ccaName == "Memory Card 2"
        except SherlockListCCAsError as e:
            pytest.fail(str(e.str_itr()))


def helper_test_add_cca(project):
    """Test add_cca API"""

    try:
        project.add_cca(
            "",
            [
                {
                    "cca_name": "Card 2",
                    "description": "Second CCA",
                    "default_solder_type": "SAC305",
                    "default_stencil_thickness": 10,
                    "default_stencil_thickness_units": "mm",
                    "default_part_temp_rise": 20,
                    "default_part_temp_rise_units": "C",
                    "guess_part_properties_enabled": False,
                },
            ],
        )
        assert False
    except SherlockAddCCAError as e:
        assert str(e) == "Add CCA error: Project name is invalid."

    try:
        project.add_cca("Test", "")
        assert False
    except SherlockAddCCAError as e:
        assert str(e) == "Add CCA error: CCA properties argument is invalid."

    try:
        project.add_cca("Test", [])
        assert False
    except SherlockAddCCAError as e:
        assert str(e) == "Add CCA error: One or more CCAs are required."

    try:
        project.add_cca("Test", [""])
        assert False
    except SherlockAddCCAError as e:
        assert str(e) == "Add CCA error: CCA properties are invalid for CCA 0."

    try:
        project.add_cca(
            "Test",
            [
                {
                    "description": "Second CCA",
                    "default_solder_type": "SAC305",
                    "default_stencil_thickness": 10,
                    "default_stencil_thickness_units": "mm",
                    "default_part_temp_rise": 20,
                    "default_part_temp_rise_units": "C",
                    "guess_part_properties_enabled": False,
                },
            ],
        )
        assert False
    except SherlockAddCCAError as e:
        assert str(e) == "Add CCA error: CCA name is missing for CCA 0."

    try:
        project.add_cca(
            "Test",
            [
                {
                    "cca_name": "",
                    "description": "Second CCA",
                    "default_solder_type": "SAC305",
                    "default_stencil_thickness": 10,
                    "default_stencil_thickness_units": "mm",
                    "default_part_temp_rise": 20,
                    "default_part_temp_rise_units": "C",
                    "guess_part_properties_enabled": False,
                },
            ],
        )
        assert False
    except SherlockAddCCAError as e:
        assert str(e) == "Add CCA error: CCA name is invalid for CCA 0."

    if not project._is_connection_up():
        return

    try:
        project.add_cca(
            "Test",
            [
                {
                    "cca_name": "Name",
                    "description": "Second CCA",
                    "default_solder_type": "SAC305",
                    "default_stencil_thickness": 10,
                    "default_stencil_thickness_units": "INVALID",
                    "default_part_temp_rise": 20,
                    "default_part_temp_rise_units": "C",
                    "guess_part_properties_enabled": False,
                },
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert type(e) == SherlockAddCCAError

    cca_name = "Test Card " + str(uuid.uuid4())
    try:
        result = project.add_cca(
            "Tutorial Project",
            [
                {
                    "cca_name": cca_name,
                    "description": "Second CCA",
                    "default_solder_type": "SAC305",
                    "default_stencil_thickness": 10,
                    "default_stencil_thickness_units": "mm",
                    "default_part_temp_rise": 20,
                    "default_part_temp_rise_units": "C",
                    "guess_part_properties_enabled": False,
                },
            ],
        )
        assert result == 0
    except SherlockAddCCAError as e:
        pytest.fail(str(e))


def helper_test_add_strain_maps(project):
    """Test add_strain_maps API"""

    try:
        project.add_strain_maps(
            "",
            [
                (
                    "StrainMap.csv",
                    "",
                    StrainMapsFileType.CSV,
                    0,
                    "SolidID",
                    "PCB Strain",
                    "µε",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert str(e.str_itr()) == "['Add strain maps error: Project name is invalid.']"

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "",
                    "",
                    StrainMapsFileType.CSV,
                    0,
                    "SolidID",
                    "PCB Strain",
                    "µε",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert str(e.str_itr()) == "['Add strain maps error: Path is required for strain map 0.']"

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.csv",
                    "",
                    StrainMapsFileType.CSV,
                    "0",  # Not an integer
                    "SolidID",
                    "PCB Strain",
                    "µε",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Header row count is required for strain map 0.']"
        )

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.csv",
                    "",
                    StrainMapsFileType.CSV,
                    -1,
                    "SolidID",
                    "PCB Strain",
                    "µε",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Header row count must be greater than or equal to 0 for strain map 0.']"
        )

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.csv",
                    "",
                    StrainMapsFileType.CSV,
                    0,
                    "",
                    "PCB Strain",
                    "µε",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Reference ID column is required for strain map 0.']"
        )

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.csv",
                    "",
                    StrainMapsFileType.CSV,
                    0,
                    "SolidID",
                    "",
                    "µε",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Strain column is required for strain map 0.']"
        )

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.csv",
                    "",
                    StrainMapsFileType.CSV,
                    0,
                    "SolidID",
                    "Strain",
                    "",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Strain units are required for strain map 0.']"
        )

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.csv",
                    "",
                    StrainMapsFileType.CSV,
                    0,
                    "SolidID",
                    "Strain",
                    "BAD",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == '[\'Add strain maps error: Strain units "BAD" '
            "are invalid for strain map 0.']"
        )

    try:
        cca_names_not_list = "Main Board"
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.csv",
                    "",
                    StrainMapsFileType.CSV,
                    0,
                    "refDes",
                    "Strain",
                    "µε",
                    cca_names_not_list,
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "cca_names is not a list for strain map 0.']"
        )

    try:
        project.add_strain_maps(
            "",
            [
                (
                    "StrainMap.xlsx",
                    "",
                    StrainMapsFileType.EXCEL,
                    0,
                    "SolidID",
                    "PCB Strain",
                    "µε",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert str(e.str_itr()) == "['Add strain maps error: Project name is invalid.']"

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "",
                    "",
                    StrainMapsFileType.EXCEL,
                    0,
                    "SolidID",
                    "PCB Strain",
                    "µε",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert str(e.str_itr()) == "['Add strain maps error: Path is required for strain map 0.']"

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.xlsx",
                    "",
                    StrainMapsFileType.EXCEL,
                    "0",  # Not an integer
                    "SolidID",
                    "PCB Strain",
                    "µε",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Header row count is required for strain map 0.']"
        )

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.xlsx",
                    "",
                    StrainMapsFileType.EXCEL,
                    -1,
                    "SolidID",
                    "PCB Strain",
                    "µε",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Header row count must be greater than or equal to 0 for strain map 0.']"
        )

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.xlsx",
                    "",
                    StrainMapsFileType.EXCEL,
                    0,
                    "",
                    "PCB Strain",
                    "µε",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Reference ID column is required for strain map 0.']"
        )

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.xlsx",
                    "",
                    StrainMapsFileType.EXCEL,
                    0,
                    "SolidID",
                    "",
                    "µε",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Strain column is required for strain map 0.']"
        )

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.xlsx",
                    "",
                    StrainMapsFileType.EXCEL,
                    0,
                    "SolidID",
                    "Strain",
                    "",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Strain units are required for strain map 0.']"
        )

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.xlsx",
                    "",
                    StrainMapsFileType.EXCEL,
                    0,
                    "SolidID",
                    "Strain",
                    "BAD",
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == '[\'Add strain maps error: Strain units "BAD" '
            "are invalid for strain map 0.']"
        )

    try:
        cca_names_not_list = "Main Board"
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "StrainMap.xlsx",
                    "",
                    StrainMapsFileType.EXCEL,
                    0,
                    "refDes",
                    "Strain",
                    "µε",
                    cca_names_not_list,
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "cca_names is not a list for strain map 0.']"
        )

    try:
        strain_map_image_properties = (
            BoardBounds([(1.0, 2.0), (3.0, 4.0), (1.0, 2.0), (1.0, 2.0)]),
            "in",
            ImageBounds(0.0, 0.0, 10.0, 8.0),
            LegendBounds(1.0, 2.0, 4.0, 2.0),
            StrainMapLegendOrientation.VERTICAL,
            20.0,
            50.0,
            "µε",
        )
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "",
                    "This is the strain map image for the project",
                    StrainMapsFileType.IMAGE,
                    strain_map_image_properties,
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: " "Path is required for strain map 0.']"
        )

    try:
        strain_map_image_properties = "Invalid list"
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "Strain Map.jpg",
                    "This is the strain map image for the project",
                    StrainMapsFileType.IMAGE,
                    strain_map_image_properties,
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "image_file is not a list for strain map 0.']"
        )

    try:
        strain_map_image_properties = (
            "BoardBounds",
            "in",
            ImageBounds(0.0, 0.0, 10.0, 8.0),
            LegendBounds(1.0, 2.0, 4.0, 2.0),
            StrainMapLegendOrientation.VERTICAL,
            20.0,
            50.0,
            "µε",
        )
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "Strain Map.jpg",
                    "This is the strain map image for the project",
                    StrainMapsFileType.IMAGE,
                    strain_map_image_properties,
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Invalid board bounds for strain map 0.']"
        )

    try:
        strain_map_image_properties = (
            BoardBounds([(1.0, 2.0), (3.0, 4.0), (1.0, 2.0), (1.0, 2.0)]),
            0,
            ImageBounds(0.0, 0.0, 10.0, 8.0),
            LegendBounds(1.0, 2.0, 4.0, 2.0),
            StrainMapLegendOrientation.VERTICAL,
            20.0,
            50.0,
            "µε",
        )
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "Strain Map.jpg",
                    "This is the strain map image for the project",
                    StrainMapsFileType.IMAGE,
                    strain_map_image_properties,
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Invalid coordinate units for strain map 0.']"
        )

    try:
        strain_map_image_properties = (
            BoardBounds([(1.0, 2.0), (3.0, 4.0), (1.0, 2.0), (1.0, 2.0)]),
            "in",
            "ImageBounds",
            LegendBounds(1.0, 2.0, 4.0, 2.0),
            StrainMapLegendOrientation.VERTICAL,
            20.0,
            50.0,
            "µε",
        )
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "Strain Map.jpg",
                    "This is the strain map image for the project",
                    StrainMapsFileType.IMAGE,
                    strain_map_image_properties,
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Invalid image bounds for strain map 0.']"
        )

    try:
        strain_map_image_properties = (
            BoardBounds([(1.0, 2.0), (3.0, 4.0), (1.0, 2.0), (1.0, 2.0)]),
            "in",
            ImageBounds(0.0, 0.0, 10.0, 8.0),
            "LegendBounds",
            StrainMapLegendOrientation.VERTICAL,
            20.0,
            50.0,
            "µε",
        )
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "Strain Map.jpg",
                    "This is the strain map image for the project",
                    StrainMapsFileType.IMAGE,
                    strain_map_image_properties,
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Invalid legend bounds for strain map 0.']"
        )

    try:
        strain_map_image_properties = (
            BoardBounds([(1.0, 2.0), (3.0, 4.0), (1.0, 2.0), (1.0, 2.0)]),
            "in",
            ImageBounds(0.0, 0.0, 10.0, 8.0),
            LegendBounds(1.0, 2.0, 4.0, 2.0),
            "StrainMapLegendOrientation.VERTICAL",
            20.0,
            50.0,
            "µε",
        )
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "Strain Map.jpg",
                    "This is the strain map image for the project",
                    StrainMapsFileType.IMAGE,
                    strain_map_image_properties,
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Invalid legend orientation for strain map 0.']"
        )

    try:
        strain_map_image_properties = (
            BoardBounds([(1.0, 2.0), (3.0, 4.0), (1.0, 2.0), (1.0, 2.0)]),
            "in",
            ImageBounds(0.0, 0.0, 10.0, 8.0),
            LegendBounds(1.0, 2.0, 4.0, 2.0),
            StrainMapLegendOrientation.VERTICAL,
            "20.0",
            50.0,
            "µε",
        )
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "Strain Map.jpg",
                    "This is the strain map image for the project",
                    StrainMapsFileType.IMAGE,
                    strain_map_image_properties,
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Invalid minimum strain for strain map 0.']"
        )

    try:
        strain_map_image_properties = (
            BoardBounds([(1.0, 2.0), (3.0, 4.0), (1.0, 2.0), (1.0, 2.0)]),
            "in",
            ImageBounds(0.0, 0.0, 10.0, 8.0),
            LegendBounds(1.0, 2.0, 4.0, 2.0),
            StrainMapLegendOrientation.VERTICAL,
            20.0,
            "50.0",
            "µε",
        )
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "Strain Map.jpg",
                    "This is the strain map image for the project",
                    StrainMapsFileType.IMAGE,
                    strain_map_image_properties,
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Invalid maximum strain for strain map 0.']"
        )

    try:
        strain_map_image_properties = (
            BoardBounds([(1.0, 2.0), (3.0, 4.0), (1.0, 2.0), (1.0, 2.0)]),
            "in",
            ImageBounds(0.0, 0.0, 10.0, 8.0),
            LegendBounds(1.0, 2.0, 4.0, 2.0),
            StrainMapLegendOrientation.VERTICAL,
            20.0,
            50.0,
            0,
        )
        project.add_strain_maps(
            "Tutorial Project",
            [
                (
                    "Strain Map.jpg",
                    "This is the strain map image for the project",
                    StrainMapsFileType.IMAGE,
                    strain_map_image_properties,
                    ["Main Board"],
                )
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddStrainMapsError as e:
        assert (
            str(e.str_itr()) == "['Add strain maps error: "
            "Invalid strain units for strain map 0.']"
        )

    if project._is_connection_up():
        # happy path test missing because needs valid file
        try:
            strain_map = "Missing strain map.csv"
            project.add_strain_maps(
                "Tutorial Project",
                [
                    (
                        strain_map,
                        "File comment",
                        0,
                        StrainMapsFileType.CSV,
                        "SolidID",
                        "PCB Strain",
                        "µε",
                        ["Main Board"],
                    )
                ],
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockAddStrainMapsError

        try:
            strain_map = "Missing strain map.xlsx"
            project.add_strain_maps(
                "Tutorial Project",
                [
                    (
                        strain_map,
                        "File comment",
                        0,
                        StrainMapsFileType.EXCEL,
                        "SolidID",
                        "PCB Strain",
                        "µε",
                        ["Main Board"],
                    )
                ],
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockAddStrainMapsError

        # happy path test missing because needs valid file
        try:
            strain_map = "Missing strain map.jpg"
            strain_map_image_properties = (
                BoardBounds([(1.0, 2.0), (3.0, 4.0), (1.0, 2.0), (1.0, 2.0)]),
                "in",
                ImageBounds(0.0, 0.0, 10.0, 8.0),
                LegendBounds(1.0, 2.0, 4.0, 2.0),
                StrainMapLegendOrientation.VERTICAL,
                20.0,
                50.0,
                "µε",
            )
            project.add_strain_maps(
                "Tutorial Project",
                [
                    (
                        strain_map,
                        "This is the strain map image for the project",
                        StrainMapsFileType.IMAGE,
                        strain_map_image_properties,
                        ["Main Board"],
                    )
                ],
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockAddStrainMapsError


def helper_test_list_strain_maps(project):
    """Test list_strain_maps API"""

    try:
        project.list_strain_maps("")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockListStrainMapsError as e:
        assert str(e.str_itr()) == "['List strain maps error: Project name is invalid.']"

    try:
        project.list_strain_maps("Tutorial Project", "Not a list")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockListStrainMapsError as e:
        assert str(e.str_itr()) == "['List strain maps error: cca_names is not a list.']"

    if project._is_connection_up():
        try:
            project.list_strain_maps("AssemblyTutorial", ["CCA name that doesn't exist"])
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockListStrainMapsError

        try:
            strain_maps = project.list_strain_maps(
                "AssemblyTutorial", ["Main Board", "Power Module"]
            )
            assert len(strain_maps) == 2
            strain_map = strain_maps[0]
            assert strain_map.ccaName == "Main Board"
            assert len(strain_map.strainMaps) == 4
            assert "MainBoardStrainBot.png" in strain_map.strainMaps
            assert "MainBoardStrainTop.png" in strain_map.strainMaps
            assert "MainBoardStrain - Bottom" in strain_map.strainMaps
            assert "MainBoardStrain - Top" in strain_map.strainMaps

            strain_map = strain_maps[1]
            assert strain_map.ccaName == "Power Module"
            assert len(strain_map.strainMaps) == 4
            assert "PowerModuleStrainBot.png" in strain_map.strainMaps
            assert "PowerModuleStrainTop.png" in strain_map.strainMaps
            assert "PowerModuleStrain - Bottom" in strain_map.strainMaps
            assert "PowerModuleStrain - Top" in strain_map.strainMaps
        except SherlockListStrainMapsError as e:
            pytest.fail(str(e.str_itr()))


def helper_test_add_project(project):
    """Test add_project API"""

    try:
        project.add_project("", "", "")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockAddProjectError as e:
        assert str(e) == "Add project error: Project name cannot be blank"

    if project._is_connection_up():
        try:
            project.add_project("Tutorial Project", "", "")
            pytest.fail("No exception raised when creating a duplicate project")
        except Exception as e:
            assert type(e) == SherlockAddProjectError

        try:
            return_code = project.add_project(PROJECT_ADD_NAME, "", "")
            assert return_code == 0
            # Fix issue where api does not finish before returning
            time.sleep(1)
            return PROJECT_ADD_NAME
        except SherlockAddProjectError as e:
            pytest.fail(str(e))


def helper_test_list_thermal_maps(project):
    """Test list_thermal_maps API"""

    expected_cca_name = "Main Board"
    expected_file_names = [
        "Thermal Map.csv",
    ]
    expected_file_types = [
        "Thermal Map (CSV)",
    ]

    try:
        project.list_thermal_maps("")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockListThermalMapsError as e:
        assert str(e.str_itr()) == "['List thermal maps error: Project name is invalid.']"

    try:
        project.list_thermal_maps("Tutorial Project", "Not a list")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockListThermalMapsError as e:
        assert str(e.str_itr()) == "['List thermal maps error: cca_names is not a list.']"

    if project._is_connection_up():
        try:
            project.list_thermal_maps("Tutorial Project", ["CCA name that doesn't exist"])
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockListThermalMapsError

        try:
            thermal_maps = project.list_thermal_maps("Tutorial Project", [expected_cca_name])
            assert len(thermal_maps) == 1
            thermal_map = thermal_maps[0]
            assert thermal_map.ccaName == expected_cca_name
            assert len(thermal_map.thermalMaps) == len(expected_file_names)

            for i, thermal_map_info in enumerate(thermal_map.thermalMaps):
                assert expected_file_names[i] == thermal_map_info.fileName
                assert expected_file_types[i] == thermal_map_info.fileType
        except SherlockListThermalMapsError as e:
            pytest.fail(str(e.str_itr()))

        try:
            thermal_maps = project.list_thermal_maps("Tutorial Project")

            for thermal_map in thermal_maps:
                assert hasattr(thermal_map, "ccaName") and hasattr(thermal_map, "thermalMaps")

                if thermal_map.thermalMaps:
                    for i, thermal_map_info in enumerate(thermal_map.thermalMaps):
                        assert hasattr(thermal_map_info, "fileName") and hasattr(
                            thermal_map_info, "fileType"
                        )

                        if thermal_map.ccaName == expected_cca_name:
                            assert expected_file_names[i] == thermal_map_info.fileName
                            assert expected_file_types[i] == thermal_map_info.fileType

        except SherlockListThermalMapsError as e:
            pytest.fail(str(e.str_itr()))


def helper_test_add_thermal_maps(project):
    """Test add_thermal_maps API"""

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == "['Add thermal maps error: Project name is invalid.']"

    try:
        add_thermal_map_files = []

        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == "['Add thermal maps error: Thermal maps are missing.']"

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "test": "test",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(list(e.str_itr())) == (
            "['Add thermal maps error: "
            f"Number of elements ({str(len(add_thermal_map_files[0]))}) "
            "is wrong for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: File path is required " "for thermal map 0.']"
        )

    try:
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": "",
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: thermal_map_file_properties "
            "is not a list for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                        "test": "test",
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        properties_length = len(add_thermal_map_files[0]["thermal_map_file_properties"][0])
        assert str(list(e.str_itr())) == (
            "['Add thermal maps error: "
            f"Number of elements ({str(properties_length)}) is wrong for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: File name is required for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": "",
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid file type for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": 0,
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid file comment for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": "0",
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid thermal board side for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": "Environmental/1 - Temp Cycle - Min",
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid temperature profiles for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": "Main Board",
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: cca_names is not a list for thermal map 0.']"
        )

    try:
        file_data = ""
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid properties for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count="0",
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid header row count for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format=0,
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid numeric format for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column=0,
            temperature_column="Temp",
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid reference id column for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column=0,
            temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid temperature column for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units=0,
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid temperature units for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds="",
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid board bounds for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units=0,
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid coordinate units for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds="",
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid image bounds for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds="",
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid legend bounds for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation="LegendOrientation.VERTICAL",
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid legend orientation for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature="47.0",
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid maximum temperature for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units=0,
            min_temperature=30.0,
            min_temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid maximum temperature units for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature="30.0",
            min_temperature_units="C",
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid minimum temperature for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units=0,
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps("Tutorial Project", add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockAddThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Add thermal maps error: Invalid minimum temperature units for thermal map 0.']"
        )

    if not project._is_connection_up():
        return

    try:
        missing_project_name = "Name of project that should not exist"
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units=0,
        )
        add_thermal_map_files = [
            {
                "thermal_map_file": "Thermal Map.csv",
                "thermal_map_file_properties": [
                    {
                        "file_name": "Thermal Map.csv",
                        "file_type": ThermalMapsFileType.CSV,
                        "file_comment": "Update",
                        "thermal_board_side": ThermalBoardSide.BOTH,
                        "file_data": file_data,
                        "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                        "cca_names": ["Main Board"],
                    },
                ],
            }
        ]
        project.add_thermal_maps(missing_project_name, add_thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except Exception as e:
        assert type(e) == SherlockAddThermalMapsError


def helper_test_update_thermal_maps(project):
    """Test update_thermal_maps API"""

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]

        project.update_thermal_maps("", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == "['Update thermal maps error: Project name is invalid.']"

    try:
        thermal_map_files = []

        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == "['Update thermal maps error: Thermal maps are missing.']"

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
                "test": "test",
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(list(e.str_itr())) == (
            "['Update thermal maps error: "
            f"Number of elements ({str(len(thermal_map_files[0]))}) "
            "is wrong for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: File name is required for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": "ThermalMapsFileType.CSV",
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid file type for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": 0,
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid file comment for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": "ThermalBoardSide.BOTH",
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid thermal board side for thermal map 0.']"
        )

    try:
        file_data = ""
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid properties for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": "Environmental/1 - Temp Cycle - Min",
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid temperature profiles for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": "Main Board",
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: cca_names is not a list for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count="0",
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid header row count for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format=0,
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid numeric format for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column=0,
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid reference id column for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column=0,
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid temperature column for thermal map 0.']"
        )

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units=0,
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid temperature units for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=(-3.7464, -2.2515),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Image.jpg",
                "file_type": ThermalMapsFileType.IMAGE,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTTOM,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid board bounds for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units=0,
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Image.jpg",
                "file_type": ThermalMapsFileType.IMAGE,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTTOM,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid coordinate units for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=0,
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Image.jpg",
                "file_type": ThermalMapsFileType.IMAGE,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTTOM,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid image bounds for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=0,
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Image.jpg",
                "file_type": ThermalMapsFileType.IMAGE,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTTOM,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid legend bounds for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation="LegendOrientation.VERTICAL",
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Image.jpg",
                "file_type": ThermalMapsFileType.IMAGE,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTTOM,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid legend orientation for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature="47.0",
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Image.jpg",
                "file_type": ThermalMapsFileType.IMAGE,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTTOM,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid maximum temperature for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units=0,
            min_temperature=30.0,
            min_temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Image.jpg",
                "file_type": ThermalMapsFileType.IMAGE,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTTOM,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid maximum temperature units for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature="30.0",
            min_temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Image.jpg",
                "file_type": ThermalMapsFileType.IMAGE,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTTOM,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid minimum temperature for thermal map 0.']"
        )

    try:
        file_data = ImageFile(
            board_bounds=BoardBounds(
                [(-3.7464, -2.2515), (3.7464, -2.141), (3.6159, 2.2395), (-3.5724, 2.2487)]
            ),
            coordinate_units="in",
            image_bounds=ImageBounds(-4.2551, -4.4217, 7.0277, 9.2132),
            legend_bounds=LegendBounds(4.1811, -3.365, 4.7947, 0.3478),
            legend_orientation=LegendOrientation.VERTICAL,
            max_temperature=47.0,
            max_temperature_units="C",
            min_temperature=30.0,
            min_temperature_units=0,
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Image.jpg",
                "file_type": ThermalMapsFileType.IMAGE,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTTOM,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps("Tutorial Project", thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")

    except SherlockUpdateThermalMapsError as e:
        assert str(e.str_itr()) == (
            "['Update thermal maps error: Invalid minimum temperature units for thermal map 0.']"
        )

    if not project._is_connection_up():
        return

    try:
        missing_project_name = "Name of project that should not exist"
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        project.update_thermal_maps(missing_project_name, thermal_map_files)
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert type(e) == SherlockUpdateThermalMapsError

    try:
        file_data = CsvExcelFile(
            header_row_count=0,
            numeric_format="French",
            reference_id_column="RefDes",
            temperature_column="Temp",
            temperature_units="C",
        )
        thermal_map_files = [
            {
                "file_name": "Thermal Map.csv",
                "file_type": ThermalMapsFileType.CSV,
                "file_comment": "Update",
                "thermal_board_side": ThermalBoardSide.BOTH,
                "file_data": file_data,
                "thermal_profiles": ["Environmental/1 - Temp Cycle - Min"],
                "cca_names": ["Main Board"],
            }
        ]
        result = project.update_thermal_maps("Tutorial Project", thermal_map_files)
        assert result == 0
    except SherlockListThermalMapsError as e:
        pytest.fail(str(e.str_itr()))


def helper_test_import_project_zip_archive(project):
    """Test import_project_zip_archive API"""
    try:
        project.import_project_zip_archive("", "Demos", "Tutorial Project.zip")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockImportProjectZipArchiveError as e:
        assert str(e) == "Import zipped project archive error: Project name is invalid."

    try:
        project.import_project_zip_archive("Tutorial Project", "", "Tutorial Project.zip")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockImportProjectZipArchiveError as e:
        assert str(e) == "Import zipped project archive error: Project category is invalid."

    try:
        project.import_project_zip_archive("Tutorial Project", "Demos", "")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockImportProjectZipArchiveError as e:
        assert str(e) == "Import zipped project archive error: Archive file path is invalid."

    if project._is_connection_up():
        try:
            project.import_project_zip_archive(
                "Tutorial Project", "Demos", "Missing Archive File.zip"
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockImportProjectZipArchiveError


def helper_test_import_project_zip_archive_single_mode(project):
    """Test import_project_zip_archive_single_mode API"""
    try:
        project.import_project_zip_archive_single_mode(
            "", "Demos", "Tutorial Project.zip", "New Tutorial Project"
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockImportProjectZipArchiveSingleModeError as e:
        assert str(e) == "Import zipped project archive error: Project name is invalid."

    try:
        project.import_project_zip_archive_single_mode(
            "Tutorial Project", "", "Tutorial Project.zip", "New Tutorial Project"
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockImportProjectZipArchiveSingleModeError as e:
        assert str(e) == "Import zipped project archive error: Project category is invalid."

    try:
        project.import_project_zip_archive_single_mode(
            "Tutorial Project", "Demos", "", "New Tutorial Project"
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockImportProjectZipArchiveSingleModeError as e:
        assert str(e) == "Import zipped project archive error: Archive file path is invalid."

    try:
        project.import_project_zip_archive_single_mode("Tutorial Project", "Demos", "File.zip", "")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockImportProjectZipArchiveSingleModeError as e:
        assert str(e) == (
            "Import zipped project archive error: Directory of the destination file is invalid."
        )

    if project._is_connection_up():
        try:
            project.import_project_zip_archive_single_mode(
                "Tutorial Project", "Demos", "Missing Archive File.zip", "New Tutorial Project"
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockImportProjectZipArchiveSingleModeError


def clean_up_after_add(project, project_name):
    if project_name is not None:
        project.delete_project(project_name)


def helper_test_export_project(project):
    """Test method for export project"""
    try:
        result = project.export_project(
            project_name="",
            export_design_files=True,
            export_result_files=True,
            export_archive_results=True,
            export_user_files=True,
            export_log_files=True,
            export_system_data=True,
            export_file_dir="/Test/Dir",
            export_file_name="ExportedProject",
            overwrite_existing_file=True,
        )
    except SherlockExportProjectError as e:
        assert str(e) == "Export project error : Project name is invalid"

    try:
        result = project.export_project(
            project_name="Tutorial Project",
            export_design_files=True,
            export_result_files=True,
            export_archive_results=True,
            export_user_files=True,
            export_log_files=True,
            export_system_data=True,
            export_file_dir="",
            export_file_name="ExportedProject",
            overwrite_existing_file=True,
        )
    except SherlockExportProjectError as e:
        assert str(e) == "Export project error : Export directory is invalid"

    try:
        result = project.export_project(
            project_name="Tutorial Project",
            export_design_files=True,
            export_result_files=True,
            export_archive_results=True,
            export_user_files=True,
            export_log_files=True,
            export_system_data=True,
            export_file_dir="/Test/Dir",
            export_file_name="",
            overwrite_existing_file=True,
        )
    except SherlockExportProjectError as e:
        assert str(e) == "Export project error : Export file name is invalid"

    if project._is_connection_up():
        try:
            result = project.export_project(
                project_name="",
                export_design_files=True,
                export_result_files=True,
                export_archive_results=True,
                export_user_files=True,
                export_log_files=True,
                export_system_data=True,
                export_file_dir="/Test/Dir",
                export_file_name="ExportedProject",
                overwrite_existing_file=True,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockExportProjectError
        this_dir = os.path.dirname(os.path.realpath(__file__))
        output_file_name = "ExportedProject"
        try:
            result = project.export_project(
                project_name="Tutorial Project",
                export_design_files=True,
                export_result_files=True,
                export_archive_results=True,
                export_user_files=True,
                export_log_files=True,
                export_system_data=True,
                export_file_dir=this_dir,
                export_file_name=output_file_name,
                overwrite_existing_file=True,
            )
            assert result == 0

            # Clean up file
            output_file = os.path.join(this_dir, output_file_name)
            if os.path.exists(output_file):
                os.remove(output_file)
            else:
                pytest.fail("Failed to generate export file.")
        except SherlockExportProjectError as e:
            pytest.fail(str(e))


def helper_test_create_cca_from_modeling_region(project):
    """Test create_cca_from_modeling_region API"""
    try:
        project.create_cca_from_modeling_region(
            "",
            [
                {
                    "cca_name": "Main Board",
                    "modeling_region_id": "MR1",
                    "description": "test MR1",
                    "default_solder_type": "SAC305",
                    "default_stencil_thickness": 10,
                    "default_stencil_thickness_units": "mm",
                    "default_part_temp_rise": 20,
                    "default_part_temp_rise_units": "C",
                    "guess_part_properties_enabled": False,
                    "generate_image_layers": False,
                },
            ],
        )
        assert False
    except SherlockCreateCCAFromModelingRegionError as e:
        assert str(e) == "Create CCA from modeling region error: Project " "name is invalid."

    try:
        project.create_cca_from_modeling_region("Test", "")
        assert False
    except SherlockCreateCCAFromModelingRegionError as e:
        assert (
            str(e) == "Create CCA from modeling region error: CCA "
            "properties argument is invalid."
        )

    try:
        project.create_cca_from_modeling_region("Test", [])
        assert False
    except SherlockCreateCCAFromModelingRegionError as e:
        assert str(e) == "Create CCA from modeling region error: One or more CCAs are required."

    try:
        project.create_cca_from_modeling_region("Test", [""])
        assert False
    except SherlockCreateCCAFromModelingRegionError as e:
        assert (
            str(e) == "Create CCA from modeling region error: CCA properties "
            "are invalid for CCA 0."
        )

    try:
        project.create_cca_from_modeling_region(
            "Test",
            [
                {
                    "modeling_region_id": "MR1",
                    "description": "tests MR1",
                    "default_solder_type": "SAC305",
                    "default_stencil_thickness": 10,
                    "default_stencil_thickness_units": "mm",
                    "default_part_temp_rise": 20,
                    "default_part_temp_rise_units": "C",
                    "guess_part_properties": False,
                    "generate_image_layers": False,
                },
            ],
        )
        assert False
    except SherlockCreateCCAFromModelingRegionError as e:
        assert str(e) == "Create CCA from modeling region error: CCA name is missing for CCA 0."

    try:
        project.create_cca_from_modeling_region(
            "Test",
            [
                {
                    "cca_name": "",
                    "modeling_region_id": "MR1",
                    "description": "Test",
                    "default_solder_type": "SAC305",
                    "default_stencil_thickness": 10,
                    "default_stencil_thickness_units": "mm",
                    "default_part_temp_rise": 20,
                    "default_part_temp_rise_units": "C",
                    "guess_part_properties": False,
                    "generate_image_layers": False,
                },
            ],
        )
        assert False
    except SherlockCreateCCAFromModelingRegionError as e:
        assert str(e) == "Create CCA from modeling region error: CCA name is invalid for CCA 0."

    try:
        project.create_cca_from_modeling_region(
            "Test",
            [
                {
                    "cca_name": "Main Board",
                    "description": "Test",
                    "default_solder_type": "SAC305",
                    "default_stencil_thickness": 10,
                    "default_stencil_thickness_units": "mm",
                    "default_part_temp_rise": 20,
                    "default_part_temp_rise_units": "C",
                    "guess_part_properties": False,
                    "generate_image_layers": False,
                },
            ],
        )
        assert False
    except SherlockCreateCCAFromModelingRegionError as e:
        assert (
            str(e) == "Create CCA from modeling region error: Modeling Region ID"
            " is missing for CCA 0."
        )

    try:
        project.create_cca_from_modeling_region(
            "Test",
            [
                {
                    "cca_name": "Card",
                    "modeling_region_id": "",
                    "description": "Test",
                    "default_solder_type": "SAC305",
                    "default_stencil_thickness": 10,
                    "default_stencil_thickness_units": "mm",
                    "default_part_temp_rise": 20,
                    "default_part_temp_rise_units": "C",
                    "guess_part_properties": False,
                    "generate_image_layers": False,
                },
            ],
        )
        assert False
    except SherlockCreateCCAFromModelingRegionError as e:
        assert (
            str(e) == "Create CCA from modeling region error: Modeling Region ID"
            " is invalid for CCA 0."
        )

    if project._is_connection_up():
        try:
            project.create_cca_from_modeling_region(
                "Tutorial Project",
                [
                    {
                        "cca_name": "Main Board",
                        "modeling_region_id": "MR1",
                        "description": "Test invalid parameter",
                        "default_solder_type": "SAC305",
                        "default_stencil_thickness": 10,
                        "default_stencil_thickness_units": "INVALID",
                        "default_part_temp_rise": 20,
                        "default_part_temp_rise_units": "C",
                        "guess_part_properties": False,
                        "generate_image_layers": False,
                    },
                ],
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockCreateCCAFromModelingRegionError

        try:
            result = project.create_cca_from_modeling_region(
                "ModelingRegion",
                [
                    {
                        "cca_name": "Main Board",
                        "modeling_region_id": "MR1",
                        "description": "Test",
                        "default_solder_type": "SAC305",
                        "default_stencil_thickness": 10,
                        "default_stencil_thickness_units": "mm",
                        "default_part_temp_rise": 20,
                        "default_part_temp_rise_units": "C",
                        "guess_part_properties": False,
                        "generate_image_layers": False,
                    },
                ],
            )
            assert result == 0
        except SherlockCreateCCAFromModelingRegionError as e:
            pytest.fail(str(e))


if __name__ == "__main__":
    test_all()
