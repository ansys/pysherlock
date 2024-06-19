# © 2023 ANSYS, Inc. All rights reserved.

"""Module containing types for the Parts Service."""

# import warnings

try:
    import SherlockCommonService_pb2
    import SherlockPartsService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockCommonService_pb2, SherlockPartsService_pb2


class PartsListSearchMatchingMode:
    """Constants for Matching Mode in the Update Parts List and Update Parts from AVL request."""

    # def deprecation(message):
    #     warnings.warn(message, DeprecationWarning, stacklevel=2)

    # TODO: JM remove this enum from common_types.py
    #          change examples to use the string values directly

    # TODO: JM this isn't working
    # def __getattribute__(self, item):
    #     # if item == 'BOTH':
    #     message = (
    #         "PartsListSearchMatchingMode is deprecated in parts_types.py. Use the string values."
    #     )
    #     warnings.warn(message, DeprecationWarning, stacklevel=2)
    #
    #     return type.__getattribute__(self, item)

    BOTH = SherlockCommonService_pb2.MatchingMode.Both
    """Both"""
    PART = SherlockCommonService_pb2.MatchingMode.Part
    """Part"""


class PartsListSearchDuplicationMode:
    """Constants for Duplication Mode in the Update Parts List and Update Parts from AVL request."""

    FIRST = SherlockPartsService_pb2.DuplicationMode.First
    """First"""
    ERROR = SherlockPartsService_pb2.DuplicationMode.Error
    """Error"""
    IGNORE = SherlockPartsService_pb2.DuplicationMode.Ignore
    """Ignore"""


class AVLPartNum:
    """Constants for AVLPartNum in the Update Parts List from AVL request."""

    ASSIGN_INTERNAL_PART_NUM = SherlockPartsService_pb2.AVLPartNum.AssignInternalPartNum
    """AssignInternalPartNum"""
    ASSIGN_VENDOR_AND_PART_NUM = SherlockPartsService_pb2.AVLPartNum.AssignVendorAndPartNum
    """AssignVendorAndPartNum"""
    DO_NOT_CHANGE_VENDOR_OR_PART_NUM = (
        SherlockPartsService_pb2.AVLPartNum.DoNotChangeVendorOrPartNum
    )
    """DoNotChangeVendorOrPartNum"""


class AVLDescription:
    """Constants for AVLDescription in the Update Parts List from AVL request."""

    ASSIGN_APPROVED_DESCRIPTION = SherlockPartsService_pb2.AVLDescription.AssignApprovedDescription
    """AssignApprovedDescription"""
    DO_NOT_CHANGE_DESCRIPTION = SherlockPartsService_pb2.AVLDescription.DoNotChangeDescription
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
