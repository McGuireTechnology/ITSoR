import os

from fastapi import Depends

from itsor.domain.ports.user_repository import UserRepository
from itsor.infrastructure.adapters.in_memory_user_repository import InMemoryUserRepository
from itsor.infrastructure.adapters.user_repository import SQLAlchemyUserRepository
from itsor.infrastructure.container.database import get_db


BACKEND = os.getenv("USER_REPOSITORY_BACKEND", "sqlalchemy").lower()


if BACKEND == "memory":
    _MEMORY_REPOSITORY = InMemoryUserRepository()


def _unsupported_backend() -> RuntimeError:
    return RuntimeError(f"Unsupported USER_REPOSITORY_BACKEND: {BACKEND}")


if BACKEND == "sqlalchemy":
    def get_user_repository(db=Depends(get_db)) -> UserRepository:
        return SQLAlchemyUserRepository(db)
elif BACKEND == "memory":
    def get_user_repository() -> UserRepository:
        return _MEMORY_REPOSITORY
else:
    def get_user_repository() -> UserRepository:
        raise _unsupported_backend()