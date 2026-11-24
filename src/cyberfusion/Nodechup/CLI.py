"""Program to manage Node.js installations."""

import sys

import typer

from cyberfusion.Nodechup.nodejs import (
    BaseDirectory,
    Installation,
    NodeJSAlreadyInstalled,
)

app = typer.Typer(no_args_is_help=True)


@app.callback()
def callback() -> None:
    """Manage Node.js installations."""

    # Keeps 'install' a subcommand: with a single command, typer would run it as the
    # top-level command


@app.command()
def install(
    base_directory_path: str = typer.Option(
        ..., "--base-directory-path", help="Path to base directory."
    ),
    version: str = typer.Option(
        ...,
        "--version",
        help="Version of Node.js installation. Exits with RC 78 if Node.js version is already installed.",
    ),
    update_default_version: bool = typer.Option(
        False,
        "--update-default-version",
        help="Update default point release for major/minor version.",
    ),
) -> None:
    """Install Node.js version."""
    base_directory = BaseDirectory(path=base_directory_path)
    installation = Installation(base_directory=base_directory, version=version)

    try:
        installation.download(update_default_version=update_default_version)
    except NodeJSAlreadyInstalled:
        print(
            "Node.js installation with the specified version already exists in the base directory"
        )

        sys.exit(78)


def main() -> None:
    """Spawn relevant class for CLI function."""
    app()
