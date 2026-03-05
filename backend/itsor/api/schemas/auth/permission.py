from pydantic import BaseModel


class PermissionCreate(BaseModel):
    name: str
    resource: str
    action: str


class PermissionReplace(PermissionCreate):
    pass


class PermissionUpdate(BaseModel):
    name: str | None = None
    resource: str | None = None
    action: str | None = None


class PermissionResponse(BaseModel):
    id: str
    name: str
    resource: str
    action: str

    model_config = {"from_attributes": True}
