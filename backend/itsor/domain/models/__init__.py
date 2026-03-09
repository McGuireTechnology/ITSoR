# Domain Models Layer

from itsor.domain.ids import GroupId, PermissionId, RoleId, TenantId, UserId
from itsor.domain.models.group_models import Group, GroupMembership, GroupRole
from itsor.domain.models.permission_models import (
    AclPolicy,
    AclPrincipal,
    AclPrincipalType,
    AclRowPredicate,
    AclScope,
    GroupAclPolicy,
    OwnerAclPolicy,
    Permission,
    PermissionEffect,
    ResourceAclPolicy,
    RowAclPolicy,
)
from itsor.domain.models.resource_models import Resource, ResourceAction
from itsor.domain.models.role_models import Role, RoleAssignment, RolePermission
from itsor.domain.models.tenant_models import Tenant
from itsor.domain.models.user_models import User, UserRole, UserTenant

GroupMember = GroupMembership

__all__ = [
    "Group",
    "GroupMembership",
    "GroupMember",
    "GroupRole",
    "UserId",
    "TenantId",
    "GroupId",
    "RoleId",
    "PermissionId",
    "Permission",
    "PermissionEffect",
    "AclScope",
    "AclPrincipalType",
    "AclPrincipal",
    "AclRowPredicate",
    "AclPolicy",
    "Resource",
    "ResourceAction",
    "ResourceAclPolicy",
    "RowAclPolicy",
    "OwnerAclPolicy",
    "GroupAclPolicy",
    "Role",
    "RoleAssignment",
    "RolePermission",
    "Tenant",
    "User",
    "UserTenant",
    "UserRole",
]
