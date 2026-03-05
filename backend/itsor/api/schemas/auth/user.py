from pydantic import BaseModel


class UserIdentitySchema(BaseModel):
    username: str
    email: str


class UserCreate(UserIdentitySchema):
    password: str


class UserReplace(UserIdentitySchema):
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None


class UserResponse(UserIdentitySchema):
    id: str

    model_config = {"from_attributes": True}


class SignupRequest(UserCreate):
    invite_group_id: str | None = None
    create_tenant_name: str | None = None


class SigninRequest(BaseModel):
    identifier: str
    password: str


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"






