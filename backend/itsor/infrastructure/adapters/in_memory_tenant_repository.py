from itsor.domain.models import PlatformTenant
from itsor.domain.ports.tenant_repository import TenantRepository
from itsor.infrastructure.adapters.in_memory_base_repository import InMemoryBaseRepository


class InMemoryTenantRepository(InMemoryBaseRepository[PlatformTenant], TenantRepository):
    def __init__(self) -> None:
        super().__init__("Tenant")

    def get_by_name(self, name: str) -> PlatformTenant | None:
        for tenant in self._items.values():
            if tenant.name == name:
                return tenant
        return None
