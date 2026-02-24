# Architecture and Subapps TODO

Priority legend: `P1` = current sprint critical, `P2` = near-term, `P3` = follow-on.

Owner legend: `Backend`, `Frontend`, `Docs`, `DevOps`, `Security`.

## Hexagonal Architecture (Vertical Slice Alignment)

- [ ] [P2][Owner: Backend] Introduce adapter implementations for persistence and external integrations behind defined ports.
- [ ] [P2][Owner: Backend] Add test strategy by layer: domain unit tests, application use-case tests, adapter integration tests.
- [ ] [P2][Owner: DevOps] Add CI check to enforce import boundaries (domain cannot depend on adapters/framework code).
- [ ] [P2][Owner: Docs] Add architecture docs page with per-slice component diagrams and request flow examples.
- [x] [P1][Owner: Backend] Define target backend package layout by slice: `grc`, `itam`, `cmdb` with `domain`, `application`, and `adapters` layers.
- [x] [P1][Owner: Backend] Add architecture decision record documenting ports/adapters boundaries and dependency rules.
- [x] [P1][Owner: Backend] Create first vertical slice (`grc`) with explicit inbound port (use case interface) and outbound ports (repository/service interfaces).
- [x] [P1][Owner: Backend] Refactor one existing endpoint flow to call an application use case instead of accessing persistence directly.

## Asset-Centric Relational Model

- [x] [P1][Owner: Backend] Define canonical asset model contract with stable asset identity, ownership, criticality, and control-impact metadata ([Domain Model Reference](../domain-model-reference.md#canonical-asset-model-contract-v1)).
- [x] [P1][Owner: Backend] Implement first-class `relationships` model with type system and temporal validity windows (`valid_from`/`valid_to`) ([Domain Model Reference](../domain-model-reference.md#relationship-model-contract-v1)).
- [x] [P1][Owner: Backend] Add versioned state snapshot strategy (baseline + delta evaluation) that supports historical reconstruction ([Domain Model Reference](../domain-model-reference.md#versioned-state-snapshot-strategy-v1)).
- [x] [P1][Owner: Backend] Define control assertion schema bound to assets/services/identities/data classifications rather than org-only scope ([Domain Model Reference](../domain-model-reference.md#control-assertion-schema-contract-v1)).
- [x] [P1][Owner: Backend] Define evidence linkage model (`assertion` -> `observed_state` -> `evaluation_result`) with timestamped traceability ([Domain Model Reference](../domain-model-reference.md#evidence-linkage-model-contract-v1)).
- [ ] [P2][Owner: Backend] Evaluate relational implementation patterns for relationship traversal performance before graph-sidecar consideration.
- [ ] [P2][Owner: Docs] Add architecture decision record for asset-anchor and temporal modeling strategy (snapshot vs. delta tradeoffs).

## Subapps (GRC, ITAM, CMDB)

- [ ] [P2][Owner: Frontend] Add per-subapp route guards and shared auth/session handling.
- [x] [P1][Owner: Frontend] Implement frontend subapp navigation shells for `grc`, `itam`, and `cmdb` ([Frontend App](../../frontend/src/App.vue)).
- [x] [P1][Owner: Backend] Define subapp-specific domain seeds: initial entities and CRUD contracts for each category ([Domain Model Reference](../domain-model-reference.md#subapp-domain-seeds-and-crud-contracts-v1)).
- [ ] [P2][Owner: DevOps] Add smoke tests to verify all subapp routes are mounted and reachable.
- [ ] [P2][Owner: Docs] Document subapp boundaries, ownership, and API prefixes.
- [x] [P1][Owner: Backend] Implement backend subapp router modules for `grc`, `itam`, and `cmdb` and mount them under `/grc`, `/itam`, `/cmdb`.
- [x] [P1][Owner: Backend] Add startup wiring to register subapp routes and shared dependencies consistently.
- [x] [P1][Owner: Backend] Create minimal health/status endpoint for each subapp to validate independent routing.

## Subapps (Phase 2 Recommendations)

- [x] [P1][Owner: Backend] Add `identity-access` subapp for users, roles, policy rules, service accounts, and API keys ([IDAM Routes](../../backend/app/idam/api/routes/admin.py)).
- [ ] [P2][Owner: Backend] Add `integrations` subapp for connectors (cloud, scanner, ticketing, SIEM, IdP) and ingestion jobs.
- [ ] [P2][Owner: Backend] Add `discovery-reconciliation` subapp for source ingestion, deduplication, and source-of-truth conflict handling.
- [ ] [P2][Owner: Backend] Add `workflow-approvals` subapp for lifecycle workflows, approvals, and exception attestations.
- [ ] [P2][Owner: Backend] Add `reporting-evidence` subapp for dashboards, evidence packs, and scheduled compliance exports.
- [ ] [P3][Owner: Backend] Add `notifications` subapp for email/webhook/event delivery with retry policies.
- [ ] [P3][Owner: Backend] Add `tenant-org` subapp for multi-tenant boundaries, org hierarchy, and scoped authorization.
- [ ] [P3][Owner: Backend] Add `search-index` subapp for cross-domain indexing and query APIs across CMDB/ITAM/GRC entities.
- [ ] [P2][Owner: Frontend] Add top-level navigation groups for all approved phase-2 subapps.
- [ ] [P2][Owner: Docs] Document phase-2 subapp boundaries, ownership model, and API/event contracts.

## Service Domain Backlog Map

- [ ] [P2][Owner: Backend] Define and prioritize `ITSM / ESM` slice scope, core entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize `CMDB` slice scope, core entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize `ITAM + SAM` slice scope, core entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize `IPAM` slice scope, core entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize `IDAM + PAM + IGA` slice scope, core entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize `SIEM + SOAR + Vulnerability Management` scope, core entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize `Observability (APM/NPM/DEM)` scope, core entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize `GRC` slice scope, core entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize `Backup / DR` scope, core entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize `Cloud & Infrastructure Management` scope, core entities, and first API contracts.
- [ ] [P2][Owner: Backend] Define and prioritize `Automation / Orchestration Layer` scope, core entities, and first API contracts.

## Current Scaffold Status

- [x] [P1][Owner: Backend] `grc` scaffolded with layered package roots (`api`, `domain`, `infrastructure`) and health route.
- [x] [P1][Owner: Backend] `itam` scaffolded with layered package roots (`api`, `domain`, `infrastructure`) and health route.
- [x] [P1][Owner: Backend] `cmdb` scaffolded with layered package roots (`api`, `domain`, `infrastructure`) and health route.
- [x] [P1][Owner: Backend] `idam` scaffolded with layered package roots (`api`, `domain`, `infrastructure`) and identity-access route.
- [x] [P2][Owner: Backend] `ipam` scaffolded with layered package roots (`api`, `domain`, `infrastructure`) and health route.
- [x] [P2][Owner: Backend] `esm` scaffolded with layered package roots (`api`, `domain`, `infrastructure`) and health route.
- [x] [P2][Owner: Backend] `siem` scaffolded with layered package roots (`api`, `domain`, `infrastructure`) and health route.