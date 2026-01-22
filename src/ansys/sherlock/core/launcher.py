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
import time
from typing import Optional

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockCannotUsePortError, SherlockConnectionError
from ansys.sherlock.core.sherlock import Sherlock
from ansys.sherlock.core.utils.cyberchannel import create_channel
from ansys.sherlock.core.utils.version_check import _EARLIEST_SUPPORTED_VERSION

ANSYS_GRPC_CERTIFICATES = "ANSYS_GRPC_CERTIFICATES"
LOCALHOST = "127.0.0.1"
SHERLOCK_DEFAULT_PORT = 9090
SHERLOCK_UDS_SERVICE = "sherlock-grpc"
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
    r"""Launch Sherlock and start gRPC on a given host and port.

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

    >>> from ansys.sherlock.core import launcher
    >>> launcher.launch_sherlock(
    >>>     port=9092,
    >>>     transport_mode="mtls",
    >>>     certs_dir="C:\\path\\to\\certs"
    >>> )

    >>> from ansys.sherlock.core import launcher
    >>> launcher.launch_sherlock(
    >>>     port=9092,
    >>>     transport_mode="uds",
    >>>     uds_dir="C:\\path\\to\\uds",
    >>>     uds_id="custom_id"
    >>> )

    """
    try:
        _is_port_available(host, port)
    except Exception as e:
        LOG.error(str(e))
        raise e

    _server_version = None
    try:
        sherlock_launch_cmd, _server_version = _get_sherlock_exe_path(
            year=year, release_number=release_number
        )
        args = [sherlock_launch_cmd]

        if transport_mode not in ["insecure", "mtls", "uds", "wnua"]:
            args.append(f"-grpcPort={port}")

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

        sherlock = connect_grpc_channel(
            port=port,
            server_version=_server_version,
            transport_mode=transport_mode,
            certs_dir=certs_dir,
            uds_dir=uds_dir,
            uds_id=uds_id,
        )

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
        LOG.error("Error encountered while starting or executing Sherlock, error = %s" + str(e))


def connect_grpc_channel(
    port: int = SHERLOCK_DEFAULT_PORT,
    server_version: Optional[int] = None,
    transport_mode: str = "mtls",
    certs_dir: str = None,
    uds_dir: str = None,
    uds_id: str = None,
) -> Sherlock:
    """Create a gRPC connection to a specified port and return the ``Sherlock`` connection object.

    The ``Sherlock`` connection object is used to invoke the APIs from their respective services.
    This can be used to connect to the Sherlock instance that is already running with the specified
    port.

    Parameters
    ----------
    port: int, optional
        Port number for the connection. Default is ``SHERLOCK_DEFAULT_PORT``.
    server_version: int, optional
        Version of Sherlock. Default is the newest version that is installed.
    transport_mode: str, optional
        Transport mode for the gRPC connection. Default is ``"mtls"``.
    certs_dir: str, optional
        Directory containing the mTLS certificates. Default is ``None``.
    uds_dir: str, optional
        Directory for the UDS socket file. Default is ``None``.
    uds_id: str, optional
        Optional ID for the UDS socket file. Default is ``None``.

    Returns
    -------
    Sherlock
        The instance of sherlock.
    """
    try:
        channel = create_channel(
            transport_mode=transport_mode,
            host=LOCALHOST,
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
        return Sherlock(channel, server_version)
    except Exception as e:
        LOG.error(f"Failed to create gRPC channel with mode '{transport_mode}': {e}")
        raise


def _get_base_ansys(
    year: Optional[int] = None, release_number: Optional[int] = None
) -> tuple[str, int]:
    supported_installed_versions = {
        env_key: path
        for env_key, path in os.environ.items()
        if env_key.startswith("AWP_ROOT") and os.path.isdir(path)
    }

    if year is not None and release_number is not None:
        try:
            year = _extract_sherlock_version_year(year)

            sherlock_version = int(f"{year}{release_number}")
            version_key = f"AWP_ROOT{sherlock_version}"
            if version_key in supported_installed_versions:
                return supported_installed_versions[version_key], sherlock_version
            else:
                raise ValueError(f"Sherlock {year} {release_number} is not installed.")
        except ValueError as e:
            LOG.error(f"Error extracting Sherlock version year: {e}")
            raise e

    for key in sorted(supported_installed_versions, reverse=True):
        ansys_version = _get_ansys_version_from_awp_root(key)
        sherlock_version = int(ansys_version)
        if ansys_version >= _EARLIEST_SUPPORTED_VERSION:
            return supported_installed_versions[key], sherlock_version

    raise ValueError("Could not find any installed version of Sherlock.")


def _get_ansys_version_from_awp_root(awp_root: str):
    if awp_root.find("AWP_ROOT") >= 0:
        return int(awp_root.replace("AWP_ROOT", ""))

    return ""


def _get_sherlock_exe_path(
    year: Optional[int] = None, release_number: Optional[int] = None
) -> tuple[str, int]:
    ansys_base, sherlock_version = _get_base_ansys(year=year, release_number=release_number)
    if not ansys_base:
        return "", 0
    if os.name == "nt":
        sherlock_bin = os.path.join(ansys_base, "sherlock", "SherlockClient.exe")
    else:
        sherlock_bin = os.path.join(ansys_base, "sherlock", "runSherlock")
    return sherlock_bin, sherlock_version


def _extract_sherlock_version_year(year: int) -> int:
    if 1000 <= year <= 9999:
        return year % 100
    raise ValueError("Year must be a 4-digit integer.")
