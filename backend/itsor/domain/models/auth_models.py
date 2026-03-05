from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

import ulid

from itsor.domain.ids import (
    GroupId,
    GroupMembershipId,
    PermissionId,
    RoleAssignmentId,
    RoleId,
    RolePermissionId,
    TenantId,
    UserId,
    UserTenantId,
)
from itsor.domain.models.base_model import DEFAULT_PERMISSIONS


class ResourceAction(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"

    @classmethod
    def from_verb(cls, verb: str) -> ResourceAction:
        normalized = verb.strip().lower()
        if normalized in {"write", "modify"}:
            normalized = cls.UPDATE.value
        try:
            return cls(normalized)
        except ValueError as exc:
            raise ValueError(f"Unsupported action verb '{verb}'") from exc

    @classmethod
    def from_nibble(cls, value: int) -> ResourceAction:
        nibble_map = {
            0x1: cls.CREATE,
            0x2: cls.READ,
            0x4: cls.UPDATE,
            0x8: cls.DELETE,
            0x10: cls.EXECUTE,
        }
        try:
            return nibble_map[value]
        except KeyError as exc:
            raise ValueError(f"Unsupported action nibble '{value}'") from exc

    def to_nibble(self) -> int:
        nibble_map = {
            ResourceAction.CREATE: 0x1,
            ResourceAction.READ: 0x2,
            ResourceAction.UPDATE: 0x4,
            ResourceAction.DELETE: 0x8,
            ResourceAction.EXECUTE: 0x10,
        }
        return nibble_map[self]


class Resource(str, Enum):
    USER = "platform.user"
    TENANT = "platform.tenant"
    GROUP = "platform.group"
    ROLE = "platform.role"
    PERMISSION = "platform.permission"
    USER_TENANT = "platform.user_tenant"
    GROUP_MEMBERSHIP = "platform.group_membership"
    USER_ROLE = "platform.user_role"
    GROUP_ROLE = "platform.group_role"
    ROLE_PERMISSION = "platform.role_permission"


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
class Tenant:
    id: TenantId = field(default_factory=lambda: TenantId(str(ulid.new())), init=False)
    name: str
    owner_id: UserId | None = None
    group_id: GroupId | None = None
    permissions: int | None = DEFAULT_PERMISSIONS


@dataclass
class Group:
    id: GroupId = field(default_factory=lambda: GroupId(str(ulid.new())), init=False)
    tenant_id: TenantId | None
    name: str
    owner_id: UserId | None = None
    group_id: GroupId | None = None
    permissions: int | None = DEFAULT_PERMISSIONS
    platform_endpoint_permissions: dict[str, list[ResourceAction | str]] = field(
        default_factory=dict
    )


@dataclass
class Role:
    id: RoleId = field(default_factory=lambda: RoleId(str(ulid.new())), init=False)
    name: str
    tenant_id: TenantId | None
    description: str


@dataclass
class Permission:
    id: PermissionId = field(default_factory=lambda: PermissionId(str(ulid.new())), init=False)
    name: str
    resource: Resource
    action: ResourceAction


@dataclass
class UserTenant:
    id: UserTenantId = field(default_factory=lambda: UserTenantId(str(ulid.new())), init=False)
    user_id: UserId
    tenant_id: TenantId


@dataclass
class GroupMembership:
    id: GroupMembershipId = field(
        default_factory=lambda: GroupMembershipId(str(ulid.new())), init=False
    )
    group_id: GroupId
    member_type: Literal["user", "group"]
    member_user_id: UserId | None = None
    member_group_id: GroupId | None = None

    def __post_init__(self) -> None:
        if self.member_type == "user":
            if self.member_user_id is None or self.member_group_id is not None:
                raise ValueError("user membership requires member_user_id only")
            return

        if self.member_type == "group":
            if self.member_group_id is None or self.member_user_id is not None:
                raise ValueError("group membership requires member_group_id only")
            return

        raise ValueError("member_type must be 'user' or 'group'")


@dataclass
class RoleAssignment:
    id: RoleAssignmentId = field(
        default_factory=lambda: RoleAssignmentId(str(ulid.new())),
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


UserRole = RoleAssignment
GroupRole = RoleAssignment


@dataclass
class RolePermission:
    id: RolePermissionId = field(
        default_factory=lambda: RolePermissionId(str(ulid.new())), init=False
    )
    role_id: RoleId
    permission_id: PermissionId
