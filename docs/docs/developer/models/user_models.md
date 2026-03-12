# User Models

Source: `backend/itsor/domain/models/user_models.py`

---

## Purpose

Represents platform users and their tenant membership relationship.

## Models

- **User**
  - Core identity fields: `name`, `username`, `email`, `password_hash`
  - Optional group association: `group_id`
- **UserTenant**
  - Join model linking `user_id` to `tenant_id`
- **UserRole**
  - Alias of `RoleAssignment` from `role_models.py`
  - For user assignments, `assignee_type = "user"` and `user_id` points to `User.id`

## Invariants

- `User.name`, `User.username`, and `User.email` must be non-empty trimmed strings.
- `User.id` and `UserTenant.id` are generated ULID-backed typed identifiers.
- For `UserRole`, user assignments must set `user_id` and leave `group_id` unset.

## PlantUML

```plantuml
@startuml
hide empty members

class User {
  +id: UserId
  +name: str
  +username: str
  +email: str
  +password_hash: str
  +group_id: GroupId?
}

class UserTenant {
  +id: UserTenantId
  +user_id: UserId
  +tenant_id: TenantId
}

class UserRole <<alias>> {
  = RoleAssignment
}

UserTenant --> User : user_id
UserTenant --> TenantId : tenant_id
User --> GroupId : group_id
UserRole --> User : user_id (when assignee_type=user)
UserRole --> RoleAssignment : alias

@enduml
```
