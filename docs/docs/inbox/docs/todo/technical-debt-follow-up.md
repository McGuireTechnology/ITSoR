# Technical Debt Follow-up TODO

Priority legend: `P1` = current sprint critical, `P2` = near-term.

Owner legend: `Backend`, `Frontend`, `DevOps`, `Security`.

## Code TODO/FIXME Follow-up (Repository Scan)

Re-scan update (2026-02-20): no new first-party code TODO/FIXME markers were found in application sources; matches were limited to docs labels/backlog pages and third-party dependencies under `.venv`.

- [x] [P1][Owner: Backend] Move route-level ORM logic in auth handlers to application-layer use cases per hexagonal slice design.
- [x] [P1][Owner: Backend] Enforce non-default `JWT_SECRET` outside local development and fail startup when insecure defaults are detected.
- [x] [P1][Owner: Backend] Replace runtime `ensure_user_role_column()` compatibility patch with Alembic-managed migration path.
- [x] [P1][Owner: Frontend] Extract auth API/session logic from `App.vue` into dedicated client/store module.
- [x] [P1][Owner: Security] Replace localStorage bearer-token persistence with hardened session strategy.
- [x] [P1][Owner: DevOps] Switch backend auth tests to isolated ephemeral DB setup with deterministic per-test cleanup.
- [x] [P1][Owner: Backend] Move admin endpoints into dedicated subapp router namespace as part of subapp rollout.

## Security Review Follow-up (2026-02-19)

- [x] [P1][Owner: Backend] Add CSRF protection for cookie-authenticated state-changing routes (at minimum `POST /auth/logout`) using origin checks and/or CSRF tokens.
- [x] [P1][Owner: Backend] Enforce strict cookie security settings in non-local environments (`SESSION_COOKIE_SECURE=true`, valid `SESSION_COOKIE_SAMESITE`, and reject insecure combinations).
- [x] [P1][Owner: DevOps] Add CI dependency vulnerability gates (`pip-audit` for Python and `npm audit` for frontend/web) in addition to dependency-review metadata checks.
- [x] [P2][Owner: Backend] Implement JWT claim hardening in access tokens (`iss`, `aud`, `jti`) and pair with revocation/rotation handling.
- [x] [P1][Owner: Security] Add abuse-prevention tests for login/signup throttling and account lockout once rate limiting is implemented.

## Open Code TODO/FIXME Traceability

- [x] [P1][Owner: Backend] Resolve `TODO` in `backend/app/auth.py` for issuer/audience/jti claim support and refresh-token rotation alignment.
- [x] [P1][Owner: Backend] Resolve `TODO` in `backend/app/main.py` by moving admin endpoints to dedicated identity/access subapp routing.
- [x] [P1][Owner: DevOps] Resolve `FIXME` in `backend/tests/test_auth.py` by using isolated ephemeral test databases with per-test cleanup.
