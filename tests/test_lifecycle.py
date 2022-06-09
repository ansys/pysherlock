import grpc

from ansys.sherlock.core.lifecycle import Lifecycle


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    lifecycle = Lifecycle(channel)
    test_add_random_vibe_event(lifecycle)


def test_add_random_vibe_event(lifecycle):
    """Test add_random_vibe_event API"""

    rc1, str1 = lifecycle.add_random_vibe_event(
        "", "", "", 1, "sec", 1, "PER SEC", "45,45", "Uniaxial", "1,2,3", description="Test1"
    )
    assert rc1 == -1
    assert str1 == "Add random vibe event error: Invalid Project Name"

    rc2, str2 = lifecycle.add_random_vibe_event(
        "Test", "", "", 1, "sec", 1, "PER SEC", "45,45", "Uniaxial", "1,2,3", description="Test1"
    )
    assert rc2 == -1
    assert str2 == "Add random vibe event error: Invalid Phase Name"

    rc3, str3 = lifecycle.add_random_vibe_event(
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
    assert rc3 == -1
    assert str3 == "Add random vibe event error: Invalid Event Name"

    rc3, str3 = lifecycle.add_random_vibe_event(
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
    assert rc3 == -1
    assert str3 == "Add random vibe event error: Duration Must Be Greater Than 0"

    rc4, str4 = lifecycle.add_random_vibe_event(
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
    assert rc4 == -1
    assert str4 == "Add random vibe event error: Invalid Duration Unit Specified"

    rc5, str5 = lifecycle.add_random_vibe_event(
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
    assert rc5 == -1
    assert str5 == "Add random vibe event error: Invalid Cycle Type"

    rc6, str6 = lifecycle.add_random_vibe_event(
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
    assert rc6 == -1
    assert str6 == "Add random vibe event error: Number of Cycles Must Be Greater Than 0"

    # Following tests depend on the existence of a connection and a project named "Test"

    # rc7, str7 = lifecycle.add_random_vibe_event(
    #     "Fake",
    #     "Example",
    #     "Event1",
    #     5,
    #     "sec",
    #     4,
    #     "PER SEC",
    #     "45,45",
    #     "Uniaxial",
    #     "1,2,3",
    #     description="Test1",
    # )
    # assert rc7 == -1
    # assert str7 == "Add random vibe event error: Cannot find project: Fake"

    # rc8, str8 = lifecycle.add_random_vibe_event(
    #     "Test",
    #     "Example",
    #     "Event1",
    #     5,
    #     "sec",
    #     4,
    #     "PER SEC",
    #     "45,45",
    #     "Uniaxial",
    #     "1,2,3",
    #     description="Test1",
    # )
    # assert rc8 == 0
    # assert str8 == ""

    # rc9, str9 = lifecycle.add_random_vibe_event(
    #     "Test",
    #     "Example",
    #     "Event1",
    #     5,
    #     "sec",
    #     4,
    #     "PER SEC",
    #     "45,45",
    #     "Uniaxial",
    #     "1,2,3",
    #     description="Test1",
    # )
    # assert rc9 == -1
    # assert str9 == (
    #     "Add random vibe event error: Duplicate phase name 'Example' specified"
    #     ".\nEnter a different name or delete the old phase before updating this phase."
    # )


if __name__ == "__main__":
    test_all()
