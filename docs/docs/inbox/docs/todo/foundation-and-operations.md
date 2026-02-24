# Foundation and Operations TODO

## Repository Management

- [x] Add CI workflows for docs build, backend checks, frontend build, and web build.
- [x] Add `.github/CODEOWNERS`.
- [x] Add PR template and issue templates.
- [x] Add dependency update automation (Dependabot or Renovate).

## Documentation Alignment

- [x] Align `docs/getting-started.md` with current `make`-based workflow.
- [x] Align `docs/developer/README.md` with split requirements and current ports.
- [x] Add a docs page explaining local host/port configuration from root `.env`.
- [x] Add release process section and changelog expectations.

## Backend Foundation

- [x] Add backend test scaffold (pytest + FastAPI TestClient).
- [x] Add backend linting/formatting config.
- [x] Add backend env var reference when config model is finalized.

## Frontend and Web Foundation

- [ ] Clean frontend/web lint warnings and remove unused starter components.
- [ ] Document API base URL strategy for local dev.
- [x] Replace Vite starter content in `frontend` app.
- [x] Replace Vite starter content in `web` app.
- [x] Add frontend/web lint and test scripts.

## Operations

- [ ] Add deployment notes for web (`www.itsor.app`).
- [x] Add deployment notes for docs on GitHub Pages (`docs.itsor.app`).
- [x] Define environment naming and promotion flow (dev/stage/prod).

## Platform Expansion Requests

- [ ] [P1][Owner: DevOps] Add Docker Compose stack for local development (backend, frontend/web, db, mailcatcher).
- [ ] [P1][Owner: DevOps] Add Docker Compose production profile with image/runtime separation and env-driven configuration.
- [ ] [P1][Owner: DevOps] Add Traefik reverse proxy/load balancer configuration for service routing.
- [ ] [P1][Owner: Docs] Add deployment guide for Docker Compose + Traefik with automatic HTTPS certificate setup.
- [ ] [P2][Owner: DevOps] Add Mailcatcher service wiring for local email recovery testing workflows.
- [ ] [P2][Owner: DevOps] Expand GitHub Actions from CI-only toward CI/CD deployment automation with protected environment promotion.

## Standards and Interoperability Expansion

- [ ] [P1][Owner: Backend] Define ingestion/normalization boundaries for SPDX and CPE identifiers within software asset records.
- [ ] [P1][Owner: Backend] Define vulnerability evidence integration contract for CVE/CVSS and check-oriented evidence sources.
- [ ] [P2][Owner: Backend] Add OSCAL import/export interoperability plan focused on control catalogs, assertions, and evidence mappings.
- [ ] [P2][Owner: Docs] Publish authoritative glossary for asset, relationship, assertion, evidence, and drift terms to avoid CMDB-only framing drift.

## Additional Foundation Items (Scan Findings)

- [x] Add frontend/web lint and test jobs to CI workflows (not only build jobs).
- [x] Add `SECURITY.md` with vulnerability reporting process.
- [x] Add branch protection guidance (required checks/review policy) to docs.
- [x] Add root `CONTRIBUTING.md` that links to `docs/contributing.md` for GitHub discoverability.

## Additional Foundation Items (Scan Findings - Round 2)

- [x] Add explicit least-privilege `permissions` blocks to non-deploy GitHub workflows.
- [x] Add repository `CODE_OF_CONDUCT.md`.
- [x] Add automated security scanning workflow (e.g., CodeQL and/or dependency audit job).
- [x] Add pre-commit hooks configuration for backend/frontend/web/docs lint checks.

## Additional Foundation Items (Scan Findings - Round 3)

- [x] Add workflow `concurrency` controls to CI/security workflows to cancel superseded runs.
- [x] Pin third-party GitHub Actions by commit SHA for stronger supply-chain hardening.