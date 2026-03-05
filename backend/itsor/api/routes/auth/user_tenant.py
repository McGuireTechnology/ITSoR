from fastapi import APIRouter, status

from itsor.api.schemas.auth.user_tenant import (
    UserTenantCreate,
    UserTenantReplace,
    UserTenantResponse,
    UserTenantUpdate,
)

router = APIRouter(tags=["user_tenants"])


@router.get("/user_tenants", response_model=list[UserTenantResponse])
def read_user_tenants():
    pass


@router.post(
    "/user_tenants",
    response_model=UserTenantResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user_tenant(body: UserTenantCreate):
    pass


@router.get("/user_tenants/{user_tenant_id}", response_model=UserTenantResponse)
def read_user_tenant(user_tenant_id: str):
    pass


@router.put("/user_tenants/{user_tenant_id}", response_model=UserTenantResponse)
def replace_user_tenant(user_tenant_id: str, body: UserTenantReplace):
    pass


@router.patch("/user_tenants/{user_tenant_id}", response_model=UserTenantResponse)
def update_user_tenant(user_tenant_id: str, body: UserTenantUpdate):
    pass

@router.delete("/user_tenants/{user_tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_tenant(user_tenant_id: str):
    pass


