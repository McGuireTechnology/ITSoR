# Domain Ports Layer

from itsor.domain.ports.base_repository import BaseRepository
from itsor.domain.ports.custom_ports import (
    EntityRecordRepository,
    EntityTypeRepository,
    NamespaceRepository,
    WorkspaceRepository,
)
from itsor.domain.ports.platform_ports import (
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
