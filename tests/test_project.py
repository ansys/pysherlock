from ansys.sherlock import project


def test_import_odb_archive():
    #   """Test delete_project API"""
    #
    #   Must evaluate results by looking at logging files, not automated
    #   Refer to test_project.txt in tests
    # TODO: Actually clean up these testcases
    RC1, STR1 = project.import_odb_archive("")
    assert RC1 == -1
    assert STR1 == "Delete project error: Invalid Blank Project Name"

    # RC2, STR2 = project.delete_project("test project")
    # assert(RC2 == -1)
    # assert(STR2 == "Delete project error: Cannot find project: {projectName} test project")
