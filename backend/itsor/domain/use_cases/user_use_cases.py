import logging
import os
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import bcrypt
from jose import JWTError, jwt

from itsor.domain.ids import generate_ulid
from itsor.domain.models.user import User
from itsor.domain.ports.user_repository import UserRepository

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
if SECRET_KEY == "change-me-in-production":
    logging.warning("SECRET_KEY is using the default insecure value. Set SECRET_KEY env var in production.")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


class UserUseCases:
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    def signup(self, username: str, email: str, password: str) -> tuple[User, str]:
        existing_by_username = self._repo.get_by_username(username)
        if existing_by_username:
            raise ValueError("Username already registered")
        existing_by_email = self._repo.get_by_email(email)
        if existing_by_email:
            raise ValueError("Email already registered")
        user = User(
            id=generate_ulid(),
            username=username,
            email=email,
            password_hash=hash_password(password),
        )
        created = self._repo.create(user)
        token = create_access_token(str(created.id))
        return created, token

    def login(self, identifier: str, password: str) -> tuple[User, str]:
        user = self._repo.get_by_email(identifier)
        if not user:
            user = self._repo.get_by_username(identifier)
        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Invalid username/email or password")
        token = create_access_token(str(user.id))
        return user, token

    def get_current_user(self, token: str) -> Optional[User]:
        user_id = decode_access_token(token)
        if not user_id:
            return None
        return self._repo.get_by_id(user_id)

    def list_users(self) -> List[User]:
        return self._repo.list()

    def get_user(self, user_id: str) -> Optional[User]:
        return self._repo.get_by_id(user_id)

    def create_user(self, username: str, email: str, password: str) -> User:
        existing_by_username = self._repo.get_by_username(username)
        if existing_by_username:
            raise ValueError("Username already registered")
        existing_by_email = self._repo.get_by_email(email)
        if existing_by_email:
            raise ValueError("Email already registered")
        user = User(
            id=generate_ulid(),
            username=username,
            email=email,
            password_hash=hash_password(password),
        )
        return self._repo.create(user)

    def update_user(
        self,
        user_id: str,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
    ) -> User:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if username is not None and username != user.username:
            existing = self._repo.get_by_username(username)
            if existing:
                raise ValueError("Username already in use")
            user.username = username
        if email is not None and email != user.email:
            existing = self._repo.get_by_email(email)
            if existing:
                raise ValueError("Email already in use")
            user.email = email
        if password is not None:
            user.password_hash = hash_password(password)
        return self._repo.update(user)

    def replace_user(self, user_id: str, username: str, email: str, password: str) -> User:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        if username != user.username:
            existing = self._repo.get_by_username(username)
            if existing:
                raise ValueError("Username already in use")
        if email != user.email:
            existing = self._repo.get_by_email(email)
            if existing:
                raise ValueError("Email already in use")
        user.username = username
        user.email = email
        user.password_hash = hash_password(password)
        return self._repo.update(user)

    def delete_user(self, user_id: str) -> None:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        self._repo.delete(user_id)
