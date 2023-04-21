# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

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


def helper_test_import_odb_archive(project):
    """Test import_odb_archive API"""
    try:
        project.import_odb_archive("hello", True, True, True, True)
        assert False
    except SherlockImportODBError as e:
        assert str(e) == "Import ODB error: File path is invalid."

    try:
        project.import_odb_archive("hello.tgz", True, True, True, True)
        assert False
    except SherlockImportODBError as e:
        assert str(e) == "Import ODB error: File path is invalid."


def helper_test_import_ipc2581_archive(project):
    """Test import_ipc2581_archive API"""
    try:
        project.import_ipc2581_archive("Hello", True, True)
        assert False
    except SherlockImportIpc2581Error as e:
        assert str(e) == "Import IPC2581 error: File path is invalid."

    try:
        project.import_ipc2581_archive("Hello.zip", True, True)
        assert False
    except SherlockImportIpc2581Error as e:
        assert str(e) == "Import IPC2581 error: File path is invalid."


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
        project.generate_project_report("Test", "John Doe", "Generic Co.", "C:/Invalid/Invalid")
        assert False
    except SherlockGenerateProjectReportError as e:
        assert str(e) == "Generate project report error: Export file directory does not exist."


def helper_test_list_ccas(project):
    """Test list_ccas API"""

    try:
        project.list_ccas("")
        assert False
    except SherlockListCCAsError as e:
        assert str(e) == "List CCAs error: Project name is invalid."

    try:
        project.list_ccas("Tutorial Project", "Not a list")
        assert False
    except SherlockListCCAsError as e:
        assert str(e) == "List CCAs error: cca_names is not a list."


def helper_test_add_strain_maps(project):
    """Test add_strain_maps API"""

    try:
        project.add_strain_maps(
            "",
            [(
                "StrainMap.csv",
                "",
                0,
                "SolidID",
                "PCB Strain",
                "µε",
                ["Main Board"],
            )],
        )
        assert False
    except SherlockAddStrainMapsError as e:
        assert e.str_itr()[0] == "Add strain maps error: Project name is invalid."

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [(
                "",
                "",
                0,
                "SolidID",
                "PCB Strain",
                "µε",
                ["Main Board"],
            )],
        )
        assert False
    except SherlockAddStrainMapsError as e:
        assert e.str_itr()[0] == "Add strain maps error: File path is required for strain map 0."

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [(
                "StrainMap.csv",
                "",
                "0",  # Not an integer
                "SolidID",
                "PCB Strain",
                "µε",
                ["Main Board"],
            )],
        )
        assert False
    except SherlockAddStrainMapsError as e:
        assert e.str_itr()[0] == "Add strain maps error: " \
                                 "Header row count is required for strain map 0."

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [(
                "StrainMap.csv",
                "",
                -1,
                "SolidID",
                "PCB Strain",
                "µε",
                ["Main Board"],
            )],
        )
        assert False
    except SherlockAddStrainMapsError as e:
        assert e.str_itr()[0] == "Add strain maps error: " \
                                 "Header row count must be greater than or equal " \
                                 "to 0 for strain map 0."

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [(
                "StrainMap.csv",
                "",
                0,
                "",
                "PCB Strain",
                "µε",
                ["Main Board"],
            )],
        )
        assert False
    except SherlockAddStrainMapsError as e:
        assert e.str_itr()[0] == "Add strain maps error: Reference ID column is required " \
                                 "for strain map 0."

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [(
                "StrainMap.csv",
                "",
                0,
                "SolidID",
                "",
                "µε",
                ["Main Board"],
            )],
        )
        assert False
    except SherlockAddStrainMapsError as e:
        assert e.str_itr()[0] == "Add strain maps error: Strain column is required " \
                                 "for strain map 0."

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [(
                "StrainMap.csv",
                "",
                0,
                "SolidID",
                "Strain",
                "",
                ["Main Board"],
            )],
        )
        assert False
    except SherlockAddStrainMapsError as e:
        assert e.str_itr()[0] == "Add strain maps error: Strain units are required for " \
                                 "strain map 0."

    try:
        project.add_strain_maps(
            "Tutorial Project",
            [(
                "StrainMap.csv",
                "",
                0,
                "SolidID",
                "Strain",
                "BAD",
                ["Main Board"],
            )],
        )
        assert False
    except SherlockAddStrainMapsError as e:
        assert e.str_itr()[0] == "Add strain maps error: Strain units 'BAD' " \
                                 "are invalid for strain map 0."

    if project._is_connection_up():
        try:
            project.add_strain_maps(
                "Tutorial Project",
                [(
                    "C:/Users/pwalters/Source/Sherlock/dist/tutorial/StrainMaps/StrainMap.csv",
                    "",
                    0,
                    "SolidID",
                    "PCB Strain",
                    "µε",
                    ["Main Board"],
                )],
            )
            assert True
        except SherlockAddStrainMapsError as e:
            print(str(e))
            assert False


def helper_test_list_strain_maps(project):
    """Test list_strain_maps API"""

    try:
        project.list_strain_maps("")
        assert False
    except SherlockListStrainMapsError as e:
        assert str(e) == "List strain maps error: Project name is invalid."

    try:
        project.list_strain_maps("Tutorial Project", "Not a list")
        assert False
    except SherlockListStrainMapsError as e:
        assert str(e) == "List strain maps error: cca_names is not a list."


if __name__ == "__main__":
    test_all()
