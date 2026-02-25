from typing import Any, List, Optional

from itsor.domain.ids import generate_ulid
from itsor.domain.models import EntityType
from itsor.domain.ports.entity_record_repository import EntityRecordRepository
from itsor.domain.ports.entity_type_repository import EntityTypeRepository
from itsor.domain.ports.namespace_repository import NamespaceRepository
from itsor.domain.use_cases.base_use_case import BaseUseCase


class EntityTypeUseCases(BaseUseCase):
    def __init__(
        self,
        repo: EntityTypeRepository,
        namespace_repo: NamespaceRepository,
        entity_record_repo: EntityRecordRepository,
    ) -> None:
        self._repo = repo
        self._namespace_repo = namespace_repo
        self._entity_record_repo = entity_record_repo

    def list_entity_types(self, namespace_id: str | None = None) -> List[EntityType]:
        items = self._repo.list()
        if namespace_id is None:
            return items
        return [item for item in items if item.namespace_id == namespace_id]

    def get_entity_type(self, entity_type_id: str) -> Optional[EntityType]:
        return self._repo.get_by_id(entity_type_id)

    def create_entity_type(
        self,
        name: str,
        namespace_id: str,
        attributes_json: dict[str, Any] | None = None,
    ) -> EntityType:
        namespace = self._namespace_repo.get_by_id(namespace_id)
        if not namespace:
            raise ValueError("Namespace not found")
        existing = self._repo.get_by_name(name, namespace_id)
        if existing:
            raise ValueError("Entity type name already registered")
        entity_type = EntityType(
            id=generate_ulid(),
            name=name,
            namespace_id=namespace_id,
            attributes_json=attributes_json or {},
        )
        return self._repo.create(entity_type)

    def update_entity_type(
        self,
        entity_type_id: str,
        name: str | None = None,
        attributes_json: dict[str, Any] | None = None,
    ) -> EntityType:
        entity_type = self._repo.get_by_id(entity_type_id)
        if not entity_type:
            raise ValueError("Entity type not found")
        if name is not None and name != entity_type.name:
            existing = self._repo.get_by_name(name, entity_type.namespace_id)
            if existing:
                raise ValueError("Entity type name already in use")
            entity_type.name = name
        if attributes_json is not None:
            entity_type.attributes_json = attributes_json
        return self._repo.update(entity_type)

    def replace_entity_type(
        self,
        entity_type_id: str,
        name: str,
        namespace_id: str,
        attributes_json: dict[str, Any] | None = None,
    ) -> EntityType:
        entity_type = self._repo.get_by_id(entity_type_id)
        if not entity_type:
            raise ValueError("Entity type not found")

        namespace = self._namespace_repo.get_by_id(namespace_id)
        if not namespace:
            raise ValueError("Namespace not found")

        if name != entity_type.name or namespace_id != entity_type.namespace_id:
            existing = self._repo.get_by_name(name, namespace_id)
            if existing and existing.id != entity_type.id:
                raise ValueError("Entity type name already in use")

        entity_type.name = name
        entity_type.namespace_id = namespace_id
        entity_type.attributes_json = attributes_json or {}
        return self._repo.update(entity_type)

    def delete_entity_type(self, entity_type_id: str) -> None:
        entity_type = self._repo.get_by_id(entity_type_id)
        if not entity_type:
            raise ValueError("Entity type not found")

        entity_records = [
            item for item in self._entity_record_repo.list() if item.entity_type_id == entity_type_id
        ]
        for record in entity_records:
            self._entity_record_repo.delete(record.id)
        self._repo.delete(entity_type_id)
