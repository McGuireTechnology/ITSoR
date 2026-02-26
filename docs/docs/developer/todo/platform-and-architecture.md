# Platform and Architecture

## P1 (Critical)

- [ ] [P1][Owner: Backend] Define target backend package layout by slice: `grc`, `itam`, `cmdb` with `domain`, `application`, and `adapters` layers.
- [ ] [P1][Owner: Backend] Add architecture decision record documenting ports/adapters boundaries and dependency rules.
- [ ] [P1][Owner: Backend] Create first vertical slice (`grc`) with explicit inbound and outbound ports.
- [ ] [P1][Owner: Backend] Refactor one existing endpoint flow to call an application use case instead of accessing persistence directly.
- [ ] [P1][Owner: Backend] Define canonical asset model contract with stable asset identity, ownership, criticality, and control-impact metadata.
- [ ] [P1][Owner: Backend] Implement first-class relationships model with temporal validity windows.
- [ ] [P1][Owner: Backend] Add versioned state snapshot strategy supporting historical reconstruction.
- [ ] [P1][Owner: Backend] Define control assertion schema bound to assets/services/identities/data classifications.
- [ ] [P1][Owner: Backend] Define evidence linkage model (`assertion` -> `observed_state` -> `evaluation_result`) with timestamped traceability.
- [ ] [P1][Owner: Frontend] Implement frontend subapp navigation shells for `grc`, `itam`, and `cmdb`.
- [ ] [P1][Owner: Backend] Define subapp-specific domain seeds and CRUD contracts for each category.
- [ ] [P1][Owner: Backend] Implement backend subapp router modules for `grc`, `itam`, and `cmdb` mounted under `/grc`, `/itam`, `/cmdb`.
- [ ] [P1][Owner: Backend] Add startup wiring to register subapp routes and shared dependencies consistently.
- [ ] [P1][Owner: Backend] Create minimal health/status endpoint per subapp for routing validation.
- [ ] [P1][Owner: Backend] Add `identity-access` subapp for users, roles, policy rules, service accounts, and API keys.
- [ ] [P1][Owner: DevOps] Add Docker Compose stack for local development (backend, frontend/web, db, mailcatcher).
- [ ] [P1][Owner: DevOps] Add Docker Compose production profile with image/runtime separation and env-driven configuration.
- [ ] [P1][Owner: DevOps] Add Traefik reverse proxy/load balancer configuration for service routing.
- [ ] [P1][Owner: Docs] Add deployment guide for Docker Compose + Traefik with automatic HTTPS certificate setup.
- [ ] [P1][Owner: Backend] Define ingestion/normalization boundaries for SPDX and CPE identifiers within software asset records.
- [ ] [P1][Owner: Backend] Define vulnerability evidence integration contract for CVE/CVSS and check-oriented evidence sources.
- [ ] [P1][Owner: Backend] `grc` scaffolded with layered package roots and health route.
- [ ] [P1][Owner: Backend] `itam` scaffolded with layered package roots and health route.
- [ ] [P1][Owner: Backend] `cmdb` scaffolded with layered package roots and health route.
- [ ] [P1][Owner: Backend] `idam` scaffolded with layered package roots and identity-access route.

## P2 (Near-term)

- [ ] [P2][Owner: Backend] Introduce adapter implementations for persistence and external integrations behind defined ports.
- [ ] [P2][Owner: Backend] Add test strategy by layer: domain unit tests, use-case tests, adapter integration tests.
- [ ] [P2][Owner: DevOps] Add CI check to enforce import boundaries (domain cannot depend on adapters/framework code).
- [ ] [P2][Owner: Docs] Add architecture docs page with per-slice component diagrams and request flow examples.
- [ ] [P2][Owner: Backend] Evaluate relational implementation patterns for relationship traversal performance before graph-sidecar consideration.
- [ ] [P2][Owner: Docs] Add ADR for asset-anchor and temporal modeling strategy (snapshot vs delta tradeoffs).
- [ ] [P2][Owner: Frontend] Add per-subapp route guards and shared auth/session handling.
- [ ] [P2][Owner: DevOps] Add smoke tests to verify all subapp routes are mounted and reachable.
- [ ] [P2][Owner: Docs] Document subapp boundaries, ownership, and API prefixes.
- [ ] [P2][Owner: Backend] Add `integrations` subapp for connectors and ingestion jobs.
- [ ] [P2][Owner: Backend] Add `discovery-reconciliation` subapp for ingestion, deduplication, and conflict handling.
- [ ] [P2][Owner: Backend] Add `workflow-approvals` subapp for lifecycle workflows and attestations.
- [ ] [P2][Owner: Backend] Add `reporting-evidence` subapp for dashboards, evidence packs, and scheduled exports.
- [ ] [P2][Owner: Frontend] Add top-level navigation groups for approved phase-2 subapps.
- [ ] [P2][Owner: Docs] Document phase-2 subapp boundaries, ownership model, and API/event contracts.
- [ ] [P2][Owner: Backend] Define and prioritize ITSM/ESM slice scope, entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize CMDB slice scope, entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize ITAM + SAM scope, entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize IPAM scope, entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize IDAM + PAM + IGA scope, entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize SIEM + SOAR + Vulnerability Management scope, entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize Observability (APM/NPM/DEM) scope, entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize GRC scope, entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize Backup/DR scope, entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize Cloud & Infrastructure Management scope, entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize Automation/Orchestration scope, entities, and first API contracts.
- [ ] [P2][Owner: Backend] `ipam` scaffolded with layered package roots and health route.
- [ ] [P2][Owner: Backend] `esm` scaffolded with layered package roots and health route.
- [ ] [P2][Owner: Backend] `siem` scaffolded with layered package roots and health route.
- [ ] [P2][Owner: DevOps] Add Mailcatcher service wiring for local email recovery testing.
- [ ] [P2][Owner: DevOps] Expand GitHub Actions toward CI/CD deployment automation with protected environment promotion.
- [ ] [P2][Owner: Backend] Add OSCAL import/export interoperability plan for controls, assertions, and evidence mappings.
- [ ] [P2][Owner: Docs] Publish authoritative glossary for asset, relationship, assertion, evidence, and drift terminology.
- [ ] [P2][Owner: DevOps] Add cross-platform sanity target for tool entry points after `make venv`.
- [ ] [P2][Owner: Docs] Add explicit OS-specific quickstart variants (Windows PowerShell vs macOS/Linux shell).

## P3 (Follow-on)

- [ ] [P3][Owner: Backend] Add `notifications` subapp for email/webhook/event delivery with retry policies.
- [ ] [P3][Owner: Backend] Add `tenant-org` subapp for multi-tenant boundaries, org hierarchy, and scoped authorization.
- [ ] [P3][Owner: Backend] Add `search-index` subapp for cross-domain indexing and query APIs.
- [ ] [P3][Owner: DevOps] Evaluate replacing `cd <dir> && npm ...` with `npm --prefix <dir> ...` for shell consistency.