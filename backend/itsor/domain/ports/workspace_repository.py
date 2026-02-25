from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import Workspace
from itsor.domain.ports.base_repository import BaseRepository


class WorkspaceRepository(BaseRepository[Workspace], ABC):
    @abstractmethod
    def get_by_name(self, name: str, tenant_id: str | None = None) -> Optional[Workspace]:
        ...
