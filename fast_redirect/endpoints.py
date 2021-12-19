"""Custom Starlette endpoints."""

from typing import Union

from starlette.endpoints import HTTPEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, RedirectResponse

from fast_redirect import settings
from fast_redirect.utilities import build_url


class Redirect(HTTPEndpoint):
    """Redirect endpoint."""

    async def get(
        self, request: Request
    ) -> Union[RedirectResponse, JSONResponse]:
        """Implement GET method."""

        # Handle errors

        if request.state.redirect_error:
            return JSONResponse(
                {"detail": request.state.redirect_error.detail},
                status_code=request.state.redirect_error.status_code,
            )

        # Build arguments to pass to 'build_url'. We have do to this here, as
        # *_params would be incomplete during middleware.

        arguments = {
            "destination_url": request.state.redirect_information.destination_url
        }

        if request.state.redirect_information.keep_path:
            # There's also 'request.url.path', but it always ends with '/', which
            # we don't want

            arguments["path"] = request.path_params["path"]

        if request.state.redirect_information.keep_query_parameters:
            arguments["query_parameters"] = request.query_params

        # Build URL with arguments constructed above

        built_url = build_url(**arguments)

        return RedirectResponse(
            url=built_url,
            status_code=request.state.redirect_information.status_code,
            headers={"X-Redirect-By": settings.APP_NAME},
        )
