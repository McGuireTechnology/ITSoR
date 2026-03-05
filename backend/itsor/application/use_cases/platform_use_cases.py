from dataclasses import MISSING, fields, is_dataclass
from typing import Any, List, Literal, Optional, Protocol, cast

from itsor.domain.models import (
    Group,
    Permission,
    Resource,
    ResourceAction,
    Role,
    RoleAssignment,
    RolePermission,
    Tenant,
    User,
    UserTenant,
    platform_models,
)
from itsor.domain.ids import GroupId, PermissionId, RoleId, TenantId, UserId
from itsor.application.ports.auth.repositories import (
    GroupRepository,
    GroupRoleRepository,
    PasswordHasher,
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
    TenantRepository,
    TokenCodec,
    UserRepository,
    UserRoleRepository,
    UserTenantRepository,
)

PrincipalType = Literal["user", "group"]
EndpointAction = Literal["read", "write"]


class GroupUseCases:
    @staticmethod
    def _default_platform_permissions() -> dict[str, list[ResourceAction | str]]:
        return {"*": [ResourceAction.READ, "write"]}

    def __init__(self, repo: GroupRepository) -> None:
        self._repo = repo

    def list_groups(self) -> List[Group]:
        return self._repo.list()

    def get_group(self, group_id: str) -> Optional[Group]:
        return self._repo.get_by_id(group_id)

    def create_group(
        self,
        name: str,
        tenant_id: str | None = None,
        creator_user_id: str | None = None,
        platform_endpoint_permissions: dict[str, list[ResourceAction | str]] | None = None,
    ) -> Group:
        existing = self._repo.get_by_name(name, tenant_id)
        if existing:
            raise ValueError("Group name already registered")
        group = Group(name=name, tenant_id=TenantId(tenant_id) if tenant_id is not None else None)
        group.owner_id = UserId(creator_user_id) if creator_user_id is not None else None
        group.group_id = None
        group.permissions = None
        group.platform_endpoint_permissions = (
            platform_endpoint_permissions or self._default_platform_permissions()
        )
        return self._repo.create(group)

    def update_group(
        self,
        group_id: str,
        name: Optional[str] = None,
        platform_endpoint_permissions: dict[str, list[ResourceAction | str]] | None = None,
    ) -> Group:
        group = self._repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")
        if name is not None and name != group.name:
            existing = self._repo.get_by_name(name, group.tenant_id)
            if existing:
                raise ValueError("Group name already in use")
            group.name = name
        if platform_endpoint_permissions is not None:
            group.platform_endpoint_permissions = platform_endpoint_permissions
        return self._repo.update(group)

    def replace_group(
        self,
        group_id: str,
        name: str,
        platform_endpoint_permissions: dict[str, list[ResourceAction | str]] | None = None,
    ) -> Group:
        group = self._repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")
        if name != group.name:
            existing = self._repo.get_by_name(name, group.tenant_id)
            if existing:
                raise ValueError("Group name already in use")
        group.name = name
        group.platform_endpoint_permissions = (
            platform_endpoint_permissions or self._default_platform_permissions()
        )
        return self._repo.update(group)

    def delete_group(self, group_id: str) -> None:
        group = self._repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")
        self._repo.delete(group_id)


class TenantUseCases:
    def __init__(
        self, repo: TenantRepository, group_repo: GroupRepository, user_repo: UserRepository
    ) -> None:
        self._repo = repo
        self._group_repo = group_repo
        self._user_repo = user_repo

    def list_tenants(self) -> List[Tenant]:
        return self._repo.list()

    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        return self._repo.get_by_id(tenant_id)

    def create_tenant(self, name: str, creator_user_id: str | None = None) -> Tenant:
        existing = self._repo.get_by_name(name)
        if existing:
            raise ValueError("Tenant name already registered")
        tenant = Tenant(name=name)
        tenant.owner_id = UserId(creator_user_id) if creator_user_id is not None else None
        tenant.group_id = None
        tenant.permissions = None
        created_tenant = self._repo.create(tenant)

        admins_group = Group(name="Tenant Admins", tenant_id=created_tenant.id)
        admins_group.owner_id = UserId(creator_user_id) if creator_user_id is not None else None
        admins_group.group_id = None
        admins_group.permissions = None
        admins_group.platform_endpoint_permissions = GroupUseCases._default_platform_permissions()
        self._group_repo.create(admins_group)

        users_group = Group(name="Tenant Users", tenant_id=created_tenant.id)
        users_group.owner_id = UserId(creator_user_id) if creator_user_id is not None else None
        users_group.group_id = None
        users_group.permissions = None
        users_group.platform_endpoint_permissions = GroupUseCases._default_platform_permissions()
        created_users_group = self._group_repo.create(users_group)

        if creator_user_id:
            creator = self._user_repo.get_by_id(creator_user_id)
            if creator:
                creator.group_id = created_users_group.id
                self._user_repo.update(creator)

        return created_tenant

    def update_tenant(self, tenant_id: str, name: Optional[str] = None) -> Tenant:
        tenant = self._repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        if name is not None and name != tenant.name:
            existing = self._repo.get_by_name(name)
            if existing:
                raise ValueError("Tenant name already in use")
            tenant.name = name
        return self._repo.update(tenant)

    def replace_tenant(self, tenant_id: str, name: str) -> Tenant:
        tenant = self._repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        if name != tenant.name:
            existing = self._repo.get_by_name(name)
            if existing:
                raise ValueError("Tenant name already in use")
        tenant.name = name
        return self._repo.update(tenant)

    def delete_tenant(self, tenant_id: str) -> None:
        tenant = self._repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        self._repo.delete(tenant_id)


class UserUseCases:
    @staticmethod
    def _default_platform_permissions() -> dict[str, list[ResourceAction | str]]:
        return {"*": [ResourceAction.READ, "write"]}

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

        tenant = Tenant(name=tenant_name)
        tenant.owner_id = user.id
        tenant.group_id = None
        tenant.permissions = None
        created_tenant = self._tenant_repo.create(tenant)

        admins_group = Group(name="Tenant Admins", tenant_id=created_tenant.id)
        admins_group.owner_id = user.id
        admins_group.group_id = None
        admins_group.permissions = None
        admins_group.platform_endpoint_permissions = GroupUseCases._default_platform_permissions()
        self._group_repo.create(admins_group)

        users_group = Group(name="Tenant Users", tenant_id=created_tenant.id)
        users_group.owner_id = user.id
        users_group.group_id = None
        users_group.permissions = None
        users_group.platform_endpoint_permissions = GroupUseCases._default_platform_permissions()
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
            name=username,
            username=username,
            email=email,
            password_hash=self._password_hasher.hash_password(password),
        )
        user.platform_endpoint_permissions = self._default_platform_permissions()
        self._assign_signup_group(user, invite_group_id)
        created = self._repo.create(user)
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
        platform_endpoint_permissions: dict[str, list[ResourceAction | str]] | None = None,
    ) -> User:
        existing_by_username = self._repo.get_by_username(username)
        if existing_by_username:
            raise ValueError("Username already registered")
        existing_by_email = self._repo.get_by_email(email)
        if existing_by_email:
            raise ValueError("Email already registered")
        user = User(
            name=username,
            username=username,
            email=email,
            password_hash=self._password_hasher.hash_password(password),
        )
        user.platform_endpoint_permissions = (
            platform_endpoint_permissions or self._default_platform_permissions()
        )
        self._assign_user_group(user, username, invite_group_id, create_tenant_name)
        return self._repo.create(user)

    def update_user(
        self,
        user_id: str,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        platform_endpoint_permissions: dict[str, list[ResourceAction | str]] | None = None,
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
            user.password_hash = self._password_hasher.hash_password(password)
        if platform_endpoint_permissions is not None:
            user.platform_endpoint_permissions = platform_endpoint_permissions
        return self._repo.update(user)

    def replace_user(
        self,
        user_id: str,
        username: str,
        email: str,
        password: str,
        platform_endpoint_permissions: dict[str, list[ResourceAction | str]] | None = None,
    ) -> User:
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
        user.password_hash = self._password_hasher.hash_password(password)
        user.platform_endpoint_permissions = (
            platform_endpoint_permissions or self._default_platform_permissions()
        )
        return self._repo.update(user)

    def delete_user(self, user_id: str) -> None:
        user = self._repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        self._repo.delete(user_id)


class PlatformRbacUseCases:
    def __init__(
        self,
        user_repo: UserRepository,
        group_repo: GroupRepository,
        tenant_repo: TenantRepository,
        role_repo: RoleRepository,
        permission_repo: PermissionRepository,
        user_tenant_repo: UserTenantRepository,
        user_role_repo: UserRoleRepository,
        group_role_repo: GroupRoleRepository,
        role_permission_repo: RolePermissionRepository,
    ) -> None:
        self._user_repo = user_repo
        self._group_repo = group_repo
        self._tenant_repo = tenant_repo
        self._role_repo = role_repo
        self._permission_repo = permission_repo
        self._user_tenant_repo = user_tenant_repo
        self._user_role_repo = user_role_repo
        self._group_role_repo = group_role_repo
        self._role_permission_repo = role_permission_repo

    def _ensure_user_exists(self, user_id: str) -> None:
        if not self._user_repo.get_by_id(user_id):
            raise ValueError("User not found")

    def _ensure_group_exists(self, group_id: str) -> None:
        if not self._group_repo.get_by_id(group_id):
            raise ValueError("Group not found")

    def _ensure_tenant_exists(self, tenant_id: str) -> None:
        if not self._tenant_repo.get_by_id(tenant_id):
            raise ValueError("Tenant not found")

    def _ensure_role_exists(self, role_id: str) -> None:
        if not self._role_repo.get_by_id(role_id):
            raise ValueError("Role not found")

    def _ensure_permission_exists(self, permission_id: str) -> None:
        if not self._permission_repo.get_by_id(permission_id):
            raise ValueError("Permission not found")

    @staticmethod
    def _coerce_resource(resource: str) -> Resource:
        try:
            return Resource(resource)
        except ValueError:
            return cast(Resource, resource)

    def list_roles(self) -> List[Role]:
        return sorted(self._role_repo.list(), key=lambda role: str(role.name).lower())

    def get_role(self, role_id: str) -> Optional[Role]:
        return self._role_repo.get_by_id(role_id)

    def create_role(self, name: str, tenant_id: str | None = None, description: str = "") -> Role:
        if tenant_id:
            self._ensure_tenant_exists(tenant_id)
        role = Role(
            name=name,
            tenant_id=cast(TenantId, TenantId(tenant_id) if tenant_id is not None else None),
            description=description,
        )
        return self._role_repo.create(role)

    def replace_role(
        self,
        role_id: str,
        name: str,
        tenant_id: str | None = None,
        description: str = "",
    ) -> Role:
        role = self._role_repo.get_by_id(role_id)
        if not role:
            raise ValueError("Role not found")
        if tenant_id:
            self._ensure_tenant_exists(tenant_id)

        role.name = name
        role.tenant_id = cast(TenantId, TenantId(tenant_id) if tenant_id is not None else None)
        role.description = description
        return self._role_repo.update(role)

    def update_role(
        self,
        role_id: str,
        name: str | None = None,
        tenant_id: str | None = None,
        description: str | None = None,
    ) -> Role:
        role = self._role_repo.get_by_id(role_id)
        if not role:
            raise ValueError("Role not found")

        if tenant_id is not None:
            self._ensure_tenant_exists(tenant_id)
            role.tenant_id = TenantId(tenant_id)
        if name is not None:
            role.name = name
        if description is not None:
            role.description = description

        return self._role_repo.update(role)

    def delete_role(self, role_id: str) -> None:
        role = self._role_repo.get_by_id(role_id)
        if not role:
            raise ValueError("Role not found")
        self._role_repo.delete(role_id)

    def list_permissions(self) -> List[Permission]:
        return sorted(
            self._permission_repo.list(), key=lambda permission: str(permission.name).lower()
        )

    def get_permission(self, permission_id: str) -> Optional[Permission]:
        return self._permission_repo.get_by_id(permission_id)

    def create_permission(self, name: str, resource: str, action) -> Permission:
        permission = Permission(
            name=name,
            resource=self._coerce_resource(resource),
            action=action,
        )
        return self._permission_repo.create(permission)

    def replace_permission(
        self,
        permission_id: str,
        name: str,
        resource: str,
        action,
    ) -> Permission:
        permission = self._permission_repo.get_by_id(permission_id)
        if not permission:
            raise ValueError("Permission not found")

        permission.name = name
        permission.resource = self._coerce_resource(resource)
        permission.action = action
        return self._permission_repo.update(permission)

    def update_permission(
        self,
        permission_id: str,
        name: str | None = None,
        resource: str | None = None,
        action=None,
    ) -> Permission:
        permission = self._permission_repo.get_by_id(permission_id)
        if not permission:
            raise ValueError("Permission not found")

        if name is not None:
            permission.name = name
        if resource is not None:
            permission.resource = self._coerce_resource(resource)
        if action is not None:
            permission.action = action

        return self._permission_repo.update(permission)

    def delete_permission(self, permission_id: str) -> None:
        permission = self._permission_repo.get_by_id(permission_id)
        if not permission:
            raise ValueError("Permission not found")
        self._permission_repo.delete(permission_id)

    def list_user_tenants(self) -> List[UserTenant]:
        return self._user_tenant_repo.list()

    def get_user_tenant(self, user_tenant_id: str) -> Optional[UserTenant]:
        return self._user_tenant_repo.get_by_id(user_tenant_id)

    def create_user_tenant(self, user_id: str, tenant_id: str) -> UserTenant:
        self._ensure_user_exists(user_id)
        self._ensure_tenant_exists(tenant_id)
        link = UserTenant(user_id=UserId(user_id), tenant_id=TenantId(tenant_id))
        return self._user_tenant_repo.create(link)

    def replace_user_tenant(
        self,
        user_tenant_id: str,
        user_id: str,
        tenant_id: str,
    ) -> UserTenant:
        link = self._user_tenant_repo.get_by_id(user_tenant_id)
        if not link:
            raise ValueError("User-tenant link not found")

        self._ensure_user_exists(user_id)
        self._ensure_tenant_exists(tenant_id)

        link.user_id = UserId(user_id)
        link.tenant_id = TenantId(tenant_id)
        return self._user_tenant_repo.update(link)

    def update_user_tenant(
        self,
        user_tenant_id: str,
        user_id: str | None = None,
        tenant_id: str | None = None,
    ) -> UserTenant:
        link = self._user_tenant_repo.get_by_id(user_tenant_id)
        if not link:
            raise ValueError("User-tenant link not found")

        if user_id is not None:
            self._ensure_user_exists(user_id)
            link.user_id = UserId(user_id)
        if tenant_id is not None:
            self._ensure_tenant_exists(tenant_id)
            link.tenant_id = TenantId(tenant_id)

        return self._user_tenant_repo.update(link)

    def delete_user_tenant(self, user_tenant_id: str) -> None:
        link = self._user_tenant_repo.get_by_id(user_tenant_id)
        if not link:
            raise ValueError("User-tenant link not found")
        self._user_tenant_repo.delete(user_tenant_id)

    def list_user_roles(self) -> List[RoleAssignment]:
        return self._user_role_repo.list()

    def get_user_role(self, user_role_id: str) -> Optional[RoleAssignment]:
        return self._user_role_repo.get_by_id(user_role_id)

    def create_user_role(self, user_id: str, role_id: str) -> RoleAssignment:
        self._ensure_user_exists(user_id)
        self._ensure_role_exists(role_id)
        link = RoleAssignment(
            role_id=RoleId(role_id),
            assignee_type="user",
            user_id=UserId(user_id),
        )
        return self._user_role_repo.create(link)

    def replace_user_role(self, user_role_id: str, user_id: str, role_id: str) -> RoleAssignment:
        link = self._user_role_repo.get_by_id(user_role_id)
        if not link:
            raise ValueError("User-role link not found")

        self._ensure_user_exists(user_id)
        self._ensure_role_exists(role_id)

        link.assignee_type = "user"
        link.user_id = UserId(user_id)
        link.group_id = None
        link.role_id = RoleId(role_id)
        return self._user_role_repo.update(link)

    def update_user_role(
        self,
        user_role_id: str,
        user_id: str | None = None,
        role_id: str | None = None,
    ) -> RoleAssignment:
        link = self._user_role_repo.get_by_id(user_role_id)
        if not link:
            raise ValueError("User-role link not found")

        link.assignee_type = "user"
        if user_id is not None:
            self._ensure_user_exists(user_id)
            link.user_id = UserId(user_id)
            link.group_id = None
        if role_id is not None:
            self._ensure_role_exists(role_id)
            link.role_id = RoleId(role_id)

        return self._user_role_repo.update(link)

    def delete_user_role(self, user_role_id: str) -> None:
        link = self._user_role_repo.get_by_id(user_role_id)
        if not link:
            raise ValueError("User-role link not found")
        self._user_role_repo.delete(user_role_id)

    def list_group_roles(self) -> List[RoleAssignment]:
        return self._group_role_repo.list()

    def get_group_role(self, group_role_id: str) -> Optional[RoleAssignment]:
        return self._group_role_repo.get_by_id(group_role_id)

    def create_group_role(self, group_id: str, role_id: str) -> RoleAssignment:
        self._ensure_group_exists(group_id)
        self._ensure_role_exists(role_id)
        link = RoleAssignment(
            role_id=RoleId(role_id),
            assignee_type="group",
            group_id=GroupId(group_id),
        )
        return self._group_role_repo.create(link)

    def replace_group_role(
        self,
        group_role_id: str,
        group_id: str,
        role_id: str,
    ) -> RoleAssignment:
        link = self._group_role_repo.get_by_id(group_role_id)
        if not link:
            raise ValueError("Group-role link not found")

        self._ensure_group_exists(group_id)
        self._ensure_role_exists(role_id)

        link.assignee_type = "group"
        link.user_id = None
        link.group_id = GroupId(group_id)
        link.role_id = RoleId(role_id)
        return self._group_role_repo.update(link)

    def update_group_role(
        self,
        group_role_id: str,
        group_id: str | None = None,
        role_id: str | None = None,
    ) -> RoleAssignment:
        link = self._group_role_repo.get_by_id(group_role_id)
        if not link:
            raise ValueError("Group-role link not found")

        link.assignee_type = "group"
        if group_id is not None:
            self._ensure_group_exists(group_id)
            link.user_id = None
            link.group_id = GroupId(group_id)
        if role_id is not None:
            self._ensure_role_exists(role_id)
            link.role_id = RoleId(role_id)

        return self._group_role_repo.update(link)

    def delete_group_role(self, group_role_id: str) -> None:
        link = self._group_role_repo.get_by_id(group_role_id)
        if not link:
            raise ValueError("Group-role link not found")
        self._group_role_repo.delete(group_role_id)

    def list_role_permissions(self) -> List[RolePermission]:
        return self._role_permission_repo.list()

    def get_role_permission(self, role_permission_id: str) -> Optional[RolePermission]:
        return self._role_permission_repo.get_by_id(role_permission_id)

    def create_role_permission(self, role_id: str, permission_id: str) -> RolePermission:
        self._ensure_role_exists(role_id)
        self._ensure_permission_exists(permission_id)
        link = RolePermission(role_id=RoleId(role_id), permission_id=PermissionId(permission_id))
        return self._role_permission_repo.create(link)

    def replace_role_permission(
        self,
        role_permission_id: str,
        role_id: str,
        permission_id: str,
    ) -> RolePermission:
        link = self._role_permission_repo.get_by_id(role_permission_id)
        if not link:
            raise ValueError("Role-permission link not found")

        self._ensure_role_exists(role_id)
        self._ensure_permission_exists(permission_id)

        link.role_id = RoleId(role_id)
        link.permission_id = PermissionId(permission_id)
        return self._role_permission_repo.update(link)

    def update_role_permission(
        self,
        role_permission_id: str,
        role_id: str | None = None,
        permission_id: str | None = None,
    ) -> RolePermission:
        link = self._role_permission_repo.get_by_id(role_permission_id)
        if not link:
            raise ValueError("Role-permission link not found")

        if role_id is not None:
            self._ensure_role_exists(role_id)
            link.role_id = RoleId(role_id)
        if permission_id is not None:
            self._ensure_permission_exists(permission_id)
            link.permission_id = PermissionId(permission_id)

        return self._role_permission_repo.update(link)

    def delete_role_permission(self, role_permission_id: str) -> None:
        link = self._role_permission_repo.get_by_id(role_permission_id)
        if not link:
            raise ValueError("Role-permission link not found")
        self._role_permission_repo.delete(role_permission_id)


class PlatformEndpointPermissionGateway(Protocol):
    def list_rows(
        self,
        *,
        principal_type: PrincipalType | None = None,
        principal_id: str | None = None,
    ) -> list[Any]: ...

    def create_row(
        self,
        *,
        principal_type: PrincipalType,
        principal_id: str,
        endpoint_name: str,
        action: EndpointAction,
    ) -> Any: ...

    def get_row(self, endpoint_permission_id: int) -> Any | None: ...

    def replace_row(
        self,
        *,
        endpoint_permission_id: int,
        principal_type: PrincipalType,
        principal_id: str,
        endpoint_name: str,
        action: EndpointAction,
    ) -> Any | None: ...

    def patch_row(
        self,
        *,
        endpoint_permission_id: int,
        principal_type: PrincipalType | None = None,
        principal_id: str | None = None,
        endpoint_name: str | None = None,
        action: EndpointAction | None = None,
    ) -> Any | None: ...

    def delete_row(self, endpoint_permission_id: int) -> bool: ...


class PlatformGroupMembershipGateway(Protocol):
    def list_memberships(self) -> list[Any]: ...

    def create_membership(
        self,
        *,
        group_id: str,
        member_type: str,
        member_user_id: str | None,
        member_group_id: str | None,
    ) -> Any: ...

    def get_membership(self, membership_id: str) -> Any | None: ...

    def patch_membership(
        self,
        *,
        membership_id: str,
        member_type: str | None = None,
        member_user_id: str | None = None,
        member_group_id: str | None = None,
    ) -> Any | None: ...

    def delete_membership(self, membership_id: str) -> bool: ...


class PlatformEndpointPermissionUseCases:
    def __init__(
        self,
        gateway: PlatformEndpointPermissionGateway,
        user_repo: UserRepository,
        group_repo: GroupRepository,
    ) -> None:
        self._gateway = gateway
        self._user_repo = user_repo
        self._group_repo = group_repo

    def _validate_principal(self, principal_type: PrincipalType, principal_id: str) -> None:
        if principal_type == "user":
            if not self._user_repo.get_by_id(principal_id):
                raise ValueError("User not found")
            return

        if not self._group_repo.get_by_id(principal_id):
            raise ValueError("Group not found")

    def list_rows(
        self,
        *,
        principal_type: PrincipalType | None = None,
        principal_id: str | None = None,
    ) -> list[Any]:
        return self._gateway.list_rows(principal_type=principal_type, principal_id=principal_id)

    def create_row(
        self,
        *,
        principal_type: PrincipalType,
        principal_id: str,
        endpoint_name: str,
        action: EndpointAction,
    ) -> Any:
        self._validate_principal(principal_type, principal_id)
        return self._gateway.create_row(
            principal_type=principal_type,
            principal_id=principal_id,
            endpoint_name=endpoint_name,
            action=action,
        )

    def get_row(self, endpoint_permission_id: int) -> Any | None:
        return self._gateway.get_row(endpoint_permission_id)

    def replace_row(
        self,
        *,
        endpoint_permission_id: int,
        principal_type: PrincipalType,
        principal_id: str,
        endpoint_name: str,
        action: EndpointAction,
    ) -> Any:
        self._validate_principal(principal_type, principal_id)
        row = self._gateway.replace_row(
            endpoint_permission_id=endpoint_permission_id,
            principal_type=principal_type,
            principal_id=principal_id,
            endpoint_name=endpoint_name,
            action=action,
        )
        if not row:
            raise ValueError("Platform endpoint permission row not found")
        return row

    def patch_row(
        self,
        *,
        endpoint_permission_id: int,
        principal_type: PrincipalType | None = None,
        principal_id: str | None = None,
        endpoint_name: str | None = None,
        action: EndpointAction | None = None,
    ) -> Any:
        row = self._gateway.get_row(endpoint_permission_id)
        if not row:
            raise ValueError("Platform endpoint permission row not found")

        if principal_type is None and principal_id is None and endpoint_name is None and action is None:
            raise ValueError("No fields provided for patch")

        effective_principal_type = principal_type or row.principal_type
        effective_principal_id = principal_id or row.principal_id
        self._validate_principal(effective_principal_type, effective_principal_id)

        patched = self._gateway.patch_row(
            endpoint_permission_id=endpoint_permission_id,
            principal_type=principal_type,
            principal_id=principal_id,
            endpoint_name=endpoint_name,
            action=action,
        )
        if not patched:
            raise ValueError("Platform endpoint permission row not found")
        return patched

    def delete_row(self, endpoint_permission_id: int) -> None:
        if not self._gateway.delete_row(endpoint_permission_id):
            raise ValueError("Platform endpoint permission row not found")


class PlatformGroupMembershipUseCases:
    def __init__(
        self,
        gateway: PlatformGroupMembershipGateway,
        user_repo: UserRepository,
        group_repo: GroupRepository,
    ) -> None:
        self._gateway = gateway
        self._user_repo = user_repo
        self._group_repo = group_repo

    def _validate_member_ref(
        self,
        *,
        member_type: str,
        member_user_id: str | None,
        member_group_id: str | None,
    ) -> None:
        if member_type not in {"user", "group"}:
            raise ValueError("member_type must be 'user' or 'group'")

        if member_type == "user":
            if not member_user_id or member_group_id:
                raise ValueError("user membership requires member_user_id only")
            if not self._user_repo.get_by_id(member_user_id):
                raise ValueError("Member user not found")
            return

        if not member_group_id or member_user_id:
            raise ValueError("group membership requires member_group_id only")
        if not self._group_repo.get_by_id(member_group_id):
            raise ValueError("Member group not found")

    def list_memberships(self) -> list[Any]:
        return self._gateway.list_memberships()

    def create_membership(
        self,
        *,
        group_id: str,
        member_type: str,
        member_user_id: str | None,
        member_group_id: str | None,
    ) -> Any:
        if not self._group_repo.get_by_id(group_id):
            raise ValueError("Group not found")

        self._validate_member_ref(
            member_type=member_type,
            member_user_id=member_user_id,
            member_group_id=member_group_id,
        )

        if member_type == "group" and member_group_id == group_id:
            raise ValueError("Group cannot directly contain itself")

        return self._gateway.create_membership(
            group_id=group_id,
            member_type=member_type,
            member_user_id=member_user_id,
            member_group_id=member_group_id,
        )

    def get_membership(self, membership_id: str) -> Any | None:
        return self._gateway.get_membership(membership_id)

    def patch_membership(
        self,
        *,
        membership_id: str,
        member_type: str | None = None,
        member_user_id: str | None = None,
        member_group_id: str | None = None,
    ) -> Any:
        membership = self._gateway.get_membership(membership_id)
        if not membership:
            raise ValueError("Group membership not found")

        next_member_type = member_type if member_type is not None else str(membership.member_type)
        next_member_user_id = member_user_id if member_user_id is not None else membership.member_user_id
        next_member_group_id = member_group_id if member_group_id is not None else membership.member_group_id

        self._validate_member_ref(
            member_type=next_member_type,
            member_user_id=next_member_user_id,
            member_group_id=next_member_group_id,
        )

        if next_member_type == "group" and str(next_member_group_id) == str(membership.group_id):
            raise ValueError("Group cannot directly contain itself")

        patched = self._gateway.patch_membership(
            membership_id=membership_id,
            member_type=member_type,
            member_user_id=member_user_id,
            member_group_id=member_group_id,
        )
        if not patched:
            raise ValueError("Group membership not found")
        return patched

    def delete_membership(self, membership_id: str) -> None:
        if not self._gateway.delete_membership(membership_id):
            raise ValueError("Group membership not found")


class PlatformModelCatalogUseCases:
    _platform_model_classes = {
        "User": platform_models.User,
        "Tenant": platform_models.Tenant,
        "Group": platform_models.Group,
        "Role": platform_models.Role,
        "Permission": platform_models.Permission,
        "UserTenant": platform_models.UserTenant,
        "GroupMembership": platform_models.GroupMembership,
        "RoleAssignment": platform_models.RoleAssignment,
        "RolePermission": platform_models.RolePermission,
    }

    @staticmethod
    def _render_default(value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, (str, int, float, bool, list, dict)):
            return value
        return str(value)

    def list_models(self) -> list[str]:
        return sorted(self._platform_model_classes.keys())

    def get_model_details(self, model_name: str) -> dict[str, Any]:
        model_class = self._platform_model_classes.get(model_name)
        if not model_class:
            raise ValueError("Platform model not found")

        if not is_dataclass(model_class):
            raise RuntimeError("Configured class is not a dataclass")

        model_fields: list[dict[str, Any]] = []
        for field_info in fields(model_class):
            field_type = field_info.type
            type_name = getattr(field_type, "__name__", str(field_type))

            default_value = None
            if field_info.default is not MISSING:
                default_value = self._render_default(field_info.default)

            if field_info.default_factory is not MISSING:
                factory_name = getattr(
                    field_info.default_factory,
                    "__name__",
                    str(field_info.default_factory),
                )
            else:
                factory_name = None

            model_fields.append(
                {
                    "name": field_info.name,
                    "type": type_name,
                    "default": default_value,
                    "default_factory": factory_name,
                    "init": field_info.init,
                }
            )

        return {
            "name": getattr(model_class, "__name__", model_name),
            "module": model_class.__module__,
            "fields": model_fields,
        }


__all__ = [
    "EndpointAction",
    "GroupUseCases",
    "PlatformEndpointPermissionUseCases",
    "PlatformGroupMembershipUseCases",
    "PlatformModelCatalogUseCases",
    "PlatformRbacUseCases",
    "PrincipalType",
    "TenantUseCases",
    "UserUseCases",
]
