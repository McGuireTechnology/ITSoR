# Backend Auth Setup Guide

This guide covers backend auth-related environment settings, local run commands, migration commands, and test commands.

## Auth-related environment variables

Set values in the root `.env` (or rely on `.env.example` defaults for local development).

### Required for non-local environments

- `JWT_SECRET` (must be strong and non-default)

### Common backend auth settings

- `BACKEND_ENV` (default: `local`)
- `BACKEND_DATABASE_URL` (default: `sqlite:///./backend/itsor.db`)
- `JWT_SECRET` (default local value: `dev-secret-change-me`)
- `JWT_ALGORITHM` (default: `HS256`)
- `JWT_ACCESS_MINUTES` (default: `60`)
- `SESSION_COOKIE_NAME` (default: `itsor_session`)
- `SESSION_COOKIE_SECURE` (default: `false`)
- `SESSION_COOKIE_SAMESITE` (default: `lax`)

Example local `.env` values:

```dotenv
BACKEND_ENV=local
BACKEND_DATABASE_URL=sqlite:///./backend/itsor.db
JWT_SECRET=dev-secret-change-me
JWT_ALGORITHM=HS256
JWT_ACCESS_MINUTES=60
SESSION_COOKIE_NAME=itsor_session
SESSION_COOKIE_SECURE=false
SESSION_COOKIE_SAMESITE=lax
```

## Install backend dependencies

```bash
make backend-install
```

## Apply database migrations

```bash
make backend-migrate
```

Alternative direct command:

```bash
python -m alembic -c backend/alembic.ini upgrade head
```

Run this from an activated virtual environment.

## Run backend locally

```bash
make backend-dev
```

Default local endpoint:

- `http://127.0.0.1:3002`

## Auth endpoints

- `POST /auth/signup`
- `POST /auth/token`
- `GET /auth/me`
- `POST /auth/logout`

Notes:

- Login sets an HTTP-only session cookie.
- `GET /auth/me` accepts cookie session auth and bearer token auth.

## Run backend auth tests

```bash
python -m pytest backend/tests/test_auth.py -q
```

Run this from an activated virtual environment.

## Security checks

- In `BACKEND_ENV` values other than local/dev/test, startup fails if `JWT_SECRET` is default or empty.
- For production, set `SESSION_COOKIE_SECURE=true` and use HTTPS.

## See also

- [Backend Environment Variable Reference](backend-env.md)
- [Security Runbooks](security-runbooks.md)
- [Frontend Auth Integration Guide](frontend-auth-integration.md)
- [Local Host and Port Configuration](local-config.md)
- [User Guide Troubleshooting](user/README.md#troubleshooting)
