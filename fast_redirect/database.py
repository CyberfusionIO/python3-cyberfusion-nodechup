"""JSON database functions."""

import json
from typing import Dict

import validators
from starlette import status

from fast_redirect import settings
from fast_redirect.exceptions.database import (
    DestinationURLInvalidError,
    DomainNotExistsError,
    StatusCodeInvalidError,
)


class Redirect:
    """Represents redirect in database."""

    VALID_STATUS_CODES = [
        status.HTTP_301_MOVED_PERMANENTLY,
        status.HTTP_302_FOUND,
        status.HTTP_303_SEE_OTHER,
        status.HTTP_307_TEMPORARY_REDIRECT,
        status.HTTP_308_PERMANENT_REDIRECT,
    ]

    def __init__(
        self,
        *,
        domain: str,
        destination_url: str,
        status_code: int,
        keep_query_parameters: bool,
        keep_path: bool,
    ) -> None:
        """Validate and set attributes."""

        # Validate attributes
        #
        # This code is reached when this specific redirect
        # actually has to be used. That's why we do validation here instead of
        # in Database.load, so that the app is resistant to misconfiguration of a
        # single redirect.

        self._validate_status_code(status_code)
        self._validate_destination_url(destination_url)

        # Set attributes

        self.domain = domain.lower()  # Should be case-insensitive
        self.destination_url = destination_url
        self.status_code = status_code
        self.keep_query_parameters = keep_query_parameters
        self.keep_path = keep_path

    def _validate_status_code(self, status_code: int) -> None:
        """Raise if status code is not valid."""
        if status_code in self.VALID_STATUS_CODES:
            return

        raise StatusCodeInvalidError

    def _validate_destination_url(self, destination_url: str) -> None:
        """Raise if destination URL is not valid."""
        if validators.url(destination_url):
            return

        raise DestinationURLInvalidError


class RedirectInformation:
    """Represents redirect information for domain."""

    def __init__(self, redirect: Redirect) -> None:
        """Set attributes."""
        self.destination_url = redirect.destination_url
        self.status_code = redirect.status_code
        self.keep_query_parameters = redirect.keep_query_parameters
        self.keep_path = redirect.keep_path


class Database:
    """Represents JSON database."""

    def __init__(self) -> None:
        """Initialise database."""
        self.load()

    def load(self) -> None:
        """Load redirects from database.

        Turns JSON objects into Python objects.
        """
        self.redirects: Dict[str, Redirect] = {}

        # Load redirects from file

        with open(settings.DATABASE_PATH, "r") as f:
            _contents = json.loads(f.read())

        # Add Redirect objects

        for domain, obj in _contents["redirects"].items():
            self.redirects[domain] = Redirect(domain=domain, **obj)

    def get_redirect_information(self, domain: str) -> RedirectInformation:
        """Get redirect information for domain."""
        try:
            redirect = self.redirects[domain]
        except KeyError:
            raise DomainNotExistsError

        return RedirectInformation(redirect)
