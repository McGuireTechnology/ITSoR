# Product and Quality TODO

Priority legend: `P1` = current sprint critical, `P2` = near-term, `P3` = follow-on.

Owner legend: `Backend`, `Frontend`, `Docs`, `DevOps`, `Security`.

## Auth and Identity

- [ ] [P3][Owner: Backend] Add password reset flow design (request token, validate token, rotate password).
- [x] [P1][Owner: Backend] Add token expiry and refresh-token strategy documentation and implementation plan.
- [x] [P1][Owner: Backend] Add role model (`admin`, `editor`, `viewer`) and protect at least one backend route by role.
- [x] [P1][Owner: Backend] Add backend auth rate limiting strategy (login and signup abuse protection).
- [x] [P1][Owner: Backend] Implement email-based password recovery flow (request token, verify token, password reset completion).

## Backend Data and Configuration

- [ ] [P2][Owner: Backend] Add structured API error format and standardize error responses across routes.
- [ ] [P2][Owner: Backend] Add backend startup validation for required config in non-dev environments.
- [x] [P1][Owner: Backend] Move DB URL and JWT settings to explicit environment variables with documented defaults.
- [x] [P1][Owner: Backend] Add Alembic migrations and create initial migration for `users` table.
- [x] [P1][Owner: Backend] Add PostgreSQL production profile (connection settings, migration path, and operational notes).

## Control and Evidence Intelligence

- [ ] [P2][Owner: Backend] Add vulnerability-to-control impact correlation views (CVE/CVSS findings mapped to affected assertions).
- [ ] [P2][Owner: Docs] Document posture scoring formula and data dependencies to avoid opaque/marketing-only scoring.
- [x] [P1][Owner: Backend] Implement asset-level control mapping (controls attached to assets/services/identities/data classifications).
- [x] [P1][Owner: Backend] Implement evidence freshness tracking and stale-evidence detection for control assertions.
- [x] [P1][Owner: Backend] Add drift evaluation pipeline (baseline vs current state) with severity and criticality-aware prioritization.
- [x] [P1][Owner: Backend] Add deterministic security posture computation inputs (criticality, vulnerability severity, control failure, exposure path, time-in-violation).

## Testing and Quality

- [ ] [P2][Owner: DevOps] Add backend coverage reporting in CI and enforce a minimum threshold.
- [ ] [P2][Owner: DevOps] Add integration smoke test that validates signup -> login -> `/auth/me` against a running stack.
- [ ] [P1][Owner: DevOps] Add Playwright end-to-end test suite for login/signup/dashboard/logout critical flows.
- [x] [P1][Owner: Backend] Add tests for invalid login, invalid token, and missing auth header behavior.
- [x] [P1][Owner: Frontend] Add frontend unit tests for login/signup state transitions and API error handling.

## Frontend UX Hardening

- [ ] [P1][Owner: Frontend] Add app-level dark mode support with persisted user preference.
- [ ] [P1][Owner: Frontend] Adopt Tailwind CSS + shadcn/ui component foundation for auth and dashboard views.
- [ ] [P2][Owner: Frontend] Expand frontend stack to TypeScript-based app modules and typed state/api contracts.
- [ ] [P2][Owner: Frontend] Add authenticated route guard pattern for dashboard views.
- [ ] [P2][Owner: Frontend] Add global sign-out on 401 responses from protected API calls.
- [x] [P1][Owner: Frontend] Split auth API logic into a dedicated client module (remove direct fetch calls from view).
- [x] [P1][Owner: Frontend] Add form validation and inline field-level errors for email/password/full name.

## API Contract and Client Generation

- [x] [P1][Owner: Backend] Publish OpenAPI contract quality gates for stable client generation.
- [x] [P1][Owner: Frontend] Add automatically generated frontend API client and replace manual auth API wiring incrementally.

## Documentation and Developer Experience

- [ ] [P2][Owner: Docs] Add architecture page section for auth flow diagram and token lifecycle.
- [ ] [P2][Owner: Docs] Add contributor checklist for updating tests/docs when API contracts change.
- [x] [P1][Owner: Docs] Add backend auth setup guide (env vars, local run commands, test commands).
- [x] [P1][Owner: Docs] Add frontend auth integration guide with `VITE_API_BASE_URL` examples.

## Operations and Security Follow-through

- [ ] [P2][Owner: DevOps] Add deployment notes for backend service runtime and DB persistence strategy.
- [ ] [P2][Owner: Security] Add runbook for auth incidents (token key rotation, forced logout procedure).
- [ ] [P3][Owner: DevOps] Add backup/restore verification checklist for environment data.
- [x] [P1][Owner: Security] Add secret scanning and dependency review checks to pull request workflows.
