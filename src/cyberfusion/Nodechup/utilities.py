"""Generic utilities."""

import codecs
import csv
import platform
import urllib.request
from typing import List, Tuple

URL_MIRROR = "https://nodejs.org/dist"
URL_VERSIONS_TAB = f"{URL_MIRROR}/index.tab"

LONG_X86_64 = "x86_64"
SHORT_X86_64 = "x64"


def _get_versions() -> List[Tuple[int, int, int]]:
    """Get available Node.js versions."""
    versions = []

    _csv = csv.DictReader(
        codecs.iterdecode(
            urllib.request.urlopen(URL_VERSIONS_TAB),
            "utf-8",  # noqa: S310
        ),
        delimiter="\t",
    )

    for row in _csv:
        major, minor, point = row["version"][len("v") :].split(
            "."
        )  # Remove leading 'v'

        versions.append((int(major), int(minor), int(point)))

    return versions


def get_latest_point_release(major: int, minor: int) -> int:
    """Get latest point release for major and minor version.

    Returns only point release, not full version number including specified major
    and minor.
    """
    versions = []

    for version in _get_versions():
        _major, _minor, _point = version

        if _major != major:
            continue

        if _minor != minor:
            continue

        versions.append(_point)

    return max(versions)


def get_architecture() -> str:
    """Get architecture that Node.js repos know about."""
    architecture = platform.machine()

    if architecture == LONG_X86_64:
        return SHORT_X86_64

    return architecture


def get_os_name() -> str:
    """Get operating system name that Node.js repos know about."""
    return platform.system().lower()
