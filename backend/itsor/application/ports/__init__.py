# Domain Ports Layer

from itsor.application.ports.base_repository import BaseRepository
from itsor.application.ports.custom_ports import (
    EntityRecordRepository,
    EntityTypeRepository,
    NamespaceRepository,
    WorkspaceRepository,
)
from itsor.application.ports.auth.repositories import (
    GroupRepository,
    GroupRoleRepository,
    PermissionRepository,
    RoleAssignmentRepository,
    RolePermissionRepository,
    RoleRepository,
    TenantRepository,
    UserRepository,
    UserRoleRepository,
    UserTenantRepository,
)

__all__ = [
    "BaseRepository",
    "EntityRecordRepository",
    "EntityTypeRepository",
    "GroupRepository",
    "GroupRoleRepository",
    "NamespaceRepository",
    "PermissionRepository",
    "RoleAssignmentRepository",
    "RolePermissionRepository",
    "RoleRepository",
    "TenantRepository",
    "UserRepository",
    "UserRoleRepository",
    "UserTenantRepository",
    "WorkspaceRepository",
]
