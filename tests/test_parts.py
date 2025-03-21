# Copyright (C) 2023-2025 ANSYS, Inc. and/or its affiliates.

import os
import platform

import grpc
import pydantic
import pytest

from ansys.sherlock.core.errors import (
    SherlockEnableLeadModelingError,
    SherlockExportNetListError,
    SherlockExportPartsListError,
    SherlockGetPartLocationError,
    SherlockImportPartsListError,
    SherlockNoGrpcConnectionException,
    SherlockUpdatePartsFromAVLError,
    SherlockUpdatePartsListError,
    SherlockUpdatePartsListPropertiesError,
    SherlockUpdatePartsLocationsByFileError,
    SherlockUpdatePartsLocationsError,
)
from ansys.sherlock.core.parts import Parts
from ansys.sherlock.core.types.common_types import TableDelimiter
from ansys.sherlock.core.types.parts_types import (
    AVLDescription,
    AVLPartNum,
    DeletePartsFromPartsListRequest,
    GetPartsListPropertiesRequest,
    PartsListSearchDuplicationMode,
    UpdatePadPropertiesRequest,
)
from ansys.sherlock.core.utils.version_check import SKIP_VERSION_CHECK


def test_all():
    """Test all parts APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    parts = Parts(channel, SKIP_VERSION_CHECK)

    helper_test_update_parts_list(parts)
    helper_test_update_parts_list_properties(parts)
    helper_test_update_parts_from_AVL(parts)
    helper_test_update_parts_locations(parts)
    helper_test_update_parts_locations_by_file(parts)
    helper_test_import_parts_list(parts)
    helper_test_export_parts_list(parts)
    helper_test_export_net_list(parts)
    helper_test_enable_lead_modeling(parts)
    helper_test_get_part_location(parts)
    helper_test_get_parts_list_properties(parts)
    helper_test_update_pad_properties(parts)


def helper_test_update_parts_list(parts: Parts):
    """Test update_parts_list API."""

    if parts._is_connection_up():
        try:
            result = parts.update_parts_list(
                "Tutorial Project",
                "Main Board",
                "Sherlock Part Library",
                "Both",
                PartsListSearchDuplicationMode.ERROR,
            )
            assert result == 0
        except Exception as e:
            pytest.fail(e.message)

        try:
            parts.update_parts_list(
                "Tutorial Project",
                "Invalid CCA",
                "Sherlock Part Library",
                "Both",
                PartsListSearchDuplicationMode.ERROR,
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockUpdatePartsListError

    try:
        parts.update_parts_list(
            "",
            "Card",
            "Sherlock Part Library",
            "Both",
            PartsListSearchDuplicationMode.ERROR,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListError as e:
        assert str(e.str_itr()) == "['Update parts list error: Project name is invalid.']"

    try:
        parts.update_parts_list(
            "Test",
            "",
            "Sherlock Part Library",
            "Both",
            PartsListSearchDuplicationMode.ERROR,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListError as e:
        assert str(e.str_itr()) == "['Update parts list error: CCA name is invalid.']"

    try:
        parts.update_parts_list(
            "Test",
            "Card",
            "",
            "Both",
            PartsListSearchDuplicationMode.ERROR,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListError as e:
        assert str(e.str_itr()) == "['Update parts list error: Parts library is invalid.']"


def helper_test_update_parts_from_AVL(parts: Parts):
    try:
        parts.update_parts_from_AVL(
            project="",
            cca_name="Main Board",
            matching_mode="Both",
            duplication_mode=PartsListSearchDuplicationMode.FIRST,
            avl_part_num=AVLPartNum.ASSIGN_INTERNAL_PART_NUM,
            avl_description=AVLDescription.ASSIGN_APPROVED_DESCRIPTION,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsFromAVLError as e:
        assert e.message == "Project name is invalid."

    try:
        parts.update_parts_from_AVL(
            project="Tutorial Project",
            cca_name="",
            matching_mode="Both",
            duplication_mode=PartsListSearchDuplicationMode.FIRST,
            avl_part_num=AVLPartNum.ASSIGN_INTERNAL_PART_NUM,
            avl_description=AVLDescription.ASSIGN_APPROVED_DESCRIPTION,
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsFromAVLError as e:
        assert e.message == "CCA name is invalid."

    if parts._is_connection_up():
        try:
            response = parts.update_parts_from_AVL(
                project="Tutorial Project",
                cca_name="Main Board",
                matching_mode="Both",
                duplication_mode=PartsListSearchDuplicationMode.FIRST,
                avl_part_num=AVLPartNum.ASSIGN_INTERNAL_PART_NUM,
                avl_description=AVLDescription.ASSIGN_APPROVED_DESCRIPTION,
            )

            assert response.returnCode.value == 0
        except SherlockUpdatePartsFromAVLError as e:
            pytest.fail(e.message)


def helper_test_update_parts_locations(parts: Parts):
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


def helper_test_update_parts_locations_by_file(parts: Parts):
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


def helper_test_import_parts_list(parts: Parts):
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


def helper_test_export_parts_list(parts: Parts):
    """Tests export_parts_list API."""
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

    try:
        parts.export_parts_list(
            "Test",
            "Card",
            "",
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportPartsListError as e:
        assert str(e) == "Export parts list error: Export filepath is required."

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


def helper_test_enable_lead_modeling(parts: Parts):
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


def helper_test_get_part_location(parts: Parts):
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


def helper_test_get_parts_list_properties(parts: Parts):
    """Test get_parts_list_properties API"""
    try:
        GetPartsListPropertiesRequest(project="", cca_name="CCA Name")
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            e.errors()[0]["msg"] == "Value error, project is invalid because it is None or empty."
        )

    try:
        GetPartsListPropertiesRequest(project="Project Name", cca_name="")
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            e.errors()[0]["msg"] == "Value error, cca_name is invalid because it is None or empty."
        )

    if not parts._is_connection_up():
        try:
            responses = parts.get_parts_list_properties(
                GetPartsListPropertiesRequest(project="Tutorial Project", cca_name="Invalid CCA")
            )
            pytest.fail("No exception raised when using an invalid parameter")
        except Exception as e:
            assert type(e) == SherlockNoGrpcConnectionException
        return

    # test error case
    responses = parts.get_parts_list_properties(
        GetPartsListPropertiesRequest(project="Tutorial Project", cca_name="Invalid CCA")
    )
    assert type(responses) == list
    assert len(responses) == 1
    assert responses[0].returnCode.value == -1
    assert responses[0].returnCode.message == "Cannot find CCA: Invalid CCA"

    # test all parts returned when no refDes is provided
    responses = parts.get_parts_list_properties(
        GetPartsListPropertiesRequest(project="Tutorial Project", cca_name="Main Board")
    )
    assert len(responses) == 221
    for response in responses:
        assert response.returnCode.value == 0
        assert response.returnCode.message == ""

    # test only specified parts are returned when refDes is provided
    responses = parts.get_parts_list_properties(
        GetPartsListPropertiesRequest(
            project="Tutorial Project", cca_name="Main Board", reference_designators=["C1", "U9"]
        )
    )
    assert len(responses) == 2
    for response in responses:
        assert response.returnCode.value == 0
        assert response.returnCode.message == ""
    assert responses[0].refDes == "C1"
    assert len(responses[0].properties) == 61
    assert responses[1].refDes == "U9"
    assert len(responses[1].properties) == 64


def helper_test_update_parts_list_properties(parts: Parts):
    """Test update_parts_list_properties API"""
    try:
        parts.update_parts_list_properties(
            "",
            "CCA_Name",
            [
                {
                    "reference_designators": ["C1"],
                    "properties": [{"name": "partType", "value": "RESISTOR"}],
                }
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListPropertiesError as e:
        assert str(e.str_itr()) == (
            "['Update parts list properties error: Project name is invalid.']"
        )

    try:
        parts.update_parts_list_properties(
            "Test",
            "",
            [
                {
                    "reference_designators": ["C1"],
                    "properties": [{"name": "partType", "value": "RESISTOR"}],
                }
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListPropertiesError as e:
        assert str(e.str_itr()) == "['Update parts list properties error: CCA name is invalid.']"

    try:
        parts.update_parts_list_properties("Test", "CCA_Name", [])
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListPropertiesError as e:
        assert str(e.str_itr()) == (
            "['Update parts list properties error: Part properties are missing.']"
        )

    try:
        parts.update_parts_list_properties(
            "Test",
            "CCA_name",
            [
                {
                    "reference_designators": ["C1"],
                    "properties": [{"name": "partType", "value": "RESISTOR"}],
                    "test": "test",
                }
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListPropertiesError as e:
        assert str(e.str_itr()) == (
            "['Update parts list properties error: Number of elements (3) "
            "is wrong for part list property 0.']"
        )

    try:
        parts.update_parts_list_properties(
            "Test",
            "CCA_name",
            [
                {
                    "reference_designators": "C1",
                    "properties": [{"name": "partType", "value": "RESISTOR"}],
                }
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListPropertiesError as e:
        assert str(e.str_itr()) == (
            "['Update parts list properties error: reference_designators is not a list "
            "for parts list property 0.']"
        )

    try:
        parts.update_parts_list_properties(
            "Test",
            "CCA_name",
            [
                {
                    "reference_designators": ["C1"],
                    "properties": [{"name": "partType", "value": "RESISTOR", "test": "test"}],
                }
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListPropertiesError as e:
        assert str(e.str_itr()) == (
            "['Update parts list properties error: Number of elements (3) "
            "is wrong for property 0.']"
        )

    try:
        parts.update_parts_list_properties(
            "Test",
            "CCA_name",
            [{"reference_designators": ["C1"], "properties": [{"name": "", "value": "RESISTOR"}]}],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListPropertiesError as e:
        assert str(e.str_itr()) == (
            "['Update parts list properties error: Name is required for property 0.']"
        )

    try:
        parts.update_parts_list_properties(
            "Test",
            "CCA_name",
            [{"reference_designators": ["C1"], "properties": [{"name": "partType", "value": 0}]}],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockUpdatePartsListPropertiesError as e:
        assert str(e.str_itr()) == ("['Update parts list properties error: Value is invalid.']")

    if not parts._is_connection_up():
        return

    try:
        parts.update_parts_list_properties(
            "Invalid project",
            "CCA_name",
            [
                {
                    "reference_designators": ["C1"],
                    "properties": [{"name": "partType", "value": "RESISTOR"}],
                }
            ],
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert type(e) == SherlockUpdatePartsListPropertiesError

    try:
        result = parts.update_parts_list_properties(
            "Tutorial Project",
            "Main Board",
            [
                {
                    "reference_designators": ["C1"],
                    "properties": [{"name": "partType", "value": "RESISTOR"}],
                }
            ],
        )

        assert result == 0

    except Exception as e:
        pytest.fail(e.message)


def helper_test_export_net_list(parts: Parts):
    """Test export_net_list API"""

    try:
        parts.export_net_list("", "Demos", "Net List.csv")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportNetListError as e:
        assert str(e) == "Export net list error: Project name is invalid."

    try:
        parts.export_net_list("Test", "", "Net List.csv")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportNetListError as e:
        assert str(e) == "Export net list error: CCA name is invalid."

    try:
        parts.export_net_list("Test", "Demos", "")
        pytest.fail("No exception raised when using an invalid parameter")
    except SherlockExportNetListError as e:
        assert str(e) == "Export net list error: Output file path is required."

    if parts._is_connection_up():
        try:
            parts.export_net_list(
                "Test",
                "Demos",
                "Missing Net List.csv",
                col_delimiter=TableDelimiter.TAB,
                overwrite_existing=True,
                utf8_enabled=True,
            )
        except SherlockExportNetListError as e:
            assert type(e) == SherlockExportNetListError


def helper_test_update_pad_properties(parts: Parts):
    """Test update pad properties API."""
    try:
        UpdatePadPropertiesRequest(
            project="", cca_name="Main Board", reference_designators=["C1", "C2", "C3"]
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            e.errors()[0]["msg"] == "Value error, project is invalid because it is None or empty."
        )

    try:
        UpdatePadPropertiesRequest(
            project="Test", cca_name="", reference_designators=["C1", "C2", "C3"]
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            e.errors()[0]["msg"] == "Value error, cca_name is invalid because it is None or empty."
        )

    try:
        request = UpdatePadPropertiesRequest(
            project="Invalid project", cca_name="Main Board", reference_designators=["C1", "C2"]
        )

        if parts._is_connection_up():
            responses = parts.update_pad_properties(request)

            assert len(responses) == 1, "Expected exactly one response in the list"
            assert responses[0].returnCode.value == -1
            assert responses[0].returnCode.message == f"Cannot find project: {request.project}"

            request.project = "Tutorial Project"
            responses = parts.update_pad_properties(request)
            responses = list(responses)

            assert len(responses) == len(
                request.reference_designators
            ), "Mismatch between responses and reference designators"
            for res in responses:
                assert res.returnCode.value == 0
                assert res.refDes in request.reference_designators
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")


def helper_test_delete_parts_from_parts_list(parts: Parts):
    """Test delete parts from parts list API."""
    try:
        DeletePartsFromPartsListRequest(
            project="", cca_name="Main Board", reference_designators=["C1", "C2", "C3"]
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            e.errors()[0]["msg"] == "Value error, project is invalid because it is None or empty."
        )

    try:
        DeletePartsFromPartsListRequest(
            project="Test", cca_name="", reference_designators=["C1", "C2", "C3"]
        )
        pytest.fail("No exception raised when using an invalid parameter")
    except Exception as e:
        assert isinstance(e, pydantic.ValidationError)
        assert (
            e.errors()[0]["msg"] == "Value error, cca_name is invalid because it is None or empty."
        )

    try:
        request = DeletePartsFromPartsListRequest(
            project="Invalid project", cca_name="Main Board", reference_designators=["C1", "C2"]
        )

        if parts._is_connection_up():
            responses = parts.delete_parts_from_parts_list(request)

            assert len(responses) == 1, "Expected exactly one response in the list"
            assert responses[0].returnCode.value == -1
            assert responses[0].returnCode.message == f"Cannot find project: {request.project}"

            request.project = "Tutorial Project"
            responses = parts.delete_parts_from_parts_list(request)
            responses = list(responses)

            assert len(responses) == len(
                request.reference_designators
            ), "Mismatch between responses and reference designators"
            for res in responses:
                assert res.returnCode.value == 0
                assert res.refDes in request.reference_designators
    except Exception as e:
        pytest.fail(f"Unexpected exception raised: {e}")


if __name__ == "__main__":
    test_all()
