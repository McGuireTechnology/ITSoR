from sqlalchemy.orm import Session

from itsor.domain.models import Group
from itsor.domain.ports.group_repository import GroupRepository
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.models.sqlalchemy_group_model import GroupModel


class SQLAlchemyGroupRepository(SQLAlchemyBaseRepository[Group, GroupModel], GroupRepository):
    model_class = GroupModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Group")

    def _to_domain(self, record: GroupModel) -> Group:
        return Group(
            id=record.id,
            name=record.name,
            tenant_id=record.tenant_id,
            owner_id=record.owner_id,
            group_id=record.group_id,
            permissions=record.permissions,
        )

    def _to_model(self, group: Group) -> GroupModel:
        return GroupModel(
            id=group.id,
            name=group.name,
            tenant_id=group.tenant_id,
            owner_id=group.owner_id,
            group_id=group.group_id,
            permissions=group.permissions,
        )

    def _apply_updates(self, record: GroupModel, group: Group) -> None:
        record.tenant_id = group.tenant_id
        record.name = group.name
        record.owner_id = group.owner_id
        record.group_id = group.group_id
        record.permissions = group.permissions

    def get_by_name(self, name: str, tenant_id: str | None = None) -> Group | None:
        record = (
            self._db.query(GroupModel)
            .filter(GroupModel.name == name, GroupModel.tenant_id == tenant_id)
            .first()
        )
        return self._to_domain(record) if record else None
