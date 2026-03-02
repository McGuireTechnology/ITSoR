from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import CustomNamespace
from itsor.domain.ports.base_repository import BaseRepository


class NamespaceRepository(BaseRepository[CustomNamespace], ABC):
    @abstractmethod
    def get_by_name(self, name: str, workspace_id: str) -> Optional[CustomNamespace]:
        ...
