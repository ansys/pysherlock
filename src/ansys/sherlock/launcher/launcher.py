"""Module for launching Sherlock locally or connecting to a local instance with gRPC."""
import errno
import os
import socket
from subprocess import check_output

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockCannotUsePortError

LOCALHOST = "127.0.0.1"
SHERLOCK_DEFAULT_PORT = 9090
EARLIEST_SUPPORTED_VERSION = 211
sherlock_cmd_args = []


def is_port_available(host=LOCALHOST, port=SHERLOCK_DEFAULT_PORT):
    #    """Checks if a port on the host is available
    #
    #    Parameters
    #    ----------
    #    host : str, required
    #        The hostname in internet domain notation or an IPv4 address
    #    port : integer, required
    #        The socket port number to use for the connection
    #    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((host, port))
            return True
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                raise SherlockCannotUsePortError(port, "Port is already in use")
            else:
                raise SherlockCannotUsePortError(port, str(e))


def launch_sherlock(*sherlock_args, host=LOCALHOST, port=SHERLOCK_DEFAULT_PORT):
    """Launches Sherlock and starts gRPC on the given port.

    Parameters
    ----------
    sherlock_args : list, optional
        A list of optional sherlock command arguments, i.e. -singleProject
    host : str, required
        The hostname in internet domain notation or an IPv4 address
    port : integer, required
        The socket port number to use for the connection

    Examples
    --------
    >>> from ansys.sherlock.launcher import launcher
    >>> launch_sherlock()

    >>> from ansys.sherlock.launcher import launcher
    >>> launch_sherlock(port=9092)

    """
    try:
        is_port_available(host, port)
    except Exception as e:
        print(str(e))
        return

    try:
        check_output([get_sherlock_exe_path(), "-grpcPort=" + str(port)] + list(sherlock_args),
                     shell=True)
    except Exception as process_return:
        if process_return.returncode == 1:
            LOG.debug("Sherlock has exited successfully.")
        else:
            LOG.error("Error encountered while starting or executing Sherlock, error = ",
                      process_return.returncode,
                      process_return.output)


def get_base_ansys():
    #    """Return the latest supported and installed ANSYS path in Windows
    #    For example: 'C:\\Program Files\\ANSYS INC\\v222'
    #    Returns
    #    -------
    #    ansys_path : str
    #    """

    supported_installed_versions = {
        env_key: path for env_key, path in os.environ.items() if env_key.startswith("AWP_ROOT") and
                                                                 os.path.isdir(path)
    }

    for key in sorted(supported_installed_versions, reverse=True):
        ansys_version = get_ansys_version_from_awp_root(key)
        if ansys_version >= EARLIEST_SUPPORTED_VERSION:
            return supported_installed_versions[key]
    return ""


def get_ansys_version_from_awp_root(awp_root):
    #    """Returns the Ansys version (ie 212, 221) given an AWP_ROOT environment variable name
    #    Parameter
    #    ---------
    #    awp_root : str
    #        The AWP_ROOT* environment variable name
    #
    #    Returns
    #    -------
    #    ansys_version : int
    #    """

    if awp_root.find("AWP_ROOT") >= 0:
        return int(awp_root.replace("AWP_ROOT", ""))
    else:
        return ""


def get_sherlock_exe_path():
    #    """Returns the latest SherlockClient.exe path
    #    Returns
    #    -------
    #    sherlock_path : str
    #    """
    ansys_base = get_base_ansys()
    if not ansys_base:
        return ""
    sherlock_bin = os.path.join(ansys_base, "sherlock", "SherlockClient.exe")
    return sherlock_bin
