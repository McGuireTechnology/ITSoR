from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import Group, Tenant, User
from itsor.domain.ports.base_repository import BaseRepository


class GroupRepository(BaseRepository[Group], ABC):
    @abstractmethod
    def get_by_name(self, name: str, tenant_id: str | None = None) -> Optional[Group]:
        ...


class TenantRepository(BaseRepository[Tenant], ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Tenant]:
        ...


class UserRepository(BaseRepository[User], ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        ...


__all__ = [
    "GroupRepository",
    "TenantRepository",
    "UserRepository",
]