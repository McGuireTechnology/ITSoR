# Documentation and Operations

## P1 (Critical)

- [ ] [P1][Owner: Docs] Define canonical audience map (`operator`, `developer`, `security/reviewer`, `admin`) and align docs accordingly.
- [ ] [P1][Owner: Docs] De-duplicate onboarding content across `README.md`, `docs/README.md`, and `docs/getting-started.md`.
- [ ] [P1][Owner: Docs] Add docs IA page showing where concept, architecture, API, operations, and backlog docs live.
- [ ] [P1][Owner: Docs] Create explicit reading path: System Definition -> Architecture -> Standards Baseline -> References -> subapp/API docs.
- [ ] [P1][Owner: Docs] Add “Next steps” blocks on major pages.
- [ ] [P1][Owner: Backend] Add API reference strategy page (OpenAPI contract, generated client workflow, versioning policy).
- [ ] [P1][Owner: Backend] Add domain model reference for asset-centric entities, relationships, assertions, evidence, and drift snapshots.
- [ ] [P1][Owner: DevOps] Add backend deployment/runtime guide (process model, persistence, migrations, rollback).
- [ ] [P1][Owner: Security] Add security runbooks for auth incidents, secret rotation, and emergency token invalidation.
- [ ] [P1][Owner: Docs] Add docs style guide for tone, heading levels, code-block language tags, and command formatting.
- [ ] [P1][Owner: Docs] Fix overlap where multiple pages provide competing quickstart/setup instructions.
- [ ] [P1][Owner: DevOps] Add CI workflows for docs build, backend checks, frontend build, and web build.
- [ ] [P1][Owner: DevOps] Add `.github/CODEOWNERS`.
- [ ] [P1][Owner: DevOps] Add PR template and issue templates.
- [ ] [P1][Owner: DevOps] Add dependency update automation (Dependabot or Renovate).
- [ ] [P1][Owner: Docs] Align `docs/getting-started.md` with current `make`-based workflow.
- [ ] [P1][Owner: Docs] Align `docs/developer/README.md` with split requirements and current ports.
- [ ] [P1][Owner: Docs] Add docs page explaining local host/port configuration from root `.env`.
- [ ] [P1][Owner: Docs] Add release process section and changelog expectations.
- [ ] [P1][Owner: Backend] Add backend test scaffold (pytest + FastAPI TestClient).
- [ ] [P1][Owner: Backend] Add backend linting/formatting config.
- [ ] [P1][Owner: Backend] Add backend env var reference when config model is finalized.
- [ ] [P1][Owner: Frontend] Replace Vite starter content in `frontend` app.
- [ ] [P1][Owner: Frontend] Replace Vite starter content in `web` app.
- [ ] [P1][Owner: Frontend] Add frontend/web lint and test scripts.
- [ ] [P1][Owner: DevOps] Add deployment notes for docs on GitHub Pages (`docs.itsor.app`).
- [ ] [P1][Owner: DevOps] Define environment naming and promotion flow (dev/stage/prod).
- [ ] [P1][Owner: DevOps] Add frontend/web lint and test jobs to CI workflows.
- [ ] [P1][Owner: Security] Add `SECURITY.md` with vulnerability reporting process.
- [ ] [P1][Owner: DevOps] Add branch protection guidance (required checks/review policy).
- [ ] [P1][Owner: DevOps] Add root `CONTRIBUTING.md` linking to docs contributing guide.
- [ ] [P1][Owner: DevOps] Add least-privilege `permissions` blocks to non-deploy workflows.
- [ ] [P1][Owner: DevOps] Add repository `CODE_OF_CONDUCT.md`.
- [ ] [P1][Owner: DevOps] Add automated security scanning workflow (CodeQL and/or dependency audit).
- [ ] [P1][Owner: DevOps] Add pre-commit hooks for backend/frontend/web/docs checks.
- [ ] [P1][Owner: DevOps] Add workflow `concurrency` controls to CI/security workflows.
- [ ] [P1][Owner: DevOps] Pin third-party GitHub Actions by commit SHA.
- [ ] [P1][Owner: Docs] Replace Windows-only docs build commands with `make docs-build` guidance.
- [ ] [P1][Owner: Docs] Replace Windows-only backend auth command snippets with cross-platform `python -m ...` guidance.
- [ ] [P1][Owner: Docs] Normalize command fence labeling to avoid mixed-shell copy/paste issues.
- [ ] [P1][Owner: DevOps] Add CI smoke job for `make venv && make docs-install && make backend-install` on Windows and macOS.
- [ ] [P1][Owner: Docs] Document Windows prerequisite path for `make` or provide no-`make` equivalents.
- [ ] [P1][Owner: DevOps] Make `make venv` resilient with `py -3` / `python3` fallback.

## P2 (Near-term)

- [ ] [P2][Owner: Docs] Normalize section naming conventions (`Guide`, `Reference`, `How-to`, `Runbook`) across docs.
- [ ] [P2][Owner: Docs] Add cross-links between auth docs, environment docs, and troubleshooting docs.
- [ ] [P2][Owner: Docs] Add role-based entry points section on docs home page.
- [ ] [P2][Owner: Frontend] Add frontend architecture guide (state boundaries, API client patterns, error handling).
- [ ] [P2][Owner: Docs] Expand user guide into task-based walkthroughs with screenshots and role-specific examples.
- [ ] [P2][Owner: DevOps] Add docs link-check and markdown-lint checks in CI.
- [ ] [P2][Owner: Docs] Add periodic docs freshness checklist (ownership, last-reviewed date, stale-page detection).
- [ ] [P2][Owner: Docs] Replace `User Guide` TODO placeholders with issue-backed milestones.
- [ ] [P2][Owner: Docs] Add missing architecture diagrams for control-to-asset-to-evidence chain and drift timeline.
- [ ] [P2][Owner: Frontend] Clean frontend/web lint warnings and remove unused starter components.
- [ ] [P2][Owner: Docs] Document API base URL strategy for local frontend dev.
- [ ] [P2][Owner: DevOps] Add deployment notes for web (`www.itsor.app`).

## P3 (Follow-on)

- [ ] [P3][Owner: Docs] Add recurring documentation quality review cadence by workstream and owner.