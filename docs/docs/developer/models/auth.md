# Auth Domain Models

Auth models support session establishment, token lifecycle, and authorization context for ITSoR APIs and UI.

## Scope

- Authentication events (`signup`, `login`, `logout`, token refresh/revocation)
- Session and token issuance
- Authorization context hydration from Platform and IDM slices
- Audit-ready authentication evidence for GRC use

## Core Entities

| Entity | Purpose | Required Fields |
| --- | --- | --- |
| `auth_principal` | Subject attempting to authenticate | `principal_id`, `principal_type` (`user`, `service`), `identity_id`, `state` |
| `credential_binding` | Reference to credential material (not raw secret) | `credential_id`, `principal_id`, `credential_type`, `hash_ref`, `state`, `valid_from`, `valid_to` |
| `auth_session` | Active authenticated session | `session_id`, `principal_id`, `tenant_id`, `issued_at`, `expires_at`, `revoked_at`, `auth_method` |
| `token_issue` | Access token issuance record | `token_id`, `session_id`, `token_type`, `scope_set`, `issued_at`, `expires_at`, `revoked_at` |
| `auth_event` | Immutable event trail | `event_id`, `event_type`, `principal_id`, `ip_ref`, `user_agent_ref`, `occurred_at`, `result` |
| `auth_factor_event` | MFA/step-up challenge and result | `factor_event_id`, `session_id`, `factor_type`, `challenge_at`, `verified_at`, `result` |

## Relationships

- `auth_principal` `uses` `credential_binding`
- `auth_principal` `establishes` `auth_session`
- `auth_session` `issues` `token_issue`
- `auth_session` `records` `auth_factor_event`
- `auth_event` `references` `auth_principal` and optional `auth_session`

## Lifecycle States

### `auth_principal.state`

- `pending`
- `active`
- `locked`
- `disabled`

### `auth_session`

- `issued`
- `active`
- `expired`
- `revoked`

### `token_issue`

- `valid`
- `expired`
- `revoked`

## API-Relevant Model Contracts

- `POST /signup` creates `auth_principal`, initial `credential_binding`, and initial `auth_session`/`token_issue`.
- `POST /login` creates `auth_session` and `token_issue`.
- `POST /logout` revokes session and active token issuance.
- Protected routes require valid `token_issue` and resolvable principal-to-platform context.

## Cross-Slice Integration

- `identity_id` links to IDM `identity`.
- `tenant_id` and group scope link to Platform `tenant` and `group`.
- `auth_event` and `auth_factor_event` provide evidence inputs to GRC controls.

## Control and Standards Alignment

| Standard | Mapping |
| --- | --- |
| ITIL v4 (Information Security Management, Access Management) | Authentication service reliability, access request fulfillment, and session governance |
| CIS Controls v8 | Control 5 (Account Management), Control 6 (Access Control Management), Control 8 (Audit Log Management) |
| NIST CSF 2.0 | `PR.AA` (Identity Management, Authentication, and Access Control), `DE.CM` (Security Continuous Monitoring) |
| NIST SP 800-63 | Digital identity assurance and authenticator lifecycle guidance |
| ISO/IEC 27001:2022 | Annex A access control and authentication controls |
