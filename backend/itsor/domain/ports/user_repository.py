from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.models import User
from itsor.domain.ports.base_repository import BaseRepository


class UserRepository(BaseRepository[User], ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        ...
