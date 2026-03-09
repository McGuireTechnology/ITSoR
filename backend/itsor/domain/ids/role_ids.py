from typing import NewType

RoleId = NewType("RoleId", str)
RoleAssignmentId = NewType("RoleAssignmentId", str)
RolePermissionId = NewType("RolePermissionId", str)

__all__ = ["RoleId", "RoleAssignmentId", "RolePermissionId"]
