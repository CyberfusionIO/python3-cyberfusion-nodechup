"""Custom Starlette middleware."""

from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from fast_redirect.exceptions.database import DatabaseError
from fast_redirect.exceptions.http_host_header import HTTPHostHeaderError
from fast_redirect.utilities import parse_host_header


class InjectRedirectInformationMiddleware(BaseHTTPMiddleware):
    """Middleware to add redirect information to request."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Add redirect information to request."""

        # Parse domain from host header (= 'request.url.hostname')

        parsed_domain = None

        try:
            parsed_domain = parse_host_header(request.url.hostname)
        except HTTPHostHeaderError as e:
            request.state.redirect_error = e
            request.state.redirect_information = None

        # If the domain is parsed, get redirect information from database

        if parsed_domain:
            try:
                request.state.redirect_information = (
                    request.app.state.database.get_redirect_information(
                        parsed_domain
                    )
                )

                request.state.redirect_error = None
            except DatabaseError as e:
                request.state.redirect_error = e
                request.state.redirect_information = None

        response = await call_next(request)

        return response
