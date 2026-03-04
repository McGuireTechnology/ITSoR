"""DB-backed SQLAlchemy models for platform RBAC resources."""

# noqa: E501

import ulid
from sqlalchemy import CheckConstraint, Column, ForeignKey, String, UniqueConstraint

from itsor.infrastructure.persistence_models.sqlalchemy_user_model import Base


def _new_platform_id() -> str:
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
