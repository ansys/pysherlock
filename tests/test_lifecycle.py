import grpc

from ansys.sherlock.core.lifecycle import Lifecycle


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    lifecycle = Lifecycle(channel)
    test_create_life_phase(lifecycle)


def test_create_life_phase(lifecycle):
    """Test create_life_phase API"""

    rc1, str1 = lifecycle.create_life_phase("", "", 1, "sec", 1, "PER SEC", description="Test1")
    assert rc1 == -1
    assert str1 == "Create life phase error: Invalid Project Name"

    rc2, str2 = lifecycle.create_life_phase("Test", "", 1, "sec", 1, "PER SEC", description="Test1")
    assert rc2 == -1
    assert str2 == "Create life phase error: Invalid Phase Name"

    rc3, str3 = lifecycle.create_life_phase(
        "Test", "Example", 0, "sec", 1, "PER SEC", description="Test1"
    )
    assert rc3 == -1
    assert str3 == "Create life phase error: Duration Must Be Greater Than 0"

    rc4, str4 = lifecycle.create_life_phase(
        "Test", "Example", 0, "invalid", 1, "PER SEC", description="Test1"
    )
    assert rc4 == -1
    assert str4 == "Create life phase error: Invalid Duration Unit Specified"

    rc5, str5 = lifecycle.create_life_phase(
        "Test", "Example", 5, "sec", 0, "invalid", description="Test1"
    )
    assert rc5 == -1
    assert str5 == "Create life phase error: Invalid Cycle Type"

    rc6, str6 = lifecycle.create_life_phase(
        "Test", "Example", 5, "sec", 0, "PER SEC", description="Test1"
    )
    assert rc6 == -1
    assert str6 == "Create life phase error: Number of Cycles Must Be Greater Than 0"

    # Following tests depend on the existence of a connection and a project named "Test"

    # rc7, str7 = lifecycle.create_life_phase(
    #     "Fake", "Example", 5, "sec", 4, "PER SEC", description="Test1"
    # )
    # assert rc7 == -1
    # assert str7 == "Create life phase error: Cannot find project: Fake"

    # rc8, str8 = lifecycle.create_life_phase(
    #     "Test", "Example", 5, "sec", 4, "PER SEC", description="Test1"
    # )
    # assert rc8 == 0
    # assert str8 == ""

    # rc9, str9 = lifecycle.create_life_phase(
    #     "Test", "Example", 5, "sec", 4, "PER SEC", description="Test1"
    # )
    # assert rc9 == -1
    # assert str9 == (
    #     "Create life phase error: Duplicate phase name 'Example' specified"
    #     ".\nEnter a different name or delete the old phase before updating this phase."
    # )


if __name__ == "__main__":
    test_all()
