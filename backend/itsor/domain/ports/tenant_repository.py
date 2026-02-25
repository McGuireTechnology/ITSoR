from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import Tenant
from itsor.domain.ports.base_repository import BaseRepository


class TenantRepository(BaseRepository[Tenant], ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Tenant]:
        ...
