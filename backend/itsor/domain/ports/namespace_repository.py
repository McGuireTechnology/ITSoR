from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import Namespace
from itsor.domain.ports.base_repository import BaseRepository


class NamespaceRepository(BaseRepository[Namespace], ABC):
    @abstractmethod
    def get_by_name(self, name: str, workspace_id: str) -> Optional[Namespace]:
        ...
