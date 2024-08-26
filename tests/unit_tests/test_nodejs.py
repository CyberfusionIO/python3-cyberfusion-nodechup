import os

from cyberfusion.Nodechup.nodejs import BaseDirectory, NodeJSVersion


def test_base_directory_created(base_directory: BaseDirectory) -> None:
    """Test that non-existent base directory is created."""
    path = "/tmp/testforbasedir"

    assert not os.path.isdir(path)

    BaseDirectory(path=path)

    assert os.path.isdir(path)


def test_nodejs_version_with_point_release(
    nodejs_version_with_point_release: NodeJSVersion,
) -> None:
    assert nodejs_version_with_point_release.major == 14
    assert nodejs_version_with_point_release.minor == 19
    assert nodejs_version_with_point_release.point == 1


def test_nodejs_version_without_point_release(
    nodejs_version_without_point_release: NodeJSVersion,
) -> None:
    assert nodejs_version_without_point_release.major == 17
    assert nodejs_version_without_point_release.minor == 7
    assert nodejs_version_without_point_release.point == 2  # Automatic
