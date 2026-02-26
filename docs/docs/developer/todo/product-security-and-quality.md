# Product, Security, and Quality

## P1 (Critical)

- [ ] [P1][Owner: Backend] Add token expiry and refresh-token strategy documentation and implementation plan.
- [ ] [P1][Owner: Backend] Add role model (`admin`, `editor`, `viewer`) and protect at least one backend route by role.
- [ ] [P1][Owner: Backend] Add backend auth rate-limiting strategy for login/signup abuse protection.
- [ ] [P1][Owner: Backend] Implement email-based password recovery flow (request token, verify token, reset completion).
- [ ] [P1][Owner: Backend] Move DB URL and JWT settings to explicit environment variables with documented defaults.
- [ ] [P1][Owner: Backend] Add Alembic migrations and create initial migration for `users`.
- [ ] [P1][Owner: Backend] Add PostgreSQL production profile (connection settings, migration path, ops notes).
- [ ] [P1][Owner: Backend] Implement asset-level control mapping (controls attached to assets/services/identities/data classifications).
- [ ] [P1][Owner: Backend] Implement evidence freshness tracking and stale-evidence detection for assertions.
- [ ] [P1][Owner: Backend] Add drift evaluation pipeline (baseline vs current state) with severity and criticality-aware prioritization.
- [ ] [P1][Owner: Backend] Add deterministic posture computation inputs (criticality, severity, control failure, exposure path, time-in-violation).
- [ ] [P1][Owner: DevOps] Add Playwright end-to-end suite for login/signup/dashboard/logout critical flows.
- [ ] [P1][Owner: Backend] Add tests for invalid login, invalid token, and missing auth header behavior.
- [ ] [P1][Owner: Frontend] Add frontend unit tests for login/signup state transitions and API error handling.
- [ ] [P1][Owner: Frontend] Add app-level dark mode support with persisted preference.
- [ ] [P1][Owner: Frontend] Adopt Tailwind CSS + shadcn/ui foundation for auth/dashboard views.
- [ ] [P1][Owner: Frontend] Split auth API logic into a dedicated client module.
- [ ] [P1][Owner: Frontend] Add form validation and inline field-level errors for auth forms.
- [ ] [P1][Owner: Backend] Publish OpenAPI contract quality gates for stable client generation.
- [ ] [P1][Owner: Frontend] Add generated frontend API client and replace manual API wiring incrementally.
- [ ] [P1][Owner: Security] Add secret scanning and dependency review checks to pull request workflows.
- [ ] [P1][Owner: Backend] Move route-level ORM logic in auth handlers to application-layer use cases.
- [ ] [P1][Owner: Backend] Enforce non-default `JWT_SECRET` outside local development and fail startup on insecure defaults.
- [ ] [P1][Owner: Backend] Replace runtime `ensure_user_role_column()` patch with Alembic-managed migrations.
- [ ] [P1][Owner: Frontend] Extract auth API/session logic from `App.vue` into dedicated module/store.
- [ ] [P1][Owner: Security] Replace localStorage bearer-token persistence with hardened session strategy.
- [ ] [P1][Owner: DevOps] Switch backend auth tests to isolated ephemeral DB with deterministic cleanup.
- [ ] [P1][Owner: Backend] Move admin endpoints into dedicated subapp router namespace.
- [ ] [P1][Owner: Backend] Add CSRF protection for cookie-authenticated state-changing routes.
- [ ] [P1][Owner: Backend] Enforce strict cookie security settings in non-local environments.
- [ ] [P1][Owner: DevOps] Add CI vulnerability gates (`pip-audit`, `npm audit`) alongside dependency-review checks.
- [ ] [P1][Owner: Security] Add abuse-prevention tests for login/signup throttling and lockout.
- [ ] [P1][Owner: Backend] Resolve TODO in auth for issuer/audience/jti claim support and refresh-token rotation alignment.
- [ ] [P1][Owner: Backend] Resolve TODO in main by moving admin endpoints to identity/access subapp routing.
- [ ] [P1][Owner: DevOps] Resolve FIXME in auth tests by using isolated ephemeral test databases.

## P2 (Near-term)

- [ ] [P2][Owner: Backend] Add structured API error format and standardize error responses.
- [ ] [P2][Owner: Backend] Add backend startup validation for required config in non-dev environments.
- [ ] [P2][Owner: Backend] Add vulnerability-to-control impact correlation views (CVE/CVSS mapped to assertions).
- [ ] [P2][Owner: Docs] Document posture scoring formula and data dependencies.
- [ ] [P2][Owner: DevOps] Add backend coverage reporting in CI and enforce minimum threshold.
- [ ] [P2][Owner: DevOps] Add integration smoke test validating signup -> login -> `/auth/me` against running stack.
- [ ] [P2][Owner: Frontend] Expand frontend stack to TypeScript-based modules and typed contracts.
- [ ] [P2][Owner: Frontend] Add authenticated route guard pattern for dashboard views.
- [ ] [P2][Owner: Frontend] Add global sign-out on 401 responses from protected API calls.
- [ ] [P2][Owner: Docs] Add architecture section for auth flow diagram and token lifecycle.
- [ ] [P2][Owner: Docs] Add contributor checklist for tests/docs updates when API contracts change.
- [ ] [P2][Owner: DevOps] Add deployment notes for backend runtime and DB persistence strategy.
- [ ] [P2][Owner: Security] Add auth incident runbook (key rotation, forced logout procedure).
- [ ] [P2][Owner: Backend] Implement JWT claim hardening (`iss`, `aud`, `jti`) with revocation/rotation handling.

## P3 (Follow-on)

- [ ] [P3][Owner: Backend] Add password reset flow design updates (request token, validate token, rotate password).
- [ ] [P3][Owner: DevOps] Add backup/restore verification checklist for environment data.