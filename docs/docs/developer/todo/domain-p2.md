# Domain P2 Implementation Tickets

Quality and ergonomics improvements after P0/P1 stabilization.

Last reviewed: 2026-03-10 (analysis refresh)

## Ticket P2-1: Reduce Alias Surface That Blurs Domain Language

### Status
- Completed (2026-03-10)

### Problem
Broad aliasing (`App = Module`, etc.) can obscure intent and bounded-context language over time.

### Scope
- Inventory aliases in `domain/models` and retain only those justified by ubiquitous language.
- Deprecate ambiguous aliases with migration notes.

### Acceptance Criteria
- Alias set is intentional and documented.
- Public imports remain stable or include deprecation path.

### Test Cases
- **Regression**: Import surface tests (if present) remain green.

### Suggested Files
- `backend/itsor/domain/models/module_models.py`
- `backend/itsor/domain/models/__init__.py`
- docs updates under `docs/docs/developer/`

### Implementation Notes (Completed)
- Canonical module names are now the primary exports: `Module`, `ModuleRole`, `ModuleUser`.
- Ambiguous aliases `App`, `AppRole`, and `AppUser` are deprecated with runtime `DeprecationWarning` and retained compatibility access.
- `from itsor.domain.models import App` continues to work during migration via package-level deprecation shims.
- Migration guidance is documented in `developer/domain-model-reference.md` under **Domain Model Alias Policy**.

---

## Ticket P2-2: Replace Lambda Default Factories with Built-ins

### Status
- Completed (2026-03-10)

### Problem
Many dataclasses use `field(default_factory=lambda: [])`/`lambda: {}` where `list`/`dict` are clearer.

### Scope
- Replace trivial lambda factories with built-ins.
- Keep semantic behavior unchanged.

### Acceptance Criteria
- No functional change in object defaults.
- Improved readability and consistency across models.

### Test Cases
- **Regression**: Dataclass default mutability tests (if added) verify unique containers per instance.

### Suggested Files
- `backend/itsor/domain/models/*.py` (targeted updates)

### Implementation Notes (Completed)
- Replaced trivial `field(default_factory=lambda: [])` and `field(default_factory=lambda: {})` with `field(default_factory=list)` and `field(default_factory=dict)` in targeted domain model dataclasses.
- Kept non-trivial lambda factories (for example time-based defaults) unchanged to preserve behavior.
- Added regression coverage to confirm mutable defaults remain unique per dataclass instance.

---

## Ticket P2-3: Shared ULID Helper for Domain Entity IDs

### Status
- Completed (2026-03-10)

### Problem
Repeated inline ULID default factories add duplication and make future ID strategy changes harder.

### Scope
- Introduce a small internal helper for generating typed ULID-backed IDs.
- Use it where it improves readability without hiding type intent.

### Acceptance Criteria
- Helper is minimal and domain-local.
- Existing entity ID behavior remains unchanged.

### Test Cases
- **Regression**: Entity instantiation tests confirm IDs are auto-generated and type-compatible.

### Suggested Files
- `backend/itsor/domain/` (new helper module)
- targeted model/ids files

### Implementation Notes (Completed)
- Added a domain-local internal helper module at `backend/itsor/domain/_ulid.py`.
- Introduced `typed_ulid_factory(...)` for typed ULID-backed IDs and `new_ulid_str()` for plain string ULIDs.
- Refactored domain model default ID factories to use the helper, reducing repeated inline ULID generation while preserving type intent and behavior.
- Added regression coverage to confirm entity IDs are auto-generated and string-compatible at runtime.

---

## Ticket P2-4: Domain Invariant Test Module for Core Entities

### Status
- Completed (2026-03-10)

### Problem
Invariant tests are concentrated in authorization behavior; model-level invariant coverage is limited.

### Scope
- Add focused tests for entity validation and normalization rules.
- Cover at least `User`, `Tenant`, `Role`, `Module`, `NavigationView`, and key resource models.

### Acceptance Criteria
- Dedicated model invariants test module exists.
- New validation behavior is covered with positive and negative tests.

### Test Cases
- **New**: Empty-field validation and normalization checks per entity.
- **New**: Range/non-negative checks for `order`/`position` fields.

### Suggested Files
- `backend/tests/` (new `test_domain_model_invariants.py`)

### Implementation Notes (Completed)
- Added a dedicated model invariants test module at `backend/tests/test_domain_model_invariants.py`.
- Added positive and negative validation coverage for `User`, `Tenant`, `Role`, `Module`, and `NavigationView` required-field invariants and normalization behavior.
- Added focused invariant coverage for key resource models including `Table`, `ResourceAttribute`, `ResourceSlice`, `ResourceAction`, `ResourceAutomationBot`, `ResourceAutomationProcess`, `ResourceSecurityRule`, and `ModuleResource`.
- Added explicit range checks covering non-negative constraints for `order`/`position` fields on `Module`, `ModuleResource`, `NavigationItem`, `NavigationView`, and `AppView`.
