# © 2023 ANSYS, Inc. All rights reserved

"""Module for launching Sherlock locally or connecting to a local instance with gRPC."""
import errno
import os
import socket
import subprocess
import time

import grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockCannotUsePortError, SherlockConnectionError
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

            raise SherlockCannotUsePortError(port, str(e))


def launch_sherlock(
    host=LOCALHOST, port=SHERLOCK_DEFAULT_PORT, single_project_path="", sherlock_cmd_args=""
):
    r"""Launch Sherlock and start gRPC on a given host and port.

    Parameters
    ----------
    host : str, optional
        IP address to start gRPC on. The default is ``"127.0.0.1"``, which
        is the IP address for the local host.
    port : int, optional
        Port number for the connection.
    single_project_path : str, optional
        Path to the Sherlock project if invoking Sherlock in the single-project mode.
    sherlock_cmd_args : str, optional
        Additional command arguments for launching Sherlock.

    Returns
    -------
    Sherlock
        The instance of sherlock.

    Examples
    --------
    >>> from ansys.sherlock.core import launcher
    >>> launch_sherlock()

    >>> from ansys.sherlock.core import launcher
    >>> launch_sherlock(port=9092)

    >>> from ansys.sherlock.core import launcher
    >>> project = "C:\\Default Projects Directory\\ODB++ Tutorial"
    >>> launch_sherlock(port=9092, single_project_path=project)

    """
    try:
        _is_port_available(host, port)
    except Exception as e:
        print(str(e))
        return None

    try:
        args = _get_sherlock_exe_path() + " -grpcPort=" + str(port)
        if single_project_path != "":
            args = f'{args} -singleProject "{single_project_path}"'
        if sherlock_cmd_args != "":
            args = f"{args} {sherlock_cmd_args}"
        subprocess.Popen(args)
    except Exception as e:
        LOG.error("Error encountered while starting or executing Sherlock, error = %s" + str(e))

    try:
        sherlock = connect_grpc_channel(port)

        # Check that the gRPC connection is up (timeout after 3 minutes).
        count = 0
        while sherlock.common.check() is False and count < 90:
            time.sleep(2)
            count = count + 1

        if sherlock.common.check() is False:
            raise SherlockConnectionError(message="Error starting gRPC service")

        # Check that the Sherlock client has finished loading (timeout after 5 minutes).
        count = 0
        while sherlock.common.is_sherlock_client_loading() is False and count < 150:
            time.sleep(2)
            count = count + 1

        return sherlock
    except Exception as e:
        LOG.error(str(e))


def connect_grpc_channel(port=SHERLOCK_DEFAULT_PORT):
    """Create a gRPC connection to a specified port and return the ``Sherlock`` connection object.

    The ``Sherlock`` connection object is used to invoke the APIs from their respective services.
    This can be used to connect to the Sherlock instance that is already running with the specified
    port.

    Parameters
    ----------
    port : int, optional
        Port number for the connection.

    Returns
    -------
    Sherlock
        The instance of sherlock.
    """
    channel_param = f"{LOCALHOST}:{port}"
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

    return ""


def _get_sherlock_exe_path():
    ansys_base = _get_base_ansys()
    if not ansys_base:
        return ""
    sherlock_bin = os.path.join(ansys_base, "sherlock", "SherlockClient.exe")
    return sherlock_bin
