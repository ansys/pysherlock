"""Module for running the gRPC APIs in the SherlockModelService."""
import errno
import grpc
import os
import socket

from ansys.sherlock.core import LOG
from ansys.sherlock.core.errors import SherlockConnectionError

LOCALHOST = "127.0.0.1"
SHERLOCK_DEFAULT_PORT = 9090
EARLIEST_SUPPORTED_VERSION = 211
sherlock_cmd_args = []

def export_trace_reinforcement_model():
    try:
        #__check_grpc_connection()
        SHERLOCK.model.export_trace_reinforcement_model(message)
    except SherlockConnectionError as err:
        LOG.error("export_trace_reinforcement_model error: ", err)
        return -1


def __check_grpc_connection():
    if SHERLOCK is None or SHERLOCK.model_stub is None:
        raise SherlockConnectionError("The Sherlock gRPC connection has not been established.")
