from pydantic import BaseModel

from itsor.api.schemas.base_schemas import UserIdentitySchema


class UserCreate(UserIdentitySchema):
    password: str
    invite_group_id: str | None = None
    create_tenant_name: str | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None


class UserReplace(UserIdentitySchema):
    password: str


class UserResponse(UserIdentitySchema):
    id: str
    group_id: str | None = None

    model_config = {"from_attributes": True}
