# Backend Environment Variable Reference

This page documents the backend environment-variable model currently implemented in `backend/app/main.py`, `backend/app/db.py`, and `backend/app/auth.py`.

## Source of values

For local development, values are loaded from the root `.env` via `make` targets.

- `make backend-dev` provides backend host/port runtime flags.
- Backend CORS configuration reads process environment values.

## Active backend environment variables

### `HOST`

- Default: `127.0.0.1`
- Used to build allowed local CORS origins.

### `FRONTEND_PORT`

- Default: `3000`
- Used to allow frontend origin in backend CORS.

### `WEB_PORT`

- Default: `3001`
- Used to allow web/marketing origin in backend CORS.

### `BACKEND_DATABASE_URL`

- Default: `sqlite:///./backend/itsor.db`
- Used by SQLAlchemy engine for backend persistence.

## PostgreSQL Production Profile

Use PostgreSQL for production persistence.

Recommended `BACKEND_DATABASE_URL` format:

```dotenv
BACKEND_DATABASE_URL=postgresql+psycopg://itsor_app:<strong-password>@db.internal.example:5432/itsor
```

Connection settings guidance:

- Use a dedicated least-privilege application user (for example `itsor_app`).
- Require strong credentials and rotate them through your secret manager.
- Keep host/port/database explicit in the URL; avoid implicit defaults.
- Use TLS-enabled transport in non-local environments.

Operational notes:

- Do not use SQLite in production.
- Ensure network policy restricts DB access to backend runtime only.
- Track PostgreSQL backup/restore and retention policy with environment runbooks.
- Keep migration execution tied to release sequencing (see backend runtime guide).

### `BACKEND_ENV`

- Default: `local`
- Controls environment safety behavior (for example, JWT secret validation strictness).

### `JWT_SECRET`

- Default: `dev-secret-change-me`
- Used to sign and verify JWT access tokens.

### `JWT_ALGORITHM`

- Default: `HS256`
- Used by JWT encode/decode operations.

### `JWT_ACCESS_MINUTES`

- Default: `60`
- Access-token lifetime in minutes.

### `JWT_ISSUER`

- Default: `itsor-backend`
- Required issuer claim for access-token validation.

### `JWT_AUDIENCE`

- Default: `itsor-clients`
- Required audience claim for access-token validation.

### `SESSION_COOKIE_NAME`

- Default: `itsor_session`
- HTTP-only cookie name used for authenticated session transport.

### `SESSION_COOKIE_SECURE`

- Default: `false`
- When `true`, cookie is sent only over HTTPS.

### `SESSION_COOKIE_SAMESITE`

- Default: `lax`
- Cookie same-site mode (`lax`, `strict`, or `none`).

## Local CORS behavior

Backend allows:

- `http://{HOST}:{FRONTEND_PORT}`
- `http://{HOST}:{WEB_PORT}`

If `HOST` is `127.0.0.1` or `0.0.0.0`, backend also allows:

- `http://localhost:{FRONTEND_PORT}`
- `http://localhost:{WEB_PORT}`

## Example root `.env`

```dotenv
HOST=127.0.0.1
FRONTEND_PORT=3000
WEB_PORT=3001
BACKEND_PORT=3002
DOCS_PORT=3003
EXTRA_PORT=3004

BACKEND_DATABASE_URL=sqlite:///./backend/itsor.db
BACKEND_ENV=local
JWT_SECRET=dev-secret-change-me
JWT_ALGORITHM=HS256
JWT_ACCESS_MINUTES=60
JWT_ISSUER=itsor-backend
JWT_AUDIENCE=itsor-clients
SESSION_COOKIE_NAME=itsor_session
SESSION_COOKIE_SECURE=false
SESSION_COOKIE_SAMESITE=lax
```

## Notes

- For production, always override `JWT_SECRET` and `BACKEND_DATABASE_URL`.
- SQLite-specific options are automatically applied only when DB URL starts with `sqlite`.
- Backend startup fails when `BACKEND_ENV` is not `local`/`development`/`dev`/`test` and `JWT_SECRET` is unset or uses an insecure default.
- Backend startup fails when `SESSION_COOKIE_SAMESITE` is not one of `lax`, `strict`, `none`.
- Backend startup fails when `BACKEND_ENV` is not `local`/`development`/`dev`/`test` and `SESSION_COOKIE_SECURE` is not `true`.
- Backend validates access-token `iss`/`aud` claims against `JWT_ISSUER` and `JWT_AUDIENCE`.
- Apply DB schema changes via Alembic migrations with `make backend-migrate`.

## See also

- [Backend Deployment and Runtime Guide](backend-deployment-runtime.md)
- [Backend Auth Setup Guide](backend-auth-setup.md)
- [Frontend Auth Integration Guide](frontend-auth-integration.md)
- [Local Host and Port Configuration](local-config.md)
- [User Guide Troubleshooting](user/README.md#troubleshooting)
