# NodeCHUP

Use NodeCHUP to easily **CH**ange and **UP**date Node.js installations.

Only Linux systems are supported. Other systems such as WSL may work, but have not been tested.

This program only takes care of managing installations. It does not modify your shell to easily use different installations/versions.

## Use case

NodeCHUP exists because we need users to be able to set their own Node.js version, but Node.js binary distributions do not support multiple versions using an [alternatives system](https://wiki.debian.org/DebianAlternatives). Therefore, we can't use an existing package manager, and need to maintain a Node.js installation per user. However, many alternatives like [nvm](https://github.com/nvm-sh/nvm) are installed by running an install script and piping it to bash, which is a security nightmare.

## Install

The package has been published to PyPI, so you could install it with `pip3 install nodechup`.

## Usage

NodeCHUP has the concepts of 'base directory' and 'Node.js installations'. Each base directory is a directory that contains one or more Node.js installations, one per version. Every Node.js installation represents a Node.js version.

When creating a Node.js installation, NodeCHUP will ask for the Node.js version. This may be either a major/minor version or a major/minor/point release. If the point release is omitted, the most recent point release for the specified major/minor version is used. For example, both '14.19.0' and '14.19' are valid versions. When '14.19' is specified, the used version will be '14.19.1', as that is the most recent point release for '14.19'.

When creating a Node.js installation, NodeCHUP will ask for the base directory path. This is the path to the base directory that contains your Node.js installations. Following the example at https://github.com/nodejs/help/wiki/Installation, we recommend using the path `/usr/local/lib/nodejs`. The base directory is created if it doesn't exist yet.

### Interfaces

You can interact with NodeCHUP using a Python API or a CLI tool. Both options are described below.

#### Python API

NodeCHUP offers a stable Python API.

Use it as follows:

```python
import os

from nodechup.nodejs import BaseDirectory, Installation

# Get base directory

base_directory_path = os.path.join(os.path.sep, *["usr", "local", "lib", "nodejs"])
base_directory = BaseDirectory(path=base_directory_path)

# Set version

version = "14.19.1"

# Get installation

installation = Installation(base_directory=base_directory, version=version)
installation.download(update_default_version=True)  # See below for explanation
```

#### CLI tool

NodeCHUP offers a stable CLI tool called `nodechup`. It is self-documenting. Run the `nodechup` command without any arguments for help.

### Update default (point release) version (for major/minor)

NodeCHUP makes updating your Node.js installations easy.

When setting update default version to true, the program creates a symlink in the base directory path **from** the major/minor version **to** the point release that is being installed. For example:

    /usr/local/lib/nodejs/14.19 -> /usr/local/lib/nodejs/14.19.1

This makes updating major/minor versions easy. By downloading the major/minor Node.js version without specifying the point release, and with `update_default_version=True`, the most recent point release for the major/minor version will be downloaded. By telling your applications to use the path to the major/minor version (e.g. `/usr/local/lib/nodejs/14.19`), the most recent point release for that major/minor version will be used.
