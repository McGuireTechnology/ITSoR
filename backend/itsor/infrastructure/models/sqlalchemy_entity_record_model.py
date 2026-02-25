from sqlalchemy import JSON, Column, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from itsor.domain.models import DEFAULT_PERMISSIONS
from itsor.infrastructure.models.sqlalchemy_user_model import Base


class EntityRecordModel(Base):
    __tablename__ = "entity_records"
    __table_args__ = (
        UniqueConstraint("entity_type_id", "name", name="uq_entity_records_entity_type_id_name"),
    )

    id = Column(String(36), primary_key=True)
    entity_type_id = Column(String(36), nullable=False, index=True)
    name = Column(String(255), nullable=False, default="", index=True)
    values_json = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)
    owner_id = Column(String(36), nullable=True, index=True)
    group_id = Column(String(36), nullable=True, index=True)
    permissions = Column(Integer, nullable=False, default=DEFAULT_PERMISSIONS)
