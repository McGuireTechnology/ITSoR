from sqlalchemy import Column, Integer, String, UniqueConstraint

from itsor.domain.models import DEFAULT_PERMISSIONS
from itsor.infrastructure.models.sqlalchemy_user_model import Base


class GroupModel(Base):
    __tablename__ = "groups"
    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_groups_tenant_id_name"),
    )

    id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36), nullable=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    owner_id = Column(String(36), nullable=True, index=True)
    group_id = Column(String(36), nullable=True, index=True)
    permissions = Column(Integer, nullable=False, default=DEFAULT_PERMISSIONS)
