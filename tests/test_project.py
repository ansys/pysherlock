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
    #
    #   Must evaluate results by looking at logging files, not automated
    #   Refer to test_project.txt in tests
    project.delete_project()
    project.delete_project("")
    project.delete_project("test project")


def test_all():
    #   """Test all project APIs"""
    #
    #   REQUIRES: Sherlock server must already be opened to port 9090
    test_delete_project()

if __name__ == "__main__":
    test_all()