from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import PlatformGroup
from itsor.domain.ports.base_repository import BaseRepository


class GroupRepository(BaseRepository[PlatformGroup], ABC):
    @abstractmethod
    def get_by_name(self, name: str, tenant_id: str | None = None) -> Optional[PlatformGroup]:
        ...
