from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import PlatformTenant
from itsor.domain.ports.base_repository import BaseRepository


class TenantRepository(BaseRepository[PlatformTenant], ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[PlatformTenant]:
        ...
