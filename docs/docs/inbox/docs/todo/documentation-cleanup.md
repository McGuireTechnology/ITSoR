# Documentation Cleanup TODO

Priority legend: `P1` = current sprint critical, `P2` = near-term, `P3` = follow-on.

Owner legend: `Docs`, `Backend`, `Frontend`, `DevOps`, `Security`.

## Scan Summary (2026-02-19)

Repository scan indicates three major documentation quality gaps:

1. **Organization overlap** between root `README.md`, `docs/README.md`, `docs/getting-started.md`, and `docs/developer/README.md`.
2. **Flow gaps** from concept -> architecture -> implementation (missing explicit domain-model and API-reference navigation path).
3. **Missing operational topics** for deployment, runbooks, troubleshooting, and audience-specific how-to guides.

## Organization and Information Architecture

- [ ] [P2][Owner: Docs] Normalize section naming conventions (`Guide`, `Reference`, `How-to`, `Runbook`) across all docs pages.
- [x] [P1][Owner: Docs] Define canonical audience map (`operator`, `developer`, `security/reviewer`, `admin`) and align each top-level docs page to one audience.
- [x] [P1][Owner: Docs] De-duplicate onboarding content across `README.md`, `docs/README.md`, and `docs/getting-started.md` with one canonical quickstart source.
- [x] [P1][Owner: Docs] Add a docs IA page (or section) that explains where concept, architecture, API, operations, and backlog docs live.

## Reader Flow and Navigation

- [x] [P1][Owner: Docs] Create an explicit reading path: `System Definition` -> `Architecture` -> `Standards Baseline` -> `References` -> subapp/API docs.
- [x] [P1][Owner: Docs] Add "Next steps" blocks on major pages to improve progression and reduce dead-end docs.
- [x] [P2][Owner: Docs] Add cross-links between auth docs, environment docs, and troubleshooting docs for common debugging paths.
- [x] [P2][Owner: Docs] Add quick "role-based entry points" section on docs home page.

## Missing Topics (High-Value)

- [ ] [P2][Owner: Frontend] Add frontend architecture guide (state boundaries, API client usage, error handling pattern).
- [ ] [P2][Owner: Docs] Expand user guide from placeholder to task-based walkthroughs with screenshots and role-specific examples.
- [x] [P1][Owner: Backend] Add API reference strategy page (OpenAPI contract, generated client workflow, versioning policy).
- [x] [P1][Owner: Backend] Add domain model reference for asset-centric entities, first-class relationships, control assertions, evidence, and drift snapshots.
- [x] [P1][Owner: DevOps] Add backend deployment/runtime guide (service process model, persistence, migrations, rollback).
- [x] [P1][Owner: Security] Add security runbooks for auth incidents, secret rotation, and emergency token invalidation flow.

## Consistency and Quality Gates

- [ ] [P2][Owner: DevOps] Add docs link-check and markdown lint checks in CI.
- [ ] [P2][Owner: Docs] Add periodic docs freshness checklist (ownership, last-reviewed date, stale-page detection).
- [x] [P1][Owner: Docs] Add docs style guide for tone, heading levels, code block language tags, and command formatting standards.

## Documentation FIXME Candidates

- [ ] [P2][Owner: Docs] Replace `User Guide` TODO placeholders with committed issue-backed tasks and delivery milestones.
- [ ] [P2][Owner: Docs] Add missing architecture diagrams for control-to-asset-to-evidence chain and drift timeline.
- [x] [P1][Owner: Docs] Fix overlap where multiple pages currently provide competing quickstart/setup instructions.
