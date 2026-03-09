from dataclasses import dataclass, field

import ulid

from itsor.domain.ids import GroupId, TenantId, UserId, UserTenantId
from itsor.domain.models.resource_models import ResourceAction
from itsor.domain.models.role_models import RoleAssignment


@dataclass
class User:
    id: UserId = field(default_factory=lambda: UserId(str(ulid.new())), init=False)
    name: str
    username: str
    email: str
    password_hash: str
    group_id: GroupId | None = None
    platform_endpoint_permissions: dict[str, list[ResourceAction | str]] = field(
        default_factory=dict
    )


@dataclass
class UserTenant:
    id: UserTenantId = field(default_factory=lambda: UserTenantId(str(ulid.new())), init=False)
    user_id: UserId
    tenant_id: TenantId


UserRole = RoleAssignment


__all__ = ["User", "UserTenant", "UserRole"]
