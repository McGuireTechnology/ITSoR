from sqlalchemy import Column, DateTime, ForeignKey, String, Text

from itsor.infrastructure.persistence_models.sqlalchemy_user_model import Base


class IdmIdentityModel(Base):
    __tablename__ = "idm_identities"

    id = Column(String(36), primary_key=True)
    person_id = Column(String(36), ForeignKey("idm_people.id"), nullable=False, index=True)
    source_system = Column(String(128), nullable=False, index=True)
    source_record_id = Column(String(255), nullable=False, index=True)
    demographic_payload = Column(Text, nullable=False, default="{}")
    valid_from = Column(DateTime, nullable=True, index=True)
    valid_to = Column(DateTime, nullable=True, index=True)
    superseded_at = Column(DateTime, nullable=True, index=True)
