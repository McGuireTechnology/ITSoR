from dataclasses import dataclass, field

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import GroupId, TenantId, UserId, UserTenantId
from itsor.domain.models.resource_models import ResourcePermissionAction
from itsor.domain.models.role_models import RoleAssignment


def _normalize_required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} is required")
    return normalized


@dataclass
class User:
    id: UserId = field(default_factory=typed_ulid_factory(UserId), init=False)
    name: str
    username: str
    email: str
    password_hash: str
    group_id: GroupId | None = None
    platform_endpoint_permissions: dict[str, list[ResourcePermissionAction | str]] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:
        self.name = _normalize_required_text(self.name, "name")
        self.username = _normalize_required_text(self.username, "username")
        self.email = _normalize_required_text(self.email, "email")


@dataclass
class UserTenant:
    id: UserTenantId = field(default_factory=typed_ulid_factory(UserTenantId), init=False)
    user_id: UserId
    tenant_id: TenantId


UserRole = RoleAssignment


__all__ = ["User", "UserTenant", "UserRole"]
