from pydantic import BaseModel


class NameSchema(BaseModel):
    name: str
    owner_id: str | None = None
    group_id: str | None = None
    permissions: int | None = None


class TenantCreate(NameSchema):
    pass


class TenantReplace(NameSchema):
    pass


class TenantUpdate(BaseModel):
    name: str | None = None
    owner_id: str | None = None
    group_id: str | None = None
    permissions: int | None = None


class TenantResponse(NameSchema):
    id: str

    model_config = {"from_attributes": True}
