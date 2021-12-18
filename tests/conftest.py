import pytest
from starlette.testclient import TestClient

from fast_redirect import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)
