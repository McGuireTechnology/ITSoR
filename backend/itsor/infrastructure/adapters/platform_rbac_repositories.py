from typing import Any, cast

from sqlalchemy.orm import Session

from itsor.domain.models import (
    Permission,
    Resource,
    ResourceAction,
    Role,
    RoleAssignment,
    RolePermission,
    UserTenant,
)
from itsor.domain.models.ids import (
    GroupId,
    PermissionId,
    RoleAssignmentId,
    RoleId,
    RolePermissionId,
    TenantId,
    UserId,
    UserTenantId,
)
from itsor.domain.ports.platform_ports import (
    GroupRoleRepository,
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
    UserRoleRepository,
    UserTenantRepository,
)
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.models.sqlalchemy_platform_rbac_models import (
    PlatformGroupRoleModel,
    PlatformPermissionModel,
    PlatformRoleModel,
    PlatformRolePermissionModel,
    PlatformUserRoleModel,
    PlatformUserTenantModel,
)


class SQLAlchemyRoleRepository(SQLAlchemyBaseRepository[Role, PlatformRoleModel], RoleRepository):
    model_class = PlatformRoleModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Role")

    def _to_domain(self, record: PlatformRoleModel) -> Role:
        role = Role(
            name=str(record.name),
            tenant_id=cast(
                TenantId, str(record.tenant_id) if record.tenant_id is not None else None
            ),
            description=str(record.description),
        )
        role.id = RoleId(str(record.id))
        return role

    def _to_model(self, entity: Role) -> PlatformRoleModel:
        return PlatformRoleModel(
            id=str(entity.id),
            name=str(entity.name),
            tenant_id=str(entity.tenant_id) if entity.tenant_id is not None else None,
            description=str(entity.description),
        )

    def _apply_updates(self, record: PlatformRoleModel, entity: Role) -> None:
        target = cast(Any, record)
        target.name = str(entity.name)
        target.tenant_id = str(entity.tenant_id) if entity.tenant_id is not None else None
        target.description = str(entity.description)

    def get_by_name(self, name: str, tenant_id: str | None = None) -> Role | None:
        record = (
            self._db.query(PlatformRoleModel)
            .filter(PlatformRoleModel.name == name, PlatformRoleModel.tenant_id == tenant_id)
            .first()
        )
        return self._to_domain(record) if record else None


class SQLAlchemyPermissionRepository(
    SQLAlchemyBaseRepository[Permission, PlatformPermissionModel],
    PermissionRepository,
):
    model_class = PlatformPermissionModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Permission")

    def _to_domain(self, record: PlatformPermissionModel) -> Permission:
        action_value = str(record.action)
        try:
            action = ResourceAction.from_verb(action_value)
        except ValueError:
            action = cast(ResourceAction, action_value)

        resource_value = str(record.resource)
        try:
            resource = Resource(resource_value)
        except ValueError:
            resource = cast(Resource, resource_value)

        permission = Permission(
            name=str(record.name),
            resource=resource,
            action=action,
        )
        permission.id = PermissionId(str(record.id))
        return permission

    def _to_model(self, entity: Permission) -> PlatformPermissionModel:
        action_value = (
            entity.action.value if isinstance(entity.action, ResourceAction) else str(entity.action)
        )
        return PlatformPermissionModel(
            id=str(entity.id),
            name=str(entity.name),
            resource=str(entity.resource),
            action=action_value,
        )

    def _apply_updates(self, record: PlatformPermissionModel, entity: Permission) -> None:
        target = cast(Any, record)
        target.name = str(entity.name)
        target.resource = str(entity.resource)
        target.action = (
            entity.action.value if isinstance(entity.action, ResourceAction) else str(entity.action)
        )


class SQLAlchemyUserTenantRepository(
    SQLAlchemyBaseRepository[UserTenant, PlatformUserTenantModel],
    UserTenantRepository,
):
    model_class = PlatformUserTenantModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "User-tenant link")

    def _to_domain(self, record: PlatformUserTenantModel) -> UserTenant:
        link = UserTenant(
            user_id=UserId(str(record.user_id)),
            tenant_id=TenantId(str(record.tenant_id)),
        )
        link.id = UserTenantId(str(record.id))
        return link

    def _to_model(self, entity: UserTenant) -> PlatformUserTenantModel:
        return PlatformUserTenantModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            tenant_id=str(entity.tenant_id),
        )

    def _apply_updates(self, record: PlatformUserTenantModel, entity: UserTenant) -> None:
        target = cast(Any, record)
        target.user_id = str(entity.user_id)
        target.tenant_id = str(entity.tenant_id)


class SQLAlchemyUserRoleRepository(
    SQLAlchemyBaseRepository[RoleAssignment, PlatformUserRoleModel],
    UserRoleRepository,
):
    model_class = PlatformUserRoleModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "User-role link")

    def _to_domain(self, record: PlatformUserRoleModel) -> RoleAssignment:
        link = RoleAssignment(
            role_id=RoleId(str(record.role_id)),
            assignee_type="user",
            user_id=UserId(str(record.user_id)),
        )
        link.id = RoleAssignmentId(str(record.id))
        return link

    def _to_model(self, entity: RoleAssignment) -> PlatformUserRoleModel:
        if entity.assignee_type != "user" or entity.user_id is None or entity.group_id is not None:
            raise ValueError("User-role repository expects user role assignments")
        return PlatformUserRoleModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            role_id=str(entity.role_id),
        )

    def _apply_updates(self, record: PlatformUserRoleModel, entity: RoleAssignment) -> None:
        if entity.assignee_type != "user" or entity.user_id is None or entity.group_id is not None:
            raise ValueError("User-role repository expects user role assignments")
        target = cast(Any, record)
        target.user_id = str(entity.user_id)
        target.role_id = str(entity.role_id)


class SQLAlchemyGroupRoleRepository(
    SQLAlchemyBaseRepository[RoleAssignment, PlatformGroupRoleModel],
    GroupRoleRepository,
):
    model_class = PlatformGroupRoleModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Group-role link")

    def _to_domain(self, record: PlatformGroupRoleModel) -> RoleAssignment:
        link = RoleAssignment(
            role_id=RoleId(str(record.role_id)),
            assignee_type="group",
            group_id=GroupId(str(record.group_id)),
        )
        link.id = RoleAssignmentId(str(record.id))
        return link

    def _to_model(self, entity: RoleAssignment) -> PlatformGroupRoleModel:
        if entity.assignee_type != "group" or entity.group_id is None or entity.user_id is not None:
            raise ValueError("Group-role repository expects group role assignments")
        return PlatformGroupRoleModel(
            id=str(entity.id),
            group_id=str(entity.group_id),
            role_id=str(entity.role_id),
        )

    def _apply_updates(self, record: PlatformGroupRoleModel, entity: RoleAssignment) -> None:
        if entity.assignee_type != "group" or entity.group_id is None or entity.user_id is not None:
            raise ValueError("Group-role repository expects group role assignments")
        target = cast(Any, record)
        target.group_id = str(entity.group_id)
        target.role_id = str(entity.role_id)


class SQLAlchemyRolePermissionRepository(
    SQLAlchemyBaseRepository[RolePermission, PlatformRolePermissionModel],
    RolePermissionRepository,
):
    model_class = PlatformRolePermissionModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Role-permission link")

    def _to_domain(self, record: PlatformRolePermissionModel) -> RolePermission:
        link = RolePermission(
            role_id=RoleId(str(record.role_id)),
            permission_id=PermissionId(str(record.permission_id)),
        )
        link.id = RolePermissionId(str(record.id))
        return link

    def _to_model(self, entity: RolePermission) -> PlatformRolePermissionModel:
        return PlatformRolePermissionModel(
            id=str(entity.id),
            role_id=str(entity.role_id),
            permission_id=str(entity.permission_id),
        )

    def _apply_updates(self, record: PlatformRolePermissionModel, entity: RolePermission) -> None:
        target = cast(Any, record)
        target.role_id = str(entity.role_id)
        target.permission_id = str(entity.permission_id)
