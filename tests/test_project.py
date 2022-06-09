import time

from ansys.sherlock.core.launcher import launch_sherlock


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

    sherlock = launch_sherlock()
    time.sleep(15)

    project = sherlock.project

    test_import_odb_archive(project)

    sherlock.common.exit(close_sherlock_client=True)


if __name__ == "__main__":
    test_all()
