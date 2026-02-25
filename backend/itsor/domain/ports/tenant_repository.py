from abc import ABC, abstractmethod
from typing import Optional, List

from itsor.domain.models.tenant import Tenant


class TenantRepository(ABC):
    @abstractmethod
    def get_by_id(self, tenant_id: str) -> Optional[Tenant]:
        ...

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Tenant]:
        ...

    @abstractmethod
    def list(self) -> List[Tenant]:
        ...

    @abstractmethod
    def create(self, tenant: Tenant) -> Tenant:
        ...

    @abstractmethod
    def update(self, tenant: Tenant) -> Tenant:
        ...

    @abstractmethod
    def delete(self, tenant_id: str) -> None:
        ...
