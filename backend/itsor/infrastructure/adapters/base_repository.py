from abc import ABC
from typing import Generic, TypeVar

from itsor.domain.ports.base_repository import BaseRepository as DomainBaseRepository


TEntity = TypeVar("TEntity")


class BaseRepository(DomainBaseRepository[TEntity], ABC, Generic[TEntity]):
    def __init__(self, entity_label: str) -> None:
        self._entity_label = entity_label

    def _not_found_message(self, entity_id: str) -> str:
        return f"{self._entity_label} {entity_id} not found"
