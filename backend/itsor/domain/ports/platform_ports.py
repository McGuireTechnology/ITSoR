from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import PlatformGroup, PlatformTenant, PlatformUser
from itsor.domain.ports.base_repository import BaseRepository


class GroupRepository(BaseRepository[PlatformGroup], ABC):
    @abstractmethod
    def get_by_name(self, name: str, tenant_id: str | None = None) -> Optional[PlatformGroup]:
        ...


class TenantRepository(BaseRepository[PlatformTenant], ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[PlatformTenant]:
        ...


class UserRepository(BaseRepository[PlatformUser], ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[PlatformUser]:
        ...

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[PlatformUser]:
        ...


__all__ = [
    "GroupRepository",
    "TenantRepository",
    "UserRepository",
]