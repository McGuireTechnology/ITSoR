from pydantic import BaseModel

from itsor.api.schemas.base_schemas import UserIdentitySchema
from itsor.domain.models import ResourceAction


class UserCreate(UserIdentitySchema):
    password: str
    invite_group_id: str | None = None
    create_tenant_name: str | None = None
    platform_endpoint_permissions: dict[str, list[ResourceAction | str]] | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None
    platform_endpoint_permissions: dict[str, list[ResourceAction | str]] | None = None


class UserReplace(UserIdentitySchema):
    password: str
    platform_endpoint_permissions: dict[str, list[ResourceAction | str]] | None = None


class UserResponse(UserIdentitySchema):
    id: str
    group_id: str | None = None
    platform_endpoint_permissions: dict[str, list[ResourceAction | str]]

    model_config = {"from_attributes": True}
