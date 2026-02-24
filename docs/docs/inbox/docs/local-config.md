# Local Host and Port Configuration

This project reads local runtime host and port settings from the root `.env` file when running `make` targets.

## How configuration is loaded

- `makefile` includes `.env` automatically when it exists.
- If a value is missing in `.env`, the default in `makefile` is used.
- These settings affect:
  - `make docs-dev`
  - `make backend-dev`
  - `make frontend-dev`
  - `make web-dev`

## Default values

Default local values are:

- `HOST=127.0.0.1`
- `FRONTEND_PORT=3000`
- `WEB_PORT=3001`
- `BACKEND_PORT=3002`
- `DOCS_PORT=3003`
- `EXTRA_PORT=3004` (reserved)

## Configure your local `.env`

Create your local config from the template:

```bash
cp .env.example .env
```

On Windows PowerShell, use:

```powershell
Copy-Item .env.example .env
```

Then edit `.env` as needed.

Example:

```dotenv
HOST=127.0.0.1
FRONTEND_PORT=3000
WEB_PORT=3001
BACKEND_PORT=3002
DOCS_PORT=3003
EXTRA_PORT=3004
```

## Host input guidance

`HOST` can be either:

- An IP address (recommended for predictable behavior), e.g. `127.0.0.1` or `0.0.0.0`
- A resolvable hostname, e.g. `localhost`

Both Uvicorn and Vite accept either form for `--host`.

## CORS behavior for local frontend/web

Backend CORS allow-list is derived from `.env` values used for local development:

- `http://{HOST}:{FRONTEND_PORT}`
- `http://{HOST}:{WEB_PORT}`

When `HOST` is `127.0.0.1` or `0.0.0.0`, backend also allows:

- `http://localhost:{FRONTEND_PORT}`
- `http://localhost:{WEB_PORT}`

This ensures local browser requests from both frontend and web projects are accepted by backend CORS preflight checks.

## Verify effective values

Run:

```bash
make help
```

The output shows the currently resolved host and ports used by targets.

## Troubleshooting path links

- Auth setup and endpoints: [Backend Auth Setup Guide](backend-auth-setup.md)
- Frontend session behavior and auth troubleshooting: [Frontend Auth Integration Guide](frontend-auth-integration.md)
- Backend auth and runtime variables: [Backend Environment Variable Reference](backend-env.md)
- End-user issue triage: [User Guide Troubleshooting](user/README.md#troubleshooting)
