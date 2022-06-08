"""Module for launching Sherlock locally or connecting to a local instance with gRPC."""
import errno
import grpc
import os
import socket
import subprocess

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockCannotUsePortError
from ansys.sherlock.core.sherlock import Sherlock

LOCALHOST = "127.0.0.1"
SHERLOCK_DEFAULT_PORT = 9090
EARLIEST_SUPPORTED_VERSION = 211
sherlock_cmd_args = []

def _is_port_available(host=LOCALHOST, port=SHERLOCK_DEFAULT_PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((host, port))
            return True
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                raise SherlockCannotUsePortError(port, "Port is already in use")
            else:
                raise SherlockCannotUsePortError(port, str(e))


def launch_sherlock(host=LOCALHOST, port=SHERLOCK_DEFAULT_PORT, sherlock_cmd_args=""):
    """Launch Sherlock and starts gRPC on the given localhost port.

    Parameters
    ----------
    port : integer, optional
        The socket port number to use for the connection. By default, 9090 is used.

    Examples
    --------
    >>> from ansys.sherlock.launcher import launcher
    >>> launch_sherlock()

    >>> from ansys.sherlock.launcher import launcher
    >>> launch_sherlock(port=9092)

    """
    try:
        _is_port_available(host, port)
    except Exception as e:
        print(str(e))
        return

    try:
        subprocess.Popen([_get_sherlock_exe_path(), "-grpcPort=" + str(port), sherlock_cmd_args])  
    except Exception as e:
            LOG.error(
                "Error encountered while starting or executing Sherlock, error = " + str(e)
            )
    
    try:
        sherlock = connect_grpc_channel()
        return sherlock
    except Exception as e:
        LOG.error(str(e))


def connect_grpc_channel(port=SHERLOCK_DEFAULT_PORT):
    """Create a gRPC connection to the specified port."""

    global SHERLOCK
    channel_param = f'{LOCALHOST}:{port}'
    channel = grpc.insecure_channel(channel_param)
    SHERLOCK = Sherlock(channel)
    return SHERLOCK


def _get_base_ansys():
    supported_installed_versions = {
        env_key: path
        for env_key, path in os.environ.items()
        if env_key.startswith("AWP_ROOT") and os.path.isdir(path)
    }

    for key in sorted(supported_installed_versions, reverse=True):
        ansys_version = _get_ansys_version_from_awp_root(key)
        if ansys_version >= EARLIEST_SUPPORTED_VERSION:
            return supported_installed_versions[key]
    return ""


def _get_ansys_version_from_awp_root(awp_root):
    if awp_root.find("AWP_ROOT") >= 0:
        return int(awp_root.replace("AWP_ROOT", ""))
    else:
        return ""


def _get_sherlock_exe_path():
    ansys_base = _get_base_ansys()
    if not ansys_base:
        return ""
    sherlock_bin = os.path.join(ansys_base, "sherlock", "SherlockClient.exe")
    return sherlock_bin
