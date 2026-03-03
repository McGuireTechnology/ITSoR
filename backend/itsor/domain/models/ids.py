from __future__ import annotations

from typing import NewType

UserId = NewType("UserId", str)
TenantId = NewType("TenantId", str)
GroupId = NewType("GroupId", str)
RoleId = NewType("RoleId", str)
PermissionId = NewType("PermissionId", str)
UserTenantId = NewType("UserTenantId", str)
GroupMembershipId = NewType("GroupMembershipId", str)
UserRoleId = NewType("UserRoleId", str)
GroupRoleId = NewType("GroupRoleId", str)
RolePermissionId = NewType("RolePermissionId", str)


__all__ = [
    "UserId",
    "TenantId",
    "GroupId",
    "RoleId",
    "PermissionId",
    "UserTenantId",
    "GroupMembershipId",
    "UserRoleId",
    "GroupRoleId",
    "RolePermissionId",
]
