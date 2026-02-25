from typing import List, Optional

from itsor.domain.ids import generate_ulid
from itsor.domain.models import Workspace
from itsor.domain.ports.entity_record_repository import EntityRecordRepository
from itsor.domain.ports.entity_type_repository import EntityTypeRepository
from itsor.domain.ports.namespace_repository import NamespaceRepository
from itsor.domain.ports.workspace_repository import WorkspaceRepository
from itsor.domain.use_cases.base_use_case import BaseUseCase


class WorkspaceUseCases(BaseUseCase):
    def __init__(
        self,
        repo: WorkspaceRepository,
        namespace_repo: NamespaceRepository,
        entity_type_repo: EntityTypeRepository,
        entity_record_repo: EntityRecordRepository,
    ) -> None:
        self._repo = repo
        self._namespace_repo = namespace_repo
        self._entity_type_repo = entity_type_repo
        self._entity_record_repo = entity_record_repo

    def list_workspaces(self, tenant_id: str | None = None) -> List[Workspace]:
        items = self._repo.list()
        if tenant_id is None:
            return items
        return [item for item in items if item.tenant_id == tenant_id]

    def get_workspace(self, workspace_id: str) -> Optional[Workspace]:
        return self._repo.get_by_id(workspace_id)

    def create_workspace(self, name: str, tenant_id: str | None = None) -> Workspace:
        existing = self._repo.get_by_name(name, tenant_id)
        if existing:
            raise ValueError("Workspace name already registered")
        workspace = Workspace(id=generate_ulid(), name=name, tenant_id=tenant_id)
        return self._repo.create(workspace)

    def update_workspace(self, workspace_id: str, name: str | None = None) -> Workspace:
        workspace = self._repo.get_by_id(workspace_id)
        if not workspace:
            raise ValueError("Workspace not found")
        if name is not None and name != workspace.name:
            existing = self._repo.get_by_name(name, workspace.tenant_id)
            if existing:
                raise ValueError("Workspace name already in use")
            workspace.name = name
        return self._repo.update(workspace)

    def replace_workspace(self, workspace_id: str, name: str, tenant_id: str | None = None) -> Workspace:
        workspace = self._repo.get_by_id(workspace_id)
        if not workspace:
            raise ValueError("Workspace not found")

        if name != workspace.name or tenant_id != workspace.tenant_id:
            existing = self._repo.get_by_name(name, tenant_id)
            if existing and existing.id != workspace.id:
                raise ValueError("Workspace name already in use")

        workspace.name = name
        workspace.tenant_id = tenant_id
        return self._repo.update(workspace)

    def delete_workspace(self, workspace_id: str) -> None:
        workspace = self._repo.get_by_id(workspace_id)
        if not workspace:
            raise ValueError("Workspace not found")

        namespaces = [item for item in self._namespace_repo.list() if item.workspace_id == workspace_id]
        namespace_ids = {item.id for item in namespaces}
        entity_types = [
            item for item in self._entity_type_repo.list() if item.namespace_id in namespace_ids
        ]
        entity_type_ids = {item.id for item in entity_types}
        entity_records = [
            item for item in self._entity_record_repo.list() if item.entity_type_id in entity_type_ids
        ]

        for record in entity_records:
            self._entity_record_repo.delete(record.id)
        for entity_type in entity_types:
            self._entity_type_repo.delete(entity_type.id)
        for namespace in namespaces:
            self._namespace_repo.delete(namespace.id)
        self._repo.delete(workspace_id)
