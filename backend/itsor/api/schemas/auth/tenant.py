from pydantic import BaseModel


class NameSchema(BaseModel):
    name: str


class TenantCreate(NameSchema):
    pass


class TenantReplace(NameSchema):
    pass


class TenantUpdate(BaseModel):
    name: str | None = None


class TenantResponse(NameSchema):
    id: str

    model_config = {"from_attributes": True}
