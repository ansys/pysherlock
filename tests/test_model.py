# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

import platform

import grpc
import os
import unittest

from ansys.sherlock.core.model import Model


class TestModel(unittest.TestCase):
    def test_model_export_file_directory(self):
        channel_param = "127.0.0.1:9090"
        channel = grpc.insecure_channel(channel_param)
        instance = Model(channel)

        if platform.system() == "Windows":
            temp_dir = os.environ.get('TEMP', 'C:\\TEMP')
        else:
            temp_dir = os.environ.get('TEMP', "/tmp")

        try:
            if platform.system() == "Windows":
                instance.export_trace_reinforcement_model(
                    "Tutorial Project", "Main Board", temp_dir + "\\export.wbjn"
                )
            else:
                instance.export_trace_reinforcement_model(
                    "Tutorial Project", "Main Board", temp_dir + "/export.wbjn"
                )
        except Exception as e:
            assert (
                    str(e) == "Sherlock model service error: Export file directory"
                              " (" + temp_dir + ") does not exist"
            )


if __name__ == "__main__":
    unittest.main()
