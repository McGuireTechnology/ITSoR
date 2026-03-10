# Permission Models

Source: `backend/itsor/domain/models/permission_models.py`

---

## Purpose

Defines fine-grained permission entries and ACL policies for resource, row, owner, and group scopes.

## Core Enums / Types

- **PermissionEffect**: `ALLOW`, `DENY`
- **AclScope**: `RESOURCE`, `ROW`, `OWNER`, `GROUP`
- **AclPrincipalType**: `USER`, `GROUP`, `ROLE`, `TENANT`, `AUTHENTICATED`, `PUBLIC`
- **ResourcePermissionAction** (from resource models): `CREATE`, `READ`, `UPDATE`, `DELETE`, `EXECUTE`
- **Resource** (from resource models): domain resource identifiers such as `platform.user`, `platform.role`, etc.

## Models

- **Permission**
  - Basic permission tuple: `resource + action + effect`
- **AclPrincipal**
  - Identifies who the policy targets
  - Implicit principals (`AUTHENTICATED`, `PUBLIC`) cannot carry IDs
  - Explicit principals require `principal_id`
- **AclRowPredicate**
  - Field/value predicate for row-level filters
- **BaseAclPolicy**
  - Shared policy fields: `name`, `resource`, `action`, `principal`, `effect`
- **ResourceAclPolicy**
  - Resource-level policy scope
- **RowAclPolicy**
  - Row-level scope with `resource_id` and/or `predicates`
- **OwnerAclPolicy**
  - Owner-based scope using `owner_field` and optional `owner_user_id`
- **GroupAclPolicy**
  - Group-based scope using `group_field` and optional `allowed_group_ids`

## Invariants

- ACL policy names must be non-empty.
- Row ACL must provide either `resource_id` or at least one predicate.
- Owner ACL requires non-empty `owner_field`.
- Group ACL requires non-empty `group_field` and either:
  - a group principal, or
  - non-empty `allowed_group_ids`.

## PlantUML

```plantuml
@startuml
hide empty members

enum PermissionEffect {
  ALLOW
  DENY
}

enum AclScope {
  RESOURCE
  ROW
  OWNER
  GROUP
}

enum AclPrincipalType {
  USER
  GROUP
  ROLE
  TENANT
  AUTHENTICATED
  PUBLIC
}

class Permission {
  +id: PermissionId
  +name: str
  +resource: Resource
  +action: ResourcePermissionAction
  +effect: PermissionEffect
}

class AclPrincipal {
  +principal_type: AclPrincipalType
  +principal_id: str?
}

class AclRowPredicate {
  +field: str
  +value: AclValue
}

abstract class BaseAclPolicy {
  +id: PermissionId
  +name: str
  +resource: Resource
  +action: ResourcePermissionAction
  +principal: AclPrincipal
  +effect: PermissionEffect
}

class ResourceAclPolicy {
  +scope: AclScope = RESOURCE
}

class RowAclPolicy {
  +scope: AclScope = ROW
  +resource_id: str?
  +predicates: List<AclRowPredicate>
}

class OwnerAclPolicy {
  +scope: AclScope = OWNER
  +owner_field: str = "owner_id"
  +owner_user_id: UserId?
}

class GroupAclPolicy {
  +scope: AclScope = GROUP
  +group_field: str = "group_id"
  +allowed_group_ids: List<GroupId>
}

BaseAclPolicy <|-- ResourceAclPolicy
BaseAclPolicy <|-- RowAclPolicy
BaseAclPolicy <|-- OwnerAclPolicy
BaseAclPolicy <|-- GroupAclPolicy

BaseAclPolicy --> AclPrincipal : principal
RowAclPolicy --> AclRowPredicate : predicates
Permission --> PermissionEffect
Permission --> Resource
Permission --> ResourcePermissionAction

@enduml
```
