from fastapi import APIRouter, status

from itsor.api.schemas.auth.tenant import TenantCreate, TenantReplace, TenantResponse, TenantUpdate

router = APIRouter(tags=["tenants"])


@router.get("/tenants", response_model=list[TenantResponse])
def read_tenants():
    pass


@router.post("/tenants", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(body: TenantCreate):
    pass


@router.get("/tenants/{tenant_id}", response_model=TenantResponse)
def read_tenant(tenant_id: str):
    pass


@router.put("/tenants/{tenant_id}", response_model=TenantResponse)
def replace_tenant(tenant_id: str, body: TenantReplace):
    pass


@router.patch("/tenants/{tenant_id}", response_model=TenantResponse)
def update_tenant(tenant_id: str, body: TenantUpdate):
    pass


@router.delete("/tenants/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tenant(tenant_id: str):
    pass


