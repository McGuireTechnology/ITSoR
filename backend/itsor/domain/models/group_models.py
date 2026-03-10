from dataclasses import dataclass, field
from typing import Literal

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import GroupId, GroupMembershipId, TenantId, UserId
from itsor.domain.models.resource_models import ResourcePermissionAction
from itsor.domain.models.role_models import RoleAssignment


@dataclass
class Group:
    id: GroupId = field(default_factory=typed_ulid_factory(GroupId), init=False)
    tenant_id: TenantId | None
    name: str
    owner_id: UserId | None = None
    group_id: GroupId | None = None
    permissions: int | None = None
    platform_endpoint_permissions: dict[str, list[ResourcePermissionAction | str]] = field(
        default_factory=dict
    )


@dataclass
class GroupMembership:
    id: GroupMembershipId = field(
        default_factory=typed_ulid_factory(GroupMembershipId), init=False
    )
    group_id: GroupId
    member_type: Literal["user", "group"]
    member_user_id: UserId | None = None
    member_group_id: GroupId | None = None

    def __post_init__(self) -> None:
        if self.member_type == "user":
            if self.member_user_id is None or self.member_group_id is not None:
                raise ValueError("user membership requires member_user_id only")
            return

        if self.member_type == "group":
            if self.member_group_id is None or self.member_user_id is not None:
                raise ValueError("group membership requires member_group_id only")
            return

        raise ValueError("member_type must be 'user' or 'group'")


GroupRole = RoleAssignment


__all__ = ["Group", "GroupMembership", "GroupRole"]
