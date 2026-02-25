from pydantic import BaseModel

from itsor.api.schemas.base_schemas import UserIdentitySchema


class LoginRequest(BaseModel):
    identifier: str
    password: str


class SignupRequest(UserIdentitySchema):
    password: str
    invite_group_id: str | None = None
    create_tenant_name: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
