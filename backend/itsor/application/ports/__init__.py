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
