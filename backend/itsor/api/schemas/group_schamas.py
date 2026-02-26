from pydantic import BaseModel

from itsor.api.schemas.base_schemas import TenantScopedNameSchema


class GroupCreate(TenantScopedNameSchema):
    pass


class GroupUpdate(BaseModel):
    name: str | None = None


class GroupReplace(TenantScopedNameSchema):
    pass


class GroupResponse(TenantScopedNameSchema):
    id: str
    owner_id: str | None = None
    group_id: str | None = None
    permissions: int

    model_config = {"from_attributes": True}
