# Copyright (C) 2021 - 2026 ANSYS, Inc. and/or its affiliates.

"""Module containing types for the Parts Service."""

from typing import List, Optional
import warnings

from pydantic import BaseModel, field_validator

from ansys.sherlock.core.types.common_types import basic_str_validator

try:
    import SherlockCommonService_pb2
    import SherlockPartsService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2, SherlockPartsService_pb2

parts_service = SherlockPartsService_pb2


def deprecation(cls: object):
    """Raise a DeprecationWarning when a deprecated class is used."""
    message = f"{cls} is deprecated. Use a string with the value of the constant name \
    as defined in the proto file."
    warnings.warn(message, DeprecationWarning, stacklevel=2)
    return cls


@deprecation
class PartsListSearchMatchingMode:
    """DEPRECATED. Constants for Matching Mode in Update Parts List & Update Parts from AVL."""

    matching_mode = SherlockCommonService_pb2.MatchingMode
    BOTH = matching_mode.Both
    """Both"""
    PART = matching_mode.Part
    """Part"""


class PartsListSearchDuplicationMode:
    """Constants for Duplication Mode in Update Parts List and Update Parts from AVL request."""

    duplication_mode = SherlockPartsService_pb2.DuplicationMode
    FIRST = duplication_mode.First
    """First"""
    ERROR = duplication_mode.Error
    """Error"""
    IGNORE = duplication_mode.Ignore
    """Ignore"""


class AVLPartNum:
    """Constants for AVLPartNum in the Update Parts List from AVL request."""

    avl_part_num = SherlockPartsService_pb2.AVLPartNum
    ASSIGN_INTERNAL_PART_NUM = avl_part_num.AssignInternalPartNum
    """AssignInternalPartNum"""
    ASSIGN_VENDOR_AND_PART_NUM = avl_part_num.AssignVendorAndPartNum
    """AssignVendorAndPartNum"""
    DO_NOT_CHANGE_VENDOR_OR_PART_NUM = avl_part_num.DoNotChangeVendorOrPartNum
    """DoNotChangeVendorOrPartNum"""


class AVLDescription:
    """Constants for AVLDescription in the Update Parts List from AVL request."""

    avl_description = SherlockPartsService_pb2.AVLDescription
    ASSIGN_APPROVED_DESCRIPTION = avl_description.AssignApprovedDescription
    """AssignApprovedDescription"""
    DO_NOT_CHANGE_DESCRIPTION = avl_description.DoNotChangeDescription
    """DoNotChangeDescription"""


class GetPartsListPropertiesRequest(BaseModel):
    """Request for getting properties of parts in the parts list of a CCA."""

    project: str
    """Name of the Sherlock project."""
    cca_name: str
    """Name of the CCA with the parts."""
    reference_designators: Optional[List[str]] = None
    """Reference designators of the parts to retrieve properties for. Use None to get all parts."""

    @field_validator("project", "cca_name")
    @classmethod
    def str_validation(cls, value: str, info):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> SherlockPartsService_pb2.GetPartsListPropertiesRequest:
        return SherlockPartsService_pb2.GetPartsListPropertiesRequest(
            project=self.project,
            ccaName=self.cca_name,
            refDes=self.reference_designators,
        )


class UpdatePadPropertiesRequest(BaseModel):
    """Contains the properties to update pad properties for one or more parts in a parts list."""

    project: str
    """Name of the Sherlock project."""
    cca_name: str
    """Name of the CCA for which pad properties will be updated."""
    reference_designators: Optional[List[str]] = None
    """Reference designators of the associated parts to be updated."""

    @field_validator("project", "cca_name")
    @classmethod
    def str_validation(cls, value: str, info):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> parts_service.UpdatePadPropertiesRequest:
        return parts_service.UpdatePadPropertiesRequest(
            project=self.project,
            ccaName=self.cca_name,
            refDes=self.reference_designators,
        )


class DeletePartsFromPartsListRequest(BaseModel):
    """Contains the information to delete parts from the parts list for a given project's CCA."""

    project: str
    """Name of the Sherlock project."""
    cca_name: str
    """Name of the CCA for which parts will be deleted."""
    reference_designators: Optional[List[str]] = None
    """Reference designators of the associated parts to be deleted."""

    @field_validator("project", "cca_name")
    @classmethod
    def str_validation(cls, value: str, info):
        """Validate string fields listed."""
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> parts_service.DeletePartsFromPartsListRequest:
        return parts_service.DeletePartsFromPartsListRequest(
            project=self.project,
            ccaName=self.cca_name,
            refDes=self.reference_designators,
        )


class ImportPartsToAVLRequest(BaseModel):
    """Request to import parts into the Approved Vendor List (AVL)."""

    import_file: str
    """Full file path to the AVL file."""

    import_type: parts_service.AVLImportType.ValueType
    """Import mode to use for AVL data."""

    """Allow non-standard types like Protobuf enums in Pydantic models."""
    model_config = {"arbitrary_types_allowed": True}

    @field_validator("import_file")
    @classmethod
    def import_file_validator(cls, value: str, info):
        """Validate that the import file path is not empty."""
        if value.strip() == "":
            raise ValueError(f"{info.field_name} cannot be empty.")
        return basic_str_validator(value, info.field_name)

    def _convert_to_grpc(self) -> parts_service.ImportPartsToAVLRequest:
        request = parts_service.ImportPartsToAVLRequest()
        request.importFile = self.import_file
        request.importType = self.import_type
        return request
