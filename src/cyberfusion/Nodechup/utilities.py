"""Generic utilities."""

import codecs
import csv
import platform
import urllib.request

import semantic_version

URL_MIRROR = "https://nodejs.org/dist"
URL_VERSIONS_TAB = f"{URL_MIRROR}/index.tab"

LONG_X86_64 = "x86_64"
SHORT_X86_64 = "x64"


class NodeJSUnexpectedVersionFormat(Exception):
    """Raised when the version format we see in the versions index tab is unexpected.

    This currently applies to encountering build tags in release versions mentioned in the tab, which
    will need separate logic to handle it.
    """


def _get_versions() -> list[tuple[int, int, int]]:
    """Get available Node.js versions."""
    versions = []

    _csv = csv.DictReader(
        codecs.iterdecode(
            urllib.request.urlopen(URL_VERSIONS_TAB),
            "utf-8",
        ),
        delimiter="\t",
    )

    for row in _csv:
        major, minor, point, release = _parse_semver(row["version"])

        if release:
            versions.append((major, minor, point))

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


def _parse_semver(version: str) -> tuple[int, int, int, bool]:
    """Parse a semantic version X.Y.Z, with optional `v` prefix and `-<pre-release tag>` suffix.

    Returns `major`, `minor`, `patch` version components, and whether this version is an actual release version.

    If build tag is present, NodeJSUnexpectedVersionFormat exception is raised."""
    parsed = semantic_version.Version(version.removeprefix("v"))

    if parsed.build:
        raise NodeJSUnexpectedVersionFormat(
            "build tags in parsed NodeJS versions are unsupported"
        )

    return (
        parsed.major,
        parsed.minor,
        parsed.patch,
        not parsed.prerelease,
    )


def get_architecture() -> str:
    """Get architecture that Node.js repos know about."""
    architecture = platform.machine()

    if architecture == LONG_X86_64:
        return SHORT_X86_64

    return architecture


def get_os_name() -> str:
    """Get operating system name that Node.js repos know about."""
    return platform.system().lower()
