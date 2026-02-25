from itsor.domain.models import Workspace
from itsor.domain.ports.workspace_repository import WorkspaceRepository
from itsor.infrastructure.adapters.in_memory_base_repository import InMemoryBaseRepository


class InMemoryWorkspaceRepository(InMemoryBaseRepository[Workspace], WorkspaceRepository):
    def __init__(self) -> None:
        super().__init__("Workspace")

    def get_by_name(self, name: str, tenant_id: str | None = None) -> Workspace | None:
        for item in self._items.values():
            if item.name == name and item.tenant_id == tenant_id:
                return item
        return None
