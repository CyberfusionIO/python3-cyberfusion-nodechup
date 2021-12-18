"""Run Starlette app using Uvicorn."""

import uvicorn

from fast_redirect import app, settings


def main() -> None:
    """Run app using Uvicorn."""
    uvicorn.run(
        app,
        host=settings.LISTEN_HOST,
        port=settings.LISTEN_PORT,
        log_level="info",
    )


if __name__ == "__main__":
    main()
