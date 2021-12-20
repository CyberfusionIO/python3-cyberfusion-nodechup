# Fast Redirect

Use Fast Redirect to easily redirect your domains.

Fast Redirects expects a JSON 'database'. This JSON 'database' contains the domains to be redirected. Fast Redirect then redirects traffic as configured.

Fast Redirect uses [Starlette](https://www.starlette.io/), a high-performance ASGI framework. Your redirects are lightning fast. Requirements for all environments can be found in the `requirements` directory.

# How to use

## Install

We recommend running Fast Redirect in a venv. The package has been published to PyPI, so you could install it with `pip3 install fast-redirect`.

## Run

All configuration variables can be found in the `.env.example` file. Only one configuration variable is **required** to be set: `DATABASE_PATH`. We recommend setting it to `/var/lib/fast-redirect.json`. Configuration variables can be set in an `.env` file or be passed as environment variables.

Run `bin/fast-redirect` to start the server. By default, it listens on port `8080` and binds to `::1` (IPv6). The server can be daemonized. An example systemd configuration can be found in `fast-redirect.service`.

## SSL

Fast Redirect does not support SSL natively. Use a proxy that takes care of SSL, such as [HAProxy](http://www.haproxy.org/).

If your proxy does health checks, make sure that the domain or IP address it uses for them is not configured as a redirect.

# JSON Database

The JSON database contains a `redirects` object. In turn, this object contains an object for each redirect. The key is the domain to redirect. Wildcards are supported.

Properties:

* `destination_url`. The URL to redirect to. Query parameters and the path may be appended (see other options). This **must** be a URL (i.e. `www.domlimev.nl` is invalid).
* `status_code`. Allowed values: `301`, `302`, `303`, `307`, `308`
* `keep_query_parameters`. Whether query parameters are kept. If this is false, query parameters are discarded from the `destination_url`. For example, if this is false, `https://domlimev.nl/page?k=v` would be redirected to `https://example.com`.
* `keep_path`. Whether the path is kept. If this is false, the path is discarded from the `destination_url`. For example, if this is false, `https://domlimev.nl/this/is/a/path` would be redirected to `https://example.com`.

In case a redirect is misconfigured, the error is returned to the visitor.

Example JSON database:

```
{
  "redirects": {
    "domlimev.nl": {
      "destination_url": "https://example.com",
      "status_code": 301,
      "keep_query_parameters": true,
      "keep_path": true
    }
  }
}
```

# Contribute

Feel free to contribute by adding support for real database engines.

## Tests

pytest is used for tests. You run it as you'd expect, i.e.:

    pytest tests/

## Security

You can reach us at `opensource@cyberfusion.nl` to report security issues.
