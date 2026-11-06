import os

from requests_mock import Mocker

from cyberfusion.Nodechup.utilities import _get_versions
from tests.unit_tests.mock import mock_versions_index

PATH_FIXTURE = os.path.join(
    os.path.dirname(__file__), "fixtures", "nodejs_org_dist_index_tab.txt"
)


def test_get_versions_excludes_header_and_pre_releases(requests_mock: Mocker) -> None:
    versions_index, _ = mock_versions_index(requests_mock)

    versions = _get_versions()

    # Header line and v27.0.0-alpha.0.0.0

    assert len(versions) == len(versions_index.splitlines()) - 2
    assert (27, 0, 0) not in versions
    assert (26, 13, 0) in versions
