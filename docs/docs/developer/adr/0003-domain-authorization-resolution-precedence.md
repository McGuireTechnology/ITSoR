# ADR-0003: Domain Authorization Resolution Precedence and Tie-Break Rules

- **Status:** Accepted
- **Date:** 2026-03-10
- **Owners:** Backend, Security
- **Applies to:** `itsor.domain.policy.authorization_resolution`

## Context

Authorization behavior in the domain layer already has strong regression tests, but the precedence model and tie-break semantics were documented across code and tests rather than as a single explicit architecture decision.

This made it harder to reason about expected outcomes for policy conflicts across resource, owner/group, and row scopes.

## Decision

Adopt one canonical decision model for authorization resolution:

1. Superuser short-circuit
2. Tenant boundary gate
3. `RESOURCE` policy evaluation
4. `OWNER`/`GROUP` coarse evaluation
5. `ROW` evaluation

### Principal precedence

When ranking matching policies in a scope, principal types are ordered (highest precedence first):

1. `user`
2. `group`
3. `role`
4. `tenant`
5. `authenticated`
6. `public`

### Scope precedence and tie-breaks

- `RESOURCE` stage must resolve before owner/group stage.
- `OWNER` and `GROUP` coarse policies share scope rank and are compared by principal precedence and specificity.
- Row policies are ranked by principal precedence, then specificity (`resource_id`/predicates before unconstrained).
- At any winning tie rank where effects conflict, **deny wins**.
- A row-level result of `none` is final deny, even if coarse stages allowed.

## Consequences

### Positive

- One authoritative precedence source for code review, onboarding, and incident analysis.
- Better alignment between resolver implementation, regression tests, and docs.
- Lower risk of semantic drift during policy refactors.

### Trade-offs

- Any future precedence change now requires ADR and policy-doc updates in addition to code/tests.

## Validation and References

- Implementation: `backend/itsor/domain/policy/authorization_resolution.py`
- Tests: `backend/tests/test_authorization_resolution.py`
- Policy guide: `docs/docs/developer/authorization-resolution-policy.md`
