# Domain Model Reference

This page defines the canonical domain-model structure for ITSoR as an asset-centric, control-aware system of record.

## Scope

This reference covers the required first-class model areas:

- Asset-centric entities
- First-class relationships
- Control assertions
- Evidence linkage
- Drift snapshots and temporal reconstruction

## Asset-Centric Entities

Assets are the primary anchor and must be represented as explicit entities, not generic blobs.

### Canonical Asset Model Contract (v1)

Every asset record must conform to this canonical contract.

Required fields:

| Field | Type | Requirement | Notes |
| --- | --- | --- | --- |
| `asset_id` | string (UUID/ULID) | Required, immutable | Stable internal identity for joins, lineage, and API references. |
| `asset_type` | enum | Required | Must be one of approved domain categories (hardware, virtual, software, identity, data, network, policy, contract). |
| `display_name` | string | Required | Human-readable canonical name; aliases belong in metadata/extensions. |
| `state` | enum | Required | Lifecycle state (`active`, `inactive`, `retired`, etc.). |
| `owner_principal_id` | string | Required | Owning identity reference; resolves to user/service principal in identity domain. |
| `steward_principal_id` | string | Optional | Operational steward where owner and maintainer differ. |
| `criticality` | enum | Required | Business criticality tier (`low`, `medium`, `high`, `critical`). |
| `control_impact` | enum | Required | Control impact tier (`low`, `moderate`, `high`) used in posture/risk weighting. |
| `source_system` | string | Required | Discovery/import/manual source of truth for provenance. |
| `source_record_id` | string | Optional | Source-native identifier for reconciliation and idempotent ingest. |
| `valid_from` | timestamp | Required | Start of temporal validity for this asset state. |
| `valid_to` | timestamp/null | Required | End of validity; `null` means currently valid. |
| `created_at` | timestamp | Required | Record creation timestamp (append-only model). |
| `updated_at` | timestamp | Required | Last mutation timestamp within current version row. |

Contract invariants:

1. `asset_id` is never re-used and never reassigned.
2. At most one currently valid row exists per `asset_id` where `valid_to` is `null`.
3. `criticality` and `control_impact` are mandatory classification inputs for posture scoring.
4. Ownership (`owner_principal_id`) must always resolve to an identity-domain principal.
5. Type-specific attributes extend this contract but cannot replace required canonical fields.

Minimum top-level categories:

- Hardware asset
- Virtual asset
- Software instance
- Identity (human or service)
- Data asset/classification
- Network construct
- Policy/document artifact
- Contract/license artifact

Common required attributes:

- Stable internal identifier
- External reference identifiers (where applicable)
- Lifecycle state (`active`, `inactive`, `retired`, etc.)
- Owner/responsible identity reference
- Source provenance (discovery/manual/import)
- Validity window (`valid_from`, `valid_to`)

## First-Class Relationships

Relationships are modeled as explicit records with temporal validity.

### Relationship Model Contract (v1)

Every relationship record must conform to this canonical contract.

Required fields:

| Field | Type | Requirement | Notes |
| --- | --- | --- | --- |
| `relationship_id` | string (UUID/ULID) | Required, immutable | Stable relationship identity for lineage and auditability. |
| `relationship_type` | enum | Required | Typed semantic edge from controlled relationship taxonomy. |
| `source_asset_id` | string | Required | Upstream/owner/source asset reference. |
| `target_asset_id` | string | Required | Downstream/dependent/target asset reference. |
| `directionality` | enum | Required | `directed` or `undirected`; query and traversal behavior must honor this value. |
| `state` | enum | Required | Lifecycle state (`active`, `inactive`, `retired`). |
| `confidence` | integer | Optional | `0-100` confidence score for inferred/discovered links. |
| `source_system` | string | Required | Discovery/import/manual provenance source. |
| `source_record_id` | string | Optional | Source-native identifier for reconciliation and idempotency. |
| `valid_from` | timestamp | Required | Start of relationship validity window. |
| `valid_to` | timestamp/null | Required | End of relationship validity; `null` means currently valid. |
| `created_at` | timestamp | Required | Record creation timestamp in append-only history. |
| `updated_at` | timestamp | Required | Last mutation timestamp for current version row. |

Approved relationship type system (initial set):

- `depends_on`
- `hosts`
- `connected_to`
- `owned_by`
- `uses_data_from`
- `implements_control_for`

Temporal and integrity invariants:

1. `source_asset_id` and `target_asset_id` must reference existing canonical assets.
2. `valid_from` must be less than `valid_to` when `valid_to` is not `null`.
3. For a given `(source_asset_id, target_asset_id, relationship_type)`, validity windows must not overlap.
4. At most one current row exists per `(source_asset_id, target_asset_id, relationship_type)` where `valid_to` is `null`.
5. Relationship semantic type (`relationship_type`) cannot be free text and must be constrained to the approved taxonomy.

Recommended relational indexes:

- `(source_asset_id, relationship_type, valid_to)` for forward traversal
- `(target_asset_id, relationship_type, valid_to)` for reverse traversal
- `(relationship_type, valid_to)` for current-state and analytics filtering
- Unique partial index on `(source_asset_id, target_asset_id, relationship_type)` where `valid_to IS NULL`

Examples:

- `depends_on`
- `hosts`
- `connected_to`
- `owned_by`
- `uses_data_from`
- `implements_control_for`

Relationship rules:

1. Store source and target entity references.
2. Store typed relationship semantics (not free text).
3. Store validity window and change provenance.
4. Avoid implicit relationships hidden in unstructured JSON fields.

## Control Assertions

Controls map expected state to concrete entities and relationships.

### Control Assertion Schema Contract (v1)

Control assertions are first-class records scoped to concrete operational targets, not org-only placeholders.

Required fields:

| Field | Type | Requirement | Notes |
| --- | --- | --- | --- |
| `assertion_id` | string (UUID/ULID) | Required, immutable | Canonical assertion identity. |
| `assertion_version` | integer | Required | Monotonic version for intent/model evolution. |
| `framework_id` | string | Required | Control framework source (e.g., `NIST-800-53`, `ISO-27001`). |
| `control_id` | string | Required | Control identifier within framework (`AC-2`, `A.9.2.1`, etc.). |
| `target_type` | enum | Required | `asset`, `service`, `identity`, `data_classification`, `relationship`. |
| `target_id` | string | Required | Canonical identifier for the target entity/classification. |
| `condition_expression` | string | Required | Declarative expected-state rule for evaluation. |
| `evaluation_method` | enum | Required | `automated`, `manual`, or `hybrid`. |
| `evaluation_frequency` | enum/string | Required | Cadence (`continuous`, `hourly`, `daily`, `weekly`, etc.). |
| `staleness_threshold_hours` | integer | Required | Max evidence age before assertion becomes stale. |
| `severity` | enum | Required | `low`, `medium`, `high`, `critical`. |
| `criticality_weight` | integer | Required | Normalized weighting input for posture/risk scoring. |
| `valid_from` | timestamp | Required | Start of assertion validity window. |
| `valid_to` | timestamp/null | Required | End of validity; `null` means currently active. |
| `created_at` | timestamp | Required | Assertion record creation timestamp. |
| `updated_at` | timestamp | Required | Last mutation timestamp for current version row. |

Target binding requirements:

1. `target_type=asset` must bind to canonical `asset_id`.
2. `target_type=service` must bind to a service asset or service-domain entity with stable identity.
3. `target_type=identity` must bind to identity-domain principal (`user`, `service_account`, etc.).
4. `target_type=data_classification` must bind to canonical data class/tier taxonomy.
5. `target_type=relationship` must bind to canonical `relationship_id` where control intent is edge-specific.

Versioning and scope invariants:

1. Assertion intent changes (target, condition, frequency, severity) create a new `assertion_version`.
2. Historical versions remain immutable and queryable for audit reconstruction.
3. Only one current active version exists per `(framework_id, control_id, target_type, target_id)` where `valid_to` is `null`.
4. Assertion records cannot exist without concrete target bindings.
5. Org-only assertions are disallowed unless represented as explicit org-scope assets/services in the canonical model.

Assertion shape:

- Control reference (framework + control identifier)
- Assertion target (asset and/or relationship scope)
- Expected condition statement
- Evaluation method (`automated`, `manual`, `hybrid`)
- Evaluation frequency and staleness threshold
- Severity / criticality
- Assertion validity window

Assertions must be versioned. New assertion intent creates a new assertion version rather than overwriting history.

## Evidence Model

Evidence proves or disproves assertions at a specific time.

### Evidence Linkage Model Contract (v1)

Evidence traceability is modeled as a strict chain:

`assertion` -> `observed_state` -> `evaluation_result`

This chain must be reconstructable for any point in time and any assertion version.

Required observed-state fields:

| Field | Type | Requirement | Notes |
| --- | --- | --- | --- |
| `observed_state_id` | string (UUID/ULID) | Required, immutable | Canonical observation identity. |
| `assertion_id` | string | Required | Links to assertion identity. |
| `assertion_version` | integer | Required | Ensures evaluation is bound to exact assertion semantics. |
| `target_type` | enum | Required | Must align with assertion target type. |
| `target_id` | string | Required | Canonical observed target identity. |
| `observed_at` | timestamp | Required | Timestamp when state was observed/measured. |
| `collected_at` | timestamp | Required | Timestamp when data was collected by tooling/user. |
| `collector_id` | string | Required | Collector/agent identity used for provenance. |
| `source_system` | string | Required | Source of observed evidence data. |
| `raw_evidence_ref` | string | Required | Immutable pointer/checksum/URI to raw evidence payload. |
| `normalized_state` | json | Required | Canonical extracted state used by evaluator. |

Required evaluation-result fields:

| Field | Type | Requirement | Notes |
| --- | --- | --- | --- |
| `evaluation_result_id` | string (UUID/ULID) | Required, immutable | Canonical evaluation outcome identity. |
| `observed_state_id` | string | Required | Links to specific observed state instance. |
| `assertion_id` | string | Required | Redundant link for query efficiency and integrity checks. |
| `assertion_version` | integer | Required | Must match observed-state assertion version. |
| `evaluated_at` | timestamp | Required | Timestamp when rule evaluation occurred. |
| `result_status` | enum | Required | `pass`, `fail`, `unknown`, `error`. |
| `result_reason` | string | Optional | Human/system-readable rationale for outcome. |
| `evaluator_version` | string | Required | Rules/engine version for reproducibility. |
| `confidence` | integer | Optional | `0-100` confidence score where applicable. |
| `stale_at` | timestamp | Required | Deterministic staleness deadline derived from assertion policy. |

Linkage and temporal invariants:

1. Every `evaluation_result` must reference exactly one `observed_state_id`.
2. Every `observed_state` must reference exactly one `(assertion_id, assertion_version)` pair.
3. `observed_at <= evaluated_at` must always hold.
4. Traceability queries must support end-to-end reconstruction from assertion to raw evidence artifact.
5. Historical records are append-only; corrections are new observations/evaluations, not in-place edits.

Minimum traceability query outcomes:

- Given an assertion, retrieve all observations and evaluations in chronological order.
- Given a failed evaluation, retrieve raw evidence and collector provenance.
- Given a timestamp $t$, reconstruct assertion outcome and evidence lineage valid at $t$.
- Given a stale result, determine missing/expired observation source and required refresh action.

Evidence record requirements:

- Linked assertion reference
- Linked target entity/relationship reference
- Observation timestamp
- Collector/source metadata
- Result status (`pass`, `fail`, `unknown`, `error`)
- Raw evidence pointer (artifact ID, URI, or checksum)
- Normalized extracted fields used in evaluation

Evidence must remain traceable and immutable enough for audit reconstruction.

## Drift Snapshots and Temporal Model

Drift is computed from time-indexed snapshots and assertion outcomes.

### Versioned State Snapshot Strategy (v1)

State reconstruction is built on two complementary artifacts: immutable baseline snapshots and append-only delta events.

Required snapshot contract fields:

| Field | Type | Requirement | Notes |
| --- | --- | --- | --- |
| `snapshot_id` | string (UUID/ULID) | Required, immutable | Unique snapshot identity. |
| `snapshot_type` | enum | Required | `baseline` or `materialized`. |
| `scope_id` | string | Required | Tenant/org/system scope for consistent reconstruction boundaries. |
| `captured_at` | timestamp | Required | Logical state capture timestamp. |
| `created_at` | timestamp | Required | Persistence timestamp for ingestion ordering/audit. |
| `parent_snapshot_id` | string/null | Optional | Prior baseline/materialized snapshot dependency. |
| `data_version` | integer | Required | Schema/contract version for replay safety. |
| `integrity_hash` | string | Required | Hash/checksum of normalized snapshot payload. |

Required delta contract fields:

| Field | Type | Requirement | Notes |
| --- | --- | --- | --- |
| `delta_id` | string (UUID/ULID) | Required, immutable | Unique event identity. |
| `scope_id` | string | Required | Must match target snapshot reconstruction scope. |
| `effective_at` | timestamp | Required | Business-effective change time. |
| `recorded_at` | timestamp | Required | Ingested timestamp; may differ from `effective_at`. |
| `entity_kind` | enum | Required | `asset`, `relationship`, `assertion`, `evidence`. |
| `entity_id` | string | Required | Canonical entity reference modified by delta. |
| `operation` | enum | Required | `create`, `update`, `close`, `delete_logical`. |
| `before_hash` | string/null | Optional | Prior-state checksum for conflict detection. |
| `after_hash` | string/null | Optional | Post-state checksum for replay verification. |
| `change_set` | json | Required | Minimal normalized field-level mutation payload. |

Reconstruction strategy:

1. Choose nearest prior `baseline` snapshot for a scope and replay deltas by `effective_at`, then `recorded_at`, then `delta_id`.
2. Produce a deterministic materialized state at time $t$ by applying only deltas where `effective_at <= t`.
3. Preserve both baseline and replayed effective state for drift comparisons and audit traceability.
4. Periodically roll forward a new baseline snapshot to cap replay depth and improve query latency.

Delta evaluation model:

- Baseline snapshot = authoritative point-in-time anchor.
- Delta set = append-only mutations since anchor.
- Evaluated state at time $t$ = `baseline + ordered_deltas(t)`.
- Drift score/event = difference between current evaluated state and selected policy baseline.

Temporal and integrity invariants:

1. Snapshots and deltas are immutable after write; corrections are represented as new deltas.
2. Replay ordering must be deterministic across environments.
3. Every delta must reference a valid `scope_id` and canonical entity identifier.
4. A reconstruction job must be able to produce the same state hash for the same `scope_id` and time $t$.
5. Baseline compaction cannot discard provenance links needed for audit reconstruction.

Snapshot model requirements:

- Snapshot timestamp and scope
- Asset and relationship state projection
- Assertion evaluation projection
- Delta against baseline/previous snapshot
- Drift window (`drift_started_at`, `drift_resolved_at`)

Temporal rules:

1. Do not overwrite authoritative historical state.
2. Use append-oriented records with validity windows.
3. Preserve baseline and observed state separately.
4. Support point-in-time queries for posture reconstruction.

## Minimal Query Outcomes (North-Star)

The model should support deterministic answers to:

- Which assets violated which controls at time $t$?
- Which control assertions currently lack fresh evidence?
- Which relationships amplify exposure for a failed control?
- When did drift begin and when was it remediated?

## Subapp Domain Seeds and CRUD Contracts (v1)

Each subapp must ship with deterministic initial domain seeds and explicit CRUD contracts for core entities.

### GRC seeds and CRUD

Initial seed entities:

- Control frameworks (`NIST 800-53`, `ISO 27001`)
- Control catalog entries (framework-specific control IDs)
- Policy baseline profiles (e.g., `default-baseline`)
- Assertion templates mapped to canonical target types

Core CRUD contracts:

- `control_frameworks`: `create`, `read/list`, `update`, `archive`
- `controls`: `create`, `read/list`, `update`, `archive`
- `assertions`: `create`, `read/list`, `update` (new version), `deactivate`
- `evidence_observations`: `create`, `read/list`, `append-evaluation`

### ITAM seeds and CRUD

Initial seed entities:

- Asset category taxonomy (`hardware`, `software`, `virtual`, `service`)
- Asset lifecycle states (`active`, `inactive`, `retired`)
- Criticality and control-impact scales
- License/contract type taxonomy

Core CRUD contracts:

- `assets`: `create`, `read/list`, `update` (versioned), `retire`
- `licenses`: `create`, `read/list`, `update`, `terminate`
- `vendors`: `create`, `read/list`, `update`, `deactivate`
- `asset_assignments`: `create`, `read/list`, `update`, `close`

### CMDB seeds and CRUD

Initial seed entities:

- CI class taxonomy (`application`, `database`, `host`, `network`, `service`)
- Relationship type taxonomy (aligned to canonical relationship contract)
- Environment taxonomy (`dev`, `stage`, `prod`)
- Ownership/stewardship role taxonomy

Core CRUD contracts:

- `configuration_items`: `create`, `read/list`, `update` (versioned), `retire`
- `relationships`: `create`, `read/list`, `update` (versioned), `close`
- `environments`: `create`, `read/list`, `update`, `deprecate`
- `service_maps`: `create`, `read/list`, `update`, `archive`

### Cross-subapp contract invariants

1. All create/update operations are append-oriented where historical reconstruction is required.
2. Soft-delete/retire/deactivate semantics are preferred over hard deletes.
3. Every mutable entity includes `valid_from`/`valid_to` or equivalent temporal lifecycle fields.
4. All CRUD endpoints must return canonical IDs and version metadata.
5. Seed datasets are idempotent and safe to re-apply in local/dev/provisioning flows.

## Modeling Anti-Patterns to Avoid

- Single polymorphic CI records without typed domain boundaries
- Relationship semantics encoded only in free-text fields
- Replacing historical records in-place
- Control status without evidence linkage

## Related Internal Docs

- [System Definition](system-definition.md)
- [Architecture](architecture.md)
- [Standards Baseline](standards-baseline.md)
- [References](references.md)

## Next steps

- Align API contract scope and client integration: [API Reference Strategy](api-reference-strategy.md)
- Continue implementation-level contribution workflow: [Developer Guide](developer/README.md)
