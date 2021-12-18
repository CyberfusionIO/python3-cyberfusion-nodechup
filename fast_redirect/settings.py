"""Settings for fast-redirect."""

from starlette.config import Config

config = Config(".env")

# App

APP_NAME = config("APP_NAME", default="fast-redirect")

LISTEN_HOST = config("LISTEN_HOST", default="::1")
LISTEN_PORT = config("LISTEN_PORT", cast=int, default=8080)

# Database

DATABASE_PATH = config("DATABASE_PATH")
