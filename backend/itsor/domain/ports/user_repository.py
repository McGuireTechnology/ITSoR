from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional, List

from itsor.domain.models.user import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        ...

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        ...

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        ...

    @abstractmethod
    def list(self) -> List[User]:
        ...

    @abstractmethod
    def create(self, user: User) -> User:
        ...

    @abstractmethod
    def update(self, user: User) -> User:
        ...

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        ...
