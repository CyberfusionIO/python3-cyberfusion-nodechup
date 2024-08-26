"""nodechup.

Usage:
   nodechup install --base-directory-path=<base-directory-path> --version=<version> [--update-default-version]

Options:
  -h --help                                      Show this screen.
  --base-directory-path=<base-directory-path>    Path to base directory
  --version=<version>                            Version of Node.js installation. Exits with RC 78 if Node.js version is already installed.
  --update-default-version                       Update default point release for major/minor version.
"""

import sys

from docopt import docopt
from schema import Schema

from cyberfusion.Nodechup.nodejs import (
    BaseDirectory,
    Installation,
    NodeJSAlreadyInstalled,
)

"""Program to manage Node.js installations."""


def main() -> None:
    """Spawn relevant class for CLI function."""

    # Validate input

    args = docopt(__doc__)
    schema = Schema(
        {
            "install": bool,
            "--base-directory-path": str,
            "--version": str,
            "--update-default-version": bool,
        }
    )
    args = schema.validate(args)

    # Run classes

    if args["install"]:
        base_directory = BaseDirectory(path=args["--base-directory-path"])
        installation = Installation(
            base_directory=base_directory, version=args["--version"]
        )

        try:
            installation.download(
                update_default_version=args["--update-default-version"]
            )
        except NodeJSAlreadyInstalled:
            print(
                "Node.js installation with the specified version already exists in the base directory"
            )

            sys.exit(78)
