"""Custom Starlette middleware."""

from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from fast_redirect.exceptions.database import DatabaseError
from fast_redirect.utilities import parse_host_header


class InjectRedirectInformationMiddleware(BaseHTTPMiddleware):
    """Middleware to add redirect information to request."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Add redirect information to request."""

        # Starlette sets 'request.url.hostname' based on the host header. It's
        # nullable, but we always need it, so raise an exception just to be sure

        if not request.url.hostname:
            raise Exception

        # Parse domain from host header

        parsed_domain = parse_host_header(request.url.hostname)

        # Get redirect information from database

        try:
            redirect_information = (
                request.app.state.database.get_redirect_information(
                    parsed_domain
                )
            )

            redirect_error = None
        except DatabaseError as e:
            # If any database error occurs, don't redirect

            redirect_error = e
            redirect_information = None

        # Set redirect information

        if redirect_information:
            request.state.redirect_information = redirect_information
            request.state.redirect_error = None
        else:
            request.state.redirect_information = None
            request.state.redirect_error = redirect_error

        response = await call_next(request)

        return response
