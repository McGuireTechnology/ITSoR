# Domain Models Layer
import warnings

from itsor.domain.ids import GroupId, PermissionId, RoleId, TenantId, UserId
from itsor.domain.models.group_models import Group, GroupMembership, GroupRole
from itsor.domain.models.module_models import (
    Module,
    ModuleRole,
    ModuleType,
    ModuleUser,
)
from itsor.domain.models.resource_models import (
    Action,
    ActionType,
    Column,
    ColumnType,
    ModuleResource,
    Resource,
    ResourceAction,
    ResourceActionType,
    ResourceAutomationBot,
    ResourceAutomationEvent,
    ResourceAutomationProcess,
    ResourceAutomationTask,
    ResourceAutomationTaskScalar,
    ResourceAutomationTaskType,
    ResourceAutomationTaskValue,
    ResourceAutomationTriggerType,
    ResourcePermissionAction,
    ResourceRecord,
    ResourceRecordScalar,
    ResourceRecordValue,
    ResourceSecurityRule,
    ResourceAttribute,
    ResourceAttributeType,
    ResourceSlice,
    Row,
    RowScalar,
    RowValue,
    SecurityRule,
    Slice,
    Table,
)
from itsor.domain.models.view_models import (
    AppView,
    AppViewType,
    ItemType,
    NavigationItem,
    NavigationView,
    ViewType,
)
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
from itsor.domain.models.role_models import Role, RoleAssignment, RolePermission
from itsor.domain.models.tenant_models import Tenant
from itsor.domain.models.user_models import User, UserRole, UserTenant

GroupMember = GroupMembership
DEFAULT_PERMISSIONS = 0
_DEPRECATED_ALIASES: dict[str, type[object]] = {
    "App": Module,
    "AppRole": ModuleRole,
    "AppUser": ModuleUser,
}


def __getattr__(name: str) -> type[object]:
    if name in _DEPRECATED_ALIASES:
        warnings.warn(
            f"`{name}` is deprecated and will be removed in a future release. Use `{_DEPRECATED_ALIASES[name].__name__}` instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return _DEPRECATED_ALIASES[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "Group",
    "GroupMembership",
    "GroupMember",
    "DEFAULT_PERMISSIONS",
    "GroupRole",
    "UserId",
    "TenantId",
    "GroupId",
    "RoleId",
    "PermissionId",
    "Permission",
    "PermissionEffect",
    "Module",
    "ModuleRole",
    "ModuleType",
    "ModuleUser",
    "ModuleResource",
    "AppView",
    "AppViewType",
    "NavigationView",
    "ViewType",
    "NavigationItem",
    "ItemType",
    "AclScope",
    "AclPrincipalType",
    "AclPrincipal",
    "AclRowPredicate",
    "AclPolicy",
    "Resource",
    "ResourceAttribute",
    "ResourceAttributeType",
    "ResourcePermissionAction",
    "ResourceAction",
    "ResourceActionType",
    "ResourceAutomationBot",
    "ResourceAutomationEvent",
    "ResourceAutomationProcess",
    "ResourceAutomationTask",
    "ResourceAutomationTaskScalar",
    "ResourceAutomationTaskType",
    "ResourceAutomationTaskValue",
    "ResourceAutomationTriggerType",
    "Action",
    "ActionType",
    "ResourceRecord",
    "ResourceRecordScalar",
    "ResourceRecordValue",
    "ResourceSecurityRule",
    "ResourceSlice",
    "Row",
    "RowScalar",
    "RowValue",
    "SecurityRule",
    "Slice",
    "Table",
    "Column",
    "ColumnType",
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
