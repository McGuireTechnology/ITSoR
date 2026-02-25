from sqlalchemy import Column, String

from itsor.infrastructure.models.user import Base


class TenantModel(Base):
    __tablename__ = "tenants"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), unique=True, nullable=False, index=True)
