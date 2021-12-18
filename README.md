# Fast Redirect

Use Fast Redirect to easily redirect your domains. The idea is simple. You have a JSON database, in which you define domains to redirect, and a few redirect options. Fast Redirect will then redirect traffic as configured.

# Install & Run

We recommend running Fast Redirect in a venv. Install the package with `pip3 install fast_redirect`.

Run `bin/fast-redirect` to start a server on `LISTEN_PORT` (default: `8080`). By default, the server binds only to `::1` (IPv6). Both are configurable.

You may daemonize the server. An example systemd configuration can be found in `fast-redirect.service`.

# Database

The database contains a `redirects` object. In turn, this object contains an object for each redirect with the following properties:

* `destination_url`. The URL to redirect to. Query parameters and the path may be appended (see other options). This **must** be a URL (i.e. `www.domlimev.nl` is invalid).
* `status_code`. Allowed values `301`, `302` and `303`.
* `keep_query_parameters`. Whether query parameters are kept. If this is false, query parameters are discarded from the `destination_url`. For example, if this is false, `https://domlimev.nl/page?k=v` will be redirected to `https://example.com`.
* `keep_path`. Whether the path is kept. If this is false, the path is discarded from the `destination_url`. For example, if this is false, `https://domlimev.nl/this/is/a/path` will be redirected to `https://example.com`.

Example database:

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

# Configuration

A number of configuration variables may be set. You may supply these as environment variables, or in an `.env` file. See the `.env.example` file for more information.

# Dependencies

Fast Redirect only needs [Starlette](https://www.starlette.io/) and [Uvicorn](https://www.uvicorn.org/) to run.
