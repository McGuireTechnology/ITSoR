# Domain P0 Implementation Tickets

Critical correctness/security work for the domain layer.

Last reviewed: 2026-03-10 (analysis refresh)

## Ticket P0-1: Tenant Principal Matching Supports Multi-Tenant Subjects

Status: ✅ Completed (2026-03-10)

### Problem
Tenant principal matching currently checks only `subject.tenant_id`, which can deny valid access for users with additional memberships in `subject.tenant_ids`.

### Scope
- Update tenant principal resolution logic in `domain/policy/authorization_resolution.py`.
- Ensure tenant principal checks evaluate both primary and effective tenant memberships.
- Preserve existing precedence behavior.

### Acceptance Criteria
- Tenant principal policy matches when `principal_id` exists in `subject.tenant_ids`.
- Tenant principal policy still matches when `principal_id == subject.tenant_id`.
- No regression for non-tenant principal types.
- Existing authorization tests remain green.

### Test Cases
- **New**: Tenant principal allow where `subject.tenant_id != principal_id` but `principal_id in subject.tenant_ids` -> allowed.
- **New**: Tenant principal deny where `principal_id` is in neither `tenant_id` nor `tenant_ids` -> denied.
- **Regression**: User/group/role/public/authenticated principal matching unchanged.

### Suggested Files
- `backend/itsor/domain/policy/authorization_resolution.py`
- `backend/tests/test_authorization_resolution.py`

### Implementation Notes
- Tenant principal matching now evaluates both `subject.tenant_id` and `subject.tenant_ids`.
- Existing principal precedence and non-tenant principal behavior remain unchanged.

### Verification
- Added tests in `backend/tests/test_authorization_resolution.py`:
	- `test_tenant_principal_matches_effective_tenant_membership`
	- `test_tenant_principal_denies_when_not_in_primary_or_effective_memberships`
- Focused suite passes: `pytest tests/test_authorization_resolution.py -q`.
- Full backend tests pass: `pytest tests -q`.

---

## Ticket P0-2: Row Access Mode for Unconstrained Allow Policies

Status: ✅ Completed (2026-03-10)

### Problem
Row resolution can return `FILTERED` even when allow row policies are unconstrained (no predicates and no `resource_id`), which effectively acts like full access.

### Scope
- Adjust row resolution semantics for collection-level decisions.
- Return `ALL` when winning allow set does not constrain rows.
- Keep deny precedence unchanged.

### Acceptance Criteria
- Unconstrained allow row policy yields `RowAccessMode.ALL`.
- Constrained allow row policy yields `RowAccessMode.FILTERED` with predicates/resource IDs populated.
- Deny tie behavior remains deny-first.

### Test Cases
- **New**: Unconstrained row allow returns `ALL`.
- **New**: Predicate/resource constrained row allow returns `FILTERED`.
- **Regression**: Row-level deny after coarse allow still returns `NONE`.

### Suggested Files
- `backend/itsor/domain/policy/authorization_resolution.py`
- `backend/tests/test_authorization_resolution.py`

### Implementation Notes
- Collection-level row resolution now returns `RowAccessMode.ALL` when the winning allow set has no `resource_id` and no predicates.
- Constrained winning allow sets continue to return `RowAccessMode.FILTERED` and include aggregated `resource_ids` and predicates.
- Deny-first behavior at winning tie rank remains unchanged.

### Verification
- Added/updated tests in `backend/tests/test_authorization_resolution.py`:
	- `test_unconstrained_row_allow_returns_all_for_collection`
	- `test_constrained_row_allow_returns_filtered_with_constraints`
	- `test_row_deny_after_coarse_allow_returns_none_for_collection`
- `pytest tests/test_authorization_resolution.py -q` passes.

---

## Ticket P0-3: Lock Resolver Semantics with Pre-Refactor Regression Coverage

Status: ✅ Completed (2026-03-10)

### Problem
Resolver behavior is sensitive to precedence and scope interaction; changes need guardrails before deeper refactor.

### Scope
- Add/expand focused authorization tests before refactoring.
- Cover tenant boundaries, precedence tie-breaks, owner/group coarse checks, and row interactions.

### Acceptance Criteria
- Test suite explicitly covers all policy scopes (`RESOURCE`, `OWNER`, `GROUP`, `ROW`).
- Tests document deny-wins behavior in same-rank conflicts.
- Future resolver changes fail fast when semantics drift.

### Test Cases
- **New**: Owner vs resource precedence validation.
- **New**: Group policy with allowed group set intersection behavior.
- **New**: Row predicate evaluation for scalar and list values.

### Suggested Files
- `backend/tests/test_authorization_resolution.py`

### Implementation Notes
- Added focused regression tests that lock coarse/resource precedence and deny-wins tie-break behavior.
- Added owner-vs-resource precedence coverage where coarse owner deny overrides resource allow when matched.
- Added group `allowed_group_ids` intersection coverage to ensure only intersecting sets participate in coarse decisions.
- Added row predicate matching coverage for both scalar equality and list-membership predicate values.

### Verification
- Added/updated tests in `backend/tests/test_authorization_resolution.py`:
	- `test_resource_scope_same_rank_conflict_prefers_deny`
	- `test_owner_deny_overrides_resource_allow_when_owner_matches`
	- `test_group_allowed_group_ids_requires_intersection`
	- `test_row_predicate_matches_scalar_value`
	- `test_row_predicate_matches_list_value`
- Focused suite passes: `pytest tests/test_authorization_resolution.py -q` (18 passed).
