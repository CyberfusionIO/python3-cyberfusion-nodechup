"""Starlette app."""

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.routing import Route

from fast_redirect.database import Database
from fast_redirect.endpoints import Redirect
from fast_redirect.middleware import InjectRedirectInformationMiddleware

# Initialise app
#
# AFAIK, 'TrustedHostMiddleware' doesn't do anything when '*' is in 'allowed_hosts'.
# It's just here for consistency's sake.

middleware = [
    Middleware(InjectRedirectInformationMiddleware),
    Middleware(TrustedHostMiddleware, allowed_hosts=["*"]),
]
routes = [Route("/{path:path}", Redirect, methods=["GET"])]

app = Starlette(routes=routes, middleware=middleware)

# Add database to app

app.state.database = Database()  # type: ignore[has-type]
