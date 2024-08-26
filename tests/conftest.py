import pytest
from starlette.testclient import TestClient

from cyberfusion.FastRedirect import app


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)
