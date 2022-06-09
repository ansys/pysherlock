import grpc

from ansys.sherlock.core.project import Project


def test_import_odb_archive(project):
    #   """Test import_odb_archive API"""

    RC1, STR1 = project.import_odb_archive("hello", True, True, True, True)
    assert RC1 == -1
    assert STR1 == "Import ODB error: Invalid project path"

    RC2, STR2 = project.import_odb_archive("hello.tgz", True, True, True, True)
    assert RC2 == -1
    assert STR2 == "Import ODB error: Invalid project path"

    # RC3, STR3 = project.import_odb_archive(
    #     "C:/Program Files/Ansys Inc/v231/sherlock/tutorial/ODB++ Tutorial.tgz",
    #     True,
    #     True,
    #     True,
    #     True,
    # )
    # assert RC3 == 0
    # assert STR3 == ""


def test_all():
    #   """Test all project APIs"""
    #

    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    project = Project(channel)

    test_import_odb_archive(project)


if __name__ == "__main__":
    test_all()
