from sqlalchemy.orm import Session
from typing import Any

from itsor.application.ports.custom_ports import EntityRecordRepository
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.persistence_models.sqlalchemy_entity_record_model import EntityRecordModel


class SQLAlchemyEntityRecordRepository(
    SQLAlchemyBaseRepository[Any, EntityRecordModel], EntityRecordRepository
):
    model_class = EntityRecordModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "EntityRecord")

    def _to_domain(self, record: EntityRecordModel) -> Any:
        return record

    def _to_model(self, entity_record: Any) -> EntityRecordModel:
        return EntityRecordModel(
            id=entity_record.id,
            entity_type_id=entity_record.entity_type_id,
            name=entity_record.name,
            values_json=entity_record.values_json,
            owner_id=entity_record.owner_id,
            group_id=entity_record.group_id,
            permissions=entity_record.permissions,
        )

    def _apply_updates(self, record: EntityRecordModel, entity: Any) -> None:
        record.name = entity.name
        record.entity_type_id = entity.entity_type_id
        record.values_json = entity.values_json
        record.owner_id = entity.owner_id
        record.group_id = entity.group_id
        record.permissions = entity.permissions

    def get_by_name(self, name: str, entity_type_id: str) -> Any | None:
        record = (
            self._db.query(EntityRecordModel)
            .filter(EntityRecordModel.name == name, EntityRecordModel.entity_type_id == entity_type_id)
            .first()
        )
        return self._to_domain(record) if record else None
