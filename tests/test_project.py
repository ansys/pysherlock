from ansys.sherlock import project


def test_import_odb_archive():
    #   """Test delete_project API"""

    RC1, STR1 = project.import_odb_archive("hello", True, True, True, True)
    assert RC1 == -1
    assert STR1 == "Import ODB Error: Archive file name must end with [.tgz, .tar.gz, .tar]"

    RC2, STR2 = project.import_odb_archive("hello.tgz", True, True, True, True)
    assert RC2 == -1
    assert STR2 == "Import ODB Error: Invalid ODB++ archive file path: hello.tgz"

    RC3, STR3 = project.import_odb_archive(
        "C:/Program Files/Ansys Inc/v231/sherlock/tutorial/ODB++ Tutorial.tgz",
        True,
        True,
        True,
        True,
    )
    assert RC3 == 0
    assert STR3 == ""


if __name__ == "__main__":
    test_import_odb_archive()
