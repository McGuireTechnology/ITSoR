from itsor.domain.models import PlatformGroup
from itsor.domain.ports.platform_ports import GroupRepository
from itsor.infrastructure.adapters.in_memory_base_repository import InMemoryBaseRepository


class InMemoryGroupRepository(InMemoryBaseRepository[PlatformGroup], GroupRepository):
    def __init__(self) -> None:
        super().__init__("Group")

    def get_by_name(self, name: str, tenant_id: str | None = None) -> PlatformGroup | None:
        for group in self._items.values():
            if group.name == name and group.tenant_id == tenant_id:
                return group
        return None
