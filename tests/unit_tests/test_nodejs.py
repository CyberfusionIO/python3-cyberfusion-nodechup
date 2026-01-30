import os
from typing import Generator

from cyberfusion.Nodechup.nodejs import BaseDirectory, NodeJSVersion

from cyberfusion.Nodechup.nodejs import Installation


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


def test_installation_download_symlink(
    base_directory: Generator[BaseDirectory, None, None],
) -> None:
    version = "17.7.2"

    installation = Installation(base_directory=base_directory, version=version)

    installation.download()

    assert (
        os.readlink(os.path.join(base_directory.path, version))
        == installation._version_path
    )
