from dataclasses import dataclass, field
from typing import Literal

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import (
    GroupId,
    PermissionId,
    RoleAssignmentId,
    RoleId,
    RolePermissionId,
    TenantId,
    UserId,
)


def _normalize_required_text(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} is required")
    return normalized


@dataclass
class Role:
    id: RoleId = field(default_factory=typed_ulid_factory(RoleId), init=False)
    name: str
    tenant_id: TenantId | None
    description: str = ""

    def __post_init__(self) -> None:
        self.name = _normalize_required_text(self.name, "name")
        if self.description is None:
            self.description = ""
        elif isinstance(self.description, str):
            self.description = self.description.strip()


@dataclass
class RoleAssignment:
    id: RoleAssignmentId = field(
        default_factory=typed_ulid_factory(RoleAssignmentId),
        init=False,
    )
    role_id: RoleId
    assignee_type: Literal["user", "group"] | None = None
    user_id: UserId | None = None
    group_id: GroupId | None = None

    def __post_init__(self) -> None:
        if self.assignee_type is None:
            if self.user_id is not None and self.group_id is None:
                self.assignee_type = "user"
            elif self.group_id is not None and self.user_id is None:
                self.assignee_type = "group"
            else:
                raise ValueError("role assignment requires exactly one assignee identifier")

        if self.assignee_type == "user":
            if self.user_id is None or self.group_id is not None:
                raise ValueError("user role assignment requires user_id only")
            return

        if self.assignee_type == "group":
            if self.group_id is None or self.user_id is not None:
                raise ValueError("group role assignment requires group_id only")
            return

        raise ValueError("assignee_type must be 'user' or 'group'")


@dataclass
class RolePermission:
    id: RolePermissionId = field(
        default_factory=typed_ulid_factory(RolePermissionId), init=False
    )
    role_id: RoleId
    permission_id: PermissionId


__all__ = ["Role", "RoleAssignment", "RolePermission"]
