# Platform Domain Models

from dataclasses import dataclass, field
from enum import Enum
from typing import NewType

from itsor.domain.ids import generate_ulid

UserId = NewType("UserId", str)
TenantId = NewType("TenantId", str)
GroupId = NewType("GroupId", str)
RoleId = NewType("RoleId", str)
PermissionId = NewType("PermissionId", str)


class PlatformResource(str, Enum):
    USER = "user"
    TENANT = "tenant"
    GROUP = "group"
    ROLE = "role"
    PERMISSION = "permission"
    USER_TENANT = "user_tenant"
    GROUP_MEMBERSHIP = "group_membership"
    USER_ROLE = "user_role"
    GROUP_ROLE = "group_role"
    ROLE_PERMISSION = "role_permission"


class PlatformResourceAction(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"


class PlatformPermissionEffect(str, Enum):
    ALLOW = "allow"
    DENY = "deny"


# Core


# User (Global)
@dataclass
class PlatformUser:
    id: UserId = field(default_factory=lambda: UserId(generate_ulid()), init=False)
    name: str
    username: str
    email: str
    password_hash: str


@dataclass
class PlatformTenant:
    id: TenantId = field(default_factory=lambda: TenantId(generate_ulid()), init=False)
    name: str

# Group (Scoped to Tenant)
@dataclass
class PlatformGroup:
    id: GroupId = field(default_factory=lambda: GroupId(generate_ulid()), init=False)
    name: str
    tenant_id: TenantId


# Role (Scoped to Tenant)
@dataclass
class PlatformRole:
    id: RoleId = field(default_factory=lambda: RoleId(generate_ulid()), init=False)
    name: str
    tenant_id: TenantId
    description: str = ""


@dataclass
class PlatformPermission:
    id: PermissionId = field(default_factory=lambda: PermissionId(generate_ulid()), init=False)
    name: str
    resource: PlatformResource
    action: PlatformResourceAction
    effect: PlatformPermissionEffect


@dataclass
class PlatformUserTenant:
    id: str = field(default_factory=generate_ulid, init=False)
    user_id: UserId
    tenant_id: TenantId


@dataclass
class PlatformGroupMembership:
    id: str = field(default_factory=generate_ulid, init=False)
    group_id: GroupId
    user_id: UserId


@dataclass
class PlatformUserRole:
    id: str = field(default_factory=generate_ulid, init=False)
    user_id: UserId
    role_id: RoleId


@dataclass
class PlatformGroupRole:
    id: str = field(default_factory=generate_ulid, init=False)
    group_id: GroupId
    role_id: RoleId


@dataclass
class PlatformRolePermission:
    id: str = field(default_factory=generate_ulid, init=False)
    role_id: RoleId
    permission_id: PermissionId
