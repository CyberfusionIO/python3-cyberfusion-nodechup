"""Database exceptions."""

from starlette import status


class DatabaseError(Exception):
    """Generic database error."""

    pass


class DomainNotExistsError(DatabaseError):
    """Domain does not exist."""

    def __init__(self) -> None:
        """Set attributes."""
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = "No redirect exists for this domain."


class StatusCodeInvalidError(DatabaseError):
    """Status code is invalid."""

    def __init__(self) -> None:
        """Set attributes."""
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = "The status code for this redirect is invalid."


class DestinationURLInvalidError(DatabaseError):
    """Destination URL is invalid."""

    def __init__(self) -> None:
        """Set attributes."""
        self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        self.detail = "The destination URL for this redirect is invalid."
