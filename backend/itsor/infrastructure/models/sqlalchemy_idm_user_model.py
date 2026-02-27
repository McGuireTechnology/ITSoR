from sqlalchemy import Column, ForeignKey, String

from itsor.infrastructure.models.sqlalchemy_user_model import Base


class IdmUserModel(Base):
    __tablename__ = "idm_users"

    id = Column(String(36), primary_key=True)
    person_id = Column(String(36), ForeignKey("idm_people.id"), nullable=False, index=True)
    username = Column(String(255), nullable=False, index=True)
    account_status = Column(String(64), nullable=False, default="active")
