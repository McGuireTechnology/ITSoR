from typing import List, Optional

from itsor.domain.ids import generate_ulid
from itsor.domain.models import Namespace
from itsor.domain.ports.entity_record_repository import EntityRecordRepository
from itsor.domain.ports.entity_type_repository import EntityTypeRepository
from itsor.domain.ports.namespace_repository import NamespaceRepository
from itsor.domain.ports.workspace_repository import WorkspaceRepository
from itsor.domain.use_cases.base_use_case import BaseUseCase


class NamespaceUseCases(BaseUseCase):
    def __init__(
        self,
        repo: NamespaceRepository,
        workspace_repo: WorkspaceRepository,
        entity_type_repo: EntityTypeRepository,
        entity_record_repo: EntityRecordRepository,
    ) -> None:
        self._repo = repo
        self._workspace_repo = workspace_repo
        self._entity_type_repo = entity_type_repo
        self._entity_record_repo = entity_record_repo

    def list_namespaces(self, workspace_id: str | None = None) -> List[Namespace]:
        items = self._repo.list()
        if workspace_id is None:
            return items
        return [item for item in items if item.workspace_id == workspace_id]

    def get_namespace(self, namespace_id: str) -> Optional[Namespace]:
        return self._repo.get_by_id(namespace_id)

    def create_namespace(self, name: str, workspace_id: str) -> Namespace:
        workspace = self._workspace_repo.get_by_id(workspace_id)
        if not workspace:
            raise ValueError("Workspace not found")
        existing = self._repo.get_by_name(name, workspace_id)
        if existing:
            raise ValueError("Namespace name already registered")
        namespace = Namespace(id=generate_ulid(), name=name, workspace_id=workspace_id)
        return self._repo.create(namespace)

    def update_namespace(self, namespace_id: str, name: str | None = None) -> Namespace:
        namespace = self._repo.get_by_id(namespace_id)
        if not namespace:
            raise ValueError("Namespace not found")
        if name is not None and name != namespace.name:
            existing = self._repo.get_by_name(name, namespace.workspace_id)
            if existing:
                raise ValueError("Namespace name already in use")
            namespace.name = name
        return self._repo.update(namespace)

    def replace_namespace(self, namespace_id: str, name: str, workspace_id: str) -> Namespace:
        namespace = self._repo.get_by_id(namespace_id)
        if not namespace:
            raise ValueError("Namespace not found")

        workspace = self._workspace_repo.get_by_id(workspace_id)
        if not workspace:
            raise ValueError("Workspace not found")

        if name != namespace.name or workspace_id != namespace.workspace_id:
            existing = self._repo.get_by_name(name, workspace_id)
            if existing and existing.id != namespace.id:
                raise ValueError("Namespace name already in use")

        namespace.name = name
        namespace.workspace_id = workspace_id
        return self._repo.update(namespace)

    def delete_namespace(self, namespace_id: str) -> None:
        namespace = self._repo.get_by_id(namespace_id)
        if not namespace:
            raise ValueError("Namespace not found")

        entity_types = [
            item for item in self._entity_type_repo.list() if item.namespace_id == namespace_id
        ]
        entity_type_ids = {item.id for item in entity_types}
        entity_records = [
            item for item in self._entity_record_repo.list() if item.entity_type_id in entity_type_ids
        ]

        for record in entity_records:
            self._entity_record_repo.delete(record.id)
        for entity_type in entity_types:
            self._entity_type_repo.delete(entity_type.id)
        self._repo.delete(namespace_id)
