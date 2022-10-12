import os
from typing import Generator

import pytest

from nodechup.nodejs import (
    BaseDirectory,
    Installation,
    NodeJSAlreadyInstalled,
    NodeJSVersion,
)
from nodechup.utilities import get_architecture, get_os_name


def test_installation_download_without_update_default_version(
    base_directory: BaseDirectory,
) -> None:
    # Get installation

    installation = Installation(
        base_directory=base_directory, version="14.19.1"
    )

    # Test attributes

    assert not installation.exists

    assert str(installation.version) == str(NodeJSVersion("14.19.1"))
    assert (
        installation._archive_name
        == f"node-v14.19.1-{get_os_name()}-{get_architecture()}"
    )
    assert (
        installation._download_url
        == f"https://nodejs.org/dist/v14.19.1/node-v14.19.1-{get_os_name()}-{get_architecture()}.tar.xz"
    )
    assert installation._version_path == os.path.join(
        base_directory.path,
        f"node-v14.19.1-{get_os_name()}-{get_architecture()}",
    )

    # Test download

    installation.download()

    assert installation.exists

    assert not os.path.isfile(installation.PATH_ARCHIVE)  # type: ignore[unreachable]

    # Test download again raises

    with pytest.raises(NodeJSAlreadyInstalled):
        installation.download()


def test_installation_download_with_update_default_version(
    base_directory: BaseDirectory,
) -> None:
    # Get installation

    installation = Installation(
        base_directory=base_directory, version="17.7.2"
    )

    # Test attributes

    assert not installation.exists

    assert str(installation.version) == str(NodeJSVersion("17.7.2"))
    assert (
        installation._archive_name
        == f"node-v17.7.2-{get_os_name()}-{get_architecture()}"
    )
    assert (
        installation._download_url
        == f"https://nodejs.org/dist/v17.7.2/node-v17.7.2-{get_os_name()}-{get_architecture()}.tar.xz"
    )
    assert installation._version_path == os.path.join(
        base_directory.path,
        f"node-v17.7.2-{get_os_name()}-{get_architecture()}",
    )

    # Test download

    installation.download(update_default_version=True)

    assert installation.exists

    assert not os.path.isfile(installation.PATH_ARCHIVE)  # type: ignore[unreachable]

    # Test symlink from major/minor to directory to major/minor/point version path

    assert (
        os.readlink(os.path.join(base_directory.path, "17.7"))
        == installation._version_path
    )
