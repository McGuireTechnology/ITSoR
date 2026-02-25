from typing import List, Optional

from itsor.domain.models.user import User
from itsor.domain.ports.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    def __init__(self) -> None:
        self._users: dict[str, User] = {}

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self._users.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def get_by_username(self, username: str) -> Optional[User]:
        for user in self._users.values():
            if user.username == username:
                return user
        return None

    def list(self) -> List[User]:
        return list(self._users.values())

    def create(self, user: User) -> User:
        self._users[user.id] = user
        return user

    def update(self, user: User) -> User:
        if user.id not in self._users:
            raise ValueError(f"User {user.id} not found")
        self._users[user.id] = user
        return user

    def delete(self, user_id: str) -> None:
        self._users.pop(user_id, None)
