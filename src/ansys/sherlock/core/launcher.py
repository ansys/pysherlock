# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module for launching Sherlock locally or connecting to a local instance with gRPC."""
import errno
import os
import shlex
import socket
import subprocess
from typing import Optional
import warnings

import grpc

from ansys.sherlock.core import LOG
from ansys.sherlock.core.common import Common
from ansys.sherlock.core.errors import SherlockCannotUsePortError, SherlockConnectionError
from ansys.sherlock.core.sherlock import Sherlock
from ansys.sherlock.core.utils.cyberchannel import create_channel
from ansys.sherlock.core.utils.version_check import _EARLIEST_SUPPORTED_VERSION

ANSYS_GRPC_CERTIFICATES = "ANSYS_GRPC_CERTIFICATES"
LOCALHOST = "127.0.0.1"
SHERLOCK_DEFAULT_PORT = 9090
SHERLOCK_UDS_SERVICE = "sherlock-grpc"
DEFAULT_CONNECT_TIMEOUT = 120
sherlock_cmd_args = []


def _is_port_available(host: str = LOCALHOST, port: int = SHERLOCK_DEFAULT_PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind((host, port))
            return True
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                raise SherlockCannotUsePortError(port, "Port is already in use")

            raise SherlockCannotUsePortError(port, str(e))


def launch_sherlock(
    host: str = LOCALHOST,
    port: int = SHERLOCK_DEFAULT_PORT,
    single_project_path: str = "",
    sherlock_command_args: str = "",
    year: Optional[int] = None,
    release_number: Optional[int] = None,
    transport_mode: str = "mtls",
    certs_dir: str = None,
    uds_dir: str = None,
    uds_id: str = None,
) -> Sherlock:
    r"""Launch Sherlock and start gRPC on a given host and port. Wait up to two minutes to connect.

    .. deprecated:: 2025 R2

    Use :func:`launch` or :func:`launch_and_connect` instead.

    Parameters
    ----------
    host: str, optional
        IP address to start gRPC on. The default is ``"127.0.0.1"``, which
        is the IP address for the local host.
    port: int, optional
        Port number for the connection.
    single_project_path : str, optional
        Path to the Sherlock project if invoking Sherlock in the single-project mode.
    sherlock_command_args : str, optional
        Additional command arguments for launching Sherlock.
    year: int, optional
        4-digit year of the Sherlock release to launch. If not provided,
        the latest installed version of Sherlock will be launched.
    release_number: int, optional
        Release number of Sherlock to launch. If not provided,
        the latest installed version of Sherlock will be launched.

    Returns
    -------
    Sherlock
        The instance of sherlock.

    Examples
    --------
    >>> from ansys.sherlock.core import launcher
    >>> launcher.launch_sherlock()

    >>> from ansys.sherlock.core import launcher
    >>> launcher.launch_sherlock(port=9092, year=2024, release_number=1)

    >>> from ansys.sherlock.core import launcher
    >>> project = "C:\\Default Projects Directory\\ODB++ Tutorial"
    >>> launcher.launch_sherlock(port=9092, single_project_path=project)

    """
    warnings.warn(
        "launch_sherlock() is deprecated and will be removed in a future release. "
        "Use launch() instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    sherlock, install_dir = launch_and_connect(
        host,
        port,
        single_project_path,
        sherlock_command_args,
        year,
        release_number,
        transport_mode=transport_mode,
        certs_dir=certs_dir,
        uds_dir=uds_dir,
        uds_id=uds_id,
    )
    return sherlock


def launch(
    host: str = LOCALHOST,
    port: int = SHERLOCK_DEFAULT_PORT,
    single_project_path: str = "",
    sherlock_command_args: str = "",
    year: Optional[int] = None,
    release_number: Optional[int] = None,
    transport_mode: str = "mtls",
    certs_dir: str = None,
    uds_dir: str = None,
    uds_id: str = None,
) -> str:
    r"""Launch Sherlock using the specified host and port for the gRPC connection.

    Available Since: 2025R2

    Parameters
    ----------
    host: str, optional
        IP address to start gRPC on.
        The default is ``"127.0.0.1"``, which is the IP address for the local host.
    port: int, optional
        Port number for the connection.
    single_project_path : str, optional
        Path to the Sherlock project if invoking Sherlock in the single-project mode.
    sherlock_command_args : str, optional
        Additional command arguments for launching Sherlock.
    year: int, optional
        4-digit year of the Sherlock release to launch. If not provided,
        the latest installed version of Sherlock will be launched.
    release_number: int, optional
        Release number of Sherlock to launch. If not provided,
        the latest installed version of Sherlock will be launched.
    transport_mode: str, optional
        gRPC transport mode. Supported values are "insecure", "mtls", "wnua", and "uds".
        Default is "mtls".
    certs_dir: str, optional
        Directory containing the mTLS certificates. Default is "./certs".
    uds_dir: str, optional
        Directory for the UDS socket file. Default is "$HOME/.conn".
    uds_id: str, optional
        Identifier for the UDS socket file name. Default is no identifier.

    Returns
    -------
    str
        Path to the Sherlock installation directory.

    Examples
    --------
    >>> from ansys.sherlock.core import launcher
    >>> project = "C:\\Default Projects Directory\\ODB++ Tutorial"
    >>> ansys_install_path = launcher.launch(
    >>>     port=9092, single_project_path=project, year=2024, release_number=2)
    """
    try:
        _is_port_available(host, port)
    except Exception as e:
        LOG.error(str(e))
        raise e

    try:
        sherlock_launch_cmd, _server_version, ansys_install_path = _get_sherlock_exe_path(
            year=year, release_number=release_number
        )
        args = [sherlock_launch_cmd]

        # Add gRPC options
        if transport_mode in ["insecure", "mtls", "wnua"]:
            args.append(f"-grpcHost={host}")
            args.append(f"-grpcPort={port}")
        args.append(f"--transport-mode={transport_mode}")
        if transport_mode == "mtls":
            if not certs_dir:
                certs_dir = os.getenv(ANSYS_GRPC_CERTIFICATES, "./certs")
            args.append(f"--certs-dir={certs_dir}")
        if transport_mode == "uds":
            if uds_dir:
                args.append(f"--uds-dir={uds_dir}")
            if uds_id:
                args.append(f"--uds-id={uds_id}")

        # Add other options
        if single_project_path:
            args.append("-singleProject")
            args.append(single_project_path)
        if sherlock_command_args:
            args.extend(shlex.split(sherlock_command_args))

        LOG.info(f"Command arguments: {args}")
        subprocess.Popen(args)

        return ansys_install_path
    except Exception as e:
        LOG.error(f"Error launching Sherlock. {e}")
        raise e


def launch_and_connect(
    host: str = LOCALHOST,
    port: int = SHERLOCK_DEFAULT_PORT,
    single_project_path: str = "",
    sherlock_command_args: str = "",
    year: Optional[int] = None,
    release_number: Optional[int] = None,
    timeout: int = DEFAULT_CONNECT_TIMEOUT,
    transport_mode: str = "mtls",
    certs_dir: str = None,
    uds_dir: str = None,
    uds_id: str = None,
) -> tuple[Sherlock, str]:
    """
    Launch Sherlock, start gRPC on a given host and port, and wait until connected to Sherlock.

    Available Since: 2025R2

    Parameters
    ----------
    host: str, optional
        IP address to start gRPC on.
        The default is ``"127.0.0.1"``, which is the IP address for the local host.
    port: int, optional
        Port number for the connection.
    single_project_path : str, optional
        Path to the Sherlock project if invoking Sherlock in the single-project mode.
    sherlock_command_args : str, optional
        Additional command arguments for launching Sherlock.
    year: int, optional
        4-digit year of the Sherlock release to launch. If not provided,
        the latest installed version of Sherlock will be launched.
    release_number: int, optional
        Release number of Sherlock to launch. If not provided,
        the latest installed version of Sherlock will be launched.
    timeout: int, optional
        Maximum time (in seconds) to wait for the connection to Sherlock to be established.
        Default is 120 seconds.
    transport_mode: str, optional
        gRPC transport mode. Supported values are "insecure", "mtls", "wnua", and "uds".
        Default is "mtls".
    certs_dir: str, optional
        Directory containing the mTLS certificates. Default is "./certs".
    uds_dir: str, optional
        Directory for the UDS socket file. Default is "$HOME/.conn".
    uds_id: str, optional
        Identifier for the UDS socket file name. Default is no identifier.

    Returns
    -------
    tuple[Sherlock, str]
        Sherlock gRPC connection object and the installation directory.
    """
    ansys_install_path = launch(
        host,
        port,
        single_project_path,
        sherlock_command_args,
        year,
        release_number,
        transport_mode=transport_mode,
        certs_dir=certs_dir,
        uds_dir=uds_dir,
        uds_id=uds_id,
    )
    try:
        sherlock = connect(
            port=port,
            timeout=timeout,
            transport_mode=transport_mode,
            uds_dir=uds_dir,
            uds_id=uds_id,
        )
        return sherlock, ansys_install_path
    except Exception as e:
        LOG.error(f"Error connecting to Sherlock after launch: {e}")
        raise RuntimeError(f"Error connecting to Sherlock after launch: {e}")


def connect(
    port: int = SHERLOCK_DEFAULT_PORT,
    timeout=DEFAULT_CONNECT_TIMEOUT,
    transport_mode: str = "mtls",
    certs_dir: str = None,
    uds_dir: str = None,
    uds_id: str = None,
) -> Sherlock:
    """Connect to a local instance of Sherlock.

    Available Since: 2025R2

    Parameters
    ----------
    port: int, optional
        Port number for the connection (ignored if transport_mode is "uds").
        Default is 9090.
    timeout: int, optional
        Maximum time (in seconds) to wait for the connection to Sherlock to be established.
        Default is 120 seconds.
    transport_mode : str, optional
        Transport mode to use:
            - "insecure" : unencrypted connection (default)
            - "mtls" : mutual TLS authentication
            - "uds" : Unix Domain Socket
            - "wnua" : Windows Named User Authentication
    certs_dir: str, optional
        Directory containing the mTLS certificates. Default is "./certs".
    uds_dir : str, optional
        Directory for the UDS socket file.
    uds_id : str, optional
        Optional ID for the UDS socket file.

    Returns
    -------
    Sherlock
        The instance of Sherlock.
    """
    try:
        channel = _connect_grpc_channel(
            host=LOCALHOST,
            port=port,
            uds_dir=uds_dir,
            uds_id=uds_id,
            transport_mode=transport_mode,
            certs_dir=certs_dir,
        )
        _wait_for_sherlock_grpc_ready(channel, timeout)

        # Create Common without version since the version is unknown
        common = Common(channel=channel, server_version=None)
        server_version = None
        try:
            sherlock_info = common.get_sherlock_info()
            if sherlock_info is not None:
                LOG.info(f"Connected to Sherlock version: {sherlock_info.releaseVersion}")
                server_version = _convert_to_server_version(sherlock_info.releaseVersion)
        except grpc.RpcError as e:
            error_message = e.details() if e.details() else "Unknown error occurred."
            LOG.error(f"Server validation error: {error_message}")
            raise SherlockConnectionError(message=error_message)

        return Sherlock(channel=channel, server_version=server_version)
    except Exception as e:
        LOG.error(f"Error encountered connecting to Sherlock: {str(e)}")
        raise e


def _convert_to_server_version(sherlock_release_version: str) -> int:
    # convert the version returned from Sherlock (e.g. "2025 R1")
    # to the version needed for the API (e.g. 251)
    tokens = sherlock_release_version.split(" ")
    year = _extract_sherlock_version_year(int(tokens[0]))
    minor_version = int(tokens[1][1:])
    server_version = year * 10 + minor_version
    return server_version


def _connect_grpc_channel(
    host: str = LOCALHOST,
    port: int = SHERLOCK_DEFAULT_PORT,
    uds_dir: str = None,
    uds_id: str = None,
    transport_mode: str = "mtls",
    certs_dir: str = None,
) -> grpc.Channel:
    """
    Connect to Sherlock gRPC via UDS, TCP, or other transport modes.

    Parameters
    ----------
    host : str
        Hostname or IP address for TCP connection (ignored for UDS).
    port : int
        Port number for TCP connection.
    uds_dir : str, optional
        Directory for the UDS socket file.
    uds_id : str, optional
        Optional ID for the UDS socket file.
    transport_mode : str
        Transport mode (e.g., "insecure", "wnua", "mtls", "uds").
    certs_dir: str, optional
        Directory containing the mTLS certificates. Default is "./certs".

    Returns
    -------
    grpc.Channel
        A gRPC channel connected to Sherlock.
    """
    try:
        channel = create_channel(
            transport_mode=transport_mode,
            host=host,
            port=port,
            uds_service=SHERLOCK_UDS_SERVICE,
            uds_dir=uds_dir,
            uds_id=uds_id,
            certs_dir=certs_dir,
            grpc_options=[
                ("grpc.max_send_message_length", 100 * 1024 * 1024),
                ("grpc.max_receive_message_length", 100 * 1024 * 1024),
            ],
        )
        LOG.info(f"gRPC channel created successfully using transport mode: {transport_mode}")
        return channel
    except Exception as e:
        LOG.error(f"Failed to create gRPC channel with mode '{transport_mode}': {e}")
        raise


def _wait_for_sherlock_grpc_ready(channel, timeout):
    # Check that the gRPC connection is up.
    try:
        LOG.info("Waiting for Sherlock gRPC service to start...")
        grpc.channel_ready_future(channel).result(timeout)
    except grpc.FutureTimeoutError:
        raise SherlockConnectionError(message="Error starting gRPC service")


def _get_base_ansys(
    year: Optional[int] = None, release_number: Optional[int] = None
) -> tuple[str, int]:
    supported_installed_versions = {
        env_key: path
        for env_key, path in os.environ.items()
        if env_key.startswith("AWP_ROOT") and os.path.isfile(_get_sherlock_exe_file_path(path))
    }

    sorted_installed_version_keys = sorted(supported_installed_versions, reverse=True)

    if year is not None:
        two_digit_year = _extract_sherlock_version_year(year)
        if release_number is None:
            # If no release number is provided, find the latest version for the given year
            for key in sorted_installed_version_keys:
                ansys_version = _get_ansys_version_from_awp_root(key)
                ansys_year = (int)(ansys_version / 10)
                if ansys_year == two_digit_year:
                    return supported_installed_versions[key], ansys_version
            raise ValueError(f"No versions of Sherlock are installed for year {year}.")
        else:
            try:
                sherlock_version = int(f"{two_digit_year}{release_number}")
                version_key = f"AWP_ROOT{sherlock_version}"
                if version_key in supported_installed_versions:
                    return supported_installed_versions[version_key], sherlock_version
                else:
                    raise ValueError(
                        f"Sherlock {two_digit_year} {release_number} is not installed."
                    )
            except ValueError as e:
                LOG.error(f"Error extracting Sherlock version year: {e}")
                raise e
    else:
        for key in sorted_installed_version_keys:
            ansys_version = _get_ansys_version_from_awp_root(key)
            if ansys_version >= _EARLIEST_SUPPORTED_VERSION:
                return supported_installed_versions[key], ansys_version

    raise ValueError("Could not find any installed version of Sherlock.")


def _get_ansys_version_from_awp_root(awp_root: str) -> int:
    if awp_root.find("AWP_ROOT") >= 0:
        return int(awp_root.replace("AWP_ROOT", ""))

    return 0


def _get_sherlock_exe_path(
    year: Optional[int] = None, release_number: Optional[int] = None
) -> tuple[str, int, str]:
    ansys_base, sherlock_version = _get_base_ansys(year=year, release_number=release_number)
    if not ansys_base:
        return "", 0, ""
    sherlock_bin = _get_sherlock_exe_file_path(ansys_base)
    return sherlock_bin, sherlock_version, ansys_base


def _get_sherlock_exe_file_path(ansys_base):
    if os.name == "nt":
        return os.path.join(ansys_base, "sherlock", "SherlockClient.exe")
    return os.path.join(ansys_base, "sherlock", "runSherlock")


def _extract_sherlock_version_year(year: int) -> int:
    if 1000 <= year <= 9999:
        return year % 100
    raise ValueError("Year must be a 4-digit integer.")
