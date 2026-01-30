"""Classes to manage Node.js installations."""

import os
import tarfile
import uuid
from contextlib import closing

import requests

from cyberfusion.Nodechup.utilities import (
    URL_MIRROR,
    get_architecture,
    get_latest_point_release,
    get_os_name,
)


class NodeJSAlreadyInstalled(Exception):
    """Node.js is already installed in path."""

    pass


class NodeJSVersion:
    """Represents Node.js version number."""

    def __init__(self, version: str):
        """Set attributes."""
        self._version = version.split(".")

    @property
    def major(self) -> int:
        """Get major version."""
        return int(self._version[0])

    @property
    def minor(self) -> int:
        """Get minor version."""
        return int(self._version[1])

    @property
    def point(self) -> int:
        """Get point release.

        If point release is not specified, most recent point release for major/minor is used.
        """
        try:
            return int(self._version[2])
        except IndexError:
            # Point release not specified

            return get_latest_point_release(self.major, self.minor)

    def __str__(self) -> str:
        """Human-readable version string."""
        return f"{self.major}.{self.minor}.{self.point}"


class BaseDirectory:
    """Represents base directory that contains Node.js installations."""

    def __init__(self, path: str) -> None:
        """Set attributes."""
        self.path = path

        self._create()

    def _create(self) -> None:
        """Create directory if it does not exist."""
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

    def set_default_version(
        self, point_version_path: str, version: NodeJSVersion
    ) -> None:
        """Set default point release for major/minor release.

        This is done by creating a symlink with the name of the major/minor version to
        the version path of the point release.

        If a symlink already exists to another (usually older) point release, it is replaced
        atomically.
        """
        major_minor_path = os.path.join(self.path, f"{version.major}.{version.minor}")
        major_minor_path_tmp = major_minor_path + "-tmp"

        os.symlink(point_version_path, major_minor_path_tmp)
        os.rename(major_minor_path_tmp, major_minor_path)


class Installation:
    """Represents Node.js installation."""

    PATH_ARCHIVE = os.path.join(
        os.path.sep, *["tmp", str(uuid.uuid4())]
    )  # Temporary path for archive

    def __init__(self, *, base_directory: BaseDirectory, version: str) -> None:
        """Set attributes."""
        self.base_directory = base_directory
        self.version = NodeJSVersion(version)

    @property
    def _archive_name(self) -> str:
        """Get name of archive in Node.js repo.

        This is the name of the archive as well as the name of the directory
        inside the archive.
        """
        return f"node-v{str(self.version)}-{get_os_name()}-{get_architecture()}"

    @property
    def _download_url(self) -> str:
        """Get URL to archive in Node.js repo."""
        return f"{URL_MIRROR}/v{str(self.version)}/{self._archive_name}.tar.xz"

    @property
    def _version_path(self) -> str:
        """Get path to version directory."""
        return os.path.join(self.base_directory.path, self._archive_name)

    @property
    def exists(self) -> bool:
        """Check if version path already exists."""
        return os.path.isdir(self._version_path)

    def download(self, *, update_default_version: bool = False) -> None:
        """Download Node.js to version path."""

        # Can't download if Node.js installation already exists

        if self.exists:
            raise NodeJSAlreadyInstalled(self._version_path)

        # Download to temporary file from Node.js website

        request = requests.get(self._download_url, allow_redirects=False)
        request.raise_for_status()

        with open(self.PATH_ARCHIVE, "wb") as f:
            f.write(request.content)

        # Extract archive to installation path

        with closing(tarfile.open(self.PATH_ARCHIVE, "r:xz")) as archive:
            archive.extractall(path=self.base_directory.path)

        # Remove now extracted archive

        os.unlink(self.PATH_ARCHIVE)

        # Symlink major/minor/point (e.g. 22.16.0 -> node-v22.16.0-linux-x64)

        os.symlink(
            self._version_path,
            os.path.join(self.base_directory.path, str(self.version)),
        )

        # Update default version (e.g. 22.16 (no point) -> node-v22.16.0-linux-x64)

        if update_default_version:
            self.base_directory.set_default_version(self._version_path, self.version)
