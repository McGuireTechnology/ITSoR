from abc import ABC, abstractmethod
from typing import Optional

from itsor.domain.ids import GroupId, TenantId
from itsor.domain.models.auth_models import (
    Group,
    GroupMembership,
    Permission,
    Role,
    RoleAssignment,
    RolePermission,
    Tenant,
    User,
    UserTenant,
)


class GroupRepository(BaseRepository[Group], ABC):
    @abstractmethod
    def get_by_name(self, name: str, tenant_id: TenantId | None = None) -> Optional[Group]: ...


class GroupMembershipRepository(BaseRepository[GroupMembership], ABC): ...


class TenantRepository(BaseRepository[Tenant], ABC):
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Tenant]: ...


class UserRepository(BaseRepository[User], ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]: ...


class RoleRepository(BaseRepository[Role], ABC):
    @abstractmethod
    def get_by_name(self, name: str, tenant_id: TenantId | None = None) -> Optional[Role]: ...


class PermissionRepository(BaseRepository[Permission], ABC): ...


class UserTenantRepository(BaseRepository[UserTenant], ABC): ...


class RoleAssignmentRepository(BaseRepository[RoleAssignment], ABC):
    @abstractmethod
    def list_for_user(self, user_id: str) -> list[RoleAssignment]: ...

    @abstractmethod
    def list_for_group(self, group_id: GroupId) -> list[RoleAssignment]: ...


class UserRoleRepository(RoleAssignmentRepository, ABC): ...


class GroupRoleRepository(RoleAssignmentRepository, ABC): ...


class RolePermissionRepository(BaseRepository[RolePermission], ABC): ...


class PasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, plain: str) -> str: ...

    @abstractmethod
    def verify_password(self, plain: str, hashed: str) -> bool: ...


class TokenCodec(ABC):
    @abstractmethod
    def create_access_token(self, subject: str) -> str: ...

    @abstractmethod
    def decode_access_token(self, token: str) -> str | None: ...
