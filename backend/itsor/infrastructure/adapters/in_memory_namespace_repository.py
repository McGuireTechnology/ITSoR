from itsor.domain.models import Namespace
from itsor.domain.ports.namespace_repository import NamespaceRepository
from itsor.infrastructure.adapters.in_memory_base_repository import InMemoryBaseRepository


class InMemoryNamespaceRepository(InMemoryBaseRepository[Namespace], NamespaceRepository):
    def __init__(self) -> None:
        super().__init__("Namespace")

    def get_by_name(self, name: str, workspace_id: str) -> Namespace | None:
        for item in self._items.values():
            if item.name == name and item.workspace_id == workspace_id:
                return item
        return None
