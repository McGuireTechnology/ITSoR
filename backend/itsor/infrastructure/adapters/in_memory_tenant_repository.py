from itsor.domain.models import Tenant
from itsor.domain.ports.tenant_repository import TenantRepository
from itsor.infrastructure.adapters.in_memory_base_repository import InMemoryBaseRepository


class InMemoryTenantRepository(InMemoryBaseRepository[Tenant], TenantRepository):
    def __init__(self) -> None:
        super().__init__("Tenant")

    def get_by_name(self, name: str) -> Tenant | None:
        for tenant in self._items.values():
            if tenant.name == name:
                return tenant
        return None
