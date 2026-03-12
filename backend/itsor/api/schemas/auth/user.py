from pydantic import BaseModel


class UserIdentitySchema(BaseModel):
    name: str
    username: str
    email: str
    group_id: str | None = None


class UserCreate(UserIdentitySchema):
    password: str
    invite_group_id: str | None = None
    create_tenant_name: str | None = None


class UserReplace(UserIdentitySchema):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    username: str | None = None
    email: str | None = None
    group_id: str | None = None
    password: str | None = None


class UserResponse(UserIdentitySchema):
    id: str

    model_config = {"from_attributes": True}


class SignupRequest(UserCreate):
    pass


class SigninRequest(BaseModel):
    identifier: str
    password: str


class AuthTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"






