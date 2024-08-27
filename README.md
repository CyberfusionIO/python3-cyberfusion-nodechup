# python3-cyberfusion-fast-redirect

fast-redirect redirects domains.

# Install

## PyPI

Run the following command to install the package from PyPI:

    pip3 install python3-cyberfusion-fast-redirect

## Debian

Run the following commands to build a Debian package:

    mk-build-deps -i -t 'apt -o Debug::pkgProblemResolver=yes --no-install-recommends -y'
    dpkg-buildpackage -us -uc

# Configure

## App

Find an example config in `.env.example`.

Add settings to the `.env` file. This file is relative to your working directory.

Only `DATABASE_PATH` is required to be set. We recommend setting it to `/var/lib/fast-redirect.json`.

These settings can be overridden by specifying them as environment variables.

## JSON Database

Find an example JSON database in `fast-redirect.json`.

Properties:

* `destination_url`. URL to redirect to. This must be a URL (i.e. `www.domlimev.nl` is invalid).
* `status_code`. Allowed values: `301`, `302`, `303`, `307`, `308`.
* `keep_query_parameters`. Whether query parameters are kept. If this is false, query parameters are discarded from the `destination_url`. For example, if this is false, `https://domlimev.nl/page?k=v` is redirected to `https://example.com`.
* `keep_path`. Whether the path is kept. If this is false, the path is discarded from the `destination_url`. For example, if this is false, `https://domlimev.nl/this/is/a/path` is redirected to `https://example.com`.

# Usage

## Manually

    bin/fast-redirect

### systemd

    systemctl start fast-redirect.service

## SSL

Use a proxy that terminates SSL. E.g. [HAProxy](http://www.haproxy.org/).

The domain or IP address that the proxy uses for health checks should not be configured as a redirect.
