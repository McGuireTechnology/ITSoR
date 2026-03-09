# Authorization Resolution Policy

This page defines the domain-level authorization resolution order implemented in the backend policy module.

## Canonical Evaluation Order

Authorization is resolved in this exact sequence:

1. **Tenant AuthZ - Superuser role check first**
2. **Tenant AuthZ - UserTenant to Resource tenant boundary check**
3. **ResourceType AuthZ within tenant**
4. **Owner AuthZ or Group AuthZ within tenant**
5. **Row-level AuthZ within tenant (filter/deny)**

If any stage denies access, evaluation stops and access is denied.

---

## Stage 1: Superuser role short-circuit

If the subject has a role ID in `superuser_role_ids`, authorization immediately allows access.

- Default superuser role set: `{"superuser"}`
- This bypasses tenant, resource, owner/group, and row-level checks.

---

## Stage 2: Tenant boundary gate

If `resource_tenant_id` is provided, the subject must be tenant-associated.

Tenant association is evaluated as:

- If `AuthorizationSubject.tenant_ids` is non-empty, `resource_tenant_id` must be in `tenant_ids`.
- Otherwise, `AuthorizationSubject.tenant_id` must equal `resource_tenant_id`.

If tenant association fails, access is denied before any resource/owner/group checks.

---

## Stage 3: ResourceType authorization within tenant

Only `AclScope.RESOURCE` policies for the requested `(resource, action)` are evaluated.

- Principal matching is applied (`user`, `group`, `role`, `tenant`, `authenticated`, `public`).
- If no matching resource-type policy exists, access is denied.
- If matching policies conflict at the same rank, **deny wins**.

This stage is intentionally evaluated before owner/group authorization.

---

## Stage 4: Owner or Group authorization within tenant

Only `AclScope.OWNER` and `AclScope.GROUP` policies are evaluated.

- If there is no matching owner/group policy, the result from resource-type authorization remains in effect.
- If there is a conflict among matching owner/group policies at the same rank, **deny wins**.
- A matching owner/group deny will deny access.

---

## Stage 5: Row-level authorization within tenant

`AclScope.ROW` policies are evaluated after coarse authorization succeeds.

Row result is one of:

- `all`: full row access
- `filtered`: access with row constraints
- `none`: no row access

If row-level result is `none`, overall authorization is denied.

---

## Domain API Contract

Primary entry point:

- `resolve_authorization(...)`

Important inputs:

- `subject`: `AuthorizationSubject`
- `subject.effective_user_ids`: delegated/extended user identities considered for owner and user-principal checks
- `subject.effective_group_ids`: inherited/extended groups considered for group-principal and group ownership checks
- `resource_tenant_id`: tenant ID for the target resource (optional but recommended)
- `superuser_role_ids`: role IDs that should bypass all checks
- `resource`, `action`, `policies`, `resource_id`, `row_values`

Decision output:

- `AuthorizationDecision.is_allowed`
- `AuthorizationDecision.coarse_effect`
- `AuthorizationDecision.winning_scope`
- `AuthorizationDecision.winning_principal`
- `AuthorizationDecision.row_access`

### Application-layer subject construction

Use `AuthorizationSubjectBuilder` to consistently populate subject identities from repositories:

- `UserTenant` links -> `tenant_ids`
- user memberships + nested group memberships -> `group_ids` and `effective_group_ids`
- user role assignments + group role assignments -> `role_ids`
- delegate/acts-for identities -> `effective_user_ids`

Location:

- `itsor.application.use_cases.auth.authorization_subject_builder.AuthorizationSubjectBuilder`

---

## Notes for Implementers

- Treat tenant authorization as a hard security boundary.
- Provide `resource_tenant_id` whenever available to enforce tenant isolation.
- Prefer populating `tenant_ids` from `UserTenant` associations for multi-tenant users.
- Prefer populating `effective_group_ids` with expanded nested memberships from the identity graph.
- Use `effective_user_ids` for delegate/acts-for identity patterns where owner checks should honor alternate effective identities.
- Keep superuser role IDs explicit and controlled by configuration.
