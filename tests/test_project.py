from ansys.sherlock import project


def test_import_odb_archive():
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


def test_delete_project():
    #   """Test delete_project API"""
    rc1, str1 = project.delete_project("")
    assert rc1 == -1
    assert str1 == "Delete project error: Invalid Blank Project Name"

    # RC2, STR2 = project.delete_project("test")
    # assert RC2 == -1
    # assert STR2 == "Delete project error: Cannot find project: {projectName} test"


def test_all():
    #   """Test all project APIs"""
    #
    #   REQUIRES: Sherlock server must already be opened to port 9090
    test_delete_project()
    test_import_odb_archive()


if __name__ == "__main__":
    test_all()
