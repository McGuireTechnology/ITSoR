from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import EntityRecord
from itsor.domain.ports.base_repository import BaseRepository


class EntityRecordRepository(BaseRepository[EntityRecord], ABC):
    @abstractmethod
    def get_by_name(self, name: str, entity_type_id: str) -> Optional[EntityRecord]:
        ...
