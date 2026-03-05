import ulid
from sqlalchemy import CheckConstraint, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase

from itsor.domain.models import DEFAULT_PERMISSIONS


class Base(DeclarativeBase):
	pass


class UserModel(Base):
	__tablename__ = "platform_users"

	id = Column(String(36), primary_key=True)
	name = Column(String(255), nullable=False, default="")
	username = Column(String(255), unique=True, nullable=False, index=True)
	email = Column(String(255), unique=True, nullable=False, index=True)
	password_hash = Column(String(255), nullable=False)
	group_id = Column(String(36), nullable=True, index=True)


class GroupModel(Base):
	__tablename__ = "platform_groups"
	__table_args__ = (
		UniqueConstraint("tenant_id", "name", name="uq_platform_groups_tenant_id_name"),
	)

	id = Column(String(36), primary_key=True)
	tenant_id = Column(String(36), nullable=True, index=True)
	name = Column(String(255), nullable=False, index=True)
	owner_id = Column(String(36), nullable=True, index=True)
	group_id = Column(String(36), nullable=True, index=True)
	permissions = Column(Integer, nullable=False, default=DEFAULT_PERMISSIONS)


class TenantModel(Base):
	__tablename__ = "platform_tenants"

	id = Column(String(36), primary_key=True)
	name = Column(String(255), unique=True, nullable=False, index=True)
	owner_id = Column(String(36), nullable=True, index=True)
	group_id = Column(String(36), nullable=True, index=True)
	permissions = Column(Integer, nullable=False, default=DEFAULT_PERMISSIONS)


def _new_platform_id() -> str:
	return str(ulid.new())


def _new_platform_membership_id() -> str:
	return str(ulid.new())


class PlatformRoleModel(Base):
	__tablename__ = "platform_roles"
	__table_args__ = (UniqueConstraint("tenant_id", "name", name="uq_platform_roles_tenant_name"),)

	id = Column(String(36), primary_key=True, default=_new_platform_id)
	name = Column(String(255), nullable=False, index=True)
	tenant_id = Column(String(36), ForeignKey("platform_tenants.id"), nullable=True, index=True)
	description = Column(String(1024), nullable=False, default="")


class PlatformPermissionModel(Base):
	__tablename__ = "platform_permissions"
	__table_args__ = (
		UniqueConstraint(
			"resource",
			"action",
			"effect",
			name="uq_platform_permissions_resource_action_effect",
		),
		CheckConstraint("effect in ('allow', 'deny')", name="ck_platform_permissions_effect"),
		CheckConstraint(
			"action in ('create', 'read', 'update', 'delete')",
			name="ck_platform_permissions_action",
		),
	)

	id = Column(String(36), primary_key=True, default=_new_platform_id)
	name = Column(String(255), nullable=False, index=True)
	resource = Column(String(255), nullable=False, index=True)
	action = Column(String(16), nullable=False, index=True)
	effect = Column(String(16), nullable=False, index=True, default="allow")


class PlatformUserTenantModel(Base):
	__tablename__ = "platform_user_tenants"
	__table_args__ = (
		UniqueConstraint("user_id", "tenant_id", name="uq_platform_user_tenants_user_tenant"),
	)

	id = Column(String(36), primary_key=True, default=_new_platform_id)
	user_id = Column(String(36), ForeignKey("platform_users.id"), nullable=False, index=True)
	tenant_id = Column(String(36), ForeignKey("platform_tenants.id"), nullable=False, index=True)


class PlatformUserRoleModel(Base):
	__tablename__ = "platform_user_roles"
	__table_args__ = (
		UniqueConstraint("user_id", "role_id", name="uq_platform_user_roles_user_role"),
	)

	id = Column(String(36), primary_key=True, default=_new_platform_id)
	user_id = Column(String(36), ForeignKey("platform_users.id"), nullable=False, index=True)
	role_id = Column(String(36), ForeignKey("platform_roles.id"), nullable=False, index=True)


class PlatformGroupRoleModel(Base):
	__tablename__ = "platform_group_roles"
	__table_args__ = (
		UniqueConstraint("group_id", "role_id", name="uq_platform_group_roles_group_role"),
	)

	id = Column(String(36), primary_key=True, default=_new_platform_id)
	group_id = Column(String(36), ForeignKey("platform_groups.id"), nullable=False, index=True)
	role_id = Column(String(36), ForeignKey("platform_roles.id"), nullable=False, index=True)


class PlatformRolePermissionModel(Base):
	__tablename__ = "platform_role_permissions"
	__table_args__ = (
		UniqueConstraint(
			"role_id",
			"permission_id",
			name="uq_platform_role_permissions_role_permission",
		),
	)

	id = Column(String(36), primary_key=True, default=_new_platform_id)
	role_id = Column(String(36), ForeignKey("platform_roles.id"), nullable=False, index=True)
	permission_id = Column(
		String(36), ForeignKey("platform_permissions.id"), nullable=False, index=True
	)


class PlatformGroupMembershipModel(Base):
	__tablename__ = "platform_group_memberships"
	__table_args__ = (
		CheckConstraint(
			"member_type in ('user', 'group')", name="ck_platform_membership_member_type"
		),
		CheckConstraint(
			"(member_type = 'user' and member_user_id is not null and member_group_id is null) or "
			"(member_type = 'group' and member_group_id is not null and member_user_id is null)",
			name="ck_platform_membership_member_ref",
		),
	)

	id = Column(String(36), primary_key=True, default=_new_platform_membership_id)
	group_id = Column(String(36), ForeignKey("platform_groups.id"), nullable=False, index=True)
	member_type = Column(String(16), nullable=False)
	member_user_id = Column(String(36), ForeignKey("platform_users.id"), nullable=True, index=True)
	member_group_id = Column(
		String(36), ForeignKey("platform_groups.id"), nullable=True, index=True
	)


class PlatformEndpointPermissionModel(Base):
	__tablename__ = "platform_endpoint_permissions"
	__table_args__ = (
		UniqueConstraint(
			"principal_type",
			"principal_id",
			"endpoint_name",
			"action",
			name="uq_platform_endpoint_permissions_principal_endpoint_action",
		),
	)

	id = Column(Integer, primary_key=True, autoincrement=True)
	principal_type = Column(String(16), nullable=False, index=True)
	principal_id = Column(String(36), nullable=False, index=True)
	endpoint_name = Column(String(128), nullable=False, index=True)
	action = Column(String(16), nullable=False)


__all__ = [
	"Base",
	"GroupModel",
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
