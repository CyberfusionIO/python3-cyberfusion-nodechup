import os

import pytest

from nodechup.nodejs import BaseDirectory, NodeJSVersion


@pytest.fixture(scope="session")
def base_directory() -> BaseDirectory:
    return BaseDirectory("/tmp/nodejs-base-path-test")


@pytest.fixture(scope="session")
def nodejs_version_with_point_release() -> NodeJSVersion:
    return NodeJSVersion("14.19.1")


@pytest.fixture(scope="session")
def nodejs_version_without_point_release() -> NodeJSVersion:
    return NodeJSVersion("17.7")
