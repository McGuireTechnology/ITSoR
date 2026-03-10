import ulid
from sqlalchemy import Boolean, CheckConstraint, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase

from itsor.domain.models import DEFAULT_PERMISSIONS


class Base(DeclarativeBase):
	pass


class UserModel(Base):
	__tablename__ = "auth_users"

	id = Column(String(36), primary_key=True)
	name = Column(String(255), nullable=False, default="")
	username = Column(String(255), unique=True, nullable=False, index=True)
	email = Column(String(255), unique=True, nullable=False, index=True)
	password_hash = Column(String(255), nullable=False)
	group_id = Column(String(36), nullable=True, index=True)


class GroupModel(Base):
	__tablename__ = "auth_groups"
	__table_args__ = (
		UniqueConstraint("tenant_id", "name", name="uq_auth_groups_tenant_id_name"),
	)

	id = Column(String(36), primary_key=True)
	tenant_id = Column(String(36), nullable=True, index=True)
	name = Column(String(255), nullable=False, index=True)
	owner_id = Column(String(36), nullable=True, index=True)
	group_id = Column(String(36), nullable=True, index=True)
	permissions = Column(Integer, nullable=False, default=DEFAULT_PERMISSIONS)


class TenantModel(Base):
	__tablename__ = "auth_tenants"

	id = Column(String(36), primary_key=True)
	name = Column(String(255), unique=True, nullable=False, index=True)
	owner_id = Column(String(36), nullable=True, index=True)
	group_id = Column(String(36), nullable=True, index=True)
	permissions = Column(Integer, nullable=False, default=DEFAULT_PERMISSIONS)


class NavigationModuleModel(Base):
	__tablename__ = "auth_navigation_modules"
	__table_args__ = (
		UniqueConstraint("tenant_id", "key", name="uq_auth_navigation_modules_tenant_key"),
	)

	id = Column(String(36), primary_key=True)
	key = Column(String(128), nullable=False, index=True)
	label = Column(String(255), nullable=False)
	module_type = Column(String(32), nullable=False, default="custom")
	tenant_id = Column(String(36), ForeignKey("auth_tenants.id"), nullable=True, index=True)
	source_id = Column(String(36), ForeignKey("auth_navigation_modules.id"), nullable=True, index=True)
	icon = Column(String(64), nullable=True)
	order = Column(Integer, nullable=False, default=0)
	enabled = Column(Boolean, nullable=False, default=True)


class NavigationResourceModel(Base):
	__tablename__ = "auth_navigation_resources"
	__table_args__ = (
		UniqueConstraint("tenant_id", "key", "module_id", name="uq_auth_navigation_resources_tenant_key_module"),
	)

	id = Column(String(36), primary_key=True)
	key = Column(String(128), nullable=False, index=True)
	label = Column(String(255), nullable=False)
	module_id = Column(String(36), ForeignKey("auth_navigation_modules.id"), nullable=False, index=True)
	list_route = Column(String(255), nullable=False)
	tenant_id = Column(String(36), ForeignKey("auth_tenants.id"), nullable=True, index=True)
	source_id = Column(String(36), ForeignKey("auth_navigation_resources.id"), nullable=True, index=True)
	icon = Column(String(64), nullable=True)
	order = Column(Integer, nullable=False, default=0)
	enabled = Column(Boolean, nullable=False, default=True)


class NavigationViewModel(Base):
	__tablename__ = "auth_navigation_views"
	__table_args__ = (
		UniqueConstraint("tenant_id", "key", "resource_id", name="uq_auth_navigation_views_tenant_key_resource"),
	)

	id = Column(String(36), primary_key=True)
	key = Column(String(128), nullable=False, index=True)
	label = Column(String(255), nullable=False)
	view_type = Column(String(32), nullable=False, default="list")
	route = Column(String(255), nullable=False)
	resource_id = Column(String(36), ForeignKey("auth_navigation_resources.id"), nullable=False, index=True)
	tenant_id = Column(String(36), ForeignKey("auth_tenants.id"), nullable=True, index=True)
	source_id = Column(String(36), ForeignKey("auth_navigation_views.id"), nullable=True, index=True)
	icon = Column(String(64), nullable=True)
	order = Column(Integer, nullable=False, default=0)
	enabled = Column(Boolean, nullable=False, default=True)


class RoleModel(Base):
	__tablename__ = "auth_roles"
	__table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_auth_roles_tenant_name"),)

	id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
	name = Column(String(255), nullable=False, index=True)
	tenant_id = Column(String(36), ForeignKey("auth_tenants.id"), nullable=True, index=True)
	description = Column(String(1024), nullable=False, default="")


class PermissionModel(Base):
	__tablename__ = "auth_permissions"
	__table_args__ = (
		UniqueConstraint(
			"resource",
			"action",
			"effect",
			name="uq_auth_permissions_resource_action_effect",
		),
		CheckConstraint("effect in ('allow', 'deny')", name="ck_auth_permissions_effect"),
		CheckConstraint(
			"action in ('create', 'read', 'update', 'delete')",
			name="ck_auth_permissions_action",
		),
	)

	id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
	name = Column(String(255), nullable=False, index=True)
	resource = Column(String(255), nullable=False, index=True)
	action = Column(String(16), nullable=False, index=True)
	effect = Column(String(16), nullable=False, index=True, default="allow")


class UserTenantModel(Base):
	__tablename__ = "auth_user_tenants"
	__table_args__ = (
		UniqueConstraint("user_id", "tenant_id", name="uq_auth_user_tenants_user_tenant"),
	)

	id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
	user_id = Column(String(36), ForeignKey("auth_users.id"), nullable=False, index=True)
	tenant_id = Column(String(36), ForeignKey("auth_tenants.id"), nullable=False, index=True)


class UserRoleModel(Base):
	__tablename__ = "auth_user_roles"
	__table_args__ = (
		UniqueConstraint("user_id", "role_id", name="uq_auth_user_roles_user_role"),
	)

	id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
	user_id = Column(String(36), ForeignKey("auth_users.id"), nullable=False, index=True)
	role_id = Column(String(36), ForeignKey("auth_roles.id"), nullable=False, index=True)


class GroupRoleModel(Base):
	__tablename__ = "auth_group_roles"
	__table_args__ = (
		UniqueConstraint("group_id", "role_id", name="uq_auth_group_roles_group_role"),
	)

	id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
	group_id = Column(String(36), ForeignKey("auth_groups.id"), nullable=False, index=True)
	role_id = Column(String(36), ForeignKey("auth_roles.id"), nullable=False, index=True)


class RolePermissionModel(Base):
	__tablename__ = "auth_role_permissions"
	__table_args__ = (
		UniqueConstraint(
			"role_id",
			"permission_id",
			name="uq_auth_role_permissions_role_permission",
		),
	)

	id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
	role_id = Column(String(36), ForeignKey("auth_roles.id"), nullable=False, index=True)
	permission_id = Column(
		String(36), ForeignKey("auth_permissions.id"), nullable=False, index=True
	)


class GroupMembershipModel(Base):
	__tablename__ = "auth_group_memberships"
	__table_args__ = (
		CheckConstraint(
			"member_type in ('user', 'group')", name="ck_auth_membership_member_type"
		),
		CheckConstraint(
			"(member_type = 'user' and member_user_id is not null and member_group_id is null) or "
			"(member_type = 'group' and member_group_id is not null and member_user_id is null)",
			name="ck_auth_membership_member_ref",
		),
	)

	id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
	group_id = Column(String(36), ForeignKey("auth_groups.id"), nullable=False, index=True)
	member_type = Column(String(16), nullable=False)
	member_user_id = Column(String(36), ForeignKey("auth_users.id"), nullable=True, index=True)
	member_group_id = Column(
		String(36), ForeignKey("auth_groups.id"), nullable=True, index=True
	)


class EndpointPermissionModel(Base):
	__tablename__ = "auth_endpoint_permissions"
	__table_args__ = (
		UniqueConstraint(
			"principal_type",
			"principal_id",
			"endpoint_name",
			"action",
			name="uq_auth_endpoint_permissions_principal_endpoint_action",
		),
	)

	id = Column(Integer, primary_key=True, autoincrement=True)
	principal_type = Column(String(16), nullable=False, index=True)
	principal_id = Column(String(36), nullable=False, index=True)
	endpoint_name = Column(String(128), nullable=False, index=True)
	action = Column(String(16), nullable=False)


PlatformEndpointPermissionModel = EndpointPermissionModel
PlatformGroupMembershipModel = GroupMembershipModel
PlatformGroupRoleModel = GroupRoleModel
PlatformPermissionModel = PermissionModel
PlatformRoleModel = RoleModel
PlatformRolePermissionModel = RolePermissionModel
PlatformUserRoleModel = UserRoleModel
PlatformUserTenantModel = UserTenantModel


__all__ = [
	"Base",
	"GroupModel",
	"NavigationModuleModel",
	"NavigationResourceModel",
	"NavigationViewModel",
	"EndpointPermissionModel",
	"GroupMembershipModel",
	"GroupRoleModel",
	"PermissionModel",
	"RoleModel",
	"RolePermissionModel",
	"UserRoleModel",
	"UserTenantModel",
	"PlatformEndpointPermissionModel",
	"PlatformGroupMembershipModel",
	"PlatformGroupRoleModel",
	"PlatformPermissionModel",
	"PlatformRoleModel",
	"PlatformRolePermissionModel",
	"PlatformUserRoleModel",
	"PlatformUserTenantModel",
	"TenantModel",
	"UserModel",
]
