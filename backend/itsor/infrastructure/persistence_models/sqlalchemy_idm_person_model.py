from sqlalchemy import Column, String

from itsor.infrastructure.persistence_models.sqlalchemy_user_model import Base


class IdmPersonModel(Base):
    __tablename__ = "idm_people"

    id = Column(String(36), primary_key=True)
    display_name = Column(String(255), nullable=False, default="")
    current_identity_id = Column(String(36), nullable=True, index=True)
