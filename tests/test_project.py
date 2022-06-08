import time

from ansys.sherlock.core.launcher import launch_sherlock


def test_delete_project(sherlock):
    #   """Test delete_project API"""
    rc1, str1 = sherlock.project.delete_project("")
    assert rc1 == -1
    assert str1 == "Delete project error: Invalid Blank Project Name"

    # RC2, STR2 = project.delete_project("test")
    # assert RC2 == -1
    # assert STR2 == "Delete project error: Cannot find project: {projectName} test"


def test_all():
    #   """Test all project APIs"""
    #
    #   REQUIRED: Sherlock needs to start fresh
    sherlock = launch_sherlock()
    time.sleep(15)

    test_delete_project(sherlock)

    sherlock.common.exit(close_sherlock_client=True)


if __name__ == "__main__":
    test_all()
