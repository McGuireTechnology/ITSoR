from __future__ import annotations

from dataclasses import dataclass, field

import ulid


from itsor.domain.models.ids import (
    GroupId,
    GroupMembershipId,
    GroupRoleId,
    PermissionId,
    RoleId,
    RolePermissionId,
    TenantId,
    UserId,
    UserRoleId,
    UserTenantId,
)

from itsor.domain.authz.platform_resource_authz import PlatformResource as Resource
from itsor.domain.authz.resource_authz import ResourceAction


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
class UserGroupMembership:
    id: GroupMembershipId = field(default_factory=lambda: GroupMembershipId(str(ulid.new())), init=False)
    group_id: GroupId
    member_user_id: UserId


@dataclass
class GroupGroupMembership:
    id: GroupMembershipId = field(default_factory=lambda: GroupMembershipId(str(ulid.new())), init=False)
    group_id: GroupId
    member_group_id: GroupId




@dataclass
class UserRole:
    id: UserRoleId = field(default_factory=lambda: UserRoleId(str(ulid.new())), init=False)
    user_id: UserId
    role_id: RoleId


@dataclass
class GroupRole:
    id: GroupRoleId = field(default_factory=lambda: GroupRoleId(str(ulid.new())), init=False)
    group_id: GroupId
    role_id: RoleId


@dataclass
class RolePermission:
    id: RolePermissionId = field(default_factory=lambda: RolePermissionId(str(ulid.new())), init=False)
    role_id: RoleId
    permission_id: PermissionId





