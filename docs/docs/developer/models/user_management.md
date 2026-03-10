# User Management Models

This page is now an overview hub. Module details are maintained in separate files.

---

## Module Documents

- [User Models](./user_models.md)
- [Group Models](./group_models.md)
- [Tenant Models](./tenant_models.md)
- [Role Models](./role_models.md)
- [Permission Models](./permission_models.md)

---

## Cross-Module Relationship Summary

```plantuml
@startuml
hide empty members

class User
class Group
class Tenant
class Role
class Permission
class UserTenant
class GroupMembership
class RoleAssignment
class RolePermission

UserTenant --> User
UserTenant --> Tenant

Group --> Tenant : tenant_id
GroupMembership --> Group : group_id
GroupMembership --> User : member_user_id (type=user)
GroupMembership --> Group : member_group_id (type=group)

RoleAssignment --> Role
RoleAssignment --> User : user assignee
RoleAssignment --> Group : group assignee

RolePermission --> Role
RolePermission --> Permission

@enduml
```

---

## Notes for Implementers

- Backend model invariants are authoritative; frontend validation should be additive only.
- Keep `RoleAssignment` and `GroupMembership` APIs strict to prevent ambiguous assignees/members.
- Prefer transport DTOs that preserve relationship meaning without leaking internal implementation details.
