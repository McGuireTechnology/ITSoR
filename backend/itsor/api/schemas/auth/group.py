from pydantic import BaseModel


class TenantScopedNameSchema(BaseModel):
    name: str
    tenant_id: str | None = None


class GroupCreate(TenantScopedNameSchema):
    pass


class GroupReplace(TenantScopedNameSchema):
    pass


class GroupUpdate(BaseModel):
    name: str | None = None
    tenant_id: str | None = None


class GroupResponse(TenantScopedNameSchema):
    id: str

    model_config = {"from_attributes": True}
