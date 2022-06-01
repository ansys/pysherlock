from ansys.sherlock import project
from ansys.sherlock.launcher import launcher


def open_connection(port=9090):
    #   """Sets up the connection between client and Sherlock
    #
    #   Paramaters
    #   ----------
    #   port : int, optional
    #       The port number for the connection
    #   """
    launcher.launch_sherlock(port=port)


def test_delete_project():
    #   """Test delete_project API"""
    RC1, STR1 = project.delete_project("")
    assert RC1 == -1
    assert STR1 == "Delete project error: Invalid Blank Project Name"

    RC2, STR2 = project.delete_project("test")
    assert RC2 == -1
    assert STR2 == "Delete project error: Cannot find project: {projectName} test"


def test_all():
    #   """Test all project APIs"""
    #
    #   REQUIRES: Sherlock server must already be opened to port 9090
    # open_connection()
    test_delete_project()


if __name__ == "__main__":
    test_all()
