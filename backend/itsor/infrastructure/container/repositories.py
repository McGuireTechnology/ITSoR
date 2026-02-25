import os

from fastapi import Depends

from itsor.domain.ports.tenant_repository import TenantRepository
from itsor.domain.ports.user_repository import UserRepository
from itsor.infrastructure.adapters.in_memory_tenant_repository import InMemoryTenantRepository
from itsor.infrastructure.adapters.in_memory_user_repository import InMemoryUserRepository
from itsor.infrastructure.adapters.tenant_repository import SQLAlchemyTenantRepository
from itsor.infrastructure.adapters.user_repository import SQLAlchemyUserRepository
from itsor.infrastructure.container.database import get_db


BACKEND = os.getenv("USER_REPOSITORY_BACKEND", "sqlalchemy").lower()


if BACKEND == "memory":
    _MEMORY_REPOSITORY = InMemoryUserRepository()
    _MEMORY_TENANT_REPOSITORY = InMemoryTenantRepository()


def _unsupported_backend() -> RuntimeError:
    return RuntimeError(f"Unsupported USER_REPOSITORY_BACKEND: {BACKEND}")


if BACKEND == "sqlalchemy":
    def get_user_repository(db=Depends(get_db)) -> UserRepository:
        return SQLAlchemyUserRepository(db)

    def get_tenant_repository(db=Depends(get_db)) -> TenantRepository:
        return SQLAlchemyTenantRepository(db)
elif BACKEND == "memory":
    def get_user_repository() -> UserRepository:
        return _MEMORY_REPOSITORY

    def get_tenant_repository() -> TenantRepository:
        return _MEMORY_TENANT_REPOSITORY
else:
    def get_user_repository() -> UserRepository:
        raise _unsupported_backend()

    def get_tenant_repository() -> TenantRepository:
        raise _unsupported_backend()
