from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import NewType

import ulid

class Resource(str, Enum):
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


class ResourceAction(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"


class ResourceActionContract(ABC):
    @classmethod
    @abstractmethod
    def allowed_actions(cls) -> tuple[ResourceAction, ...]:
        ...

    @classmethod
    def allows(cls, action: ResourceAction) -> bool:
        return action in cls.allowed_actions()


UserId = NewType("UserId", str)


@dataclass
class User(ResourceActionContract):
    id: UserId = field(default_factory=lambda: UserId(str(ulid.new())), init=False)
    username: str
    email: str
    password_hash: str

    @classmethod
    def allowed_actions(cls) -> tuple[ResourceAction, ...]:
        return (
            ResourceAction.CREATE,
            ResourceAction.READ,
            ResourceAction.UPDATE,
            ResourceAction.DELETE,
        )


TenantId = NewType("TenantId", str)


@dataclass
class  Tenant(ResourceActionContract):
    id: TenantId = field(default_factory=lambda: TenantId(str(ulid.new())), init=False)

    @classmethod
    def allowed_actions(cls) -> tuple[ResourceAction, ...]:
        return (
            ResourceAction.CREATE,
            ResourceAction.READ,
            ResourceAction.UPDATE,
            ResourceAction.DELETE,
        )


GroupId = NewType("GroupId", str)


@dataclass
class  Group(ResourceActionContract):
    id: GroupId = field(default_factory=lambda: GroupId(str(ulid.new())), init=False)
    tenant_id: str | None = None

    @classmethod
    def allowed_actions(cls) -> tuple[ResourceAction, ...]:
        return (
            ResourceAction.CREATE,
            ResourceAction.READ,
            ResourceAction.UPDATE,
            ResourceAction.DELETE,
        )


RoleId = NewType("RoleId", str)


@dataclass
class  Role(ResourceActionContract):
    id: RoleId = field(default_factory=lambda: RoleId(str(ulid.new())), init=False)
    tenant_id: str | None = None
    description: str = ""

    @classmethod
    def allowed_actions(cls) -> tuple[ResourceAction, ...]:
        return (
            ResourceAction.CREATE,
            ResourceAction.READ,
            ResourceAction.UPDATE,
            ResourceAction.DELETE,
        )

PermissionId = NewType("PermissionId", str)


@dataclass
class  Permission(ResourceActionContract):
    id: PermissionId = field(default_factory=lambda: PermissionId(str(ulid.new())), init=False)
    resource:  Resource =  Resource.USER
    action:  ResourceAction =  ResourceAction.READ

    @classmethod
    def allowed_actions(cls) -> tuple[ResourceAction, ...]:
        return (
            ResourceAction.CREATE,
            ResourceAction.READ,
            ResourceAction.UPDATE,
            ResourceAction.DELETE,
        )


UserTenantId = NewType("UserTenantId", str)


@dataclass
class  UserTenant(ResourceActionContract):
    id: UserTenantId = field(default_factory=lambda: UserTenantId(str(ulid.new())), init=False)
    user_id: UserId
    tenant_id: TenantId

    @classmethod
    def allowed_actions(cls) -> tuple[ResourceAction, ...]:
        return (
            ResourceAction.CREATE,
            ResourceAction.READ,
            ResourceAction.UPDATE,
            ResourceAction.DELETE,
        )

GroupMembershipId = NewType("GroupMembershipId", str)


@dataclass
class  GroupMembership(ResourceActionContract):
    id: GroupMembershipId = field(default_factory=lambda: GroupMembershipId(str(ulid.new())), init=False)
    group_id: GroupId
    user_id: UserId

    @classmethod
    def allowed_actions(cls) -> tuple[ResourceAction, ...]:
        return (
            ResourceAction.CREATE,
            ResourceAction.READ,
            ResourceAction.UPDATE,
            ResourceAction.DELETE,
        )


UserRoleId = NewType("UserRoleId", str)


@dataclass
class  UserRole(ResourceActionContract):
    id: UserRoleId = field(default_factory=lambda: UserRoleId(str(ulid.new())), init=False)
    user_id: UserId
    role_id: RoleId

    @classmethod
    def allowed_actions(cls) -> tuple[ResourceAction, ...]:
        return (
            ResourceAction.CREATE,
            ResourceAction.READ,
            ResourceAction.UPDATE,
            ResourceAction.DELETE,
        )


GroupRoleId = NewType("GroupRoleId", str)


@dataclass
class  GroupRole(ResourceActionContract):
    id: GroupRoleId = field(default_factory=lambda: GroupRoleId(str(ulid.new())), init=False)
    group_id: GroupId
    role_id: RoleId

    @classmethod
    def allowed_actions(cls) -> tuple[ResourceAction, ...]:
        return (
            ResourceAction.CREATE,
            ResourceAction.READ,
            ResourceAction.UPDATE,
            ResourceAction.DELETE,
        )


RolePermissionId = NewType("RolePermissionId", str)


@dataclass
class  RolePermission(ResourceActionContract):
    id: RolePermissionId = field(default_factory=lambda: RolePermissionId(str(ulid.new())), init=False)
    role_id: RoleId
    permission_id: PermissionId

    @classmethod
    def allowed_actions(cls) -> tuple[ResourceAction, ...]:
        return (
            ResourceAction.CREATE,
            ResourceAction.READ,
            ResourceAction.UPDATE,
            ResourceAction.DELETE,
        )
