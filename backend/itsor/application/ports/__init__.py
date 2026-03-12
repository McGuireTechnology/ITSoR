# Domain Ports Layer


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
from itsor.application.ports.oscal import OscalDocumentRepository

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
    "OscalDocumentRepository",
    "WorkspaceRepository",
]
