from itsor.domain.models import PlatformUser
from itsor.domain.ports.platform_ports import UserRepository
from itsor.infrastructure.adapters.in_memory_base_repository import InMemoryBaseRepository


class InMemoryUserRepository(InMemoryBaseRepository[PlatformUser], UserRepository):
    def __init__(self) -> None:
        super().__init__("User")

    def get_by_email(self, email: str) -> PlatformUser | None:
        for user in self._items.values():
            if user.email == email:
                return user
        return None

    def get_by_username(self, username: str) -> PlatformUser | None:
        for user in self._items.values():
            if user.username == username:
                return user
        return None
