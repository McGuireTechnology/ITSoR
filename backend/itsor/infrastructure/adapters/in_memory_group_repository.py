from itsor.domain.models import Group
from itsor.domain.ports.group_repository import GroupRepository
from itsor.infrastructure.adapters.in_memory_base_repository import InMemoryBaseRepository


class InMemoryGroupRepository(InMemoryBaseRepository[Group], GroupRepository):
    def __init__(self) -> None:
        super().__init__("Group")

    def get_by_name(self, name: str, tenant_id: str | None = None) -> Group | None:
        for group in self._items.values():
            if group.name == name and group.tenant_id == tenant_id:
                return group
        return None
