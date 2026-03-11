import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from itsor.application.ports.auth.repositories import (
    GroupMembershipRepository,
    GroupRepository,
    GroupRoleRepository,
    PasswordHasher,
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
    TenantRepository,
    TokenCodec,
    UserRepository,
    UserRoleRepository,
    UserTenantRepository,
)
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.database.sqlalchemy.models.auth import GroupModel
from itsor.infrastructure.database.sqlalchemy.models.auth import (
    PlatformEndpointPermissionModel,
)
from itsor.infrastructure.database.sqlalchemy.models.auth import (
    PlatformGroupMembershipModel,
)
from itsor.infrastructure.database.sqlalchemy.models.auth import (
    PlatformGroupRoleModel,
    PlatformPermissionModel,
    PlatformRoleModel,
    PlatformRolePermissionModel,
    PlatformUserRoleModel,
    PlatformUserTenantModel,
)
from itsor.infrastructure.database.sqlalchemy.models.auth import TenantModel, UserModel


def _normalize_action(value: Any) -> str:
    if hasattr(value, "value"):
        return str(getattr(value, "value")).strip().lower()
    return str(value).strip().lower()


def _to_action(value: str) -> str:
    return str(value).strip().lower()


class SQLAlchemyUserRepository(SQLAlchemyBaseRepository[Any, UserModel], UserRepository):
    model_class = UserModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "User")

    def _to_domain(self, record: UserModel) -> Any:
        return record

    def _to_model(self, user: Any) -> UserModel:
        return UserModel(
            id=user.id,
            name=user.name,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            group_id=user.group_id,
        )

    def _apply_updates(self, record: UserModel, user: Any) -> None:
        record.name = user.name
        record.username = user.username
        record.email = user.email
        record.password_hash = user.password_hash
        record.group_id = user.group_id

    def get_by_email(self, email: str) -> Any | None:
        record = self._db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_domain(record) if record else None

    def get_by_username(self, username: str) -> Any | None:
        record = self._db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_domain(record) if record else None


class SQLAlchemyTenantRepository(SQLAlchemyBaseRepository[Any, TenantModel], TenantRepository):
    model_class = TenantModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Tenant")

    def _to_domain(self, record: TenantModel) -> Any:
        return record

    def _to_model(self, tenant: Any) -> TenantModel:
        return TenantModel(
            id=tenant.id,
            name=tenant.name,
            owner_id=getattr(tenant, "owner_id", None),
            group_id=getattr(tenant, "group_id", None),
            permissions=getattr(tenant, "permissions", None),
        )

    def _apply_updates(self, record: TenantModel, tenant: Any) -> None:
        record.name = tenant.name
        record.owner_id = getattr(tenant, "owner_id", None)
        record.group_id = getattr(tenant, "group_id", None)
        record.permissions = getattr(tenant, "permissions", None)

    def get_by_name(self, name: str) -> Any | None:
        record = self._db.query(TenantModel).filter(TenantModel.name == name).first()
        return self._to_domain(record) if record else None


class SQLAlchemyGroupRepository(SQLAlchemyBaseRepository[Any, GroupModel], GroupRepository):
    model_class = GroupModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Group")

    def _to_domain(self, record: GroupModel) -> Any:
        return record

    def _to_model(self, group: Any) -> GroupModel:
        return GroupModel(
            id=group.id,
            name=group.name,
            tenant_id=getattr(group, "tenant_id", None),
            owner_id=getattr(group, "owner_id", None),
            group_id=getattr(group, "group_id", None),
            permissions=getattr(group, "permissions", None),
        )

    def _apply_updates(self, record: GroupModel, group: Any) -> None:
        record.tenant_id = getattr(group, "tenant_id", None)
        record.name = group.name
        record.owner_id = getattr(group, "owner_id", None)
        record.group_id = getattr(group, "group_id", None)
        record.permissions = getattr(group, "permissions", None)

    def get_by_name(self, name: str, tenant_id: str | None = None) -> Any | None:
        record = (
            self._db.query(GroupModel)
            .filter(GroupModel.name == name, GroupModel.tenant_id == tenant_id)
            .first()
        )
        return self._to_domain(record) if record else None


class SQLAlchemyGroupMembershipRepository(
    SQLAlchemyBaseRepository[Any, PlatformGroupMembershipModel],
    GroupMembershipRepository,
):
    model_class = PlatformGroupMembershipModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Group membership")

    def _to_domain(self, record: PlatformGroupMembershipModel) -> Any:
        return record

    def _to_model(self, entity: Any) -> PlatformGroupMembershipModel:
        return PlatformGroupMembershipModel(
            id=str(entity.id),
            group_id=str(entity.group_id),
            member_type=str(entity.member_type),
            member_user_id=(
                str(entity.member_user_id) if getattr(entity, "member_user_id", None) is not None else None
            ),
            member_group_id=(
                str(entity.member_group_id) if getattr(entity, "member_group_id", None) is not None else None
            ),
        )

    def _apply_updates(self, record: PlatformGroupMembershipModel, entity: Any) -> None:
        record.group_id = str(entity.group_id)
        record.member_type = str(entity.member_type)
        record.member_user_id = (
            str(entity.member_user_id) if getattr(entity, "member_user_id", None) is not None else None
        )
        record.member_group_id = (
            str(entity.member_group_id) if getattr(entity, "member_group_id", None) is not None else None
        )


class SQLAlchemyPlatformEndpointPermissionGateway:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_rows(self, *, principal_type=None, principal_id=None) -> list[PlatformEndpointPermissionModel]:
        query = self._db.query(PlatformEndpointPermissionModel)
        if principal_type:
            query = query.filter(PlatformEndpointPermissionModel.principal_type == principal_type)
        if principal_id:
            query = query.filter(PlatformEndpointPermissionModel.principal_id == principal_id)
        return query.order_by(PlatformEndpointPermissionModel.id.asc()).all()

    def create_row(self, *, principal_type, principal_id, endpoint_name, action) -> PlatformEndpointPermissionModel:
        model = PlatformEndpointPermissionModel(
            principal_type=principal_type,
            principal_id=principal_id,
            endpoint_name=endpoint_name,
            action=action,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return model

    def get_row(self, endpoint_permission_id: int) -> PlatformEndpointPermissionModel | None:
        return (
            self._db.query(PlatformEndpointPermissionModel)
            .filter(PlatformEndpointPermissionModel.id == endpoint_permission_id)
            .first()
        )

    def replace_row(self, *, endpoint_permission_id, principal_type, principal_id, endpoint_name, action):
        row = self.get_row(endpoint_permission_id)
        if not row:
            return None
        row.principal_type = principal_type
        row.principal_id = principal_id
        row.endpoint_name = endpoint_name
        row.action = action
        self._db.commit()
        self._db.refresh(row)
        return row

    def patch_row(
        self,
        *,
        endpoint_permission_id,
        principal_type=None,
        principal_id=None,
        endpoint_name=None,
        action=None,
    ):
        row = self.get_row(endpoint_permission_id)
        if not row:
            return None
        if principal_type is not None:
            row.principal_type = principal_type
        if principal_id is not None:
            row.principal_id = principal_id
        if endpoint_name is not None:
            row.endpoint_name = endpoint_name
        if action is not None:
            row.action = action
        self._db.commit()
        self._db.refresh(row)
        return row

    def delete_row(self, endpoint_permission_id: int) -> bool:
        row = self.get_row(endpoint_permission_id)
        if not row:
            return False
        self._db.delete(row)
        self._db.commit()
        return True


class SQLAlchemyPlatformGroupMembershipGateway:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_memberships(self) -> list[PlatformGroupMembershipModel]:
        return self._db.query(PlatformGroupMembershipModel).all()

    def create_membership(self, *, group_id, member_type, member_user_id, member_group_id):
        membership = PlatformGroupMembershipModel(
            group_id=group_id,
            member_type=member_type,
            member_user_id=member_user_id,
            member_group_id=member_group_id,
        )
        self._db.add(membership)
        self._db.commit()
        self._db.refresh(membership)
        return membership

    def get_membership(self, membership_id: str):
        return (
            self._db.query(PlatformGroupMembershipModel)
            .filter(PlatformGroupMembershipModel.id == membership_id)
            .first()
        )

    def patch_membership(self, *, membership_id, member_type=None, member_user_id=None, member_group_id=None):
        membership = self.get_membership(membership_id)
        if not membership:
            return None

        if member_type is not None:
            membership.member_type = member_type
        if member_user_id is not None:
            membership.member_user_id = member_user_id
        if member_group_id is not None:
            membership.member_group_id = member_group_id

        self._db.commit()
        self._db.refresh(membership)
        return membership

    def delete_membership(self, membership_id: str) -> bool:
        membership = self.get_membership(membership_id)
        if not membership:
            return False
        self._db.delete(membership)
        self._db.commit()
        return True


class SQLAlchemyRoleRepository(SQLAlchemyBaseRepository[Any, PlatformRoleModel], RoleRepository):
    model_class = PlatformRoleModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Role")

    def _to_domain(self, record: PlatformRoleModel) -> Any:
        return record

    def _to_model(self, entity: Any) -> PlatformRoleModel:
        return PlatformRoleModel(
            id=str(entity.id),
            name=str(entity.name),
            tenant_id=str(entity.tenant_id) if getattr(entity, "tenant_id", None) is not None else None,
            description=str(getattr(entity, "description", "")),
        )

    def _apply_updates(self, record: PlatformRoleModel, entity: Any) -> None:
        record.name = str(entity.name)
        record.tenant_id = str(entity.tenant_id) if getattr(entity, "tenant_id", None) is not None else None
        record.description = str(getattr(entity, "description", ""))

    def get_by_name(self, name: str, tenant_id: str | None = None) -> Any | None:
        record = (
            self._db.query(PlatformRoleModel)
            .filter(PlatformRoleModel.name == name, PlatformRoleModel.tenant_id == tenant_id)
            .first()
        )
        return self._to_domain(record) if record else None


class SQLAlchemyPermissionRepository(
    SQLAlchemyBaseRepository[Any, PlatformPermissionModel],
    PermissionRepository,
):
    model_class = PlatformPermissionModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Permission")

    def _to_domain(self, record: PlatformPermissionModel) -> Any:
        record.action = _to_action(str(record.action))
        return record

    def _to_model(self, entity: Any) -> PlatformPermissionModel:
        action_value = _normalize_action(getattr(entity, "action", ""))
        return PlatformPermissionModel(
            id=str(entity.id),
            name=str(entity.name),
            resource=str(getattr(entity, "resource", "")),
            action=action_value,
        )

    def _apply_updates(self, record: PlatformPermissionModel, entity: Any) -> None:
        record.name = str(entity.name)
        record.resource = str(getattr(entity, "resource", ""))
        record.action = _normalize_action(getattr(entity, "action", ""))


class SQLAlchemyUserTenantRepository(
    SQLAlchemyBaseRepository[Any, PlatformUserTenantModel],
    UserTenantRepository,
):
    model_class = PlatformUserTenantModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "User-tenant link")

    def _to_domain(self, record: PlatformUserTenantModel) -> Any:
        return record

    def _to_model(self, entity: Any) -> PlatformUserTenantModel:
        return PlatformUserTenantModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            tenant_id=str(entity.tenant_id),
        )

    def _apply_updates(self, record: PlatformUserTenantModel, entity: Any) -> None:
        record.user_id = str(entity.user_id)
        record.tenant_id = str(entity.tenant_id)


class SQLAlchemyUserRoleRepository(
    SQLAlchemyBaseRepository[Any, PlatformUserRoleModel],
    UserRoleRepository,
):
    model_class = PlatformUserRoleModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "User-role link")

    def _to_domain(self, record: PlatformUserRoleModel) -> Any:
        setattr(record, "assignee_type", "user")
        setattr(record, "group_id", None)
        return record

    def _to_model(self, entity: Any) -> PlatformUserRoleModel:
        if getattr(entity, "assignee_type", "user") != "user" or getattr(entity, "user_id", None) is None or getattr(entity, "group_id", None) is not None:
            raise ValueError("User-role repository expects user role assignments")
        return PlatformUserRoleModel(
            id=str(entity.id),
            user_id=str(entity.user_id),
            role_id=str(entity.role_id),
        )

    def _apply_updates(self, record: PlatformUserRoleModel, entity: Any) -> None:
        if getattr(entity, "assignee_type", "user") != "user" or getattr(entity, "user_id", None) is None or getattr(entity, "group_id", None) is not None:
            raise ValueError("User-role repository expects user role assignments")
        record.user_id = str(entity.user_id)
        record.role_id = str(entity.role_id)

    def list_for_user(self, user_id: str) -> list[Any]:
        records = self._db.query(PlatformUserRoleModel).filter(PlatformUserRoleModel.user_id == user_id).all()
        return [self._to_domain(record) for record in records]

    def list_for_group(self, group_id) -> list[Any]:
        return []


class SQLAlchemyGroupRoleRepository(
    SQLAlchemyBaseRepository[Any, PlatformGroupRoleModel],
    GroupRoleRepository,
):
    model_class = PlatformGroupRoleModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Group-role link")

    def _to_domain(self, record: PlatformGroupRoleModel) -> Any:
        setattr(record, "assignee_type", "group")
        setattr(record, "user_id", None)
        return record

    def _to_model(self, entity: Any) -> PlatformGroupRoleModel:
        if getattr(entity, "assignee_type", "group") != "group" or getattr(entity, "group_id", None) is None or getattr(entity, "user_id", None) is not None:
            raise ValueError("Group-role repository expects group role assignments")
        return PlatformGroupRoleModel(
            id=str(entity.id),
            group_id=str(entity.group_id),
            role_id=str(entity.role_id),
        )

    def _apply_updates(self, record: PlatformGroupRoleModel, entity: Any) -> None:
        if getattr(entity, "assignee_type", "group") != "group" or getattr(entity, "group_id", None) is None or getattr(entity, "user_id", None) is not None:
            raise ValueError("Group-role repository expects group role assignments")
        record.group_id = str(entity.group_id)
        record.role_id = str(entity.role_id)

    def list_for_user(self, user_id: str) -> list[Any]:
        return []

    def list_for_group(self, group_id) -> list[Any]:
        records = self._db.query(PlatformGroupRoleModel).filter(PlatformGroupRoleModel.group_id == group_id).all()
        return [self._to_domain(record) for record in records]


class SQLAlchemyRolePermissionRepository(
    SQLAlchemyBaseRepository[Any, PlatformRolePermissionModel],
    RolePermissionRepository,
):
    model_class = PlatformRolePermissionModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Role-permission link")

    def _to_domain(self, record: PlatformRolePermissionModel) -> Any:
        return record

    def _to_model(self, entity: Any) -> PlatformRolePermissionModel:
        return PlatformRolePermissionModel(
            id=str(entity.id),
            role_id=str(entity.role_id),
            permission_id=str(entity.permission_id),
        )

    def _apply_updates(self, record: PlatformRolePermissionModel, entity: Any) -> None:
        record.role_id = str(entity.role_id)
        record.permission_id = str(entity.permission_id)


class BcryptPasswordHasher(PasswordHasher):
    def hash_password(self, plain: str) -> str:
        return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode(), hashed.encode())


class JwtTokenCodec(TokenCodec):
    def __init__(self) -> None:
        self._secret_key = os.getenv("SECRET_KEY", "change-me-in-production")
        if self._secret_key == "change-me-in-production":
            logging.warning(
                "SECRET_KEY is using the default insecure value. Set SECRET_KEY env var in production."
            )
        self._algorithm = "HS256"
        self._access_token_expire_minutes = 60

    def create_access_token(self, subject: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self._access_token_expire_minutes)
        payload = {"sub": subject, "exp": expire}
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_access_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            value = payload.get("sub")
            return str(value) if value is not None else None
        except JWTError:
            return None


__all__ = [
    "SQLAlchemyUserRepository",
    "SQLAlchemyTenantRepository",
    "SQLAlchemyGroupRepository",
    "SQLAlchemyGroupMembershipRepository",
    "SQLAlchemyRoleRepository",
    "SQLAlchemyPermissionRepository",
    "SQLAlchemyUserTenantRepository",
    "SQLAlchemyUserRoleRepository",
    "SQLAlchemyGroupRoleRepository",
    "SQLAlchemyRolePermissionRepository",
    "SQLAlchemyPlatformEndpointPermissionGateway",
    "SQLAlchemyPlatformGroupMembershipGateway",
    "BcryptPasswordHasher",
    "JwtTokenCodec",
]
