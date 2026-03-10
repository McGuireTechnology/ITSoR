# Platform Domain Models

Platform models define the operational structure that lets ITSoR host multiple organizations, users, and working contexts.

## Users

`user` is the platform-resident representation of an authenticated person.

Required fields:

- `id`
- `username`
- `email`
- `group_id`
- `state` (`active`, `disabled`)
- `created_at`, `updated_at`

Primary relationships:

- `user` belongs to one primary `group`
- `user` may own one or more `tenant` records

## Person Mapping

`platform_user_person_map` links platform users to IDM persons for client portal and cross-domain identity resolution.

Required fields:

- `mapping_id`
- `platform_user_id` (FK -> `platform.user.id`)
- `person_id` (external ref -> `idm.person.person_id`)
- `mapping_type` (`primary`, `delegate`, `support`, `historical`)
- `valid_from`, `valid_to`
- `created_at`, `updated_at`

Rules:

1. No direct FK is required from `platform.user` to IDM tables.
2. Person linkage is performed through `platform_user_person_map`.
3. A platform user may map to multiple persons over time, but only one active `primary` mapping is allowed at once.
4. A person may map to multiple platform users where business policy allows.

Portal display guidance:

- `platform.user` remains minimal (`username`, `email`) for operational identity.
- Human-readable person naming in portal views should resolve via `platform_user_person_map` -> `idm.person` -> `idm.person.current_identity_id` -> `idm.identity` name fields.
- This avoids denormalizing mutable person profile attributes into platform tables.

## Tenants

`tenant` is the primary isolation boundary for data, policy, and operational ownership.

Required fields:

- `id`
- `name`
- `owner_id`
- `group_id`
- `permissions`
- `state` (`active`, `suspended`, `retired`)
- `created_at`, `updated_at`

Primary relationships:

- `tenant` is owned by a `user`
- `tenant` is associated to a controlling `group`
- `tenant` scopes workspaces, namespaces, entity types, and entity records

## Groups

`group` is the coarse-grained collaboration and policy boundary for users and tenants.

Required fields:

- `id`
- `name`
- `state`
- `created_at`, `updated_at`

Primary relationships:

- `group` contains `user` members
- `group` governs one or more `tenant` records

## Platform Invariants

1. Every `tenant.owner_id` resolves to an active `user`.
2. Every `user.group_id` resolves to an existing `group`.
3. Cross-slice person resolution must use `platform_user_person_map`.
4. If a person display name is needed, resolve it from IDM through the active mapping and current identity.
5. Tenant-scoped data never crosses tenant boundaries without explicit policy and audit.
6. Deactivation is non-destructive: records become inactive, history remains queryable.

## Operational Alignment

- Supports ITIL v4 service configuration and access service operations.
- Provides the structural context required by GRC assertions and IDM identities.

