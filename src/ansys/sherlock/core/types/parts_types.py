# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module containing types for the Parts Service."""

from typing import List, Optional

from ansys.api.sherlock.v0 import SherlockCommonService_pb2
from ansys.api.sherlock.v0 import SherlockPartsService_pb2 as PartsService
from pydantic import BaseModel, field_validator

from ansys.sherlock.core.types.common_types import basic_str_validator, deprecation


@deprecation("27.1")
class PartsListSearchMatchingMode:
    """DEPRECATED. Constants for Matching Mode in Update Parts List & Update Parts from AVL."""

    matching_mode = SherlockCommonService_pb2.MatchingMode
    BOTH = matching_mode.Both
    """Both"""
    PART = matching_mode.Part
    """Part"""


@deprecation("27.1")
class PartsListSearchDuplicationMode:
    """Constants for Duplication Mode in Update Parts List and Update Parts from AVL request."""

    duplication_mode = PartsService.DuplicationMode
    FIRST = duplication_mode.First
    """First"""
    ERROR = duplication_mode.Error
    """Error"""
    IGNORE = duplication_mode.Ignore
    """Ignore"""


@deprecation("27.1")
class AVLPartNum:
    """Constants for AVLPartNum in the Update Parts List from AVL request."""

    avl_part_num = PartsService.AVLPartNum
    ASSIGN_INTERNAL_PART_NUM = avl_part_num.AssignInternalPartNum
    """AssignInternalPartNum"""
    ASSIGN_VENDOR_AND_PART_NUM = avl_part_num.AssignVendorAndPartNum
    """AssignVendorAndPartNum"""
    DO_NOT_CHANGE_VENDOR_OR_PART_NUM = avl_part_num.DoNotChangeVendorOrPartNum
    """DoNotChangeVendorOrPartNum"""


@deprecation("27.1")
class AVLDescription:
    """Constants for AVLDescription in the Update Parts List from AVL request."""

    avl_description = PartsService.AVLDescription
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

    def _convert_to_grpc(self) -> PartsService.GetPartsListPropertiesRequest:
        return PartsService.GetPartsListPropertiesRequest(
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

    def _convert_to_grpc(self) -> PartsService.UpdatePadPropertiesRequest:
        return PartsService.UpdatePadPropertiesRequest(
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

    def _convert_to_grpc(self) -> PartsService.DeletePartsFromPartsListRequest:
        return PartsService.DeletePartsFromPartsListRequest(
            project=self.project,
            ccaName=self.cca_name,
            refDes=self.reference_designators,
        )


class ImportPartsToAVLRequest(BaseModel):
    """Request to import parts into the Approved Vendor List (AVL)."""

    import_file: str
    """Full file path to the AVL file."""

    import_type: PartsService.AVLImportType.ValueType
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

    def _convert_to_grpc(self) -> PartsService.ImportPartsToAVLRequest:
        request = PartsService.ImportPartsToAVLRequest()
        request.importFile = self.import_file
        request.importType = self.import_type
        return request
