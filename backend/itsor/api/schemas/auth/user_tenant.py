from pydantic import BaseModel


class UserTenantCreate(BaseModel):
    user_id: str
    tenant_id: str


class UserTenantReplace(UserTenantCreate):
    pass


class UserTenantUpdate(BaseModel):
    user_id: str | None = None
    tenant_id: str | None = None


class UserTenantResponse(BaseModel):
    id: str
    user_id: str
    tenant_id: str

    model_config = {"from_attributes": True}
