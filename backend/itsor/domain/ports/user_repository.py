from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import PlatformUser
from itsor.domain.ports.base_repository import BaseRepository


class UserRepository(BaseRepository[PlatformUser], ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[PlatformUser]:
        ...

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[PlatformUser]:
        ...
