from pydantic import BaseModel


class TenantBase(BaseModel):
    name: str


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    name: str | None = None


class TenantReplace(TenantBase):
    pass


class TenantResponse(TenantBase):
    id: str

    model_config = {"from_attributes": True}
