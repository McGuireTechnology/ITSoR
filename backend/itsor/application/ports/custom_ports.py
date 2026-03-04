from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import CustomEntityRecord, CustomEntityType, CustomNamespace, CustomWorkspace
from itsor.application.ports.base_repository import BaseRepository


class WorkspaceRepository(BaseRepository[CustomWorkspace], ABC):
    @abstractmethod
    def get_by_name(self, name: str, tenant_id: str | None = None) -> Optional[CustomWorkspace]:
        ...


class NamespaceRepository(BaseRepository[CustomNamespace], ABC):
    @abstractmethod
    def get_by_name(self, name: str, workspace_id: str) -> Optional[CustomNamespace]:
        ...


class EntityTypeRepository(BaseRepository[CustomEntityType], ABC):
    @abstractmethod
    def get_by_name(self, name: str, namespace_id: str) -> Optional[CustomEntityType]:
        ...


class EntityRecordRepository(BaseRepository[CustomEntityRecord], ABC):
    @abstractmethod
    def get_by_name(self, name: str, entity_type_id: str) -> Optional[CustomEntityRecord]:
        ...


__all__ = [
    "WorkspaceRepository",
    "NamespaceRepository",
    "EntityTypeRepository",
    "EntityRecordRepository",
]