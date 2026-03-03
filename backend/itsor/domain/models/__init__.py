# Domain Models Layer

from itsor.domain.models.base_model import (
    DEFAULT_CONTROL_FLAGS,
    DEFAULT_GROUP_PERMISSIONS,
    DEFAULT_OWNER_PERMISSIONS,
    DEFAULT_PERMISSIONS,
    DEFAULT_WORLD_PERMISSIONS,
    BaseModel,
    PermissionControlFlag,
    PermissionLevel,
)
from itsor.domain.models.custom_models import (
    CustomEntityRecord,
    CustomEntityType,
    CustomNamespace,
    CustomWorkspace,
)
from itsor.domain.models.idm_models import (
    IdmGroup,
    IdmGroupMembership,
    IdmIdentity,
    IdmPerson,
    IdmUser,
)
from itsor.domain.models.ids import GroupId, PermissionId, RoleId, TenantId, UserId
from itsor.domain.models.platform_models import (
    Group,
    GroupGroupMembership,
    GroupRole,
    Permission,
    Resource,
    ResourceAction,
    Role,
    RolePermission,
    Tenant,
    User,
    UserGroupMembership,
    UserRole,
    UserTenant,
)

GroupMember = UserGroupMembership
Namespace = CustomNamespace
EntityType = CustomEntityType
EntityRecord = CustomEntityRecord
Workspace = CustomWorkspace

__all__ = [
    "BaseModel",
    "PermissionLevel",
    "PermissionControlFlag",
    "DEFAULT_OWNER_PERMISSIONS",
    "DEFAULT_GROUP_PERMISSIONS",
    "DEFAULT_WORLD_PERMISSIONS",
    "DEFAULT_CONTROL_FLAGS",
    "DEFAULT_PERMISSIONS",
    "Group",
    "UserGroupMembership",
    "GroupGroupMembership",
    "GroupMember",
    "UserId",
    "TenantId",
    "GroupId",
    "RoleId",
    "PermissionId",
    "Permission",
    "Resource",
    "ResourceAction",
    "Role",
    "RolePermission",
    "UserTenant",
    "UserRole",
    "GroupRole",
    "IdmGroup",
    "IdmGroupMembership",
    "IdmIdentity",
    "IdmPerson",
    "IdmUser",
    "CustomNamespace",
    "Namespace",
    "CustomEntityType",
    "CustomEntityRecord",
    "Tenant",
    "EntityType",
    "EntityRecord",
    "User",
    "CustomWorkspace",
    "Workspace",
]
