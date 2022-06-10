import grpc

from ansys.sherlock.core.errors import SherlockAddRandomVibeEventError
from ansys.sherlock.core.lifecycle import Lifecycle


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    lifecycle = Lifecycle(channel)
    test_add_random_vibe_event(lifecycle)


def test_add_random_vibe_event(lifecycle):
    """Test add_random_vibe_event API"""

    try:
        lifecycle.add_random_vibe_event(
            "", "", "", 1, "sec", 1, "PER SEC", "45,45", "Uniaxial", "1,2,3", description="Test1"
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.strItr()[0] == "Add random vibe event error: Invalid Project Name"

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "",
            "",
            1,
            "sec",
            1,
            "PER SEC",
            "45,45",
            "Uniaxial",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.strItr()[0] == "Add random vibe event error: Invalid Phase Name"

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "",
            1,
            "sec",
            1,
            "PER SEC",
            "45,45",
            "Uniaxial",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.strItr()[0] == "Add random vibe event error: Invalid Event Name"

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            0,
            "sec",
            1,
            "PER SEC",
            "45,45",
            "Uniaxial",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.strItr()[0] == "Add random vibe event error: Duration Must Be Greater Than 0"

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            0,
            "invalid",
            1,
            "PER SEC",
            "45,45",
            "Uniaxial",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.strItr()[0] == "Add random vibe event error: Invalid Duration Unit Specified"

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            5,
            "sec",
            0,
            "invalid",
            "45,45",
            "Uniaxial",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.strItr()[0] == "Add random vibe event error: Invalid Cycle Type"

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            5,
            "sec",
            0,
            "PER SEC",
            "45,45",
            "Uniaxial",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert (
            e.strItr()[0] == "Add random vibe event error: Number of Cycles Must Be Greater Than 0"
        )

    # Following tests depend on the existence of a connection and a project named "Test"

    # try:
    #     lifecycle.add_random_vibe_event(
    #         "Fake",
    #         "Example",
    #         "Event1",
    #         5,
    #         "sec",
    #         4,
    #         "PER SEC",
    #         "45,45",
    #         "Uniaxial",
    #         "1,2,3",
    #         description="Test1",
    #     )
    #     assert False
    # except SherlockAddRandomVibeEventError as e:
    #     assert e.strItr()[0] == "Add random vibe event error: Cannot find project: Fake"

    # try:
    #     lifecycle.add_random_vibe_event(
    #         "Test",
    #         "Example",
    #         "Event1",
    #         5,
    #         "sec",
    #         4,
    #         "PER SEC",
    #         "45,45",
    #         "Uniaxial",
    #         "1,2,3",
    #         description="Test1",
    #     )
    # except SherlockAddRandomVibeEventError as e:
    #     assert False

    # try:
    #     lifecycle.add_random_vibe_event(
    #         "Test",
    #         "Example",
    #         "Event1",
    #         5,
    #         "sec",
    #         4,
    #         "PER SEC",
    #         "45,45",
    #         "Uniaxial",
    #         "1,2,3",
    #         description="Test1",
    #     )
    #     assert False
    # except SherlockAddRandomVibeEventError as e:
    #     assert e.strItr()[0] == (
    #         "Add random vibe event error: Duplicate phase name 'Example' specified"
    #         ".\nEnter a different name or delete the old phase before updating this phase."
    #     )


if __name__ == "__main__":
    test_all()
