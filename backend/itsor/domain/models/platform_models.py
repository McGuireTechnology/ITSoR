from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import ulid

from itsor.domain.authz.authz import ResourceAction
from itsor.domain.authz.platform_authz import PlatformResource as Resource
from itsor.domain.models.ids import (
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


@dataclass
class User:
    id: UserId = field(default_factory=lambda: UserId(str(ulid.new())), init=False)
    name: str
    username: str
    email: str
    password_hash: str


@dataclass
class Tenant:
    id: TenantId = field(default_factory=lambda: TenantId(str(ulid.new())), init=False)
    name: str


@dataclass
class Group:
    id: GroupId = field(default_factory=lambda: GroupId(str(ulid.new())), init=False)
    tenant_id: TenantId
    name: str


@dataclass
class Role:
    id: RoleId = field(default_factory=lambda: RoleId(str(ulid.new())), init=False)
    name: str
    tenant_id: TenantId
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
