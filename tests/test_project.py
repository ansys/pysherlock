import grpc

from ansys.sherlock.core.errors import (
    SherlockDeleteProjectError,
    SherlockGenerateProjectReportError,
    SherlockImportIpc2581Error,
    SherlockImportODBError,
)
from ansys.sherlock.core.project import Project


def test_all():
    """Test all project APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    project = Project(channel)

    helper_test_delete_project(project)
    helper_test_import_odb_archive(project)
    helper_test_import_ipc2581_archive(project)
    helper_test_generate_project_report(project)


def helper_test_delete_project(project):
    """Test delete_project API"""
    try:
        project.delete_project("")
        assert False
    except SherlockDeleteProjectError as e:
        assert str(e) == "Delete project error: Invalid Blank Project Name"


def helper_test_import_odb_archive(project):
    """Test import_odb_archive API"""
    try:
        project.import_odb_archive("hello", True, True, True, True)
        assert False
    except SherlockImportODBError as e:
        assert str(e) == "Import ODB error: Invalid file path"

    try:
        project.import_odb_archive("hello.tgz", True, True, True, True)
        assert False
    except SherlockImportODBError as e:
        assert str(e) == "Import ODB error: Invalid file path"


def helper_test_import_ipc2581_archive(project):
    """Test import_ipc2581_archive API"""
    try:
        project.import_ipc2581_archive("Hello", True, True)
        assert False
    except SherlockImportIpc2581Error as e:
        assert str(e) == "Import IPC2581 error: Invalid file path"

    try:
        project.import_ipc2581_archive("Hello.zip", True, True)
        assert False
    except SherlockImportIpc2581Error as e:
        assert str(e) == "Import IPC2581 error: Invalid file path"


def helper_test_generate_project_report(project):
    """Test generate_project_report API."""
    try:
        project.generate_project_report("", "John Doe", "Generic Co.", "C:/report.pdf")
        assert False
    except SherlockGenerateProjectReportError as e:
        assert str(e) == "Generate project report error: Invalid project name"

    try:
        project.generate_project_report("Test", "", "Generic Co.", "C:/report.pdf")
        assert False
    except SherlockGenerateProjectReportError as e:
        assert str(e) == "Generate project report error: Invalid author name"

    try:
        project.generate_project_report("Test", "John Doe", "", "C:/report.pdf")
        assert False
    except SherlockGenerateProjectReportError as e:
        assert str(e) == "Generate project report error: Invalid company name"

    try:
        project.generate_project_report("Test", "John Doe", "Generic Co.", "Invalid")
        assert False
    except SherlockGenerateProjectReportError as e:
        assert str(e) == "Generate project report error: Invalid file path"


if __name__ == "__main__":
    test_all()
