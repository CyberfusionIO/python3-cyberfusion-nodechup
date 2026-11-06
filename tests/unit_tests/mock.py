import os

from requests_mock import Mocker
from requests_mock.adapter import _Matcher

from cyberfusion.Nodechup.utilities import URL_VERSIONS_TAB


def mock_versions_index(requests_mock: Mocker) -> tuple[str, _Matcher]:
    with open(
        os.path.join(
            os.path.dirname(__file__), "fixtures", "nodejs_org_dist_index_tab.txt"
        ),
        "r",
    ) as f:
        nodejs_index_contents = f.read()

    mock = requests_mock.get(
        URL_VERSIONS_TAB, text=nodejs_index_contents, status_code=200
    )

    return nodejs_index_contents, mock
