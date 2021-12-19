"""JSON database functions."""

import json
from typing import Dict, Optional

import validators
from starlette import status

from fast_redirect import settings
from fast_redirect.exceptions.database import (
    DestinationURLInvalidError,
    DomainNotExistsError,
    StatusCodeInvalidError,
)
from fast_redirect.utilities import CHAR_LABEL, get_domain_is_wildcard


class Redirect:
    """Represents redirect in database."""

    def __init__(
        self,
        *,
        domain: str,
        destination_url: str,
        status_code: int,
        keep_query_parameters: bool,
        keep_path: bool,
    ) -> None:
        """Set attributes."""
        self.domain = domain
        self.destination_url = destination_url
        self.status_code = status_code
        self.keep_query_parameters = keep_query_parameters
        self.keep_path = keep_path


class RedirectInformation:
    """Represents redirect information for domain."""

    VALID_STATUS_CODES = [
        status.HTTP_301_MOVED_PERMANENTLY,
        status.HTTP_302_FOUND,
        status.HTTP_303_SEE_OTHER,
        status.HTTP_307_TEMPORARY_REDIRECT,
        status.HTTP_308_PERMANENT_REDIRECT,
    ]

    def __init__(self, redirect: Redirect) -> None:
        """Validate and set attributes."""

        # Validate attributes
        #
        # Has to be done here instead of in 'Redirect', because raising exceptions
        # in middleware isn't ideal

        self._validate_status_code(redirect.status_code)
        self._validate_destination_url(redirect.destination_url)

        # Set attributes

        self.destination_url = redirect.destination_url
        self.status_code = redirect.status_code
        self.keep_query_parameters = redirect.keep_query_parameters
        self.keep_path = redirect.keep_path

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
            domain = domain.lower()  # Should be case-insensitive

            self.redirects[domain] = Redirect(domain=domain, **obj)

    def _get_redirect_by_literal_domain(
        self, domain: str
    ) -> Optional[Redirect]:
        """Get redirect from database by literal domain."""
        try:
            return self.redirects[domain]
        except KeyError:
            # Not in database

            return None

    def _get_redirect_by_wildcard_domain(
        self, domain: str
    ) -> Optional[Redirect]:
        """Get redirect from database by wildcard domain."""
        for _domain, redirect in self.redirects.items():
            # This can't match if the _domain is not a wildcard

            if not get_domain_is_wildcard(_domain):
                continue

            # When we get here, we know '_domain[1:]' is '*'. If we remove both
            # first parts, and they are the same, domain is covered by the
            # wildcard _domain

            if domain.split(CHAR_LABEL)[1:] != _domain.split(CHAR_LABEL)[1:]:
                continue

            return redirect

        return None

    def get_redirect_information(self, domain: str) -> RedirectInformation:
        """Get redirect information for domain.

        There are two cases in which a domain can be matched to a redirect:

        - When a redirect for the literal domain exists (preferred).
        - When a redirect for a wildcard domain exists.
        """

        # Get redirect by literal domain (prefer over wildcard)

        _redirect_by_literal_domain = self._get_redirect_by_literal_domain(
            domain
        )

        if _redirect_by_literal_domain:
            return RedirectInformation(_redirect_by_literal_domain)

        # Get redirect by wildcard domain

        _redirect_by_wildcard_domain = self._get_redirect_by_wildcard_domain(
            domain
        )

        if _redirect_by_wildcard_domain:
            return RedirectInformation(_redirect_by_wildcard_domain)

        # At this point, there is no match for either a literal domain or
        # wildcard domain

        raise DomainNotExistsError
