# Group Models

Source: `backend/itsor/domain/models/group_models.py`

---

## Purpose

Defines security or organizational groups and how users/groups become members.

## Models

- **Group**
  - May be tenant-scoped (`tenant_id`) or broader depending on use case
  - Optional owner (`owner_id`) and parent group (`group_id`) references
  - Optional legacy/integer permissions value (`permissions`)
- **GroupMembership**
  - Membership edge with polymorphic member target
  - `member_type` determines whether membership is by user or nested group
- **GroupRole**
  - Alias of `RoleAssignment` from `role_models.py`

## Invariants

- For `member_type = "user"`: `member_user_id` must be set and `member_group_id` must be `None`.
- For `member_type = "group"`: `member_group_id` must be set and `member_user_id` must be `None`.

## PlantUML

```plantuml
@startuml
hide empty members

class Group {
  +id: GroupId
  +tenant_id: TenantId?
  +name: str
  +owner_id: UserId?
  +group_id: GroupId?
  +permissions: int?
}

class GroupMembership {
  +id: GroupMembershipId
  +group_id: GroupId
  +member_type: "user"|"group"
  +member_user_id: UserId?
  +member_group_id: GroupId?
}

class GroupRole <<alias>> {
  = RoleAssignment
}

GroupMembership --> Group : group_id
GroupMembership --> UserId : member_user_id (when type=user)
GroupMembership --> GroupId : member_group_id (when type=group)
Group --> TenantId : tenant_id
Group --> UserId : owner_id
Group --> GroupId : parent group_id
GroupRole --> RoleAssignment : alias

@enduml
```
