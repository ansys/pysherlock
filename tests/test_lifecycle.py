import grpc

from ansys.sherlock.core.errors import SherlockAddRandomVibeProfileError
from ansys.sherlock.core.lifecycle import Lifecycle


def test_all():
    #   """Test all lifecycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    lifecycle = Lifecycle(channel)

    test_add_random_vibe_profile(lifecycle)


def test_add_random_vibe_profile(lifecycle):
    #   "Test the add_random_vibe_profile API"

    try:
        lifecycle.add_random_vibe_profile(
            "Test",
            "Example",
            "Event1",
            "",
            "HZ",
            "G2/Hz",
            [(1, 2), (3, 4), (5, 6)],
        )
        assert False
    except SherlockAddRandomVibeProfileError as e:
        assert e.strItr()[0] == "Add random vibe profile error: Invalid Profile Name"

    try:
        lifecycle.add_random_vibe_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "per sec",
            "G2/Hz",
            [(1, 2), (3, 4), (5, 6)],
        )
        assert False
    except SherlockAddRandomVibeProfileError as e:
        assert e.strItr()[0] == "Add random vibe profile error: Invalid Frequency Unit"

    try:
        lifecycle.add_random_vibe_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "HZ",
            "G2/sec",
            [(1, 2), (3, 4), (5, 6)],
        )
        assert False
    except SherlockAddRandomVibeProfileError as e:
        assert e.strItr()[0] == "Add random vibe profile error: Invalid Amplitude Type"

    try:
        lifecycle.add_random_vibe_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "HZ",
            "G2/Hz",
            [(12,), (3, 4), (5, 6)],
        )
        assert False
    except SherlockAddRandomVibeProfileError as e:
        assert (
            e.strItr()[0] == "Add random vibe profile error: Invalid entry 0: Wrong number of args"
        )

    try:
        lifecycle.add_random_vibe_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "HZ",
            "G2/Hz",
            [(12, 4), (3, "x"), (5, 6)],
        )
        assert False
    except SherlockAddRandomVibeProfileError as e:
        assert e.strItr()[0] == "Add random vibe profile error: Invalid entry 1: Invalid freq/ampl"

    try:
        lifecycle.add_random_vibe_profile(
            "Test",
            "Example",
            "Event1",
            "Profile1",
            "HZ",
            "G2/Hz",
            [(12, 4), (3, 4), (-5, 6)],
        )
        assert False
    except SherlockAddRandomVibeProfileError as e:
        assert (
            e.strItr()[0]
            == "Add random vibe profile error: Invalid entry 2: Frequencies must be greater than 0"
        )

    # Below are the grpc-reliants testcases

    # try:
    #     lifecycle.add_random_vibe_profile(
    #         "Test",
    #         "Example",
    #         "Event1",
    #         "Profile1",
    #         "HZ",
    #         "G2/Hz",
    #         [(1, 2), (3, 4), (5, 6)],
    #     )
    #     assert True
    # except SherlockAddRandomVibeProfileError as e:
    #     assert False


if __name__ == "__main__":
    test_all()
