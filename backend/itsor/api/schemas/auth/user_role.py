from pydantic import BaseModel


class UserRoleCreate(BaseModel):
    user_id: str
    role_id: str


class UserRoleReplace(UserRoleCreate):
    pass


class UserRoleUpdate(BaseModel):
    user_id: str | None = None
    role_id: str | None = None


class UserRoleResponse(BaseModel):
    id: str
    user_id: str
    role_id: str

    model_config = {"from_attributes": True}
