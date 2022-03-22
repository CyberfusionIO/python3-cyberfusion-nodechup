# NodeCHUP

Use NodeCHUP to easily **CH**ange and **UP**date Node.js installations.

Only Linux systems are supported. Other systems such as WSL may work, but have not been tested.

This program only takes care of managing installations. It does not modify your shell to easily use different installations/versions.

## Use case

NodeCHUP exists because we need users to be able to set their own Node.js version, but Node.js binary distributions do not support multiple versions using an [alternatives system](https://wiki.debian.org/DebianAlternatives). Therefore, we can't use an existing package manager, and need to maintain a Node.js installation per user. However, many alternatives like [nvm](https://github.com/nvm-sh/nvm) are installed by running an install script and piping it to bash, which is a security nightmare.

NodeCHUP is designed to run on behalf of non-privileged users, i.e. you should not run this as root.

## Install

The package has been published to PyPI, so you could install it with `pip3 install nodechup`.

## Usage

NodeCHUP offers a stable Python API.

NodeCHUP has the concepts of 'base directory' and 'Node.js installations'. Each base directory is a directory that contains one or more Node.js installations, one per version. Every Node.js installation represents a Node.js version.

### Create Node.js installation

The magic happens in the `nodejs.Installation` class. Use it as follows:

```python
import os

from nodechup.nodejs import BaseDirectory, Installation

# Get base directory

base_directory_path = os.path.join(os.path.sep, *["usr", "local", "lib", "nodejs"])  # Following the example at https://github.com/nodejs/help/wiki/Installation. The base directory is created if it doesn't exist yet.
base_directory = BaseDirectory(path=base_directory_path)

# Set version. If a point release is not specified, the most recent point release for the major/minor is used.

version = "14.19.1"
version = "14.19"

# Get installation

installation = Installation(base_directory=base_directory, version=version)
installation.download(update_default_version=True)  # See below for explanation
```

#### Update default (point release) version (for major/minor)

When passing `update_default_version=True` to the `download` method, the program creates a symlink in the base directory path **from** the major/minor version **to** the point release that is being installed. The above example would create the following symlink:

    /usr/local/lib/nodejs/14.19 -> /usr/local/lib/nodejs/14.19.1

This makes updating major/minor versions easy. By downloading the major/minor Node.js version without specifying the point release, and with `update_default_version=True`, the most recent point release for the major/minor version will be downloaded. By telling your applications to use the path to the major/minor version (e.g. `/usr/local/lib/nodejs/14.19`), the most recent point release for that major/minor version will be used.
