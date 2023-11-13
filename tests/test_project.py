# © 2023 ANSYS, Inc. All rights reserved

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
    SherlockDeleteProjectError,
    SherlockGenerateProjectReportError,
    SherlockImportIpc2581Error,
    SherlockImportODBError,
    SherlockListCCAsError,
    SherlockListStrainMapsError,
    SherlockListThermalMapsError,
)
from ansys.sherlock.core.project import Project

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
    helper_test_generate_project_report(project)
    helper_test_list_ccas(project)
    helper_test_add_cca(project)
    helper_test_list_strain_maps(project)
    helper_test_list_thermal_maps(project)
    project_name = None
    try:
        project_name = helper_test_add_project(project)
    finally:
        clean_up_after_add(project, project_name)


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
        "Thermal Map.xlsx",
        "Thermal Map.tmap",
        "Thermal Image.jpg",
        "Thermal Map.csv",
    ]
    expected_file_types = [
        "Thermal Map (Excel)",
        "Icepak Thermal Map (TMAP)",
        "Thermal Map (Image)",
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
            project.list_thermal_maps("AssemblyTutorial", ["CCA name that doesn't exist"])
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


def clean_up_after_add(project, project_name):
    if project_name is not None:
        project.delete_project(project_name)


if __name__ == "__main__":
    test_all()
