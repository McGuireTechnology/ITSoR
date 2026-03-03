from __future__ import annotations

from dataclasses import dataclass, field
from typing import NewType

import ulid

from itsor.domain.authorization.platform_resources import (
    PLATFORM_RESOURCE_CATALOG,
    PlatformResource,
    PlatformResourceProvider,
)
from itsor.domain.authorization.resources import (
    MergePolicy,
    ResourceAction as PlatformResourceAction,
    ResourceCatalog,
    ResourceProvider,
    merge_resource_catalogs,
)


def build_resource_catalog(
    extra_providers: list[type[ResourceProvider]] | None = None,
    *,
    policy: MergePolicy = "error_on_conflict",
) -> ResourceCatalog:
    providers: list[type[ResourceProvider]] = [PlatformResourceProvider, *(extra_providers or [])]
    return merge_resource_catalogs(providers, policy=policy)


def platform_resource_catalog() -> ResourceCatalog:
    return PLATFORM_RESOURCE_CATALOG


Resource = PlatformResource
ResourceAction = PlatformResourceAction


UserId = NewType("UserId", str)
TenantId = NewType("TenantId", str)
GroupId = NewType("GroupId", str)
RoleId = NewType("RoleId", str)
PermissionId = NewType("PermissionId", str)
UserTenantId = NewType("UserTenantId", str)
GroupMembershipId = NewType("GroupMembershipId", str)
UserRoleId = NewType("UserRoleId", str)
GroupRoleId = NewType("GroupRoleId", str)
RolePermissionId = NewType("RolePermissionId", str)


@dataclass
class PlatformUser:
    id: UserId = field(default_factory=lambda: UserId(str(ulid.new())), init=False)
    name: str
    username: str
    email: str
    password_hash: str


@dataclass
class PlatformTenant:
    id: TenantId = field(default_factory=lambda: TenantId(str(ulid.new())), init=False)
    name: str


@dataclass
class PlatformGroup:
    id: GroupId = field(default_factory=lambda: GroupId(str(ulid.new())), init=False)
    tenant_id: TenantId
    name: str


@dataclass
class PlatformRole:
    id: RoleId = field(default_factory=lambda: RoleId(str(ulid.new())), init=False)
    name: str
    tenant_id: TenantId
    description: str


@dataclass
class PlatformPermission:
    id: PermissionId = field(default_factory=lambda: PermissionId(str(ulid.new())), init=False)
    name: str
    resource: PlatformResource
    action: PlatformResourceAction


@dataclass
class PlatformUserTenant:
    id: UserTenantId = field(default_factory=lambda: UserTenantId(str(ulid.new())), init=False)
    user_id: UserId
    tenant_id: TenantId


@dataclass
class GroupMemberUser:
    id: GroupMembershipId = field(default_factory=lambda: GroupMembershipId(str(ulid.new())), init=False)
    group_id: GroupId
    member_user_id: UserId

@dataclass
class GroupMembershipGroup:
    id: GroupMembershipId = field(default_factory=lambda: GroupMembershipId(str(ulid.new())), init=False)
    group_id: GroupId
    member_group_id: GroupId



@dataclass
class PlatformUserRole:
    id: UserRoleId = field(default_factory=lambda: UserRoleId(str(ulid.new())), init=False)
    user_id: UserId
    role_id: RoleId


@dataclass
class PlatformGroupRole:
    id: GroupRoleId = field(default_factory=lambda: GroupRoleId(str(ulid.new())), init=False)
    group_id: GroupId
    role_id: RoleId


@dataclass
class PlatformRolePermission:
    id: RolePermissionId = field(default_factory=lambda: RolePermissionId(str(ulid.new())), init=False)
    role_id: RoleId
    permission_id: PermissionId
