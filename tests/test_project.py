import grpc

from ansys.sherlock.core.project import Project


def test_import_ipc2581_archive(project):
    #   """Test import_ipc2581_archive API"""
    rc1, str1 = project.import_ipc2581_archive("Hello", True, True)
    assert rc1 == -1
    assert str1 == "Import IPC2581 error: Invalid file path"

    rc2, str2 = project.import_ipc2581_archive("Hello.zip", True, True)
    assert rc2 == -1
    assert str2 == "Import IPC2581 error: Invalid file path"

    # rc3, str3 = project.import_ipc2581_archive(
    #   "C:/Program Files/ANSYS Inc/v231/sherlock/tutorial/Ad Hoc Tutorial.zip",
    #   True, True
    # )
    # assert rc3 == -1
    # assert str3 == "Import IPC2581 error: Timeout waiting for IPC-2581 Import"


def test_all():
    #   """Test all project APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    project = Project(channel)

    test_import_ipc2581_archive(project)


if __name__ == "__main__":
    test_all()
