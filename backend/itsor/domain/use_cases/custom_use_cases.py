from typing import Any, List, Optional

from backend.itsor.domain.models.ids import generate_ulid
from itsor.domain.models import CustomEntityRecord, CustomEntityType, CustomNamespace, CustomWorkspace
from itsor.domain.ports.custom_ports import EntityRecordRepository, EntityTypeRepository, NamespaceRepository, WorkspaceRepository
from itsor.domain.use_cases.base_use_case import BaseUseCase


class EntityRecordUseCases(BaseUseCase):
    def __init__(self, repo: EntityRecordRepository, entity_type_repo: EntityTypeRepository) -> None:
        self._repo = repo
        self._entity_type_repo = entity_type_repo

    def list_entity_records(self, entity_type_id: str | None = None) -> List[CustomEntityRecord]:
        items = self._repo.list()
        if entity_type_id is None:
            return items
        return [item for item in items if item.entity_type_id == entity_type_id]

    def search_entity_records(
        self,
        entity_type_id: str | None,
        field: str,
        value: str,
        operator: str = "eq",
    ) -> List[CustomEntityRecord]:
        items = self.list_entity_records(entity_type_id)
        normalized_operator = operator.lower().strip()
        if normalized_operator not in {"eq", "neq", "contains"}:
            raise ValueError("Unsupported operator")

        matched: List[CustomEntityRecord] = []
        for item in items:
            field_value = item.values_json.get(field)
            field_value_text = "" if field_value is None else str(field_value)

            if normalized_operator == "eq" and field_value_text == value:
                matched.append(item)
                continue

            if normalized_operator == "neq" and field_value_text != value:
                matched.append(item)
                continue

            if normalized_operator == "contains":
                if isinstance(field_value, list):
                    if any(str(entry) == value for entry in field_value):
                        matched.append(item)
                    continue
                if value in field_value_text:
                    matched.append(item)

        return matched

    def get_entity_record(self, entity_record_id: str) -> Optional[CustomEntityRecord]:
        return self._repo.get_by_id(entity_record_id)

    def create_entity_record(
        self,
        entity_type_id: str,
        values_json: dict[str, Any],
        name: str = "",
        creator_user_id: str | None = None,
    ) -> CustomEntityRecord:
        entity_type = self._entity_type_repo.get_by_id(entity_type_id)
        if not entity_type:
            raise ValueError("Entity type not found")
        if name:
            existing = self._repo.get_by_name(name, entity_type_id)
            if existing:
                raise ValueError("Entity record name already in use")
        entity_record = CustomEntityRecord(
            id=str(ulid.new()),
            name=name,
            entity_type_id=entity_type_id,
            values_json=values_json,
            owner_id=creator_user_id,
        )
        return self._repo.create(entity_record)

    def update_entity_record(
        self,
        entity_record_id: str,
        name: str | None = None,
        values_json: dict[str, Any] | None = None,
    ) -> CustomEntityRecord:
        entity_record = self._repo.get_by_id(entity_record_id)
        if not entity_record:
            raise ValueError("Entity record not found")
        if name is not None and name != entity_record.name:
            if name:
                existing = self._repo.get_by_name(name, entity_record.entity_type_id)
                if existing:
                    raise ValueError("Entity record name already in use")
            entity_record.name = name
        if values_json is not None:
            entity_record.values_json = values_json
        return self._repo.update(entity_record)

    def replace_entity_record(
        self,
        entity_record_id: str,
        entity_type_id: str,
        values_json: dict[str, Any],
        name: str = "",
    ) -> CustomEntityRecord:
        entity_record = self._repo.get_by_id(entity_record_id)
        if not entity_record:
            raise ValueError("Entity record not found")

        entity_type = self._entity_type_repo.get_by_id(entity_type_id)
        if not entity_type:
            raise ValueError("Entity type not found")

        if name:
            existing = self._repo.get_by_name(name, entity_type_id)
            if existing and existing.id != entity_record.id:
                raise ValueError("Entity record name already in use")

        entity_record.name = name
        entity_record.entity_type_id = entity_type_id
        entity_record.values_json = values_json
        return self._repo.update(entity_record)

    def delete_entity_record(self, entity_record_id: str) -> None:
        entity_record = self._repo.get_by_id(entity_record_id)
        if not entity_record:
            raise ValueError("Entity record not found")
        self._repo.delete(entity_record_id)


class EntityTypeUseCases(BaseUseCase):
    def __init__(
        self,
        repo: EntityTypeRepository,
        namespace_repo: NamespaceRepository,
        entity_record_repo: EntityRecordRepository,
    ) -> None:
        self._repo = repo
        self._namespace_repo = namespace_repo
        self._entity_record_repo = entity_record_repo

    def list_entity_types(self, namespace_id: str | None = None) -> List[CustomEntityType]:
        items = self._repo.list()
        if namespace_id is None:
            return items
        return [item for item in items if item.namespace_id == namespace_id]

    def get_entity_type(self, entity_type_id: str) -> Optional[CustomEntityType]:
        return self._repo.get_by_id(entity_type_id)

    def create_entity_type(
        self,
        name: str,
        namespace_id: str,
        attributes_json: dict[str, Any] | None = None,
        creator_user_id: str | None = None,
    ) -> CustomEntityType:
        namespace = self._namespace_repo.get_by_id(namespace_id)
        if not namespace:
            raise ValueError("Namespace not found")
        existing = self._repo.get_by_name(name, namespace_id)
        if existing:
            raise ValueError("Entity type name already registered")
        entity_type = CustomEntityType(
            id=str(ulid.new()),
            name=name,
            namespace_id=namespace_id,
            attributes_json=attributes_json or {},
            owner_id=creator_user_id,
        )
        return self._repo.create(entity_type)

    def update_entity_type(
        self,
        entity_type_id: str,
        name: str | None = None,
        attributes_json: dict[str, Any] | None = None,
    ) -> CustomEntityType:
        entity_type = self._repo.get_by_id(entity_type_id)
        if not entity_type:
            raise ValueError("Entity type not found")
        if name is not None and name != entity_type.name:
            existing = self._repo.get_by_name(name, entity_type.namespace_id)
            if existing:
                raise ValueError("Entity type name already in use")
            entity_type.name = name
        if attributes_json is not None:
            entity_type.attributes_json = attributes_json
        return self._repo.update(entity_type)

    def replace_entity_type(
        self,
        entity_type_id: str,
        name: str,
        namespace_id: str,
        attributes_json: dict[str, Any] | None = None,
    ) -> CustomEntityType:
        entity_type = self._repo.get_by_id(entity_type_id)
        if not entity_type:
            raise ValueError("Entity type not found")

        namespace = self._namespace_repo.get_by_id(namespace_id)
        if not namespace:
            raise ValueError("Namespace not found")

        if name != entity_type.name or namespace_id != entity_type.namespace_id:
            existing = self._repo.get_by_name(name, namespace_id)
            if existing and existing.id != entity_type.id:
                raise ValueError("Entity type name already in use")

        entity_type.name = name
        entity_type.namespace_id = namespace_id
        entity_type.attributes_json = attributes_json or {}
        return self._repo.update(entity_type)

    def delete_entity_type(self, entity_type_id: str) -> None:
        entity_type = self._repo.get_by_id(entity_type_id)
        if not entity_type:
            raise ValueError("Entity type not found")

        entity_records = [
            item for item in self._entity_record_repo.list() if item.entity_type_id == entity_type_id
        ]
        for record in entity_records:
            self._entity_record_repo.delete(record.id)
        self._repo.delete(entity_type_id)


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

    def list_namespaces(self, workspace_id: str | None = None) -> List[CustomNamespace]:
        items = self._repo.list()
        if workspace_id is None:
            return items
        return [item for item in items if item.workspace_id == workspace_id]

    def get_namespace(self, namespace_id: str) -> Optional[CustomNamespace]:
        return self._repo.get_by_id(namespace_id)

    def create_namespace(self, name: str, workspace_id: str, creator_user_id: str | None = None) -> CustomNamespace:
        workspace = self._workspace_repo.get_by_id(workspace_id)
        if not workspace:
            raise ValueError("Workspace not found")
        existing = self._repo.get_by_name(name, workspace_id)
        if existing:
            raise ValueError("Namespace name already registered")
        namespace = CustomNamespace(id=str(ulid.new()), name=name, workspace_id=workspace_id, owner_id=creator_user_id)
        return self._repo.create(namespace)

    def update_namespace(self, namespace_id: str, name: str | None = None) -> CustomNamespace:
        namespace = self._repo.get_by_id(namespace_id)
        if not namespace:
            raise ValueError("Namespace not found")
        if name is not None and name != namespace.name:
            existing = self._repo.get_by_name(name, namespace.workspace_id)
            if existing:
                raise ValueError("Namespace name already in use")
            namespace.name = name
        return self._repo.update(namespace)

    def replace_namespace(self, namespace_id: str, name: str, workspace_id: str) -> CustomNamespace:
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

    def list_workspaces(self, tenant_id: str | None = None) -> List[CustomWorkspace]:
        items = self._repo.list()
        if tenant_id is None:
            return items
        return [item for item in items if item.tenant_id == tenant_id]

    def get_workspace(self, workspace_id: str) -> Optional[CustomWorkspace]:
        return self._repo.get_by_id(workspace_id)

    def create_workspace(self, name: str, tenant_id: str | None = None, creator_user_id: str | None = None) -> CustomWorkspace:
        existing = self._repo.get_by_name(name, tenant_id)
        if existing:
            raise ValueError("Workspace name already registered")
        workspace = CustomWorkspace(id=str(ulid.new()), name=name, tenant_id=tenant_id, owner_id=creator_user_id)
        return self._repo.create(workspace)

    def update_workspace(self, workspace_id: str, name: str | None = None) -> CustomWorkspace:
        workspace = self._repo.get_by_id(workspace_id)
        if not workspace:
            raise ValueError("Workspace not found")
        if name is not None and name != workspace.name:
            existing = self._repo.get_by_name(name, workspace.tenant_id)
            if existing:
                raise ValueError("Workspace name already in use")
            workspace.name = name
        return self._repo.update(workspace)

    def replace_workspace(self, workspace_id: str, name: str, tenant_id: str | None = None) -> CustomWorkspace:
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


__all__ = [
    "EntityRecordUseCases",
    "EntityTypeUseCases",
    "NamespaceUseCases",
    "WorkspaceUseCases",
]