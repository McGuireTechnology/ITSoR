# Auth Token Expiry and Refresh Strategy

This document defines the token lifecycle strategy for ITSoR auth and provides an implementation plan.

## Current state

- Backend currently issues short-lived access tokens from `POST /auth/token`.
- Access token expiry is controlled by `JWT_ACCESS_MINUTES` (default `60`).
- JWT signing key is `JWT_SECRET`.
- No refresh-token endpoint or persistence model exists yet.

## Target strategy

Use dual-token auth:

- Access token (JWT): short-lived bearer token for API authorization.
- Refresh token: long-lived, server-tracked token used only to mint new access tokens.

Recommended defaults:

- Access token TTL: `15` minutes.
- Refresh token TTL: `14` days.
- Refresh token rotation: enabled (single-use refresh tokens).

## Security requirements

- Store refresh tokens hashed in DB (never store plaintext).
- Include `jti` and `sub` claims in access and refresh tokens.
- Include `token_type` claim (`access` or `refresh`).
- Rotate refresh token on each refresh call.
- Revoke prior refresh token after successful rotation.
- Invalidate all active refresh tokens on password change or manual forced logout.
- Keep clock skew tolerance small (for example, <= 60 seconds).

## Proposed API contract

### `POST /auth/token`

Behavior:

- Validate credentials.
- Return access token and refresh token pair.

Response model example:

```json
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer",
  "expires_in": 900
}
```

### `POST /auth/refresh`

Behavior:

- Accept refresh token.
- Validate signature, expiry, token type, and DB revocation state.
- Rotate refresh token and return a new token pair.

### `POST /auth/logout`

Behavior:

- Revoke current refresh token (or all user refresh tokens for global logout mode).

## Data model additions

Add a refresh-token persistence table (suggested name: `refresh_tokens`):

- `id` (ULID PK)
- `user_id` (FK -> `users.id`)
- `token_hash` (hashed refresh token)
- `issued_at` (UTC timestamp)
- `expires_at` (UTC timestamp)
- `revoked_at` (nullable UTC timestamp)
- `replaced_by_token_id` (nullable self-reference)
- `created_ip` (nullable)
- `user_agent` (nullable)

Indexes:

- `user_id`
- `expires_at`
- `revoked_at`

## Environment variables

Current:

- `JWT_SECRET`
- `JWT_ACCESS_MINUTES`

Add:

- `JWT_REFRESH_DAYS` (default `14`)
- `JWT_ISSUER` (recommended, e.g. `itsor-backend`)
- `JWT_AUDIENCE` (recommended, e.g. `itsor-clients`)

## Implementation plan

### Phase 1: Token model and settings

1. Add env settings for refresh TTL, issuer, and audience.
2. Update token helper functions to include `jti`, `token_type`, `iss`, and `aud`.
3. Lower default access-token TTL from 60m to 15m.

### Phase 2: Persistence and migrations

1. Add `refresh_tokens` SQLAlchemy model.
2. Add Alembic migration for the new table and indexes.
3. Implement hashing utility for refresh token storage and lookup.

### Phase 3: API endpoints

1. Extend `POST /auth/token` to return refresh token.
2. Add `POST /auth/refresh` with rotation and revocation logic.
3. Add `POST /auth/logout` to revoke active refresh token(s).

### Phase 4: Client integration

1. Update frontend auth client to store refresh token securely for current app model.
2. On access-token expiry/401, call refresh endpoint once, then retry original request.
3. Force logout when refresh fails or token is revoked.

### Phase 5: Testing and operations

1. Add tests for refresh success, rotation, replay prevention, and revocation.
2. Add runbook steps for JWT secret rotation and global session invalidation.
3. Add observability counters for refresh success/failure and token revocation events.

## Acceptance criteria

- Access token expiry is enforced.
- Refresh-token rotation prevents replay of previous refresh token.
- Logout revokes refresh token and prevents further refresh.
- Tests cover token expiry, refresh, rotation, and revocation paths.
- Environment-variable docs are updated and reflected in `.env.example`.