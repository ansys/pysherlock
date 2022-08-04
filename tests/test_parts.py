import grpc

from ansys.sherlock.core.errors import (
    SherlockImportPartsListError,
    SherlockUpdatePartsListError,
    SherlockUpdatePartsLocationsByFileError,
    SherlockUpdatePartsLocationsError,
)
from ansys.sherlock.core.parts import Parts


def test_all():
    """Test all parts APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    parts = Parts(channel)

    helper_test_update_parts_list(parts)
    helper_test_update_parts_locations(parts)
    helper_test_update_parts_locations_by_file(parts)
    helper_test_import_parts_list(parts)


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


def helper_test_update_parts_locations(parts):
    """Test update_parts_locations API."""

    try:
        parts.update_parts_locations(
            "",
            "Card",
            [
                ("C1", "-2.7", "-1.65", "0", "in", "TOP", "False"),
                ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
            ],
        )
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert e.str_itr()[0] == "Update parts locations error: Invalid project name"

    try:
        parts.update_parts_locations(
            "Test",
            "",
            [
                ("C1", "-2.7", "-1.65", "0", "in", "TOP", "False"),
                ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
            ],
        )
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert e.str_itr()[0] == "Update parts locations error: Invalid cca name"

    try:
        parts.update_parts_locations("Test", "Card", "Invalid")
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert e.str_itr()[0] == "Update parts locations error: Invalid part_loc argument"

    try:
        parts.update_parts_locations("Test", "Card", [])
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert e.str_itr()[0] == "Update parts locations error: Missing part location properties"

    try:
        parts.update_parts_locations(
            "Test",
            "Card",
            [
                ("C1", "-2.7", "-1.65", "0", "TOP", "False"),
                ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
            ],
        )
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert (
            e.str_itr()[0]
            == "Update parts locations error: Invalid part location 0: Invalid number of fields"
        )

    try:
        parts.update_parts_locations(
            "Test",
            "Card",
            [
                ("C1", "-2.7", "-1.65", "0", "in", "TOP", "False"),
                ("", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
            ],
        )
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert (
            e.str_itr()[0]
            == "Update parts locations error: Invalid part location 1: Missing ref des"
        )

    if parts._is_connection_up():
        try:
            parts.update_parts_locations(
                "Test",
                "Card",
                [
                    ("C1", "-2.7", "-1.65", "0", "Invalid", "TOP", "False"),
                    ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
                ],
            )
            assert False
        except SherlockUpdatePartsLocationsError as e:
            assert e.str_itr()[0] == (
                "Update parts locations error: "
                "Invalid part location 0: Invalid location units specified"
            )

    try:
        parts.update_parts_locations(
            "Test",
            "Card",
            [
                ("C1", "-2.7", "-1.65", "0", "", "TOP", "False"),
                ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
            ],
        )
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert (
            e.str_itr()[0]
            == "Update parts locations error: Invalid part location 0: Missing location units"
        )

    try:
        parts.update_parts_locations(
            "Test",
            "Card",
            [
                ("C1", "Invalid", "-1.65", "0", "in", "TOP", "False"),
                ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
            ],
        )
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert e.str_itr()[0] == (
            "Update parts locations error: Invalid part location 0: "
            "Invalid location X coordinate specified"
        )

    try:
        parts.update_parts_locations(
            "Test",
            "Card",
            [
                ("C1", "-2.7", "-1.65", "0", "in", "TOP", "False"),
                ("J1", "-3.55", "Invalid", "90", "in", "TOP", "False"),
            ],
        )
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert e.str_itr()[0] == (
            "Update parts locations error: Invalid part location 1: "
            "Invalid location Y coordinate specified"
        )

    try:
        parts.update_parts_locations(
            "Test",
            "Card",
            [
                ("C1", "-2.7", "-1.65", "0", "in", "TOP", "False"),
                ("J1", "", "-2.220446049250313E-16", "90", "", "TOP", "False"),
            ],
        )
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert (
            e.str_itr()[0]
            == "Update parts locations error: Invalid part location 1: Missing location units"
        )

    try:
        parts.update_parts_locations(
            "Test",
            "Card",
            [
                ("C1", "-2.7", "-1.65", "Invalid", "in", "TOP", "False"),
                ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
            ],
        )
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert e.str_itr()[0] == (
            "Update parts locations error: Invalid part location 0: "
            "Invalid location rotation specified"
        )

    try:
        parts.update_parts_locations(
            "Test",
            "Card",
            [
                ("C1", "-2.7", "-1.65", "0", "in", "TOP", "False"),
                ("J1", "-3.55", "-2.220446049250313E-16", "400", "in", "TOP", "False"),
            ],
        )
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert e.str_itr()[0] == (
            "Update parts locations error: Invalid part location 1: "
            "Invalid location rotation specified"
        )

    if parts._is_connection_up():
        try:
            parts.update_parts_locations(
                "Test",
                "Card",
                [
                    ("C1", "-2.7", "-1.65", "0", "in", "Invalid", "False"),
                    ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
                ],
            )
            assert False
        except SherlockUpdatePartsLocationsError as e:
            assert e.str_itr()[0] == (
                "Update parts locations error: Invalid part location 0: "
                "Invalid location board side specified"
            )

    try:
        parts.update_parts_locations(
            "Test",
            "Card",
            [
                ("C1", "-2.7", "-1.65", "0", "in", "TOP", "Invalid"),
                ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
            ],
        )
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert e.str_itr()[0] == (
            "Update parts locations error: Invalid part location 0: "
            "Invalid location mirrored specified"
        )


def helper_test_update_parts_locations_by_file(parts):
    """Test update_parts_locations_by_file API."""

    try:
        parts.update_parts_locations_by_file(
            "",
            "Card",
            "Parts Locations.csv",
        )
        assert False
    except SherlockUpdatePartsLocationsByFileError as e:
        assert e.str_itr()[0] == "Update parts locations by file error: Invalid project name"

    try:
        parts.update_parts_locations_by_file(
            "Test",
            "",
            "Parts Locations.csv",
        )
        assert False
    except SherlockUpdatePartsLocationsByFileError as e:
        assert e.str_itr()[0] == "Update parts locations by file error: Invalid cca name"

    try:
        parts.update_parts_locations_by_file(
            "Test",
            "Card",
            "Invalid",
        )
        assert False
    except SherlockUpdatePartsLocationsByFileError as e:
        assert e.str_itr()[0] == "Update parts locations by file error: Invalid file path"


def helper_test_import_parts_list(parts):
    """Tests import_parts_list API."""
    try:
        parts.import_parts_list(
            "",
            "Card",
            "Parts List.csv",
            True,
        )
        assert False
    except SherlockImportPartsListError as e:
        assert str(e) == "Import parts list error: Invalid project name"

    try:
        parts.import_parts_list(
            "Test",
            "",
            "Parts List.csv",
            True,
        )
        assert False
    except SherlockImportPartsListError as e:
        assert str(e) == "Import parts list error: Invalid cca name"

    try:
        parts.import_parts_list(
            "Test",
            "Card",
            "Invalid",
            True,
        )
        assert False
    except SherlockImportPartsListError as e:
        assert str(e) == "Import parts list error: Invalid file path"


if __name__ == "__main__":
    test_all()
