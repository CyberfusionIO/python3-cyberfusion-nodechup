"""JSON database functions."""

import json

import validators
from starlette import status

from fast_redirect import settings
from fast_redirect.exceptions.database import (
    DestinationURLInvalidError,
    DomainNotExistsError,
    StatusCodeInvalidError,
)


class RedirectInformation:
    """Represents redirect information for domain."""

    def __init__(
        self,
        *,
        destination_url: str,
        status_code: int,
        keep_query_parameters: bool,
        keep_path: bool,
    ) -> None:
        """Set attributes."""

        if status_code not in [
            status.HTTP_301_MOVED_PERMANENTLY,
            status.HTTP_302_FOUND,
            status.HTTP_303_SEE_OTHER,
        ]:
            raise StatusCodeInvalidError

        if not validators.url(destination_url):
            raise DestinationURLInvalidError

        self.destination_url = destination_url
        self.status_code = status_code
        self.keep_query_parameters = keep_query_parameters
        self.keep_path = keep_path


class Database:
    """Represents JSON database."""

    def __init__(self) -> None:
        """Initialise database."""
        self.load()

    def load(self) -> None:
        """Load database contents."""
        with open(settings.DATABASE_PATH, "r") as f:
            self.contents = json.loads(f.read())

    def get_redirect_information(self, domain: str) -> RedirectInformation:
        """Get redirect information from database."""
        try:
            redirect_information = self.contents["redirects"][domain]
        except KeyError:
            raise DomainNotExistsError

        return RedirectInformation(
            destination_url=redirect_information["destination_url"],
            status_code=redirect_information["status_code"],
            keep_query_parameters=redirect_information[
                "keep_query_parameters"
            ],
            keep_path=redirect_information["keep_path"],
        )
