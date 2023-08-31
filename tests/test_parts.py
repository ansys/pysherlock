# © 2023 ANSYS, Inc. All rights reserved

import os
import platform
import time

import grpc
import pytest

from ansys.sherlock.core.errors import (
    SherlockEnableLeadModelingError,
    SherlockExportPartsListError,
    SherlockGetPartAVLError,
    SherlockGetPartLocationError,
    SherlockImportPartsListError,
    SherlockUpdatePartsListError,
    SherlockUpdatePartsLocationsByFileError,
    SherlockUpdatePartsLocationsError,
)
from ansys.sherlock.core.parts import Parts
from ansys.sherlock.core.types.parts_types import (
    AVLDescription,
    AVLPartNum,
    UpdatesPartsListRequestDuplicationMode,
    UpdatesPartsListRequestMatchingMode,
)


def test_all():
    """Test all parts APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    parts = Parts(channel)

    helper_test_update_parts_list(parts)
    helper_test_update_parts_from_AVL(parts)
    helper_test_update_parts_locations(parts)
    helper_test_update_parts_locations_by_file(parts)
    helper_test_import_parts_list(parts)
    helper_test_export_parts_list(parts)
    helper_test_enable_lead_modeling(parts)
    helper_test_get_part_location(parts)


def helper_test_update_parts_list(parts):
    """Test update_parts_list API."""

    if parts._is_connection_up():
        try:
            result = parts.update_parts_list(
                "Tutorial Project",
                "Main Board",
                "Sherlock Part Library",
                UpdatesPartsListRequestMatchingMode.BOTH,
                UpdatesPartsListRequestDuplicationMode.ERROR,
            )
            assert result == 0
            # wait for Sherlock to finish updating so subsequent tests don't fail
            time.sleep(1)
        except Exception as e:
            pytest.fail(e.message)

        try:
            parts.update_parts_list(
                "Tutorial Project",
                "Invalid CCA",
                "Sherlock Part Library",
                UpdatesPartsListRequestMatchingMode.BOTH,
                UpdatesPartsListRequestDuplicationMode.ERROR,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdatePartsListError

    try:
        parts.update_parts_list(
            "",
            "Card",
            "Sherlock Part Library",
            UpdatesPartsListRequestMatchingMode.BOTH,
            UpdatesPartsListRequestDuplicationMode.ERROR,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListError as e:
        assert str(e.str_itr()) == "['Update parts list error: Project name is invalid.']"

    try:
        parts.update_parts_list(
            "Test",
            "",
            "Sherlock Part Library",
            UpdatesPartsListRequestMatchingMode.BOTH,
            UpdatesPartsListRequestDuplicationMode.ERROR,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListError as e:
        assert str(e.str_itr()) == "['Update parts list error: CCA name is invalid.']"

    try:
        parts.update_parts_list(
            "Test",
            "Card",
            "",
            UpdatesPartsListRequestMatchingMode.BOTH,
            UpdatesPartsListRequestDuplicationMode.ERROR,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListError as e:
        assert str(e.str_itr()) == "['Update parts list error: Parts library is invalid.']"


def helper_test_update_parts_from_AVL(parts):
    try:
        response = parts.update_parts_from_AVL(
            project="",
            cca_name="Main Board",
            matching_mode=UpdatesPartsListRequestMatchingMode.BOTH,
            duplication_mode=UpdatesPartsListRequestDuplicationMode.FIRST,
            avl_part_num=AVLPartNum.ASSIGN_INTERNAL_PART_NUM,
            avl_description=AVLDescription.ASSIGN_APPROVED_DESCRIPTION,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetPartAVLError as e:
        assert e.message == "Project name is invalid."

    try:
        response = parts.update_parts_from_AVL(
            project="Tutorial Project",
            cca_name="",
            matching_mode=UpdatesPartsListRequestMatchingMode.BOTH,
            duplication_mode=UpdatesPartsListRequestDuplicationMode.FIRST,
            avl_part_num=AVLPartNum.ASSIGN_INTERNAL_PART_NUM,
            avl_description=AVLDescription.ASSIGN_APPROVED_DESCRIPTION,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetPartAVLError as e:
        assert e.message == "CCA name is invalid."

    try:
        response = parts.update_parts_from_AVL(
            project="Tutorial Project",
            cca_name="Main Board",
            matching_mode="BOTH",
            duplication_mode=UpdatesPartsListRequestDuplicationMode.ERROR,
            avl_part_num=AVLPartNum.ASSIGN_INTERNAL_PART_NUM,
            avl_description=AVLDescription.ASSIGN_APPROVED_DESCRIPTION,
        )
    except Exception as e:
        # The matching_mode should not be a string
        assert type(e) == ValueError

    try:
        response = parts.update_parts_from_AVL(
            project="Tutorial Project",
            cca_name="Main Board",
            matching_mode=UpdatesPartsListRequestMatchingMode.BOTH,
            duplication_mode="ERROR",
            avl_part_num=AVLPartNum.ASSIGN_INTERNAL_PART_NUM,
            avl_description=AVLDescription.ASSIGN_APPROVED_DESCRIPTION,
        )
    except Exception as e:
        # The duplication should not be a string
        assert type(e) == ValueError

    try:
        response = parts.update_parts_from_AVL(
            project="Tutorial Project",
            cca_name="Main Board",
            matching_mode=UpdatesPartsListRequestMatchingMode.BOTH,
            duplication_mode=UpdatesPartsListRequestDuplicationMode.ERROR,
            avl_part_num="AssignInternalPartNum",
            avl_description=AVLDescription.ASSIGN_APPROVED_DESCRIPTION,
        )
    except Exception as e:
        # The avl_part_num should not be a string
        assert type(e) == ValueError

    try:
        response = parts.update_parts_from_AVL(
            project="Tutorial Project",
            cca_name="Main Board",
            matching_mode=UpdatesPartsListRequestMatchingMode.BOTH,
            duplication_mode=UpdatesPartsListRequestDuplicationMode.ERROR,
            avl_part_num=AVLPartNum.ASSIGN_INTERNAL_PART_NUM,
            avl_description="AssignApprovedDescription",
        )
    except Exception as e:
        # The avl_description should not be a string
        assert type(e) == ValueError

    if parts._is_connection_up():
        try:
            response = parts.update_parts_from_AVL(
                project="Tutorial Project",
                cca_name="Main Board",
                matching_mode=UpdatesPartsListRequestMatchingMode.BOTH,
                duplication_mode=UpdatesPartsListRequestDuplicationMode.FIRST,
                avl_part_num=AVLPartNum.ASSIGN_INTERNAL_PART_NUM,
                avl_description=AVLDescription.ASSIGN_APPROVED_DESCRIPTION,
            )

            assert response.returnCode.value == 0
        except SherlockGetPartAVLError as e:
            pytest.fail(e.message)


def helper_test_update_parts_locations(parts):
    """Test update_parts_locations API."""

    if parts._is_connection_up():
        try:
            parts.update_parts_locations(
                "Tutorial Project",
                "Invalid CCA",
                [
                    ("C1", "-2.7", "-1.65", "0", "in", "TOP", "False"),
                    ("J1", "-3.55", "1", "90", "in", "TOP", "False"),
                ],
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdatePartsLocationsError

        try:
            result = parts.update_parts_locations(
                "Tutorial Project",
                "Main Board",
                [
                    ("C1", "-2.7", "-1.65", "0", "in", "TOP", "False"),
                    ("J1", "-3.55", "1", "90", "in", "TOP", "False"),
                ],
            )
            assert result == 0
        except SherlockUpdatePartsLocationsError as e:
            pytest.fail(e.message)

    try:
        parts.update_parts_locations(
            "",
            "Card",
            [
                ("C1", "-2.7", "-1.65", "60", "in", "TOP", "False"),
                ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert str(e.str_itr()) == "['Update parts locations error: Project name is invalid.']"

    try:
        parts.update_parts_locations(
            "Test",
            "",
            [
                ("C1", "-2.7", "-1.65", "0", "in", "TOP", "False"),
                ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert str(e.str_itr()) == "['Update parts locations error: CCA name is invalid.']"

    try:
        parts.update_parts_locations("Test", "Card", "Invalid")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert (
            str(e.str_itr()) == "['Update parts locations error: "
            "Part location argument is invalid.']"
        )

    try:
        parts.update_parts_locations("Test", "Card", [])
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert (
            str(e.str_itr()) == "['Update parts locations error: "
            "Part location properties are missing.']"
        )

    try:
        parts.update_parts_locations(
            "Test",
            "Card",
            [
                ("C1", "-2.7", "-1.65", "0", "TOP", "False"),
                ("J1", "-3.55", "-2.220446049250313E-16", "90", "in", "TOP", "False"),
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert (
            str(e.str_itr()) == "['Update parts locations error: "
            "Invalid part location 0: Number of fields is invalid.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert (
            str(e.str_itr()) == "['Update parts locations error: "
            "Invalid part location 1: Reference designator is missing.']"
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
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockUpdatePartsLocationsError as e:
            assert (
                str(e.str_itr()) == "['Update parts locations error: "
                "Invalid part location 0: Location units are invalid.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert (
            str(e.str_itr()) == "['Update parts locations error: "
            "Invalid part location 0: Location units are missing.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert (
            str(e.str_itr()) == "['Update parts locations error: "
            "Invalid part location 0: Location X coordinate is invalid.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert (
            str(e.str_itr()) == "['Update parts locations error: "
            "Invalid part location 1: Location Y coordinate is invalid.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert (
            str(e.str_itr()) == "['Update parts locations error: "
            "Invalid part location 1: Location units are missing.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert (
            str(e.str_itr()) == "['Update parts locations error: "
            "Invalid part location 0: Location rotation is invalid.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert (
            str(e.str_itr()) == "['Update parts locations error: "
            "Invalid part location 1: Location rotation is invalid.']"
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
            pytest.fail("No exception raised when using an invalid parameter")
        except SherlockUpdatePartsLocationsError as e:
            assert (
                str(e.str_itr()) == "['Update parts locations error: "
                "Invalid part location 0: Location board side is invalid.']"
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
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsError as e:
        assert (
            str(e.str_itr()) == "['Update parts locations error: "
            "Invalid part location 0: Location mirrored is invalid.']"
        )


def helper_test_update_parts_locations_by_file(parts):
    """Test update_parts_locations_by_file API."""

    if parts._is_connection_up():
        # happy path test missing because needs valid file
        try:
            parts.update_parts_locations_by_file(
                "Tutorial Project",
                "Main Board",
                "Invalid file path",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdatePartsLocationsByFileError

    try:
        parts.update_parts_locations_by_file(
            "",
            "Card",
            "Parts Locations.csv",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsByFileError as e:
        assert (
            str(e.str_itr()) == "['Update parts locations by file error: Project name is invalid.']"
        )

    try:
        parts.update_parts_locations_by_file(
            "Test",
            "",
            "Parts Locations.csv",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsLocationsByFileError as e:
        assert str(e.str_itr()) == "['Update parts locations by file error: CCA name is invalid.']"


def helper_test_import_parts_list(parts):
    """Tests import_parts_list API."""
    if parts._is_connection_up():
        # happy path test missing because needs valid file
        try:
            parts.import_parts_list(
                "Tutorial Project",
                "Main Board",
                "Invalid file path",
                False,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockImportPartsListError

    try:
        parts.import_parts_list(
            "",
            "Card",
            "Parts List.csv",
            True,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockImportPartsListError as e:
        assert str(e) == "Import parts list error: Project name is invalid."

    try:
        parts.import_parts_list(
            "Test",
            "",
            "Parts List.csv",
            True,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockImportPartsListError as e:
        assert str(e) == "Import parts list error: CCA name is invalid."


def helper_test_export_parts_list(parts):
    """Tests export_parts_list API."""
    if parts._is_connection_up():
        if platform.system() == "Windows":
            temp_dir = os.environ.get("TEMP", "C:\\TEMP")
        else:
            temp_dir = os.environ.get("TEMP", "/tmp")
        parts_list_file = os.path.join(temp_dir, "PySherlock unit test exported parts.csv")

        try:
            # use a CCA with not many parts so it finishes faster
            result = parts.export_parts_list(
                "AssemblyTutorial",
                "Memory Card 1",
                parts_list_file,
            )
            assert os.path.exists(parts_list_file)
            # may need to wait for a bit because the response may be returned
            # before Sherlock finishes writing the file
            time.sleep(0.5)
            assert result == 0
        except Exception as e:
            pytest.fail(e.message)
        finally:
            try:
                os.remove(parts_list_file)
            except Exception as e:
                print(str(e))

        try:
            parts.export_parts_list(
                "Tutorial Project",
                "Invalid CCA",
                parts_list_file,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockExportPartsListError

    try:
        parts.export_parts_list(
            "",
            "Card",
            "Parts List.csv",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportPartsListError as e:
        assert str(e) == "Export parts list error: Project name is invalid."

    try:
        parts.export_parts_list(
            "Test",
            "",
            "Parts List.csv",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportPartsListError as e:
        assert str(e) == "Export parts list error: CCA name is invalid."


def helper_test_enable_lead_modeling(parts):
    """Test enable_lead_modelign API."""
    if parts._is_connection_up():
        try:
            result = parts.enable_lead_modeling(
                "Tutorial Project",
                "Main Board",
            )
            assert result == 0
        except Exception as e:
            pytest.fail(e.message)

        try:
            parts.enable_lead_modeling(
                "Tutorial Project",
                "Invalid CCA",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockEnableLeadModelingError

    try:
        parts.enable_lead_modeling(
            "",
            "Card",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockEnableLeadModelingError as e:
        assert str(e) == "Enable lead modeling error: Project name is invalid."

    try:
        parts.enable_lead_modeling(
            "Test",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockEnableLeadModelingError as e:
        assert str(e) == "Enable lead modeling error: CCA name is invalid."


def helper_test_get_part_location(parts):
    """Test get_part_location API"""

    if parts._is_connection_up():
        try:
            parts.get_part_location(
                "Tutorial Project",
                "Invalid CCA",
                "C1",
                "in",
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockGetPartLocationError

        try:
            locations = parts.get_part_location(
                "Tutorial Project",
                "Main Board",
                "C1, C3",
                "in",
            )

            assert len(locations) == 2, "Incorrect number of locations"
            location_c1 = locations[0]
            assert location_c1.ref_des == "C1", "Incorrect refDes"
            assert location_c1.x == -2.7, "Incorrect X coordinate for C1"
            assert location_c1.y == -1.65, "Incorrect Y coordinate for C1"
            assert location_c1.rotation == 0, "Incorrect rotation for C1"
            assert location_c1.location_units == "in", "Incorrect location units for C1"
            assert location_c1.board_side == "TOP", "Incorrect board side for C1"
            assert location_c1.mirrored is False, "Incorrect mirrored for C1"

            location_c3 = locations[1]
            assert location_c3.ref_des == "C3", "Incorrect refDes"
            assert location_c3.x == -2.4, "Incorrect X coordinate for C3"
            assert location_c3.y == -1.9, "Incorrect Y coordinate for C3"
            assert location_c3.rotation == 180, "Incorrect rotation for C3"
            assert location_c3.location_units == "in", "Incorrect location units for C3"
            assert location_c3.board_side == "TOP", "Incorrect board side for C3"
            assert location_c3.mirrored is False, "Incorrect mirrored for C3"

        except SherlockGetPartLocationError as e:
            pytest.fail(e.message)

    try:
        parts.get_part_location(
            "",
            "Card",
            "C1",
            "in",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetPartLocationError as e:
        assert str(e) == "Get part location error: Project name is invalid."

    try:
        parts.get_part_location(
            "Test",
            "",
            "C1",
            "in",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetPartLocationError as e:
        assert str(e) == "Get part location error: CCA name is invalid."

    try:
        parts.get_part_location(
            "Test",
            "Card",
            "",
            "in",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetPartLocationError as e:
        assert str(e) == "Get part location error: Ref Des is invalid."

    try:
        parts.get_part_location(
            "Test",
            "Card",
            "C1",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockGetPartLocationError as e:
        assert str(e) == "Get part location error: Location unit is invalid."


if __name__ == "__main__":
    test_all()
