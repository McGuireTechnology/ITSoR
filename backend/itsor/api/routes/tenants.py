from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_current_user, get_tenant_use_cases
from itsor.api.schemas.tenant import TenantCreate, TenantUpdate, TenantReplace, TenantResponse
from itsor.domain.models.user import User
from itsor.domain.use_cases.tenant_use_cases import TenantUseCases

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.get("", response_model=List[TenantResponse])
def list_tenants(
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
    _: User = Depends(get_current_user),
):
    return use_cases.list_tenants()


@router.post("", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(
    body: TenantCreate,
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.create_tenant(body.name)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{tenant_id}", response_model=TenantResponse)
def get_tenant(
    tenant_id: str,
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
    _: User = Depends(get_current_user),
):
    tenant = use_cases.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    return tenant


@router.patch("/{tenant_id}", response_model=TenantResponse)
def update_tenant(
    tenant_id: str,
    body: TenantUpdate,
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.update_tenant(tenant_id, body.name)
    except ValueError as exc:
        error_detail = str(exc)
        if error_detail == "Tenant not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_detail)


@router.put("/{tenant_id}", response_model=TenantResponse)
def replace_tenant(
    tenant_id: str,
    body: TenantReplace,
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.replace_tenant(tenant_id, body.name)
    except ValueError as exc:
        error_detail = str(exc)
        if error_detail == "Tenant not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_detail)


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tenant(
    tenant_id: str,
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        use_cases.delete_tenant(tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
