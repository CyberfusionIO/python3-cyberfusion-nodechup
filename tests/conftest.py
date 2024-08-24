import shutil
import uuid
from typing import Generator

import pytest

from nodechup.nodejs import BaseDirectory, NodeJSVersion


@pytest.fixture(scope="session")
def base_directory() -> Generator[BaseDirectory, None, None]:
    path = "/tmp/nodejs-base-path-test-" + str(uuid.uuid4())

    yield BaseDirectory(path)

    shutil.rmtree(path)


@pytest.fixture(scope="session")
def nodejs_version_with_point_release() -> NodeJSVersion:
    return NodeJSVersion("14.19.1")


@pytest.fixture(scope="session")
def nodejs_version_without_point_release() -> NodeJSVersion:
    return NodeJSVersion("17.7")
