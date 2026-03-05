from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_tenant_use_cases
from itsor.api.schemas.auth.tenant import TenantCreate, TenantReplace, TenantResponse, TenantUpdate
from itsor.application.use_cases.auth import TenantUseCases
from itsor.domain.ids import TenantId

router = APIRouter(prefix="/tenants", tags=["tenants"])


@router.get("/", response_model=list[TenantResponse])
def read_tenants(use_cases: TenantUseCases = Depends(get_tenant_use_cases)):
    return use_cases.list_tenants()


@router.post("/", response_model=TenantResponse, status_code=status.HTTP_201_CREATED)
def create_tenant(body: TenantCreate, use_cases: TenantUseCases = Depends(get_tenant_use_cases)):
    try:
        return use_cases.create_tenant(name=body.name)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{tenant_id}", response_model=TenantResponse)
def read_tenant(tenant_id: TenantId, use_cases: TenantUseCases = Depends(get_tenant_use_cases)):
    tenant = use_cases.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    return tenant


@router.put("/{tenant_id}", response_model=TenantResponse)
def replace_tenant(
    tenant_id: TenantId,
    body: TenantReplace,
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
):
    try:
        return use_cases.replace_tenant(tenant_id=tenant_id, name=body.name)
    except ValueError as exc:
        message = str(exc)
        code = status.HTTP_409_CONFLICT if "already" in message.lower() else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=code, detail=message)


@router.patch("/{tenant_id}", response_model=TenantResponse)
def update_tenant(
    tenant_id: TenantId,
    body: TenantUpdate,
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
):
    try:
        return use_cases.update_tenant(tenant_id=tenant_id, name=body.name)
    except ValueError as exc:
        message = str(exc)
        code = status.HTTP_409_CONFLICT if "already" in message.lower() else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=code, detail=message)


@router.delete("/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tenant(tenant_id: TenantId, use_cases: TenantUseCases = Depends(get_tenant_use_cases)):
    try:
        use_cases.delete_tenant(tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return None


