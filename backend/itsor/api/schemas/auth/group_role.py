from pydantic import BaseModel


class GroupRoleCreate(BaseModel):
    group_id: str
    role_id: str


class GroupRoleReplace(GroupRoleCreate):
    pass


class GroupRoleUpdate(BaseModel):
    group_id: str | None = None
    role_id: str | None = None


class GroupRoleResponse(BaseModel):
    id: str
    group_id: str
    role_id: str

    model_config = {"from_attributes": True}
