from typing import NewType

GroupId = NewType("GroupId", str)
GroupMembershipId = NewType("GroupMembershipId", str)
GroupRoleId = NewType("GroupRoleId", str)

__all__ = ["GroupId", "GroupMembershipId", "GroupRoleId"]
