from sqlalchemy.orm import Session

from itsor.domain.models import PlatformGroup
from itsor.domain.ports.platform_ports import GroupRepository
from itsor.infrastructure.adapters.platform_endpoint_permissions import (
    fetch_platform_endpoint_permissions,
    replace_platform_endpoint_permissions,
)
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.models.sqlalchemy_group_model import GroupModel


class SQLAlchemyGroupRepository(SQLAlchemyBaseRepository[PlatformGroup, GroupModel], GroupRepository):
    model_class = GroupModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Group")

    def _to_domain(self, record: GroupModel) -> PlatformGroup:
        return PlatformGroup(
            id=record.id,
            name=record.name,
            tenant_id=record.tenant_id,
            owner_id=record.owner_id,
            group_id=record.group_id,
            permissions=record.permissions,
            platform_endpoint_permissions=fetch_platform_endpoint_permissions(
                self._db,
                principal_type="group",
                principal_id=record.id,
            ),
        )

    def _to_model(self, group: PlatformGroup) -> GroupModel:
        return GroupModel(
            id=group.id,
            name=group.name,
            tenant_id=group.tenant_id,
            owner_id=group.owner_id,
            group_id=group.group_id,
            permissions=group.permissions,
        )

    def _apply_updates(self, record: GroupModel, group: PlatformGroup) -> None:
        record.tenant_id = group.tenant_id
        record.name = group.name
        record.owner_id = group.owner_id
        record.group_id = group.group_id
        record.permissions = group.permissions

    def create(self, entity: PlatformGroup) -> PlatformGroup:
        created = super().create(entity)
        replace_platform_endpoint_permissions(
            self._db,
            principal_type="group",
            principal_id=created.id,
            permissions=entity.platform_endpoint_permissions,
        )
        return self.get_by_id(created.id) or created

    def update(self, entity: PlatformGroup) -> PlatformGroup:
        updated = super().update(entity)
        replace_platform_endpoint_permissions(
            self._db,
            principal_type="group",
            principal_id=updated.id,
            permissions=entity.platform_endpoint_permissions,
        )
        return self.get_by_id(updated.id) or updated

    def get_by_name(self, name: str, tenant_id: str | None = None) -> PlatformGroup | None:
        record = (
            self._db.query(GroupModel)
            .filter(GroupModel.name == name, GroupModel.tenant_id == tenant_id)
            .first()
        )
        return self._to_domain(record) if record else None
