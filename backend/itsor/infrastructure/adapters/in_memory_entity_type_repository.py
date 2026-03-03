from itsor.domain.models import CustomEntityType
from itsor.domain.ports.custom_ports import EntityTypeRepository
from itsor.infrastructure.adapters.in_memory_base_repository import InMemoryBaseRepository


class InMemoryEntityTypeRepository(InMemoryBaseRepository[CustomEntityType], EntityTypeRepository):
    def __init__(self) -> None:
        super().__init__("EntityType")

    def get_by_name(self, name: str, namespace_id: str) -> CustomEntityType | None:
        for item in self._items.values():
            if item.name == name and item.namespace_id == namespace_id:
                return item
        return None
