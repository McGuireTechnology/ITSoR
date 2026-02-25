from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import EntityType
from itsor.domain.ports.base_repository import BaseRepository


class EntityTypeRepository(BaseRepository[EntityType], ABC):
    @abstractmethod
    def get_by_name(self, name: str, namespace_id: str) -> Optional[EntityType]:
        ...
