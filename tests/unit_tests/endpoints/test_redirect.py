import pytest
from starlette.testclient import TestClient

from fast_redirect.exceptions import HTTPHostHeaderDomainInvalid

# 'allow_redirects=False' is needed, related: https://github.com/tiangolo/fastapi/issues/790#issuecomment-607636599

REDIRECT_REQUEST_OPTS = {"allow_redirects": False}

HEADERS_301_KEEP_ALL = {"Host": "301-keep-all.com"}
HEADERS_302_KEEP_NONE = {"Host": "302-keep-none.com"}
HEADERS_303_KEEP_ALL = {"Host": "303-keep-all.com"}

DEFAULT_PATH_PARAMS = [
    ("/we/might/or/might/not/keep/this/path"),
    ("we/might/or/might/not/keep/this/path"),
]

# Generic


def test_redirect_domain_not_exists(test_client: TestClient) -> None:
    """Test that no redirect occurs when the domain doesn't exist."""
    response = test_client.get("/", headers={"Host": "domlimev.nl"})
    assert response.status_code == 400
    assert response.json() == {"detail": "No redirect exists for this domain."}


def test_invalid_host_header(test_client: TestClient) -> None:
    """Test that API returns 500 when the HTTP Host header is invalud."""
    with pytest.raises(HTTPHostHeaderDomainInvalid):
        test_client.get("/", headers={"Host": "123"})


def test_redirect_domain_invalid_destination_url_ignored(
    test_client: TestClient,
) -> None:
    """Test that no redirect occurs when the destination URL is invalid."""
    response = test_client.get(
        "/", headers={"Host": "301-invalid-destination-url.com"}
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "The destination URL for this redirect is invalid."
    }


def test_redirect_domain_invalid_status_code_ignored(
    test_client: TestClient,
) -> None:
    """Test that no redirect occurs when the status code is invalid."""
    response = test_client.get(
        "/", headers={"Host": "200-invalid-status-code.com"}
    )
    assert response.status_code == 500
    assert response.json() == {
        "detail": "The status code for this redirect is invalid."
    }


def test_redirect_domain_x_redirect_by_header(test_client: TestClient) -> None:
    """Test that response has X-Redirect-By header, and its value."""
    response = test_client.get(
        "/", headers=HEADERS_301_KEEP_ALL, **REDIRECT_REQUEST_OPTS
    )
    assert response.headers["x-redirect-by"] == "fast-redirect"


# Path


@pytest.mark.parametrize("path", DEFAULT_PATH_PARAMS)
def test_redirect_domain_keep_path(path: str, test_client: TestClient) -> None:
    """Test that path is kept."""
    response = test_client.get(
        path, headers=HEADERS_301_KEEP_ALL, **REDIRECT_REQUEST_OPTS
    )
    assert (
        response.headers["location"]
        == "https://nos.nl/we/might/or/might/not/keep/this/path"
    )


@pytest.mark.parametrize("path", DEFAULT_PATH_PARAMS)
def test_redirect_domain_discard_path(
    path: str, test_client: TestClient
) -> None:
    """Test that path is discarded."""
    response = test_client.get(
        path, headers=HEADERS_302_KEEP_NONE, **REDIRECT_REQUEST_OPTS
    )
    assert response.headers["location"] == "https://nu.nl"


# Query parameters


def test_redirect_domain_keep_query_parameters(
    test_client: TestClient,
) -> None:
    """Test that query parameters are kept."""
    response = test_client.get(
        "/?a=b", headers=HEADERS_301_KEEP_ALL, **REDIRECT_REQUEST_OPTS
    )
    assert response.headers["location"] == "https://nos.nl?a=b"


def test_redirect_domain_discard_query_parameters(
    test_client: TestClient,
) -> None:
    """Test that query parameters are discarded."""
    response = test_client.get(
        "/?a=b", headers=HEADERS_302_KEEP_NONE, **REDIRECT_REQUEST_OPTS
    )
    assert response.headers["location"] == "https://nu.nl"


def test_redirect_domain_keep_destination_url_query_parameters(
    test_client: TestClient,
) -> None:
    """Test that query parameters from the destination URL are kept."""
    response = test_client.get(
        "/?a=b",
        headers={"Host": "301-query-parameter-in-destination-url.com"},
        **REDIRECT_REQUEST_OPTS,
    )
    assert response.headers["location"] == "https://nos.nl?e=f&a=b"


# Path and query parameters


def test_redirect_domain_keep_path_and_query_parameters(
    test_client: TestClient,
) -> None:
    """Test that path and query parameters are kept."""
    response = test_client.get(
        "/we/might/or/might/not/keep/this/path?a=b",
        headers=HEADERS_301_KEEP_ALL,
        **REDIRECT_REQUEST_OPTS,
    )
    assert (
        response.headers["location"]
        == "https://nos.nl/we/might/or/might/not/keep/this/path?a=b"
    )


def test_redirect_domain_discard_path_and_query_parameters(
    test_client: TestClient,
) -> None:
    """Test that path and query parameters are discarded."""
    response = test_client.get(
        "/we/might/or/might/not/keep/this/path?a=b",
        headers=HEADERS_302_KEEP_NONE,
        **REDIRECT_REQUEST_OPTS,
    )
    assert response.headers["location"] == "https://nu.nl"


# Status codes


def test_redirect_domain_301_status_code(test_client: TestClient) -> None:
    """Test that correct 301 status code is returned."""
    response = test_client.get(
        "/", headers=HEADERS_301_KEEP_ALL, **REDIRECT_REQUEST_OPTS
    )
    assert response.status_code == 301


def test_redirect_domain_302_status_code(test_client: TestClient) -> None:
    """Test that correct 302 status code is returned."""
    response = test_client.get(
        "/", headers=HEADERS_302_KEEP_NONE, **REDIRECT_REQUEST_OPTS
    )
    assert response.status_code == 302


def test_redirect_domain_303_status_code(test_client: TestClient) -> None:
    """Test that correct 303 status code is returned."""
    response = test_client.get(
        "/", headers=HEADERS_303_KEEP_ALL, **REDIRECT_REQUEST_OPTS
    )
    assert response.status_code == 303
