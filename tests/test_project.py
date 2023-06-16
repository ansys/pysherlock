# © 2023 ANSYS, Inc. All rights reserved

import os
import platform

import grpc

from ansys.sherlock.core.errors import (
    SherlockAddStrainMapsError,
    SherlockDeleteProjectError,
    SherlockGenerateProjectReportError,
    SherlockImportIpc2581Error,
    SherlockImportODBError,
    SherlockListCCAsError,
    SherlockListStrainMapsError,
)
from ansys.sherlock.core.project import Project


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
    helper_test_list_strain_maps(project)


def helper_test_delete_project(project):
    """Test delete_project API"""
    try:
        project.delete_project("")
        assert False
    except SherlockDeleteProjectError as e:
        assert str(e) == "Delete project error: Project name is blank. Specify a project name."

    if project._is_connection_up():
        try:
            missing_project_name = "Name of project that should not exist"
            project.delete_project(missing_project_name)
            assert False
        except Exception as e:
            assert type(e) == SherlockDeleteProjectError


def helper_test_import_odb_archive(project):
    """Test import_odb_archive API"""
    try:
        project.import_odb_archive("", True, True, True, True)
        assert False
    except SherlockImportODBError as e:
        assert str(e) == "Import ODB error: Archive path is required."

    if project._is_connection_up():
        try:
            missing_archive_file = "Missing ODB.tgz"
            project.import_odb_archive(missing_archive_file, True, True, True, True)
            assert False
        except Exception as e:
            assert type(e) == SherlockImportODBError


def helper_test_import_ipc2581_archive(project):
    """Test import_ipc2581_archive API"""
    try:
        project.import_ipc2581_archive("", True, True)
        assert False
    except SherlockImportIpc2581Error as e:
        assert str(e) == "Import IPC2581 error: Archive file path is required."

    if project._is_connection_up():
        try:
            project.import_ipc2581_archive("Missing Archive File.zip", True, True)
            assert False
        except Exception as e:
            assert type(e) == SherlockImportIpc2581Error


def helper_test_generate_project_report(project):
    """Test generate_project_report API."""
    try:
        project.generate_project_report("", "John Doe", "Generic Co.", "C:/report.pdf")
        assert False
    except SherlockGenerateProjectReportError as e:
        assert str(e) == "Generate project report error: Project name is invalid."

    try:
        project.generate_project_report("Test", "", "Generic Co.", "C:/report.pdf")
        assert False
    except SherlockGenerateProjectReportError as e:
        assert str(e) == "Generate project report error: Author name is invalid."

    try:
        project.generate_project_report("Test", "John Doe", "", "C:/report.pdf")
        assert False
    except SherlockGenerateProjectReportError as e:
        assert str(e) == "Generate project report error: Company name is invalid."

    try:
        project.generate_project_report("Test", "John Doe", "Generic Co.", "")
        assert False
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
            assert False
        except Exception as e:
            assert type(e) == SherlockGenerateProjectReportError


def helper_test_list_ccas(project):
    """Test list_ccas API"""

    try:
        project.list_ccas("")
        assert False
    except SherlockListCCAsError as e:
        assert e.str_itr()[0] == "List CCAs error: Project name is invalid."

    try:
        project.list_ccas("Tutorial Project", "CCA names that is not a list")
        assert False
    except SherlockListCCAsError as e:
        assert e.str_itr()[0] == "List CCAs error: cca_names is not a list."

    if project._is_connection_up():
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

        try:
            project.list_ccas("Project that doesn't exist")
            assert False
        except Exception as e:
            assert type(e) == SherlockListCCAsError


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
        assert False
    except SherlockAddStrainMapsError as e:
        assert e.str_itr()[0] == "Add strain maps error: Project name is invalid."

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
        assert False
    except SherlockAddStrainMapsError as e:
        assert e.str_itr()[0] == "Add strain maps error: Path is required for strain map 0."

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
        assert False
    except SherlockAddStrainMapsError as e:
        assert (
            e.str_itr()[0] == "Add strain maps error: "
            "Header row count is required for strain map 0."
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
        assert False
    except SherlockAddStrainMapsError as e:
        assert (
            e.str_itr()[0] == "Add strain maps error: "
            "Header row count must be greater than or equal "
            "to 0 for strain map 0."
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
        assert False
    except SherlockAddStrainMapsError as e:
        assert (
            e.str_itr()[0] == "Add strain maps error: Reference ID column is required "
            "for strain map 0."
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
        assert False
    except SherlockAddStrainMapsError as e:
        assert (
            e.str_itr()[0] == "Add strain maps error: Strain column is required "
            "for strain map 0."
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
        assert False
    except SherlockAddStrainMapsError as e:
        assert (
            e.str_itr()[0] == "Add strain maps error: Strain units are required for "
            "strain map 0."
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
        assert False
    except SherlockAddStrainMapsError as e:
        assert (
            e.str_itr()[0] == 'Add strain maps error: Strain units "BAD" '
            "are invalid for strain map 0."
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
        assert False
    except SherlockAddStrainMapsError as e:
        assert e.str_itr()[0] == "Add strain maps error: cca_names is not a list for strain map 0."

    if project._is_connection_up():
        # project.add_strain_maps(
        #     "Tutorial Project",
        #     [
        #         (
        #             "C:/Users/pwalters/Source/Sherlock/dist/tutorial/StrainMaps/StrainMap.csv",
        #             "File comment",
        #             0,
        #             "SolidID",
        #             "PCB Strain",
        #             "µε",
        #             ["Main Board"],
        #         )
        #     ],
        # )

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
            assert False
        except Exception as e:
            assert type(e) == SherlockAddStrainMapsError


def helper_test_list_strain_maps(project):
    """Test list_strain_maps API"""

    try:
        project.list_strain_maps("")
        assert False
    except SherlockListStrainMapsError as e:
        assert e.str_itr()[0] == "List strain maps error: Project name is invalid."

    try:
        project.list_strain_maps("Tutorial Project", "Not a list")
        assert False
    except SherlockListStrainMapsError as e:
        assert e.str_itr()[0] == "List strain maps error: cca_names is not a list."

    if project._is_connection_up():
        strain_maps = project.list_strain_maps("AssemblyTutorial", ["Main Board", "Power Module"])
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

        try:
            project.list_strain_maps("AssemblyTutorial", ["CCA name that doesn't exist"])
            assert False
        except Exception as e:
            assert type(e) == SherlockListStrainMapsError


if __name__ == "__main__":
    test_all()
