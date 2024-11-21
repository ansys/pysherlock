# Copyright (C) 2023-2024 ANSYS, Inc. and/or its affiliates.

"""Module containing types for the Parts Service."""

import warnings

try:
    import SherlockCommonService_pb2
    import SherlockPartsService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2, SherlockPartsService_pb2


def deprecation(cls: object):
    """Raise a DeprecationWarning when a deprecated class is used."""
    # if str(cls).find("PartsListSearchMatchingMode") != -1:
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


class PartLocation:
    """Part Location property values."""

    def __init__(self, location):
        """Initialize members from the location."""
        self.x = location.x
        """x coordinate"""
        self.y = location.y
        """y coordinate"""
        self.rotation = location.rotation
        """rotation (in degrees)"""
        self.location_units = location.locationUnits
        """units for location coordinates"""
        self.board_side = location.boardSide
        """board side - ``"TOP"`` or ``"BOTTOM"`` """
        self.mirrored = location.mirrored
        """mirrored - ``True`` or ``False`` """
        self.ref_des = location.refDes
        """reference designator"""
