from pydantic import BaseModel, field_validator

from itsor.domain.models import ResourceAction


def _coerce_resource_action(value):
    if isinstance(value, ResourceAction):
        return value
    if isinstance(value, int):
        return ResourceAction.from_nibble(value)
    if isinstance(value, str):
        trimmed = value.strip().lower()
        if trimmed.isdigit():
            return ResourceAction.from_nibble(int(trimmed))
        return ResourceAction.from_verb(trimmed)
    return value


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
    action: ResourceAction

    @field_validator("action", mode="before")
    @classmethod
    def validate_action(cls, value):
        return _coerce_resource_action(value)


class PlatformPermissionUpdate(BaseModel):
    name: str | None = None
    resource: str | None = None
    action: ResourceAction | None = None

    @field_validator("action", mode="before")
    @classmethod
    def validate_action(cls, value):
        if value is None:
            return None
        return _coerce_resource_action(value)


class PlatformPermissionResponse(BaseModel):
    id: str
    name: str
    resource: str
    action: ResourceAction

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
