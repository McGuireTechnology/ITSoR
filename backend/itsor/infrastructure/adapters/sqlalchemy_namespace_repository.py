from sqlalchemy.orm import Session
from typing import Any

from itsor.application.ports.custom_ports import NamespaceRepository
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.persistence_models.sqlalchemy_namespace_model import NamespaceModel


class SQLAlchemyNamespaceRepository(SQLAlchemyBaseRepository[Any, NamespaceModel], NamespaceRepository):
    model_class = NamespaceModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Namespace")

    def _to_domain(self, record: NamespaceModel) -> Any:
        return record

    def _to_model(self, namespace: Any) -> NamespaceModel:
        return NamespaceModel(
            id=namespace.id,
            workspace_id=namespace.workspace_id,
            name=namespace.name,
            owner_id=namespace.owner_id,
            group_id=namespace.group_id,
            permissions=namespace.permissions,
        )

    def _apply_updates(self, record: NamespaceModel, entity: Any) -> None:
        record.name = entity.name
        record.workspace_id = entity.workspace_id
        record.owner_id = entity.owner_id
        record.group_id = entity.group_id
        record.permissions = entity.permissions

    def get_by_name(self, name: str, workspace_id: str) -> Any | None:
        record = (
            self._db.query(NamespaceModel)
            .filter(NamespaceModel.name == name, NamespaceModel.workspace_id == workspace_id)
            .first()
        )
        return self._to_domain(record) if record else None
