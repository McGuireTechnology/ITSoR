# Domain Layer Improvements

This backlog captures recommended improvements for the `backend/itsor/domain` layer and sublayers.

Last reviewed: 2026-03-10 (analysis refresh)

## Implementation Tickets

- [Domain P0 Implementation Tickets](domain-p0.md)
- [Domain P1 Implementation Tickets](domain-p1.md)
- [Domain P2 Implementation Tickets](domain-p2.md)

## Priority Legend

- **P0**: Correctness/Security risk, should be addressed first.
- **P1**: High-value consistency and maintainability improvements.
- **P2**: Quality and ergonomics improvements.

## Policy (`domain/policy`)

### P0

- [x] **Tenant principal matching should support all tenant memberships**
	- Update tenant principal checks to evaluate both `tenant_id` and `tenant_ids`.
	- Current behavior only checks `subject.tenant_id` for tenant principals.
	- Add tests for users with multiple tenant memberships and tenant-scoped policies.
	- Completed in `domain-p0.md` (Ticket P0-1) with resolver and regression tests.

- [x] **Clarify row access mode when allow rules are unconstrained**
	- When row allow policies have no `resource_id` and no predicates, return `ALL` instead of `FILTERED`.
	- Add tests for collection-level access where row policies are broad allows.

### P1

- [ ] **Refine owner policy behavior for collection queries**
	- Revisit owner policy matching when `row_values` is not present.
	- Decide whether owner policy should constrain list access by predicate generation vs hard deny.
	- Add tests for owner-based list/read without row context.

- [x] **Document conflict resolution precedence in one place**
	- Capture principal precedence, scope precedence, and deny-wins tie-break in docs.
	- Include examples for `RESOURCE` vs `OWNER`/`GROUP` and row-deny overrides.
	- Completed with `authorization-resolution-policy.md` precedence/ranking updates and ADR linkage (`adr/0003-domain-authorization-resolution-precedence.md`).

## IDs (`domain/ids`)

### P1

- [x] **Separate `AppId` and `ModuleId` as explicit value types**
	- Replace aliasing (`AppId = ModuleId`) with distinct `NewType` declarations.
	- Keep temporary compatibility aliases only if needed for migration.
	- Update imports/usages incrementally and add regression tests.
	- Completed in `domain-p1.md` (Ticket P1-1).

- [ ] **Normalize ID module boundaries and exports**
	- Ensure `app_ids.py` does not simply mirror module IDs unless intentional.
	- Keep `ids/__init__.py` as the canonical export surface.

### P2

- [x] **Adopt a shared ID generation helper**
	- Consider a small utility for ULID creation to reduce repeated lambdas.
	- Keep domain IDs explicit and strongly typed.
	- Completed in `domain-p2.md` (Ticket P2-3) via `backend/itsor/domain/_ulid.py`.

## Models (`domain/models`)

### P1

- [x] **Add consistent validation for core entities**
	- Add `__post_init__` checks for required fields and normalization in `User`, `Tenant`, and `Role`.
	- Enforce non-empty `name`/`username`/`email` and normalized string inputs.
	- Completed in `domain-p1.md` (Ticket P1-2).

- [ ] **Unify typed IDs across models**
	- Introduce a typed ID for `NavigationItem` instead of raw `str` ID.
	- Review remaining raw string identifiers and convert to typed IDs where appropriate.
	- Analysis update: `NavigationItemId` has been implemented and validated (see `domain-p1.md`, Ticket P1-3); broader raw-ID review remains open.

- [ ] **Tighten permission payload typing**
	- Standardize `platform_endpoint_permissions` value types to avoid mixed enum/string usage.
	- Add a conversion point if external input still sends strings.

### P2

- [x] **Reduce alias surface where it blurs domain concepts**
	- Review aliases like `App = Module` and similar renames for long-term clarity.
	- Keep aliases only where they represent true ubiquitous language.
	- Completed in `domain-p2.md` (Ticket P2-1) with deprecation shims and migration notes.

- [x] **Use plain `list`/`dict` default factories**
	- Replace `field(default_factory=lambda: [])` and `lambda: {}` with `list` and `dict` for readability.
	- Completed in `domain-p2.md` (Ticket P2-2) with mutable-default regression coverage in `backend/tests/test_domain_default_factories.py`.

## IDM Models (`domain/models/idm`)

### P1

- [ ] **Align IDM models with domain conventions**
	- Introduce typed IDs where possible.
	- Add validation for required fields and enum-like constrained strings.

- [ ] **Replace JSON-as-string fields with structured types**
	- Replace `demographic_payload: str = "{}"` with structured dict typing and explicit serialization boundaries.

### P2

- [ ] **Add temporal validity invariants**
	- Validate `valid_from <= valid_to` when both are present.
	- Validate supersession semantics (`superseded_at`) for identity history records.

## Testing & Documentation

### P0

- [x] **Add policy regression tests before refactor**
	- Covers all policy scopes (`RESOURCE`, `OWNER`, `GROUP`, `ROW`) and tenant boundary gating.
	- Adds explicit same-rank deny-wins assertions for coarse/resource conflicts.
	- Adds owner-vs-resource precedence, group `allowed_group_ids` intersection, and row predicate scalar/list regression tests.
	- Completed in `domain-p0.md` (Ticket P0-3) with focused resolver-semantic coverage in `backend/tests/test_authorization_resolution.py`.

### P1

- [x] **Create model invariant test module**
	- Add focused tests for dataclass validation and normalization across domain models.
	- Completed in `domain-p2.md` (Ticket P2-4) at `backend/tests/test_domain_model_invariants.py`.

- [x] **Add a domain decision record for authorization rules**
	- Capture final decisions for precedence and row/coarse interplay.
	- Completed via `docs/docs/developer/adr/0003-domain-authorization-resolution-precedence.md`.
	- Link this record from developer architecture docs.

## Suggested Execution Order

1. **P0 Policy tests + fixes**
2. **P1 IDs/model consistency updates**
3. **P1 IDM alignment + payload typing**
4. **P2 cleanup, alias minimization, and helper extraction**

