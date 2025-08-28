# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.

import grpc
import pytest

from ansys.sherlock.core.common import Common
from ansys.sherlock.core.errors import SherlockVersionError


def test_all():
    test_version_check()


def test_version_check():
    try:
        channel_param = "127.0.0.1:9090"
        channel = grpc.insecure_channel(channel_param)
        # Set Sherlock version to 24R2 which is before 25R1, when
        # "get_sherlock_version" was added to PySherlock / Sherlock.
        common = Common(channel, 242)
        # This should fail since it did not exist in 242
        common.get_sherlock_info()
        pytest.fail("Sherlock version should be too low to launch this method")
    except Exception as e:
        if not isinstance(e, SherlockVersionError):
            pytest.fail("Unexpected exception " + str(e))


def assert_float_equals(expected, actual):
    assert pytest.approx(actual, abs=1e-14) == pytest.approx(expected, abs=1e-14)


if __name__ == "__main__":
    test_all()
