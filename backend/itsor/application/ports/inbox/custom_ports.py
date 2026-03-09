from abc import ABC, abstractmethod
from typing import Any, Optional

from itsor.application.ports.inbox.base_repository import BaseRepository


class WorkspaceRepository(BaseRepository[Any], ABC):
    @abstractmethod
    def get_by_name(self, name: str, tenant_id: str | None = None) -> Optional[Any]:
        ...


class NamespaceRepository(BaseRepository[Any], ABC):
    @abstractmethod
    def get_by_name(self, name: str, workspace_id: str) -> Optional[Any]:
        ...


class EntityTypeRepository(BaseRepository[Any], ABC):
    @abstractmethod
    def get_by_name(self, name: str, namespace_id: str) -> Optional[Any]:
        ...


class EntityRecordRepository(BaseRepository[Any], ABC):
    @abstractmethod
    def get_by_name(self, name: str, entity_type_id: str) -> Optional[Any]:
        ...


__all__ = [
    "WorkspaceRepository",
    "NamespaceRepository",
    "EntityTypeRepository",
    "EntityRecordRepository",
]
