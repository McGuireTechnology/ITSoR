from itsor.domain.models import EntityRecord
from itsor.domain.ports.entity_record_repository import EntityRecordRepository
from itsor.infrastructure.adapters.in_memory_base_repository import InMemoryBaseRepository


class InMemoryEntityRecordRepository(InMemoryBaseRepository[EntityRecord], EntityRecordRepository):
    def __init__(self) -> None:
        super().__init__("EntityRecord")

    def get_by_name(self, name: str, entity_type_id: str) -> EntityRecord | None:
        for item in self._items.values():
            if item.name == name and item.entity_type_id == entity_type_id:
                return item
        return None
