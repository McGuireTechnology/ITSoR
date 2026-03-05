from pydantic import BaseModel


class RolePermissionCreate(BaseModel):
    role_id: str
    permission_id: str


class RolePermissionReplace(RolePermissionCreate):
    pass


class RolePermissionUpdate(BaseModel):
    role_id: str | None = None
    permission_id: str | None = None


class RolePermissionResponse(BaseModel):
    id: str
    role_id: str
    permission_id: str

    model_config = {"from_attributes": True}
