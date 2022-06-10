import grpc

from ansys.sherlock.core.errors import SherlockDeleteProjectError, SherlockImportODBError
from ansys.sherlock.core.project import Project


def test_import_odb_archive(project):
    #   """Test import_odb_archive API"""
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

    # try:
    #     project.import_odb_archive(
    #         "C:/Program Files/Ansys Inc/v231/sherlock/tutorial/ODB++ Tutorial.tgz",
    #         True,
    #         True,
    #         True,
    #         True,
    #     )
    # except SherlockImportODBError as e:
    #     assert False


def test_delete_project(project):
    #   """Test delete_project API"""
    try:
        project.delete_project("")
        assert False
    except SherlockDeleteProjectError as e:
        assert str(e) == "Delete project error: Invalid Blank Project Name"

    # try:
    #     project.delete_project("Invalid")
    #     assert False
    # except SherlockDeleteProjectError as e:
    #     assert str(e) == "Delete project error: Cannot find project: {projectName} Invalid"


def test_all():
    #   """Test all project APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    project = Project(channel)

    test_delete_project(project)
    test_import_odb_archive(project)


if __name__ == "__main__":
    test_all()
