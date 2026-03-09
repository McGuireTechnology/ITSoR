from typing import NewType

UserId = NewType("UserId", str)
UserRoleId = NewType("UserRoleId", str)
UserTenantId = NewType("UserTenantId", str)

__all__ = ["UserId", "UserRoleId", "UserTenantId"]
