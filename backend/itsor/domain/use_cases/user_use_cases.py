import logging
import os
from datetime import datetime, timedelta, timezone
from typing import List, Optional

import bcrypt
from jose import JWTError, jwt

from itsor.domain.ids import generate_ulid
from itsor.domain.models import Group, Tenant, User
from itsor.domain.ports.group_repository import GroupRepository
from itsor.domain.ports.tenant_repository import TenantRepository
from itsor.domain.ports.user_repository import UserRepository
from itsor.domain.use_cases.base_use_case import BaseUseCase

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


class UserUseCases(BaseUseCase):
    def __init__(self, repo: UserRepository, tenant_repo: TenantRepository, group_repo: GroupRepository) -> None:
        self._repo = repo
        self._tenant_repo = tenant_repo
        self._group_repo = group_repo

    def _assign_user_group(
        self,
        user: User,
        username: str,
        invite_group_id: str | None = None,
        create_tenant_name: str | None = None,
    ) -> None:
        if invite_group_id:
            invited_group = self._group_repo.get_by_id(invite_group_id)
            if not invited_group:
                raise ValueError("Invite group not found")
            user.group_id = invited_group.id
            return

        tenant_name = (create_tenant_name or "").strip()
        if not tenant_name:
            raise ValueError("User must be invited to a group or create a tenant")

        existing_tenant = self._tenant_repo.get_by_name(tenant_name)
        if existing_tenant:
            raise ValueError("Tenant name already registered")

        tenant = Tenant(id=generate_ulid(), name=tenant_name, owner_id=user.id)
        created_tenant = self._tenant_repo.create(tenant)

        admins_group = Group(
            id=generate_ulid(),
            name="Tenant Admins",
            tenant_id=created_tenant.id,
            owner_id=user.id,
        )
        self._group_repo.create(admins_group)

        users_group = Group(
            id=generate_ulid(),
            name="Tenant Users",
            tenant_id=created_tenant.id,
            owner_id=user.id,
        )
        created_users_group = self._group_repo.create(users_group)

        user.group_id = created_users_group.id

    def _assign_signup_group(self, user: User, invite_group_id: str | None = None) -> None:
        if not invite_group_id:
            user.group_id = None
            return

        invited_group = self._group_repo.get_by_id(invite_group_id)
        if not invited_group:
            raise ValueError("Invite group not found")
        user.group_id = invited_group.id

    def signup(
        self,
        username: str,
        email: str,
        password: str,
        invite_group_id: str | None = None,
        create_tenant_name: str | None = None,
    ) -> tuple[User, str]:
        existing_by_username = self._repo.get_by_username(username)
        if existing_by_username:
            raise ValueError("Username already registered")
        existing_by_email = self._repo.get_by_email(email)
        if existing_by_email:
            raise ValueError("Email already registered")
        user = User(
            id=generate_ulid(),
            name=username,
            username=username,
            email=email,
            password_hash=hash_password(password),
        )
        self._assign_signup_group(user, invite_group_id)
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

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        invite_group_id: str | None = None,
        create_tenant_name: str | None = None,
    ) -> User:
        existing_by_username = self._repo.get_by_username(username)
        if existing_by_username:
            raise ValueError("Username already registered")
        existing_by_email = self._repo.get_by_email(email)
        if existing_by_email:
            raise ValueError("Email already registered")
        user = User(
            id=generate_ulid(),
            name=username,
            username=username,
            email=email,
            password_hash=hash_password(password),
        )
        self._assign_user_group(user, username, invite_group_id, create_tenant_name)
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
            previous_username = user.username
            existing = self._repo.get_by_username(username)
            if existing:
                raise ValueError("Username already in use")
            user.username = username
            if not user.name or user.name == previous_username:
                user.name = username
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
        previous_username = user.username
        if username != user.username:
            existing = self._repo.get_by_username(username)
            if existing:
                raise ValueError("Username already in use")
        if email != user.email:
            existing = self._repo.get_by_email(email)
            if existing:
                raise ValueError("Email already in use")
        user.username = username
        if not user.name or user.name == previous_username:
            user.name = username
        user.email = email
        user.password_hash = hash_password(password)
        return self._repo.update(user)

    def delete_user(self, user_id: str) -> None:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        self._repo.delete(user_id)
