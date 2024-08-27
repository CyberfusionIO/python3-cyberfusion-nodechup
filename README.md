# python3-cyberfusion-nodechup

Use nodechup to install multiple Node.js versions.

Need multiple Node.js versions on your system? Installing multiple Node.js Debian packages is not supported. nodechup allows you to install multiple Node.js versions with a Python API and a CLI.

# Install

## PyPI

Run the following command to install the package from PyPI:

    pip3 install python3-cyberfusion-nodechup

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

# Configure

No configuration is supported.

# Usage

## Concepts

* Base directory: contains one or more Node.js installations.
* Node.js installation: represents Node.js version.

### Notes about point release

#### Omit point release

Node.js versions must contain major/minor release. Point release is optional.

If the point release is omitted, the most recent point release for the specified major/minor release is used.

#### Release symlink

If 'update default version' is true, nodechup creates a symlink in the base directory path from the major/minor release to the installed point release.

For example:

    /usr/local/lib/nodejs/14.19 -> /usr/local/lib/nodejs/14.19.1

### Notes about base directory

* The [Node.js wiki](https://github.com/nodejs/help/wiki/Installation) recommends using the base directory `/usr/local/lib/nodejs`.
* The base directory is created if it doesn't exist yet.

## Python API

Use the Python API as follows:

```python
import os

from cyberfusion.Nodechup import BaseDirectory, Installation

Installation(base_directory=BaseDirectory(path="/usr/local/lib/nodejs/"), version="14.19.1").download(
    update_default_version=True)
```

## CLI

Run the `nodechup` command without any arguments for help.
