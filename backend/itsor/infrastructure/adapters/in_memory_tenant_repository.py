from typing import List, Optional

from itsor.domain.models.tenant import Tenant
from itsor.domain.ports.tenant_repository import TenantRepository


class InMemoryTenantRepository(TenantRepository):
    def __init__(self) -> None:
        self._tenants: dict[str, Tenant] = {}

    def get_by_id(self, tenant_id: str) -> Optional[Tenant]:
        return self._tenants.get(tenant_id)

    def get_by_name(self, name: str) -> Optional[Tenant]:
        for tenant in self._tenants.values():
            if tenant.name == name:
                return tenant
        return None

    def list(self) -> List[Tenant]:
        return list(self._tenants.values())

    def create(self, tenant: Tenant) -> Tenant:
        self._tenants[tenant.id] = tenant
        return tenant

    def update(self, tenant: Tenant) -> Tenant:
        if tenant.id not in self._tenants:
            raise ValueError(f"Tenant {tenant.id} not found")
        self._tenants[tenant.id] = tenant
        return tenant

    def delete(self, tenant_id: str) -> None:
        self._tenants.pop(tenant_id, None)
