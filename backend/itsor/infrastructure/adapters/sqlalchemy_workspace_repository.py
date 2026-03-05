from sqlalchemy.orm import Session
from typing import Any

from itsor.application.ports.custom_ports import WorkspaceRepository
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.database.sqlalchemy.models.custom import WorkspaceModel


class SQLAlchemyWorkspaceRepository(SQLAlchemyBaseRepository[Any, WorkspaceModel], WorkspaceRepository):
    model_class = WorkspaceModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Workspace")

    def _to_domain(self, record: WorkspaceModel) -> Any:
        return record

    def _to_model(self, workspace: Any) -> WorkspaceModel:
        return WorkspaceModel(
            id=workspace.id,
            tenant_id=workspace.tenant_id,
            name=workspace.name,
            owner_id=workspace.owner_id,
            group_id=workspace.group_id,
            permissions=workspace.permissions,
        )

    def _apply_updates(self, record: WorkspaceModel, entity: Any) -> None:
        record.name = entity.name
        record.tenant_id = entity.tenant_id
        record.owner_id = entity.owner_id
        record.group_id = entity.group_id
        record.permissions = entity.permissions

    def get_by_name(self, name: str, tenant_id: str | None = None) -> Any | None:
        record = (
            self._db.query(WorkspaceModel)
            .filter(WorkspaceModel.name == name, WorkspaceModel.tenant_id == tenant_id)
            .first()
        )
        return self._to_domain(record) if record else None
