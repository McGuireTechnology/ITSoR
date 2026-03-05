import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt

from itsor.application.ports.auth.repositories import (
    GroupRepository,
    PasswordHasher,
    TenantRepository,
    TokenCodec,
    UserRepository,
)
from itsor.infrastructure.adapters.in_memory_base_repository import InMemoryBaseRepository


class InMemoryUserRepository(InMemoryBaseRepository[Any], UserRepository):
    def __init__(self) -> None:
        super().__init__("User")

    def get_by_email(self, email: str) -> Any | None:
        for user in self._items.values():
            if user.email == email:
                return user
        return None

    def get_by_username(self, username: str) -> Any | None:
        for user in self._items.values():
            if user.username == username:
                return user
        return None


class InMemoryTenantRepository(InMemoryBaseRepository[Any], TenantRepository):
    def __init__(self) -> None:
        super().__init__("Tenant")

    def get_by_name(self, name: str) -> Any | None:
        for tenant in self._items.values():
            if tenant.name == name:
                return tenant
        return None


class InMemoryGroupRepository(InMemoryBaseRepository[Any], GroupRepository):
    def __init__(self) -> None:
        super().__init__("Group")

    def get_by_name(self, name: str, tenant_id: str | None = None) -> Any | None:
        for group in self._items.values():
            if group.name == name and group.tenant_id == tenant_id:
                return group
        return None


class BcryptPasswordHasher(PasswordHasher):
    def hash_password(self, plain: str) -> str:
        return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

    def verify_password(self, plain: str, hashed: str) -> bool:
        return bcrypt.checkpw(plain.encode(), hashed.encode())


class JwtTokenCodec(TokenCodec):
    def __init__(self) -> None:
        self._secret_key = os.getenv("SECRET_KEY", "change-me-in-production")
        if self._secret_key == "change-me-in-production":
            logging.warning(
                "SECRET_KEY is using the default insecure value. Set SECRET_KEY env var in production."
            )
        self._algorithm = "HS256"
        self._access_token_expire_minutes = 60

    def create_access_token(self, subject: str) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self._access_token_expire_minutes)
        payload = {"sub": subject, "exp": expire}
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_access_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            value = payload.get("sub")
            return str(value) if value is not None else None
        except JWTError:
            return None

__all__ = [
    "InMemoryUserRepository",
    "InMemoryTenantRepository",
    "InMemoryGroupRepository",
    "BcryptPasswordHasher",
    "JwtTokenCodec",
]
