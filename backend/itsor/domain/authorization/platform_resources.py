from __future__ import annotations

from enum import Enum

from itsor.domain.authorization.resources import ResourceAction, ResourceCatalog, ResourceProvider


class PlatformResource(str, Enum):
    USER = "platform.user"
    TENANT = "platform.tenant"
    GROUP = "platform.group"
    ROLE = "platform.role"
    PERMISSION = "platform.permission"
    USER_TENANT = "platform.user_tenant"
    GROUP_MEMBERSHIP = "platform.group_membership"
    USER_ROLE = "platform.user_role"
    GROUP_ROLE = "platform.group_role"
    ROLE_PERMISSION = "platform.role_permission"


_ITEM_ACTIONS = frozenset(
    (
        ResourceAction.CREATE,
        ResourceAction.READ,
        ResourceAction.UPDATE,
        ResourceAction.DELETE,
    )
)


PLATFORM_RESOURCE_CATALOG: ResourceCatalog = {
    PlatformResource.USER.value: _ITEM_ACTIONS,
    PlatformResource.TENANT.value: _ITEM_ACTIONS,
    PlatformResource.GROUP.value: _ITEM_ACTIONS,
    PlatformResource.ROLE.value: _ITEM_ACTIONS,
    PlatformResource.PERMISSION.value: _ITEM_ACTIONS,
    PlatformResource.USER_TENANT.value: _ITEM_ACTIONS,
    PlatformResource.GROUP_MEMBERSHIP.value: _ITEM_ACTIONS,
    PlatformResource.USER_ROLE.value: _ITEM_ACTIONS,
    PlatformResource.GROUP_ROLE.value: _ITEM_ACTIONS,
    PlatformResource.ROLE_PERMISSION.value: _ITEM_ACTIONS,
}


class PlatformResourceProvider(ResourceProvider):
    @classmethod
    def catalog(cls) -> ResourceCatalog:
        return PLATFORM_RESOURCE_CATALOG
