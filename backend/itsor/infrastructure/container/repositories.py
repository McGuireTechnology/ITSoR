import os

from fastapi import Depends

from itsor.domain.ports.entity_record_repository import EntityRecordRepository
from itsor.domain.ports.entity_type_repository import EntityTypeRepository
from itsor.domain.ports.group_repository import GroupRepository
from itsor.domain.ports.namespace_repository import NamespaceRepository
from itsor.domain.ports.tenant_repository import TenantRepository
from itsor.domain.ports.user_repository import UserRepository
from itsor.domain.ports.workspace_repository import WorkspaceRepository
from itsor.infrastructure.adapters.sqlalchemy_entity_record_repository import SQLAlchemyEntityRecordRepository
from itsor.infrastructure.adapters.sqlalchemy_entity_type_repository import SQLAlchemyEntityTypeRepository
from itsor.infrastructure.adapters.sqlalchemy_group_repository import SQLAlchemyGroupRepository
from itsor.infrastructure.adapters.sqlalchemy_namespace_repository import SQLAlchemyNamespaceRepository
from itsor.infrastructure.adapters.sqlalchemy_workspace_repository import SQLAlchemyWorkspaceRepository
from itsor.infrastructure.adapters.in_memory_entity_record_repository import InMemoryEntityRecordRepository
from itsor.infrastructure.adapters.in_memory_entity_type_repository import InMemoryEntityTypeRepository
from itsor.infrastructure.adapters.in_memory_group_repository import InMemoryGroupRepository
from itsor.infrastructure.adapters.in_memory_namespace_repository import InMemoryNamespaceRepository
from itsor.infrastructure.adapters.in_memory_tenant_repository import InMemoryTenantRepository
from itsor.infrastructure.adapters.in_memory_user_repository import InMemoryUserRepository
from itsor.infrastructure.adapters.in_memory_workspace_repository import InMemoryWorkspaceRepository
from itsor.infrastructure.adapters.sqlalchemy_tenant_repository import SQLAlchemyTenantRepository
from itsor.infrastructure.adapters.sqlalchemy_user_repository import SQLAlchemyUserRepository
from itsor.infrastructure.container.database import get_db


BACKEND = os.getenv("USER_REPOSITORY_BACKEND", "sqlalchemy").lower()


if BACKEND == "memory":
    _MEMORY_REPOSITORY = InMemoryUserRepository()
    _MEMORY_TENANT_REPOSITORY = InMemoryTenantRepository()
    _MEMORY_GROUP_REPOSITORY = InMemoryGroupRepository()
    _MEMORY_WORKSPACE_REPOSITORY = InMemoryWorkspaceRepository()
    _MEMORY_NAMESPACE_REPOSITORY = InMemoryNamespaceRepository()
    _MEMORY_ENTITY_TYPE_REPOSITORY = InMemoryEntityTypeRepository()
    _MEMORY_ENTITY_RECORD_REPOSITORY = InMemoryEntityRecordRepository()


def _unsupported_backend() -> RuntimeError:
    return RuntimeError(f"Unsupported USER_REPOSITORY_BACKEND: {BACKEND}")


if BACKEND == "sqlalchemy":
    def get_user_repository(db=Depends(get_db)) -> UserRepository:
        return SQLAlchemyUserRepository(db)

    def get_tenant_repository(db=Depends(get_db)) -> TenantRepository:
        return SQLAlchemyTenantRepository(db)

    def get_group_repository(db=Depends(get_db)) -> GroupRepository:
        return SQLAlchemyGroupRepository(db)

    def get_workspace_repository(db=Depends(get_db)) -> WorkspaceRepository:
        return SQLAlchemyWorkspaceRepository(db)

    def get_namespace_repository(db=Depends(get_db)) -> NamespaceRepository:
        return SQLAlchemyNamespaceRepository(db)

    def get_entity_type_repository(db=Depends(get_db)) -> EntityTypeRepository:
        return SQLAlchemyEntityTypeRepository(db)

    def get_entity_record_repository(db=Depends(get_db)) -> EntityRecordRepository:
        return SQLAlchemyEntityRecordRepository(db)
elif BACKEND == "memory":
    def get_user_repository() -> UserRepository:
        return _MEMORY_REPOSITORY

    def get_tenant_repository() -> TenantRepository:
        return _MEMORY_TENANT_REPOSITORY

    def get_group_repository() -> GroupRepository:
        return _MEMORY_GROUP_REPOSITORY

    def get_workspace_repository() -> WorkspaceRepository:
        return _MEMORY_WORKSPACE_REPOSITORY

    def get_namespace_repository() -> NamespaceRepository:
        return _MEMORY_NAMESPACE_REPOSITORY

    def get_entity_type_repository() -> EntityTypeRepository:
        return _MEMORY_ENTITY_TYPE_REPOSITORY

    def get_entity_record_repository() -> EntityRecordRepository:
        return _MEMORY_ENTITY_RECORD_REPOSITORY
else:
    def get_user_repository() -> UserRepository:
        raise _unsupported_backend()

    def get_tenant_repository() -> TenantRepository:
        raise _unsupported_backend()

    def get_group_repository() -> GroupRepository:
        raise _unsupported_backend()

    def get_workspace_repository() -> WorkspaceRepository:
        raise _unsupported_backend()

    def get_namespace_repository() -> NamespaceRepository:
        raise _unsupported_backend()

    def get_entity_type_repository() -> EntityTypeRepository:
        raise _unsupported_backend()

    def get_entity_record_repository() -> EntityRecordRepository:
        raise _unsupported_backend()
