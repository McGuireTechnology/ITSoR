from sqlalchemy import Column, String

from itsor.infrastructure.persistence_models.sqlalchemy_user_model import Base


class IdmGroupModel(Base):
    __tablename__ = "idm_groups"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(String(255), nullable=False, default="")
