from sqlalchemy.orm import Session
from typing import Any

from itsor.application.ports.custom_ports import EntityTypeRepository
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.persistence_models.sqlalchemy_entity_type_model import EntityTypeModel


class SQLAlchemyEntityTypeRepository(
    SQLAlchemyBaseRepository[Any, EntityTypeModel], EntityTypeRepository
):
    model_class = EntityTypeModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "EntityType")

    def _to_domain(self, record: EntityTypeModel) -> Any:
        return record

    def _to_model(self, entity_type: Any) -> EntityTypeModel:
        return EntityTypeModel(
            id=entity_type.id,
            namespace_id=entity_type.namespace_id,
            name=entity_type.name,
            attributes_json=entity_type.attributes_json,
            owner_id=entity_type.owner_id,
            group_id=entity_type.group_id,
            permissions=entity_type.permissions,
        )

    def _apply_updates(self, record: EntityTypeModel, entity: Any) -> None:
        record.name = entity.name
        record.namespace_id = entity.namespace_id
        record.attributes_json = entity.attributes_json
        record.owner_id = entity.owner_id
        record.group_id = entity.group_id
        record.permissions = entity.permissions

    def get_by_name(self, name: str, namespace_id: str) -> Any | None:
        record = (
            self._db.query(EntityTypeModel)
            .filter(EntityTypeModel.name == name, EntityTypeModel.namespace_id == namespace_id)
            .first()
        )
        return self._to_domain(record) if record else None
