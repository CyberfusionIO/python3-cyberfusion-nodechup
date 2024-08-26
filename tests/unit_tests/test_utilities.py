from cyberfusion.Nodechup.utilities import (
    _get_versions,
    get_architecture,
    get_latest_point_release,
    get_os_name,
)


def test_get_latest_point_release() -> None:
    assert get_latest_point_release(16, 14) == 2
    assert get_latest_point_release(15, 5) == 1


def test_get_versions() -> None:
    assert (
        len(_get_versions()) > 630
    )  # Amount at the time of writing, so can only increase


def test_get_architecture() -> None:
    """Test that get_architecture does not yield an empty string.

    We can't know the literal value of the string, as it depends on the environment.
    """
    assert get_architecture()


def test_get_os_name() -> None:
    """Test that get_os_name does not yield an empty string.

    We can't know the literal value of the string, as it depends on the environment.
    """
    assert get_os_name()
