import grpc

from ansys.sherlock.core.errors import SherlockUpdatePartsListError
from ansys.sherlock.core.parts import Parts


def test_all():
    """Test all parts APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    parts = Parts(channel)

    helper_test_update_parts_list(parts)


def helper_test_update_parts_list(parts):
    """Test update_parts_list API."""

    try:
        parts.update_parts_list(
            "",
            "Card",
            "Sherlock Part Library",
            "Both",
            "Error",
        )
        assert False
    except SherlockUpdatePartsListError as e:
        assert e.str_itr()[0] == "Update parts list error: Invalid project name"

    try:
        parts.update_parts_list(
            "Test",
            "",
            "Sherlock Part Library",
            "Both",
            "Error",
        )
        assert False
    except SherlockUpdatePartsListError as e:
        assert e.str_itr()[0] == "Update parts list error: Invalid cca name"

    try:
        parts.update_parts_list(
            "Test",
            "Card",
            "",
            "Both",
            "Error",
        )
        assert False
    except SherlockUpdatePartsListError as e:
        assert e.str_itr()[0] == "Update parts list error: Invalid parts library"

    try:
        parts.update_parts_list(
            "Test",
            "Card",
            "Sherlock Part Library",
            "Invalid",
            "Error",
        )
        assert False
    except SherlockUpdatePartsListError as e:
        assert e.str_itr()[0] == "Update parts list error: Invalid matching argument"

    try:
        parts.update_parts_list(
            "Test",
            "Card",
            "Sherlock Part Library",
            "Both",
            "Invalid",
        )
        assert False
    except SherlockUpdatePartsListError as e:
        assert e.str_itr()[0] == "Update parts list error: Invalid duplication argument"


if __name__ == "__main__":
    test_all()
