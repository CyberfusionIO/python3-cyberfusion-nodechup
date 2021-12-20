"""HTTP host header exceptions."""

from starlette import status


class HTTPHostHeaderError(Exception):
    """Generic HTTP host header error."""

    pass


class HTTPHostHeaderDomainInvalidError(HTTPHostHeaderError):
    """Domain in HTTP host header is invalid."""

    def __init__(self) -> None:
        """Set attributes."""
        self.status_code = status.HTTP_200_OK
        self.detail = "It seems like I'm alive."  # Handle gracefully


class HTTPHostHeaderDomainEmptyError(HTTPHostHeaderError):
    """Domain in HTTP host header is empty."""

    def __init__(self) -> None:
        """Set attributes."""
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "Specify redirect to look for."
