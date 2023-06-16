# © 2023 ANSYS, Inc. All rights reserved.

"""Module containing types for the Parts Service."""

try:
    import SherlockPartsService_pb2
except ModuleNotFoundError:
    from ansys.api.sherlock.v0 import SherlockPartsService_pb2


class UpdatesPartsListRequestMatchingMode:
    """Values for Matching Mode in the Update Parts List request."""

    BOTH = SherlockPartsService_pb2.UpdatePartsListRequest.MatchingMode.Both
    PART = SherlockPartsService_pb2.UpdatePartsListRequest.MatchingMode.Part


class UpdatesPartsListRequestDuplicationMode:
    """Values for Duplication Mode in the Update Parts List request."""

    FIRST = SherlockPartsService_pb2.UpdatePartsListRequest.DuplicationMode.First
    ERROR = SherlockPartsService_pb2.UpdatePartsListRequest.DuplicationMode.Error
    IGNORE = SherlockPartsService_pb2.UpdatePartsListRequest.DuplicationMode.Ignore
