from typing import Any, List, Optional

from itsor.domain.ids import generate_ulid
from itsor.domain.models import EntityRecord
from itsor.domain.ports.entity_record_repository import EntityRecordRepository
from itsor.domain.ports.entity_type_repository import EntityTypeRepository
from itsor.domain.use_cases.base_use_case import BaseUseCase


class EntityRecordUseCases(BaseUseCase):
    def __init__(self, repo: EntityRecordRepository, entity_type_repo: EntityTypeRepository) -> None:
        self._repo = repo
        self._entity_type_repo = entity_type_repo

    def list_entity_records(self, entity_type_id: str | None = None) -> List[EntityRecord]:
        items = self._repo.list()
        if entity_type_id is None:
            return items
        return [item for item in items if item.entity_type_id == entity_type_id]

    def search_entity_records(
        self,
        entity_type_id: str | None,
        field: str,
        value: str,
        operator: str = "eq",
    ) -> List[EntityRecord]:
        items = self.list_entity_records(entity_type_id)
        normalized_operator = operator.lower().strip()
        if normalized_operator not in {"eq", "neq", "contains"}:
            raise ValueError("Unsupported operator")

        matched: List[EntityRecord] = []
        for item in items:
            field_value = item.values_json.get(field)
            field_value_text = "" if field_value is None else str(field_value)

            if normalized_operator == "eq" and field_value_text == value:
                matched.append(item)
                continue

            if normalized_operator == "neq" and field_value_text != value:
                matched.append(item)
                continue

            if normalized_operator == "contains":
                if isinstance(field_value, list):
                    if any(str(entry) == value for entry in field_value):
                        matched.append(item)
                    continue
                if value in field_value_text:
                    matched.append(item)

        return matched

    def get_entity_record(self, entity_record_id: str) -> Optional[EntityRecord]:
        return self._repo.get_by_id(entity_record_id)

    def create_entity_record(
        self,
        entity_type_id: str,
        values_json: dict[str, Any],
        name: str = "",
    ) -> EntityRecord:
        entity_type = self._entity_type_repo.get_by_id(entity_type_id)
        if not entity_type:
            raise ValueError("Entity type not found")
        if name:
            existing = self._repo.get_by_name(name, entity_type_id)
            if existing:
                raise ValueError("Entity record name already in use")
        entity_record = EntityRecord(
            id=generate_ulid(),
            name=name,
            entity_type_id=entity_type_id,
            values_json=values_json,
        )
        return self._repo.create(entity_record)

    def update_entity_record(
        self,
        entity_record_id: str,
        name: str | None = None,
        values_json: dict[str, Any] | None = None,
    ) -> EntityRecord:
        entity_record = self._repo.get_by_id(entity_record_id)
        if not entity_record:
            raise ValueError("Entity record not found")
        if name is not None and name != entity_record.name:
            if name:
                existing = self._repo.get_by_name(name, entity_record.entity_type_id)
                if existing:
                    raise ValueError("Entity record name already in use")
            entity_record.name = name
        if values_json is not None:
            entity_record.values_json = values_json
        return self._repo.update(entity_record)

    def replace_entity_record(
        self,
        entity_record_id: str,
        entity_type_id: str,
        values_json: dict[str, Any],
        name: str = "",
    ) -> EntityRecord:
        entity_record = self._repo.get_by_id(entity_record_id)
        if not entity_record:
            raise ValueError("Entity record not found")

        entity_type = self._entity_type_repo.get_by_id(entity_type_id)
        if not entity_type:
            raise ValueError("Entity type not found")

        if name:
            existing = self._repo.get_by_name(name, entity_type_id)
            if existing and existing.id != entity_record.id:
                raise ValueError("Entity record name already in use")

        entity_record.name = name
        entity_record.entity_type_id = entity_type_id
        entity_record.values_json = values_json
        return self._repo.update(entity_record)

    def delete_entity_record(self, entity_record_id: str) -> None:
        entity_record = self._repo.get_by_id(entity_record_id)
        if not entity_record:
            raise ValueError("Entity record not found")
        self._repo.delete(entity_record_id)
