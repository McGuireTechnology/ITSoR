from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str
    tenant_id: str | None = None
    description: str = ""


class RoleReplace(RoleCreate):
    pass


class RoleUpdate(BaseModel):
    name: str | None = None
    tenant_id: str | None = None
    description: str | None = None


class RoleResponse(BaseModel):
    id: str
    name: str
    tenant_id: str | None = None
    description: str

    model_config = {"from_attributes": True}
