from typing import Literal

from itsor.application.ports.auth.repositories import (
    GroupMembershipRepository,
    GroupRepository,
    GroupRoleRepository,
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
    TenantRepository,
    UserRoleRepository,
    UserTenantRepository,
)
from itsor.domain.ids import (
    GroupId,
    GroupMembershipId,
    GroupRoleId,
    PermissionId,
    RoleId,
    RolePermissionId,
    TenantId,
    UserId,
    UserRoleId,
    UserTenantId,
)
from itsor.domain.models import (
    Group,
    GroupMembership,
    Permission,
    Resource,
    ResourceAction,
    Role,
    RoleAssignment,
    RolePermission,
    Tenant,
    UserTenant,
)


class TenantUseCases:
    def __init__(self, repo: TenantRepository) -> None:
        self._repo = repo

    def list_tenants(self) -> list[Tenant]:
        return self._repo.list()

    def get_tenant(self, tenant_id: TenantId) -> Tenant | None:
        return self._repo.get_by_id(tenant_id)

    def create_tenant(self, name: str) -> Tenant:
        if self._repo.get_by_name(name):
            raise ValueError("Tenant name already registered")
        return self._repo.create(Tenant(name=name))

    def update_tenant(self, tenant_id: TenantId, name: str | None = None) -> Tenant:
        tenant = self._repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        if name is not None and name != tenant.name:
            if self._repo.get_by_name(name):
                raise ValueError("Tenant name already in use")
            tenant.name = name
        return self._repo.update(tenant)

    def replace_tenant(self, tenant_id: TenantId, name: str) -> Tenant:
        return self.update_tenant(tenant_id=tenant_id, name=name)

    def delete_tenant(self, tenant_id: TenantId) -> None:
        if not self._repo.get_by_id(tenant_id):
            raise ValueError("Tenant not found")
        self._repo.delete(tenant_id)


class GroupUseCases:
    def __init__(self, repo: GroupRepository) -> None:
        self._repo = repo

    def list_groups(self) -> list[Group]:
        return self._repo.list()

    def get_group(self, group_id: GroupId) -> Group | None:
        return self._repo.get_by_id(group_id)

    def create_group(self, name: str, tenant_id: TenantId | None = None) -> Group:
        if self._repo.get_by_name(name, tenant_id):
            raise ValueError("Group name already registered")
        return self._repo.create(Group(name=name, tenant_id=tenant_id))

    def update_group(self, group_id: GroupId, name: str | None = None) -> Group:
        group = self._repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")
        if name is not None and name != group.name:
            if self._repo.get_by_name(name, group.tenant_id):
                raise ValueError("Group name already in use")
            group.name = name
        return self._repo.update(group)

    def replace_group(self, group_id: GroupId, name: str, tenant_id: TenantId | None = None) -> Group:
        group = self._repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")
        if name != group.name and self._repo.get_by_name(name, tenant_id or group.tenant_id):
            raise ValueError("Group name already in use")
        group.name = name
        group.tenant_id = tenant_id
        return self._repo.update(group)

    def delete_group(self, group_id: GroupId) -> None:
        if not self._repo.get_by_id(group_id):
            raise ValueError("Group not found")
        self._repo.delete(group_id)


class RoleUseCases:
    def __init__(self, repo: RoleRepository) -> None:
        self._repo = repo

    def list_roles(self) -> list[Role]:
        return self._repo.list()

    def get_role(self, role_id: RoleId) -> Role | None:
        return self._repo.get_by_id(role_id)

    def create_role(self, name: str, tenant_id: TenantId | None = None, description: str = "") -> Role:
        if self._repo.get_by_name(name, tenant_id):
            raise ValueError("Role name already registered")
        return self._repo.create(Role(name=name, tenant_id=tenant_id, description=description))

    def update_role(
        self,
        role_id: RoleId,
        name: str | None = None,
        tenant_id: TenantId | None = None,
        description: str | None = None,
    ) -> Role:
        role = self._repo.get_by_id(role_id)
        if not role:
            raise ValueError("Role not found")

        effective_tenant_id = tenant_id if tenant_id is not None else role.tenant_id
        if name is not None and name != role.name:
            if self._repo.get_by_name(name, effective_tenant_id):
                raise ValueError("Role name already in use")
            role.name = name
        if tenant_id is not None:
            role.tenant_id = tenant_id
        if description is not None:
            role.description = description

        return self._repo.update(role)

    def replace_role(self, role_id: RoleId, name: str, tenant_id: TenantId | None = None, description: str = "") -> Role:
        role = self._repo.get_by_id(role_id)
        if not role:
            raise ValueError("Role not found")
        if (name != role.name or tenant_id != role.tenant_id) and self._repo.get_by_name(name, tenant_id):
            raise ValueError("Role name already in use")
        role.name = name
        role.tenant_id = tenant_id
        role.description = description
        return self._repo.update(role)

    def delete_role(self, role_id: RoleId) -> None:
        if not self._repo.get_by_id(role_id):
            raise ValueError("Role not found")
        self._repo.delete(role_id)


class PermissionUseCases:
    def __init__(self, repo: PermissionRepository) -> None:
        self._repo = repo

    def list_permissions(self) -> list[Permission]:
        return self._repo.list()

    def get_permission(self, permission_id: PermissionId) -> Permission | None:
        return self._repo.get_by_id(permission_id)

    def create_permission(self, name: str, resource: str, action: str) -> Permission:
        permission = Permission(
            name=name,
            resource=Resource(resource),
            action=ResourceAction(action),
        )
        return self._repo.create(permission)

    def update_permission(
        self,
        permission_id: PermissionId,
        name: str | None = None,
        resource: str | None = None,
        action: str | None = None,
    ) -> Permission:
        permission = self._repo.get_by_id(permission_id)
        if not permission:
            raise ValueError("Permission not found")
        if name is not None:
            permission.name = name
        if resource is not None:
            permission.resource = Resource(resource)
        if action is not None:
            permission.action = ResourceAction(action)
        return self._repo.update(permission)

    def replace_permission(self, permission_id: PermissionId, name: str, resource: str, action: str) -> Permission:
        permission = self._repo.get_by_id(permission_id)
        if not permission:
            raise ValueError("Permission not found")
        permission.name = name
        permission.resource = Resource(resource)
        permission.action = ResourceAction(action)
        return self._repo.update(permission)

    def delete_permission(self, permission_id: PermissionId) -> None:
        if not self._repo.get_by_id(permission_id):
            raise ValueError("Permission not found")
        self._repo.delete(permission_id)


class UserTenantUseCases:
    def __init__(self, repo: UserTenantRepository) -> None:
        self._repo = repo

    def list_user_tenants(self) -> list[UserTenant]:
        return self._repo.list()

    def get_user_tenant(self, user_tenant_id: UserTenantId) -> UserTenant | None:
        return self._repo.get_by_id(user_tenant_id)

    def create_user_tenant(self, user_id: UserId, tenant_id: TenantId) -> UserTenant:
        return self._repo.create(UserTenant(user_id=user_id, tenant_id=tenant_id))

    def update_user_tenant(
        self,
        user_tenant_id: UserTenantId,
        user_id: UserId | None = None,
        tenant_id: TenantId | None = None,
    ) -> UserTenant:
        user_tenant = self._repo.get_by_id(user_tenant_id)
        if not user_tenant:
            raise ValueError("User tenant link not found")
        if user_id is not None:
            user_tenant.user_id = user_id
        if tenant_id is not None:
            user_tenant.tenant_id = tenant_id
        return self._repo.update(user_tenant)

    def replace_user_tenant(self, user_tenant_id: UserTenantId, user_id: UserId, tenant_id: TenantId) -> UserTenant:
        return self.update_user_tenant(user_tenant_id, user_id=user_id, tenant_id=tenant_id)

    def delete_user_tenant(self, user_tenant_id: UserTenantId) -> None:
        if not self._repo.get_by_id(user_tenant_id):
            raise ValueError("User tenant link not found")
        self._repo.delete(user_tenant_id)


class UserRoleUseCases:
    def __init__(self, repo: UserRoleRepository) -> None:
        self._repo = repo

    def list_user_roles(self) -> list[RoleAssignment]:
        return self._repo.list()

    def get_user_role(self, user_role_id: UserRoleId) -> RoleAssignment | None:
        return self._repo.get_by_id(user_role_id)

    def create_user_role(self, user_id: UserId, role_id: RoleId) -> RoleAssignment:
        return self._repo.create(RoleAssignment(user_id=user_id, role_id=role_id))

    def update_user_role(
        self,
        user_role_id: UserRoleId,
        user_id: UserId | None = None,
        role_id: RoleId | None = None,
    ) -> RoleAssignment:
        user_role = self._repo.get_by_id(user_role_id)
        if not user_role:
            raise ValueError("User role assignment not found")
        if user_id is not None:
            user_role.user_id = user_id
            user_role.group_id = None
            user_role.assignee_type = "user"
        if role_id is not None:
            user_role.role_id = role_id
        return self._repo.update(user_role)

    def replace_user_role(self, user_role_id: UserRoleId, user_id: UserId, role_id: RoleId) -> RoleAssignment:
        return self.update_user_role(user_role_id, user_id=user_id, role_id=role_id)

    def delete_user_role(self, user_role_id: UserRoleId) -> None:
        if not self._repo.get_by_id(user_role_id):
            raise ValueError("User role assignment not found")
        self._repo.delete(user_role_id)


class GroupRoleUseCases:
    def __init__(self, repo: GroupRoleRepository) -> None:
        self._repo = repo

    def list_group_roles(self) -> list[RoleAssignment]:
        return self._repo.list()

    def get_group_role(self, group_role_id: GroupRoleId) -> RoleAssignment | None:
        return self._repo.get_by_id(group_role_id)

    def create_group_role(self, group_id: GroupId, role_id: RoleId) -> RoleAssignment:
        return self._repo.create(RoleAssignment(group_id=group_id, role_id=role_id))

    def update_group_role(
        self,
        group_role_id: GroupRoleId,
        group_id: GroupId | None = None,
        role_id: RoleId | None = None,
    ) -> RoleAssignment:
        group_role = self._repo.get_by_id(group_role_id)
        if not group_role:
            raise ValueError("Group role assignment not found")
        if group_id is not None:
            group_role.group_id = group_id
            group_role.user_id = None
            group_role.assignee_type = "group"
        if role_id is not None:
            group_role.role_id = role_id
        return self._repo.update(group_role)

    def replace_group_role(self, group_role_id: GroupRoleId, group_id: GroupId, role_id: RoleId) -> RoleAssignment:
        return self.update_group_role(group_role_id, group_id=group_id, role_id=role_id)

    def delete_group_role(self, group_role_id: GroupRoleId) -> None:
        if not self._repo.get_by_id(group_role_id):
            raise ValueError("Group role assignment not found")
        self._repo.delete(group_role_id)


class RolePermissionUseCases:
    def __init__(self, repo: RolePermissionRepository) -> None:
        self._repo = repo

    def list_role_permissions(self) -> list[RolePermission]:
        return self._repo.list()

    def get_role_permission(self, role_permission_id: RolePermissionId) -> RolePermission | None:
        return self._repo.get_by_id(role_permission_id)

    def create_role_permission(self, role_id: RoleId, permission_id: PermissionId) -> RolePermission:
        return self._repo.create(RolePermission(role_id=role_id, permission_id=permission_id))

    def update_role_permission(
        self,
        role_permission_id: RolePermissionId,
        role_id: RoleId | None = None,
        permission_id: PermissionId | None = None,
    ) -> RolePermission:
        role_permission = self._repo.get_by_id(role_permission_id)
        if not role_permission:
            raise ValueError("Role permission link not found")
        if role_id is not None:
            role_permission.role_id = role_id
        if permission_id is not None:
            role_permission.permission_id = permission_id
        return self._repo.update(role_permission)

    def replace_role_permission(
        self,
        role_permission_id: RolePermissionId,
        role_id: RoleId,
        permission_id: PermissionId,
    ) -> RolePermission:
        return self.update_role_permission(
            role_permission_id,
            role_id=role_id,
            permission_id=permission_id,
        )

    def delete_role_permission(self, role_permission_id: RolePermissionId) -> None:
        if not self._repo.get_by_id(role_permission_id):
            raise ValueError("Role permission link not found")
        self._repo.delete(role_permission_id)


class GroupMembershipUseCases:
    def __init__(self, repo: GroupMembershipRepository) -> None:
        self._repo = repo

    def list_group_memberships(self) -> list[GroupMembership]:
        return self._repo.list()

    def get_group_membership(self, membership_id: GroupMembershipId) -> GroupMembership | None:
        return self._repo.get_by_id(membership_id)

    def create_group_membership(
        self,
        group_id: GroupId,
        member_type: Literal["user", "group"],
        member_user_id: UserId | None = None,
        member_group_id: GroupId | None = None,
    ) -> GroupMembership:
        membership = GroupMembership(
            group_id=group_id,
            member_type=member_type,
            member_user_id=member_user_id,
            member_group_id=member_group_id,
        )
        return self._repo.create(membership)

    def update_group_membership(
        self,
        membership_id: GroupMembershipId,
        member_type: Literal["user", "group"] | None = None,
        member_user_id: UserId | None = None,
        member_group_id: GroupId | None = None,
    ) -> GroupMembership:
        membership = self._repo.get_by_id(membership_id)
        if not membership:
            raise ValueError("Group membership not found")

        next_member_type = member_type or membership.member_type
        next_user_id = member_user_id if member_type == "user" else member_user_id or membership.member_user_id
        next_group_id = member_group_id if member_type == "group" else member_group_id or membership.member_group_id

        updated = GroupMembership(
            group_id=membership.group_id,
            member_type=next_member_type,
            member_user_id=next_user_id,
            member_group_id=next_group_id,
        )
        object.__setattr__(updated, "id", membership.id)
        return self._repo.update(updated)

    def replace_group_membership(
        self,
        membership_id: GroupMembershipId,
        group_id: GroupId,
        member_type: Literal["user", "group"],
        member_user_id: UserId | None = None,
        member_group_id: GroupId | None = None,
    ) -> GroupMembership:
        if not self._repo.get_by_id(membership_id):
            raise ValueError("Group membership not found")
        replacement = GroupMembership(
            group_id=group_id,
            member_type=member_type,
            member_user_id=member_user_id,
            member_group_id=member_group_id,
        )
        object.__setattr__(replacement, "id", membership_id)
        return self._repo.update(replacement)

    def delete_group_membership(self, membership_id: GroupMembershipId) -> None:
        if not self._repo.get_by_id(membership_id):
            raise ValueError("Group membership not found")
        self._repo.delete(membership_id)
