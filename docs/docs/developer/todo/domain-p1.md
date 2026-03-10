# Domain P1 Implementation Tickets

High-value consistency and maintainability improvements.

## Ticket P1-1: Separate `AppId` and `ModuleId` Value Types

### Problem
`AppId` currently aliases `ModuleId`, which weakens bounded-context semantics and allows accidental cross-usage.

### Scope
- Define explicit `NewType` for `AppId` distinct from `ModuleId`.
- Update domain models and imports incrementally.
- Add temporary compatibility aliases only if migration requires it.

### Acceptance Criteria
- `AppId` and `ModuleId` are separate types in `domain/ids`.
- Domain models referencing app concepts use `AppId` explicitly.
- No broken imports in domain/application/infrastructure layers.

### Test Cases
- **New**: Type-focused usage tests for models that require `AppId`.
- **Regression**: Existing tests compiling/importing domain IDs stay green.

### Suggested Files
- `backend/itsor/domain/ids/module_ids.py`
- `backend/itsor/domain/ids/app_ids.py`
- `backend/itsor/domain/ids/__init__.py`
- impacted model files under `backend/itsor/domain/models/`

### Status
- Completed (2026-03-10)

### Implementation Notes (Completed)
- Split `AppId` from `ModuleId` by defining `AppId = NewType("AppId", str)` in `backend/itsor/domain/ids/app_ids.py`.
- Removed `AppId` aliasing from `backend/itsor/domain/ids/module_ids.py` to preserve bounded-context semantics.
- Updated `backend/itsor/domain/ids/__init__.py` exports so `AppId` is sourced from `app_ids` and `ModuleId` remains in `module_ids`.
- Added type-focused tests in `backend/tests/test_domain_app_id_types.py` to verify distinct ID types and `AppId` annotations on app-scoped domain models.

---

## Ticket P1-2: Add Consistent Validation in `User`, `Tenant`, and `Role`

### Problem
Validation rigor differs across domain entities; core identity entities have minimal invariant enforcement.

### Scope
- Add `__post_init__` normalization and required-field checks.
- Enforce non-empty key fields (trimmed) and sensible defaults.
- Keep behavior backward-compatible where possible.

### Acceptance Criteria
- Empty/whitespace-only required strings are rejected.
- Inputs are normalized (e.g., trim `name`, `username`, `email`).
- Existing valid fixtures continue to work.

### Test Cases
- **New**: Reject empty `User.name`, `User.username`, `User.email`.
- **New**: Reject empty `Role.name`, `Tenant.name`.
- **New**: Normalization tests ensure trimmed values are stored.

### Suggested Files
- `backend/itsor/domain/models/user_models.py`
- `backend/itsor/domain/models/tenant_models.py`
- `backend/itsor/domain/models/role_models.py`
- new/updated tests in `backend/tests/`

### Status
- Completed (2026-03-10)

### Implementation Notes (Completed)
- Added `__post_init__` normalization + required-field validation for:
	- `User.name`, `User.username`, `User.email`
	- `Tenant.name`
	- `Role.name`
- Added a backward-compatible default for `Role.description` and normalized it when provided.
- Added new validation and normalization tests in `backend/tests/test_domain_identity_validation.py`.
- Verified backend regressions by running `pytest backend/tests` (31 passed).

---

## Ticket P1-3: Typed ID Consistency for Navigation and Related Models

### Status
- Completed (2026-03-10)

### Problem
Some models (e.g., `NavigationItem`) use raw string IDs while most domain models use typed IDs.

### Scope
- Introduce a typed navigation item ID.
- Update model fields and exports.
- Ensure serialization/deserialization boundaries remain stable.

### Acceptance Criteria
- `NavigationItem.id` uses a typed ID object.
- No runtime regressions in consumers that rely on string conversion.

### Test Cases
- **New**: Navigation item creation uses typed ID and still serializes as expected.
- **Regression**: Navigation view/model tests (if present) remain green.

### Suggested Files
- `backend/itsor/domain/ids/view_ids.py`
- `backend/itsor/domain/models/view_models.py`
- `backend/itsor/domain/models/__init__.py`

### Implementation Notes (Completed)
- Added `NavigationItemId = NewType("NavigationItemId", str)` in `backend/itsor/domain/ids/view_ids.py` and exported it via `backend/itsor/domain/ids/__init__.py`.
- Updated `NavigationItem.id` in `backend/itsor/domain/models/view_models.py` to use `NavigationItemId` with `typed_ulid_factory(NavigationItemId)`.
- Added regression/type coverage in `backend/tests/test_domain_app_id_types.py` to assert type annotations and runtime string compatibility.

### Verification
- `pytest backend/tests/test_domain_app_id_types.py -q` (3 passed)
- `pytest backend/tests/test_domain_default_factories.py backend/tests/test_domain_model_invariants.py -q` (28 passed)

---

## Ticket P1-4: Align IDM Models with Domain Conventions

### Status
- Open (reviewed 2026-03-10)

### Problem
IDM models are loosely typed and allow weak invariants compared to core domain models.

### Scope
- Introduce typed IDs where feasible.
- Add invariant validation for required fields and constrained values.
- Replace JSON-as-string payloads with structured types and explicit conversion at boundaries.

### Acceptance Criteria
- Key IDM entities validate required fields.
- `demographic_payload` is represented as structured data type.
- Temporal fields support basic consistency validation.

### Test Cases
- **New**: Reject missing required IDs/fields for IDM entities.
- **New**: Reject invalid temporal intervals (`valid_from > valid_to`).
- **New**: Structured payload validation and round-trip behavior.

### Suggested Files
- `backend/itsor/domain/models/idm/idm_models.py`
- new tests in `backend/tests/`

### Analysis Notes (2026-03-10)
- `backend/itsor/domain/models/idm/idm_models.py` still uses raw `str` IDs and permissive defaults for key fields.
- `IdmIdentity.demographic_payload` remains `str = "{}"`; structured payload typing is not yet represented in the domain model.
- Temporal invariant checks (`valid_from <= valid_to`, supersession semantics) are not currently enforced in IDM domain dataclasses.

---

## Ticket P1-5: Domain Authorization Decision Record

### Status
- Completed (2026-03-10)

### Problem
Resolver precedence rules are encoded in code/tests but not documented as an explicit architecture decision.

### Scope
- Add concise decision record documenting precedence, tie-breakers, and row/coarse interactions.
- Link from developer architecture docs.

### Acceptance Criteria
- Decision record exists and is referenced from domain/authorization docs.
- Includes examples for common conflict scenarios.

### Test Cases
- N/A (documentation ticket)

### Suggested Files
- `docs/docs/developer/` (new ADR or policy note)
- `docs/docs/developer/authorization-resolution-policy.md` (or equivalent)

### Implementation Notes (Completed)
- Added `ADR-0003: Domain Authorization Resolution Precedence and Tie-Break Rules` at `docs/docs/developer/adr/0003-domain-authorization-resolution-precedence.md`.
- Expanded `docs/docs/developer/authorization-resolution-policy.md` with explicit principal precedence order, scope/tie-break details, and conflict examples.
- Updated ADR references in `docs/docs/developer/adr/README.md` and `docs/docs/developer/architecture.md`.

### Verification
- Documentation-only change; no runtime code path modified.
