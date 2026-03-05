from sqlalchemy import JSON, Column, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from itsor.domain.models import DEFAULT_PERMISSIONS
from itsor.infrastructure.database.sqlalchemy.models.auth import Base


class WorkspaceModel(Base):
	__tablename__ = "workspaces"
	__table_args__ = (
		UniqueConstraint("tenant_id", "name", name="uq_workspaces_tenant_id_name"),
	)

	id = Column(String(36), primary_key=True)
	tenant_id = Column(String(36), nullable=True, index=True)
	name = Column(String(255), nullable=False, index=True)
	owner_id = Column(String(36), nullable=True, index=True)
	group_id = Column(String(36), nullable=True, index=True)
	permissions = Column(Integer, nullable=False, default=DEFAULT_PERMISSIONS)


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


class EntityRecordModel(Base):
	__tablename__ = "entity_records"
	__table_args__ = (
		UniqueConstraint("entity_type_id", "name", name="uq_entity_records_entity_type_id_name"),
	)

	id = Column(String(36), primary_key=True)
	entity_type_id = Column(String(36), nullable=False, index=True)
	name = Column(String(255), nullable=False, default="", index=True)
	values_json = Column(JSON().with_variant(JSONB, "postgresql"), nullable=False, default=dict)
	owner_id = Column(String(36), nullable=True, index=True)
	group_id = Column(String(36), nullable=True, index=True)
	permissions = Column(Integer, nullable=False, default=DEFAULT_PERMISSIONS)


__all__ = [
	"EntityRecordModel",
	"EntityTypeModel",
	"NamespaceModel",
	"WorkspaceModel",
]