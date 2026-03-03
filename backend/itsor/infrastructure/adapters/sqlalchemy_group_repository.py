from sqlalchemy.orm import Session

from itsor.domain.models import Group
from itsor.domain.ports.platform_ports import GroupRepository
from itsor.infrastructure.adapters.platform_endpoint_permissions import (
    fetch_platform_endpoint_permissions,
    replace_platform_endpoint_permissions,
)
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.models.sqlalchemy_group_model import GroupModel


class SQLAlchemyGroupRepository(SQLAlchemyBaseRepository[Group, GroupModel], GroupRepository):
    model_class = GroupModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Group")

    def _to_domain(self, record: GroupModel) -> Group:
        group = Group(name=record.name, tenant_id=record.tenant_id)
        group.id = record.id
        group.owner_id = record.owner_id
        group.group_id = record.group_id
        group.permissions = record.permissions
        group.platform_endpoint_permissions = fetch_platform_endpoint_permissions(
            self._db,
            principal_type="group",
            principal_id=record.id,
        )
        return group

    def _to_model(self, group: Group) -> GroupModel:
        return GroupModel(
            id=group.id,
            name=group.name,
            tenant_id=group.tenant_id,
            owner_id=getattr(group, "owner_id", None),
            group_id=getattr(group, "group_id", None),
            permissions=getattr(group, "permissions", None),
        )

    def _apply_updates(self, record: GroupModel, group: Group) -> None:
        record.tenant_id = group.tenant_id
        record.name = group.name
        record.owner_id = getattr(group, "owner_id", None)
        record.group_id = getattr(group, "group_id", None)
        record.permissions = getattr(group, "permissions", None)

    def create(self, entity: Group) -> Group:
        created = super().create(entity)
        replace_platform_endpoint_permissions(
            self._db,
            principal_type="group",
            principal_id=created.id,
            permissions=getattr(entity, "platform_endpoint_permissions", None),
        )
        return self.get_by_id(created.id) or created

    def update(self, entity: Group) -> Group:
        updated = super().update(entity)
        replace_platform_endpoint_permissions(
            self._db,
            principal_type="group",
            principal_id=updated.id,
            permissions=getattr(entity, "platform_endpoint_permissions", None),
        )
        return self.get_by_id(updated.id) or updated

    def get_by_name(self, name: str, tenant_id: str | None = None) -> Group | None:
        record = (
            self._db.query(GroupModel)
            .filter(GroupModel.name == name, GroupModel.tenant_id == tenant_id)
            .first()
        )
        return self._to_domain(record) if record else None
