import grpc

from ansys.sherlock.core.errors import SherlockUpdateMountPointsByFileError
from ansys.sherlock.core.layer import Layer


def test_all():
    """Test all layer APIs"""
    channel_param = "127.0.0.1:9090"
    channel = grpc.insecure_channel(channel_param)
    layer = Layer(channel)

    helper_test_update_mount_points_by_file(layer)


def helper_test_update_mount_points_by_file(layer):
    """Test update_mount_points_by_file API."""
    try:
        layer.update_mount_points_by_file(
            "",
            "Card",
            "MountPointImport.csv",
        )
        assert False
    except SherlockUpdateMountPointsByFileError as e:
        assert e.str_itr()[0] == "Update mount points by file error: Invalid project name"

    try:
        layer.update_mount_points_by_file(
            "Test",
            "",
            "MountPointImport.csv",
        )
        assert False
    except SherlockUpdateMountPointsByFileError as e:
        assert e.str_itr()[0] == "Update mount points by file error: Invalid cca name"

    try:
        layer.update_mount_points_by_file(
            "Test",
            "Card",
            "Invalid",
        )
        assert False
    except SherlockUpdateMountPointsByFileError as e:
        assert e.str_itr()[0] == "Update mount points by file error: Invalid file path"


if __name__ == "__main__":
    test_all()
