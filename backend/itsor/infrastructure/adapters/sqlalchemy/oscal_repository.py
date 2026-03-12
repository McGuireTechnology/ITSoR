from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from itsor.application.ports.oscal import OscalDocumentRepository
from itsor.infrastructure.adapters.in_memory_base_repository import InMemoryBaseRepository
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.database.sqlalchemy.models.oscal import OscalDocumentModel


@dataclass
class OscalDocumentRecord:
    id: str
    document_type: str
    content_json: dict[str, Any]
    title: str | None = None


class SQLAlchemyOscalDocumentRepository(
    SQLAlchemyBaseRepository[Any, OscalDocumentModel],
    OscalDocumentRepository,
):
    model_class = OscalDocumentModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "OSCAL document")

    def _to_domain(self, record: OscalDocumentModel) -> Any:
        return OscalDocumentRecord(
            id=str(record.id),
            document_type=str(record.document_type),
            title=getattr(record, "title", None),
            content_json=dict(getattr(record, "content_json", {}) or {}),
        )

    def _to_model(self, entity: Any) -> OscalDocumentModel:
        return OscalDocumentModel(
            id=str(entity.id),
            document_type=str(entity.document_type),
            title=getattr(entity, "title", None),
            content_json=dict(getattr(entity, "content_json", {}) or {}),
        )

    def _apply_updates(self, record: OscalDocumentModel, entity: Any) -> None:
        record.document_type = str(entity.document_type)
        record.title = getattr(entity, "title", None)
        record.content_json = dict(getattr(entity, "content_json", {}) or {})

    def list_by_document_type(self, document_type: str) -> list[Any]:
        rows = self._db.query(OscalDocumentModel).filter(OscalDocumentModel.document_type == document_type).all()
        return [self._to_domain(row) for row in rows]


class InMemoryOscalDocumentRepository(InMemoryBaseRepository[Any], OscalDocumentRepository):
    def __init__(self) -> None:
        super().__init__("OSCAL document")

    def list_by_document_type(self, document_type: str) -> list[Any]:
        return [item for item in self._items.values() if getattr(item, "document_type", None) == document_type]


__all__ = ["SQLAlchemyOscalDocumentRepository", "InMemoryOscalDocumentRepository"]
