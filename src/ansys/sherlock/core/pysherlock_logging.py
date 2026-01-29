# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.
# © 2023 - 2024 ANSYS, Inc. All rights reserved
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
