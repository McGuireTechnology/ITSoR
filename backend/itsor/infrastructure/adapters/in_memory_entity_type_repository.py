from itsor.domain.models import EntityType
from itsor.domain.ports.entity_type_repository import EntityTypeRepository
from itsor.infrastructure.adapters.in_memory_base_repository import InMemoryBaseRepository


class InMemoryEntityTypeRepository(InMemoryBaseRepository[EntityType], EntityTypeRepository):
    def __init__(self) -> None:
        super().__init__("EntityType")

    def get_by_name(self, name: str, namespace_id: str) -> EntityType | None:
        for item in self._items.values():
            if item.name == name and item.namespace_id == namespace_id:
                return item
        return None
