# Identity Management Domain Models

IDM models unify human and machine identity data into lifecycle-managed, policy-governed access primitives.

This model treats `person` and `identity` as distinct:

- `person` is the durable root anchor.
- `identity` is a versioned detail record over time.
- `person.current_identity_id` points to the currently effective identity record.

## People

`person` is the root entity used to correlate all identity iterations for a human.

Required fields:

- `person_id`
- `current_identity_id` (FK -> `identity.identity_id`)
- `person_state` (`prehire`, `active`, `leave`, `terminated`)
- `created_at`, `updated_at`

Rules:

1. `person` does not store mutable profile attributes like name or gender.
2. `current_identity_id` must always reference an `identity` record for the same `person_id`.
3. Identity history is append-only; new profile truth creates a new `identity` row.

## Identities

`identity` represents a point-in-time iteration of person profile details.

Required fields:

- `identity_id`
- `person_id` (FK -> `person.person_id`)
- `identity_version` (monotonic per person)
- `legal_name`
- `preferred_name` (optional)
- `gender` (optional, policy-governed)
- `date_of_birth` (optional, policy-governed)
- `assurance_level`
- `state` (`draft`, `active`, `superseded`, `retired`)
- `valid_from`, `valid_to`
- `created_at`, `updated_at`

Key relationships:

- `person` `has_many` `identity`
- `person.current_identity_id` `references` the active `identity`
- `identity` `binds_to` one or more `account`

Versioning expectations:

1. A name/gender/profile update creates a new `identity` row instead of mutating prior rows.
2. Prior `identity` rows are retained for historical traceability.
3. Exactly one current identity exists per person where `valid_to` is `null`, and it should match `person.current_identity_id`.

## Contacts

`contact_point` tracks verifiable communication attributes used in identity proofing and notifications.

Required fields:

- `contact_id`
- `identity_id`
- `contact_type` (`email`, `phone`, `pager`, `other`)
- `value_ref`
- `verified_at`
- `is_primary`

Rules:

1. At most one primary email per identity.
2. Verification state is explicit and time-stamped.
3. Contact history remains auditable after updates.

## Users

`user_account` is a system-specific credentialed account linked to a person.

Required fields:

- `account_id`
- `person_id` (FK -> `person.person_id`)
- `identity_id` (FK -> `identity.identity_id`, optional but recommended for current profile resolution)
- `system_id`
- `username`
- `credential_policy_id`
- `state` (`provisioning`, `active`, `locked`, `disabled`, `deprovisioned`)
- `last_auth_at`

Rules:

1. `user_account.person_id` is required and is the canonical ownership FK.
2. If `identity_id` is present, it must belong to the same `person_id`.
3. New identity iterations do not require new user accounts; repoint to the new identity as needed.

Supporting entities:

- `role_assignment` (`assignment_id`, `account_id`, `role_id`, `scope`, `valid_from`, `valid_to`)
- `entitlement_grant` (`grant_id`, `account_id`, `resource_id`, `access_level`, `justification`, `expires_at`)
- `access_request` (`request_id`, `identity_id`, `requested_access`, `approver_id`, `status`)

## Lifecycle Flows

- Joiner: create `person` -> create initial `identity` -> set `person.current_identity_id` -> provision `user_account` and access.
- Change event (name/gender/profile): append new `identity` -> close prior identity (`valid_to`) -> repoint `person.current_identity_id`.
- Mover: entitlement and role recalculation with approval trail.
- Leaver: account disable, entitlement revoke, session revoke, evidence capture.

## Standards Alignment

| Standard | Mapping |
| --- | --- |
| ITIL v4 | Workforce and access lifecycle via Service Request Management and Information Security Management |
| CIS Controls v8 | Control 5 (Account Management), Control 6 (Access Control Management) |
| NIST CSF 2.0 | `PR.AA` identity, credential, and access governance |
| NIST SP 800-63 | Identity assurance, authenticator lifecycle, federation principles |
| NIST SP 800-53 | `AC`, `IA`, `PS` control families |
| ISO/IEC 27001:2022 | Identity and access control clauses and operational controls |

## Cross-Slice Dependencies

- Auth uses IDM identities and account state for authentication decisions.
- Platform users map to IDM persons through `platform_user_person_map` (defined in Platform slice).
- GRC controls evaluate identity hygiene, orphaned accounts, and privilege drift.
