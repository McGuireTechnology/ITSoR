from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, NewType, TypeVar

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



TId = TypeVar("TId")


def _new_id(caster: Callable[[str], TId]) -> TId:
    return caster(str(ulid.new()))


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
    id: UserId = field(default_factory=lambda: _new_id(UserId))
    name: str = ""
    username: str = ""
    email: str = ""
    password_hash: str = ""


@dataclass
class PlatformTenant:
    id: TenantId = field(default_factory=lambda: _new_id(TenantId))
    name: str = ""


@dataclass
class PlatformGroup:
    id: GroupId = field(default_factory=lambda: _new_id(GroupId))
    tenant_id: TenantId | None = None
    name: str = ""


@dataclass
class PlatformRole:
    id: RoleId = field(default_factory=lambda: _new_id(RoleId))
    name: str = ""
    tenant_id: TenantId | None = None
    description: str = ""


@dataclass
class PlatformPermission:
    id: PermissionId = field(default_factory=lambda: _new_id(PermissionId))
    name: str = ""
    resource: str = PlatformResource.USER.value
    action: PlatformResourceAction = PlatformResourceAction.READ


@dataclass
class PlatformUserTenant:
    id: UserTenantId = field(default_factory=lambda: _new_id(UserTenantId))
    user_id: UserId = UserId("")
    tenant_id: TenantId = TenantId("")


@dataclass
class PlatformGroupMembership:
    id: GroupMembershipId = field(default_factory=lambda: _new_id(GroupMembershipId))
    group_id: GroupId = GroupId("")
    member_type: str = "user"
    member_user_id: UserId | None = None
    member_group_id: GroupId | None = None


@dataclass
class PlatformUserRole:
    id: UserRoleId = field(default_factory=lambda: _new_id(UserRoleId))
    user_id: UserId = UserId("")
    role_id: RoleId = RoleId("")


@dataclass
class PlatformGroupRole:
    id: GroupRoleId = field(default_factory=lambda: _new_id(GroupRoleId))
    group_id: GroupId = GroupId("")
    role_id: RoleId = RoleId("")


@dataclass
class PlatformRolePermission:
    id: RolePermissionId = field(default_factory=lambda: _new_id(RolePermissionId))
    role_id: RoleId = RoleId("")
    permission_id: PermissionId = PermissionId("")
