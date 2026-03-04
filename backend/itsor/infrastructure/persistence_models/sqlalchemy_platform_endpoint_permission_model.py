from sqlalchemy import Column, Integer, String, UniqueConstraint

from itsor.infrastructure.persistence_models.sqlalchemy_user_model import Base


class PlatformEndpointPermissionModel(Base):
    __tablename__ = "platform_endpoint_permissions"
    __table_args__ = (
        UniqueConstraint(
            "principal_type",
            "principal_id",
            "endpoint_name",
            "action",
            name="uq_platform_endpoint_permissions_principal_endpoint_action",
        ),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    principal_type = Column(String(16), nullable=False, index=True)
    principal_id = Column(String(36), nullable=False, index=True)
    endpoint_name = Column(String(128), nullable=False, index=True)
    action = Column(String(16), nullable=False)
