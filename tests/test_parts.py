# Copyright (c) 2023 ANSYS, Inc. and/or its affiliates.

import grpc

from ansys.sherlock.core.errors import (
    SherlockEnableLeadModelingError,
    SherlockExportPartsListError,
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
    helper_test_export_parts_list(parts)
    helper_test_enable_lead_modeling(parts)


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
        assert e.str_itr()[0] == "Update parts list error: Project name is invalid."

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
        assert e.str_itr()[0] == "Update parts list error: CCA name is invalid."

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
        assert e.str_itr()[0] == "Update parts list error: Parts library is invalid."

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
        assert e.str_itr()[0] == "Update parts list error: Matching argument is invalid."

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
        assert e.str_itr()[0] == "Update parts list error: Duplication argument is invalid."


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
        assert e.str_itr()[0] == "Update parts locations error: Project name is invalid."

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
        assert e.str_itr()[0] == "Update parts locations error: CCA name is invalid."

    try:
        parts.update_parts_locations("Test", "Card", "Invalid")
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert e.str_itr()[0] == "Update parts locations error: Part location argument is invalid."

    try:
        parts.update_parts_locations("Test", "Card", [])
        assert False
    except SherlockUpdatePartsLocationsError as e:
        assert e.str_itr()[0] == "Update parts locations error: Part location properties " \
                                 "are missing."

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
            == "Update parts locations error: Invalid part location 0: Number of fields is invalid."
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
            == "Update parts locations error: Invalid part location 1: Reference designator " \
                "is missing."
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
                "Invalid part location 0: Location units are invalid."
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
            == "Update parts locations error: Invalid part location 0: Location units are missing."
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
            "Location X coordinate is invalid."
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
            "Location Y coordinate is invalid."
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
            == "Update parts locations error: Invalid part location 1: Location units are missing."
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
            "Location rotation is invalid."
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
            "Location rotation is invalid."
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
                "Location board side is invalid."
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
            "Location mirrored is invalid."
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
        assert e.str_itr()[0] == "Update parts locations by file error: Project name is invalid."

    try:
        parts.update_parts_locations_by_file(
            "Test",
            "",
            "Parts Locations.csv",
        )
        assert False
    except SherlockUpdatePartsLocationsByFileError as e:
        assert e.str_itr()[0] == "Update parts locations by file error: CCA name is invalid."

    try:
        parts.update_parts_locations_by_file(
            "Test",
            "Card",
            "Invalid",
        )
        assert False
    except SherlockUpdatePartsLocationsByFileError as e:
        assert e.str_itr()[0] == "Update parts locations by file error: File path is invalid."


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
        assert str(e) == "Import parts list error: Project name is invalid."

    try:
        parts.import_parts_list(
            "Test",
            "",
            "Parts List.csv",
            True,
        )
        assert False
    except SherlockImportPartsListError as e:
        assert str(e) == "Import parts list error: CCA name is invald."

    try:
        parts.import_parts_list(
            "Test",
            "Card",
            "Invalid",
            True,
        )
        assert False
    except SherlockImportPartsListError as e:
        assert str(e) == "Import parts list error: File path is invalid."


def helper_test_export_parts_list(parts):
    """Tests export_parts_list API."""
    try:
        parts.export_parts_list(
            "",
            "Card",
            "Parts List.csv",
        )
        assert False
    except SherlockExportPartsListError as e:
        assert str(e) == "Export parts list error: Project name is invalid."

    try:
        parts.export_parts_list(
            "Test",
            "",
            "Parts List.csv",
        )
        assert False
    except SherlockExportPartsListError as e:
        assert str(e) == "Export parts list error: CCA name is invalid."

    try:
        parts.export_parts_list(
            "Test",
            "Card",
            "C:Invalid/Invalid",
        )
        assert False
    except SherlockExportPartsListError as e:
        assert str(e) == "Export parts list error: Export file directory does not exist."


def helper_test_enable_lead_modeling(parts):
    """Test enable_lead_modelign API."""
    try:
        parts.enable_lead_modeling(
            "",
            "Card",
        )
        assert False
    except SherlockEnableLeadModelingError as e:
        assert str(e) == "Enable lead modeling error: Project name is invalid."

    try:
        parts.enable_lead_modeling(
            "Test",
            "",
        )
        assert False
    except SherlockEnableLeadModelingError as e:
        assert str(e) == "Enable lead modeling error: CCA name is invalid."


if __name__ == "__main__":
    test_all()
