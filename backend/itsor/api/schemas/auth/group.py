from pydantic import BaseModel

from itsor.api.schemas.base_schemas import TenantScopedNameSchema


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
