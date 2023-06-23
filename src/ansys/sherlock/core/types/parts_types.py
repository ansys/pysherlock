# © 2023 ANSYS, Inc. All rights reserved.

"""Module containing types for the Parts Service."""

try:
    import SherlockPartsService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockPartsService_pb2


class UpdatesPartsListRequestMatchingMode:
    """Constants for Matching Mode in the Update Parts List request."""

    BOTH = SherlockPartsService_pb2.UpdatePartsListRequest.MatchingMode.Both
    PART = SherlockPartsService_pb2.UpdatePartsListRequest.MatchingMode.Part


class UpdatesPartsListRequestDuplicationMode:
    """Constants for Duplication Mode in the Update Parts List request."""

    FIRST = SherlockPartsService_pb2.UpdatePartsListRequest.DuplicationMode.First
    ERROR = SherlockPartsService_pb2.UpdatePartsListRequest.DuplicationMode.Error
    IGNORE = SherlockPartsService_pb2.UpdatePartsListRequest.DuplicationMode.Ignore


class PartLocation:
    """Part Location property values."""

    def __init__(self, location):
        """Initialize members from the location."""
        self.x = location.x
        """x coordinate"""
        self.y = location.y
        """y coordinate"""
        self.rotation = location.rotation
        """rotation"""
        self.location_units = location.locationUnits
        """units for location coordinates"""
        self.board_side = location.boardSide
        """board side - ``"TOP"`` or ``"BOTTOM"`` """
        self.mirrored = location.mirrored
        """mirrored"""
        self.ref_des = location.refDes
        """reference designator"""
