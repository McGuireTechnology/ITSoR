from itsor.domain.models.base_model import (
	BaseModel,
	DEFAULT_CONTROL_FLAGS,
	DEFAULT_GROUP_PERMISSIONS,
	DEFAULT_OWNER_PERMISSIONS,
	DEFAULT_PERMISSIONS,
	DEFAULT_WORLD_PERMISSIONS,
	PermissionControlFlag,
	PermissionLevel,
)
from itsor.domain.models.idm_models import IdmGroup, IdmGroupMembership, IdmIdentity, IdmPerson, IdmUser
from itsor.domain.models.platform_models import (
	PlatformGroup,
	PlatformGroupMembership,
	PlatformGroupRole,
	PlatformRole,
	PlatformRolePermission,
	PlatformTenant,
	PlatformUser,
	PlatformUserRole,
)
from itsor.domain.models.custom_models import CustomEntityRecord, CustomEntityType, CustomNamespace, CustomWorkspace

Group = PlatformGroup
GroupMember = PlatformGroupMembership
Tenant = PlatformTenant
User = PlatformUser
Role = PlatformRole
RolePermission = PlatformRolePermission
UserRole = PlatformUserRole
GroupRole = PlatformGroupRole
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
	"PlatformGroup",
	"PlatformGroupMembership",
	"PlatformRole",
	"PlatformRolePermission",
	"PlatformUserRole",
	"PlatformGroupRole",
	"Group",
	"GroupMember",
	"IdmGroup",
	"IdmGroupMembership",
	"IdmIdentity",
	"IdmPerson",
	"IdmUser",
	"CustomNamespace",
	"Namespace",
	"CustomEntityType",
	"CustomEntityRecord",
	"PlatformTenant",
	"Tenant",
	"EntityType",
	"EntityRecord",
	"PlatformUser",
	"User",
	"Role",
	"RolePermission",
	"UserRole",
	"GroupRole",
	"CustomWorkspace",
	"Workspace",
]
