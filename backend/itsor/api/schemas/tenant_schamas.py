from pydantic import BaseModel

from itsor.api.schemas.base_schemas import NameSchema


class TenantCreate(NameSchema):
    pass


class TenantUpdate(BaseModel):
    name: str | None = None


class TenantReplace(NameSchema):
    pass


class TenantResponse(NameSchema):
    id: str
    owner_id: str | None = None
    group_id: str | None = None
    permissions: int

    model_config = {"from_attributes": True}
