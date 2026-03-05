from typing import Optional

from itsor.application.ports.auth.repositories import (
    GroupRepository,
    PasswordHasher,
    TenantRepository,
    TokenCodec,
    UserRepository,
)
from itsor.domain.ids import GroupId, TenantId, UserId
from itsor.domain.models.auth_models import Group, Tenant, User


class UserUseCases:
    def __init__(
        self,
        repo: UserRepository,
        tenant_repo: TenantRepository,
        group_repo: GroupRepository,
        password_hasher: PasswordHasher,
        token_codec: TokenCodec,
    ) -> None:
        self._repo = repo
        self._tenant_repo = tenant_repo
        self._group_repo = group_repo
        self._password_hasher = password_hasher
        self._token_codec = token_codec

    def _assign_group(
        self,
        user: User,
        invite_group_id: GroupId | None = None,
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
            user.group_id = None
            return

        existing_tenant = self._tenant_repo.get_by_name(tenant_name)
        if existing_tenant:
            raise ValueError("Tenant name already registered")

        tenant = Tenant(name=tenant_name)
        tenant.owner_id = user.id
        tenant.group_id = None
        tenant.permissions = None
        created_tenant = self._tenant_repo.create(tenant)

        users_group = Group(name="Tenant Users", tenant_id=created_tenant.id)
        users_group.owner_id = user.id
        users_group.group_id = None
        users_group.permissions = None
        created_users_group = self._group_repo.create(users_group)

        user.group_id = created_users_group.id

    def signup(
        self,
        username: str,
        email: str,
        password: str,
        invite_group_id: GroupId | None = None,
        create_tenant_name: str | None = None,
    ) -> tuple[User, str]:
        created = self.create_user(
            username=username,
            email=email,
            password=password,
            invite_group_id=invite_group_id,
            create_tenant_name=create_tenant_name,
        )
        token = self._token_codec.create_access_token(str(created.id))
        return created, token

    def login(self, identifier: str, password: str) -> tuple[User, str]:
        user = self._repo.get_by_email(identifier)
        if not user:
            user = self._repo.get_by_username(identifier)
        if not user or not self._password_hasher.verify_password(password, user.password_hash):
            raise ValueError("Invalid username/email or password")
        token = self._token_codec.create_access_token(str(user.id))
        return user, token

    def get_current_user(self, token: str) -> Optional[User]:
        user_id = self._token_codec.decode_access_token(token)
        if not user_id:
            return None
        return self._repo.get_by_id(user_id)

    def list_users(self) -> list[User]:
        return self._repo.list()

    def get_user(self, user_id: UserId) -> Optional[User]:
        return self._repo.get_by_id(user_id)

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        invite_group_id: GroupId | None = None,
        create_tenant_name: str | None = None,
    ) -> User:
        if self._repo.get_by_username(username):
            raise ValueError("Username already registered")
        if self._repo.get_by_email(email):
            raise ValueError("Email already registered")

        user = User(
            name=username,
            username=username,
            email=email,
            password_hash=self._password_hasher.hash_password(password),
        )
        self._assign_group(user, invite_group_id, create_tenant_name)
        return self._repo.create(user)

    def update_user(
        self,
        user_id: UserId,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
    ) -> User:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if username is not None and username != user.username:
            if self._repo.get_by_username(username):
                raise ValueError("Username already in use")
            previous_username = user.username
            user.username = username
            if not user.name or user.name == previous_username:
                user.name = username

        if email is not None and email != user.email:
            if self._repo.get_by_email(email):
                raise ValueError("Email already in use")
            user.email = email

        if password is not None:
            user.password_hash = self._password_hasher.hash_password(password)

        return self._repo.update(user)

    def replace_user(
        self,
        user_id: UserId,
        username: str,
        email: str,
        password: str,
    ) -> User:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if username != user.username and self._repo.get_by_username(username):
            raise ValueError("Username already in use")
        if email != user.email and self._repo.get_by_email(email):
            raise ValueError("Email already in use")

        previous_username = user.username
        user.username = username
        if not user.name or user.name == previous_username:
            user.name = username
        user.email = email
        user.password_hash = self._password_hasher.hash_password(password)
        return self._repo.update(user)

    def delete_user(self, user_id: UserId) -> None:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        self._repo.delete(user_id)
