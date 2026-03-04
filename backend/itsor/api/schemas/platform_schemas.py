from typing import Literal

from pydantic import BaseModel, field_validator

from itsor.api.schemas.base_schemas import NameSchema, TenantScopedNameSchema, UserIdentitySchema


PlatformPermissionAction = Literal["create", "read", "update", "delete"]

_PLATFORM_PERMISSION_ACTIONS = {
    "create",
    "read",
    "update",
    "delete",
}


def _coerce_resource_action(value):
    if isinstance(value, int):
        nibble_map = {1: "create", 2: "read", 4: "update", 8: "delete"}
        if value not in nibble_map:
            raise ValueError("Invalid action nibble")
        return nibble_map[value]
    if isinstance(value, str):
        trimmed = value.strip().lower()
        if trimmed.isdigit():
            return _coerce_resource_action(int(trimmed))
        return trimmed
    return value


class UserCreate(UserIdentitySchema):
    password: str
    invite_group_id: str | None = None
    create_tenant_name: str | None = None
    platform_endpoint_permissions: dict[str, list[str]] | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    platform_endpoint_permissions: dict[str, list[str]] | None = None


class UserReplace(UserIdentitySchema):
    password: str
    platform_endpoint_permissions: dict[str, list[str]] | None = None


class UserResponse(UserIdentitySchema):
    id: str
    group_id: str | None = None
    platform_endpoint_permissions: dict[str, list[str]]

    model_config = {"from_attributes": True}


class TenantCreate(NameSchema):
    pass


class TenantUpdate(BaseModel):
    name: str | None = None


class TenantReplace(NameSchema):
    pass


class TenantResponse(NameSchema):
    id: str
    owner_id: str | None = None
    group_id: str | None = None
    permissions: int

    model_config = {"from_attributes": True}


class GroupCreate(TenantScopedNameSchema):
    platform_endpoint_permissions: dict[str, list[str]] | None = None


class GroupUpdate(BaseModel):
    name: str | None = None
    platform_endpoint_permissions: dict[str, list[str]] | None = None


class GroupReplace(TenantScopedNameSchema):
    platform_endpoint_permissions: dict[str, list[str]] | None = None


class GroupResponse(TenantScopedNameSchema):
    id: str
    owner_id: str | None = None
    group_id: str | None = None
    permissions: int
    platform_endpoint_permissions: dict[str, list[str]]

    model_config = {"from_attributes": True}


class PlatformRoleCreate(BaseModel):
    name: str
    tenant_id: str | None = None
    description: str = ""


class PlatformRoleUpdate(BaseModel):
    name: str | None = None
    tenant_id: str | None = None
    description: str | None = None


class PlatformRoleResponse(BaseModel):
    id: str
    name: str
    tenant_id: str | None = None
    description: str

    model_config = {"from_attributes": True}


class PlatformPermissionCreate(BaseModel):
    name: str
    resource: str
    action: PlatformPermissionAction

    @field_validator("action", mode="before")
    @classmethod
    def validate_action(cls, value):
        action = _coerce_resource_action(value)
        if action not in _PLATFORM_PERMISSION_ACTIONS:
            raise ValueError(
                "Platform permission action must be one of: create, read, update, delete"
            )
        return action


class PlatformPermissionUpdate(BaseModel):
    name: str | None = None
    resource: str | None = None
    action: PlatformPermissionAction | None = None

    @field_validator("action", mode="before")
    @classmethod
    def validate_action(cls, value):
        if value is None:
            return None
        action = _coerce_resource_action(value)
        if action not in _PLATFORM_PERMISSION_ACTIONS:
            raise ValueError(
                "Platform permission action must be one of: create, read, update, delete"
            )
        return action


class PlatformPermissionResponse(BaseModel):
    id: str
    name: str
    resource: str
    action: PlatformPermissionAction

    @field_validator("action", mode="before")
    @classmethod
    def validate_action(cls, value):
        return _coerce_resource_action(value)

    model_config = {"from_attributes": True}


class PlatformUserTenantCreate(BaseModel):
    user_id: str
    tenant_id: str


class PlatformUserTenantUpdate(BaseModel):
    user_id: str | None = None
    tenant_id: str | None = None


class PlatformUserTenantResponse(BaseModel):
    id: str
    user_id: str
    tenant_id: str

    model_config = {"from_attributes": True}


class PlatformUserRoleCreate(BaseModel):
    user_id: str
    role_id: str


class PlatformUserRoleUpdate(BaseModel):
    user_id: str | None = None
    role_id: str | None = None


class PlatformUserRoleResponse(BaseModel):
    id: str
    user_id: str
    role_id: str

    model_config = {"from_attributes": True}


class PlatformGroupRoleCreate(BaseModel):
    group_id: str
    role_id: str


class PlatformGroupRoleUpdate(BaseModel):
    group_id: str | None = None
    role_id: str | None = None


class PlatformGroupRoleResponse(BaseModel):
    id: str
    group_id: str
    role_id: str

    model_config = {"from_attributes": True}


class PlatformRolePermissionCreate(BaseModel):
    role_id: str
    permission_id: str


class PlatformRolePermissionUpdate(BaseModel):
    role_id: str | None = None
    permission_id: str | None = None


class PlatformRolePermissionResponse(BaseModel):
    id: str
    role_id: str
    permission_id: str

    model_config = {"from_attributes": True}


class PlatformGroupMembershipCreate(BaseModel):
    group_id: str
    member_type: str
    member_user_id: str | None = None
    member_group_id: str | None = None


class PlatformGroupMembershipUpdate(BaseModel):
    member_type: str | None = None
    member_user_id: str | None = None
    member_group_id: str | None = None


class PlatformGroupMembershipResponse(BaseModel):
    id: str
    group_id: str
    member_type: str
    member_user_id: str | None = None
    member_group_id: str | None = None

    model_config = {"from_attributes": True}