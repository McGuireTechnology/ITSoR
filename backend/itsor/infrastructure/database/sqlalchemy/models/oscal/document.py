import ulid
from sqlalchemy import JSON, Column, String
from sqlalchemy.dialects.postgresql import JSONB

from itsor.infrastructure.database.sqlalchemy.models.auth import Base


class OscalDocumentModel(Base):
    __tablename__ = "oscal_documents"

    id = Column(String(36), primary_key=True, default=lambda: str(ulid.new()))
    document_type = Column(String(64), nullable=False, index=True)
    title = Column(String(255), nullable=True)
    content_json = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)


__all__ = ["OscalDocumentModel"]
