from sqlalchemy import JSON, Column, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from itsor.domain.models import DEFAULT_PERMISSIONS
from itsor.infrastructure.models.sqlalchemy_user_model import Base


class EntityTypeModel(Base):
    __tablename__ = "entity_types"
    __table_args__ = (
        UniqueConstraint("namespace_id", "name", name="uq_entity_types_namespace_id_name"),
    )

    id = Column(String(36), primary_key=True)
    namespace_id = Column(String(36), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    attributes_json = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)
    owner_id = Column(String(36), nullable=True, index=True)
    group_id = Column(String(36), nullable=True, index=True)
    permissions = Column(Integer, nullable=False, default=DEFAULT_PERMISSIONS)
