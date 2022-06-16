import grpc

from ansys.sherlock.core.errors import SherlockAddRandomVibeEventError, SherlockCreateLifePhaseError
from ansys.sherlock.core.lifecycle import Lifecycle


def test_all():
    """Test all life cycle APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    lifecycle = Lifecycle(channel)

    helper_test_create_life_phase(lifecycle)
    helper_test_add_random_vibe_event(lifecycle)


def helper_test_add_random_vibe_event(lifecycle):
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

    if lifecycle._is_connection_up():
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

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            5,
            "sec",
            4,
            "PER SEC",
            "45,x",
            "Uniaxial",
            "1,2,3",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert e.strItr()[0] == "Add random vibe event error: Invalid elevation value"

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            5,
            "sec",
            4,
            "PER MIN",
            "45,45",
            "Uniaxial",
            "0,0,0",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert (
            e.strItr()[0]
            == "Add random vibe event error: At least one direction coordinate must be non-zero"
        )

    try:
        lifecycle.add_random_vibe_event(
            "Test",
            "Example",
            "Event1",
            5,
            "sec",
            4,
            "PER MIN",
            "4545",
            "Uniaxial",
            "0,1,0",
            description="Test1",
        )
        assert False
    except SherlockAddRandomVibeEventError as e:
        assert (
            e.strItr()[0] == "Add random vibe event error: Invalid number of spherical coordinates"
        )


def helper_test_create_life_phase(lifecycle):
    """Test create_life_phase API"""

    try:
        lifecycle.create_life_phase("", "", 1, "sec", 1, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.strItr()[0] == "Create life phase error: Invalid Project Name"

    try:
        lifecycle.create_life_phase("Test", "", 1, "sec", 1, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.strItr()[0] == "Create life phase error: Invalid Phase Name"

    try:
        lifecycle.create_life_phase("Test", "Example", 0, "sec", 1, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.strItr()[0] == "Create life phase error: Duration Must Be Greater Than 0"

    if lifecycle._is_connection_up():
        try:
            lifecycle.create_life_phase(
                "Test", "Example", 0, "invalid", 1, "PER SEC", description="Test1"
            )
            assert False
        except SherlockCreateLifePhaseError as e:
            assert e.strItr()[0] == "Create life phase error: Invalid Duration Unit Specified"

        try:
            lifecycle.create_life_phase(
                "Test", "Example", 5, "sec", 0, "invalid", description="Test1"
            )
            assert False
        except SherlockCreateLifePhaseError as e:
            assert e.strItr()[0] == "Create life phase error: Invalid Cycle Type"

    try:
        lifecycle.create_life_phase("Test", "Example", 5, "sec", 0, "PER SEC", description="Test1")
        assert False
    except SherlockCreateLifePhaseError as e:
        assert e.strItr()[0] == "Create life phase error: Number of Cycles Must Be Greater Than 0"


if __name__ == "__main__":
    test_all()
