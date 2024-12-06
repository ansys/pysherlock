# © 2023-2024 ANSYS, Inc. All rights reserved

"""PySherlock logger."""
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
import sys

LOG_LEVEL = logging.DEBUG
FILE_NAME = "PySherlock.log"

# Formatting
STDOUT_MSG_FORMAT = logging.Formatter("%(levelname)s - %(module)s - %(funcName)s - %(message)s")
FILE_MSG_FORMAT = STDOUT_MSG_FORMAT

DEFAULT_STDOUT_HEADER = """
LEVEL - INSTANCE NAME - MODULE - FUNCTION - MESSAGE
"""
DEFAULT_FILE_HEADER = DEFAULT_STDOUT_HEADER

NEW_SESSION_HEADER = f"""
===============================================================================
       NEW SESSION - {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
==============================================================================="""


def _get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(STDOUT_MSG_FORMAT)
    return console_handler


def _get_file_handler():
    file_handler = TimedRotatingFileHandler(FILE_NAME, when="midnight")
    file_handler.setFormatter(STDOUT_MSG_FORMAT)
    file_handler.stream.write(NEW_SESSION_HEADER)
    file_handler.stream.write(DEFAULT_FILE_HEADER)
    return file_handler


class Logger:
    """Provides the PySherlock logger."""

    def __init__(self, logger_name: str):
        """Initialize logger."""
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(LOG_LEVEL)
        self.logger.addHandler(_get_console_handler())
        self.logger.addHandler(_get_file_handler())
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.log = self.logger.log
