from sqlalchemy import Column, Integer, String, UniqueConstraint

from itsor.domain.models import DEFAULT_PERMISSIONS
from itsor.infrastructure.models.sqlalchemy_user_model import Base


class NamespaceModel(Base):
    __tablename__ = "namespaces"
    __table_args__ = (
        UniqueConstraint("workspace_id", "name", name="uq_namespaces_workspace_id_name"),
    )

    id = Column(String(36), primary_key=True)
    workspace_id = Column(String(36), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    owner_id = Column(String(36), nullable=True, index=True)
    group_id = Column(String(36), nullable=True, index=True)
    permissions = Column(Integer, nullable=False, default=DEFAULT_PERMISSIONS)
