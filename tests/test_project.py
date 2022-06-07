from ansys.sherlock import project


def test_delete_project():
    #   """Test delete_project API"""
    rc1, str1 = project.delete_project("")
    assert rc1 == -1
    assert str1 == "Delete project error: Invalid Blank Project Name"

    # RC2, STR2 = project.delete_project("test")
    # assert RC2 == -1
    # assert STR2 == "Delete project error: Cannot find project: {projectName} test"


def test_import_ipc2581_archive():
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
    #
    #   REQUIRES: Sherlock server must already be opened to port 9090
    test_delete_project()
    test_import_ipc2581_archive()


if __name__ == "__main__":
    test_all()
