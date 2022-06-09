import grpc

from ansys.sherlock.core.project import Project


def test_import_odb_archive(project):
    #   """Test import_odb_archive API"""
    rc1, str1 = project.import_odb_archive("hello", True, True, True, True)
    assert rc1 == -1
    assert str1 == "Import ODB error: Invalid file path"

    rc2, str2 = project.import_odb_archive("hello.tgz", True, True, True, True)
    assert rc2 == -1
    assert str2 == "Import ODB error: Invalid file path"

    # RC3, STR3 = project.import_odb_archive(
    #     "C:/Program Files/Ansys Inc/v231/sherlock/tutorial/ODB++ Tutorial.tgz",
    #     True,
    #     True,
    #     True,
    #     True,
    # )
    # assert RC3 == 0
    # assert STR3 == ""


def test_delete_project(project):
    #   """Test delete_project API"""
    rc1, str1 = project.delete_project("")
    assert rc1 == -1
    assert str1 == "Delete project error: Invalid Blank Project Name"

    # rc2, str2 = project.delete_project("Invalid")
    # assert rc2 == -1
    # assert str2 == "Delete project error: Cannot find project: {projectName} Invalid"


def test_all():
    #   """Test all project APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    project = Project(channel)

    test_delete_project(project)
    test_import_odb_archive(project)


if __name__ == "__main__":
    test_all()
