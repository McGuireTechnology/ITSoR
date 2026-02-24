# Frontend Auth Integration Guide

This guide covers frontend auth integration settings and local verification for backend-connected login/signup/session flows.

## API base URL configuration

Frontend auth calls are routed through `frontend/src/auth/client.js` (generated-client wrapper) and read `VITE_API_BASE_URL`.

Current fallback:

- `http://127.0.0.1:3002`

Set explicit value in `frontend/.env.local` (recommended):

```dotenv
VITE_API_BASE_URL=http://127.0.0.1:3002
```

Example for remote backend:

```dotenv
VITE_API_BASE_URL=https://api.example.com
```

## How auth is wired

- `frontend/src/api/generated/Api.js` is generated from `frontend/openapi/schema.json`.
- `frontend/src/auth/client.js` wraps generated auth operations and normalizes API errors for UI flows.
- `frontend/src/auth/session.js` manages in-memory session state and hydration.
- `frontend/src/App.vue` consumes session actions (`login`, `signup`, `logout`, `hydrateSession`).

## Regenerating the frontend API client

From repo root:

```bash
make frontend-api-client
```

This command:

- Exports backend OpenAPI JSON to `frontend/openapi/schema.json`.
- Regenerates `frontend/src/api/generated/Api.js` (+ type declarations) from that contract.

## Session behavior

- Login calls `POST /auth/token` and relies on backend-set HTTP-only cookie.
- Session hydration calls `GET /auth/me` with cookie credentials.
- Logout calls `POST /auth/logout` and clears local in-memory user state.

## Local run commands

Install dependencies:

```bash
make frontend-install
```

Run dev server:

```bash
make frontend-dev
```

Build for validation:

```bash
cd frontend
npm run build
```

Run unit tests:

```bash
cd frontend
npm run test
```

## Troubleshooting

### Login succeeds but user is not authenticated

- Confirm backend CORS includes frontend origin.
- Confirm frontend requests use `credentials: "include"`.
- Confirm cookie settings are compatible with your host/protocol (`SESSION_COOKIE_SECURE`, `SESSION_COOKIE_SAMESITE`).

### API request failures show generic status text

- Check backend response payload for `detail` field.
- Verify `VITE_API_BASE_URL` points to reachable backend.

### Cross-origin cookie issues in local development

- Keep frontend and backend on same hostname family (e.g., both `127.0.0.1` or both `localhost`).
- Use HTTPS + `SESSION_COOKIE_SECURE=true` when testing secure-cookie behavior.

## See also

- [Backend Auth Setup Guide](backend-auth-setup.md)
- [Backend Environment Variable Reference](backend-env.md)
- [Local Host and Port Configuration](local-config.md)
- [User Guide Troubleshooting](user/README.md#troubleshooting)
