from sqlalchemy import Column, Integer, String

from itsor.domain.models import DEFAULT_PERMISSIONS
from itsor.infrastructure.models.sqlalchemy_user_model import Base


class TenantModel(Base):
    __tablename__ = "tenants"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
    owner_id = Column(String(36), nullable=True, index=True)
    group_id = Column(String(36), nullable=True, index=True)
    permissions = Column(Integer, nullable=False, default=DEFAULT_PERMISSIONS)
