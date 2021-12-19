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
        """Validate and set attributes."""

        # Validate attributes. This code is reached when this specific redirect
        # actually has to be used. That's why we do validation here instead of
        # in Database.load, so that the app is resistant to misconfiguration of a
        # single redirect.

        if status_code not in [
            status.HTTP_301_MOVED_PERMANENTLY,
            status.HTTP_302_FOUND,
            status.HTTP_303_SEE_OTHER,
            status.HTTP_307_TEMPORARY_REDIRECT,
            status.HTTP_308_PERMANENT_REDIRECT,
        ]:
            raise StatusCodeInvalidError

        if not validators.url(destination_url):
            raise DestinationURLInvalidError

        # Set attributes

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
        """Load redirects from database."""

        # Load JSON file

        with open(settings.DATABASE_PATH, "r") as f:
            _contents = json.loads(f.read())

        # Convert JSON file to database

        for domain, obj in _contents["redirects"].items():
            # Ensure domain is lowercase

            domain = domain.lower()

            # Add domain to database

            _contents[domain] = obj

        # Set self.redirects

        self.redirects = _contents

    def get_redirect_information(self, domain: str) -> RedirectInformation:
        """Get redirect information for domain."""
        try:
            redirect = self.redirects[domain]
        except KeyError:
            raise DomainNotExistsError

        return RedirectInformation(
            destination_url=redirect["destination_url"],
            status_code=redirect["status_code"],
            keep_query_parameters=redirect["keep_query_parameters"],
            keep_path=redirect["keep_path"],
        )
