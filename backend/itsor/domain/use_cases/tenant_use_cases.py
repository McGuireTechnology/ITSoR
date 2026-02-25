from typing import List, Optional

from itsor.domain.ids import generate_ulid
from itsor.domain.models.tenant import Tenant
from itsor.domain.ports.tenant_repository import TenantRepository


class TenantUseCases:
    def __init__(self, repo: TenantRepository) -> None:
        self._repo = repo

    def list_tenants(self) -> List[Tenant]:
        return self._repo.list()

    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        return self._repo.get_by_id(tenant_id)

    def create_tenant(self, name: str) -> Tenant:
        existing = self._repo.get_by_name(name)
        if existing:
            raise ValueError("Tenant name already registered")
        tenant = Tenant(id=generate_ulid(), name=name)
        return self._repo.create(tenant)

    def update_tenant(self, tenant_id: str, name: Optional[str] = None) -> Tenant:
        tenant = self._repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        if name is not None and name != tenant.name:
            existing = self._repo.get_by_name(name)
            if existing:
                raise ValueError("Tenant name already in use")
            tenant.name = name
        return self._repo.update(tenant)

    def replace_tenant(self, tenant_id: str, name: str) -> Tenant:
        tenant = self._repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        if name != tenant.name:
            existing = self._repo.get_by_name(name)
            if existing:
                raise ValueError("Tenant name already in use")
        tenant.name = name
        return self._repo.update(tenant)

    def delete_tenant(self, tenant_id: str) -> None:
        tenant = self._repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        self._repo.delete(tenant_id)
