from sqlalchemy.orm import Session

from itsor.domain.models import Namespace
from itsor.domain.ports.namespace_repository import NamespaceRepository
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.models.sqlalchemy_namespace_model import NamespaceModel


class SQLAlchemyNamespaceRepository(SQLAlchemyBaseRepository[Namespace, NamespaceModel], NamespaceRepository):
    model_class = NamespaceModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "Namespace")

    def _to_domain(self, record: NamespaceModel) -> Namespace:
        return Namespace(
            id=record.id,
            workspace_id=record.workspace_id,
            name=record.name,
            owner_id=record.owner_id,
            group_id=record.group_id,
            permissions=record.permissions,
        )

    def _to_model(self, namespace: Namespace) -> NamespaceModel:
        return NamespaceModel(
            id=namespace.id,
            workspace_id=namespace.workspace_id,
            name=namespace.name,
            owner_id=namespace.owner_id,
            group_id=namespace.group_id,
            permissions=namespace.permissions,
        )

    def _apply_updates(self, record: NamespaceModel, entity: Namespace) -> None:
        record.name = entity.name
        record.workspace_id = entity.workspace_id
        record.owner_id = entity.owner_id
        record.group_id = entity.group_id
        record.permissions = entity.permissions

    def get_by_name(self, name: str, workspace_id: str) -> Namespace | None:
        record = (
            self._db.query(NamespaceModel)
            .filter(NamespaceModel.name == name, NamespaceModel.workspace_id == workspace_id)
            .first()
        )
        return self._to_domain(record) if record else None
