from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_current_user, get_user_tenant_use_cases
from itsor.api.schemas.auth.user_tenant import (
    UserTenantCreate,
    UserTenantReplace,
    UserTenantResponse,
    UserTenantUpdate,
)
from itsor.application.use_cases.auth import UserTenantUseCases
from itsor.domain.ids import TenantId, UserId, UserTenantId

router = APIRouter(
    prefix="/user_tenants",
    tags=["user_tenants"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[UserTenantResponse])
def read_user_tenants(use_cases: UserTenantUseCases = Depends(get_user_tenant_use_cases)):
    return use_cases.list_user_tenants()


@router.post(
    "/",
    response_model=UserTenantResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user_tenant(
    body: UserTenantCreate,
    use_cases: UserTenantUseCases = Depends(get_user_tenant_use_cases),
):
    return use_cases.create_user_tenant(user_id=UserId(body.user_id), tenant_id=TenantId(body.tenant_id))


@router.get("/{user_tenant_id}", response_model=UserTenantResponse)
def read_user_tenant(user_tenant_id: UserTenantId, use_cases: UserTenantUseCases = Depends(get_user_tenant_use_cases)):
    row = use_cases.get_user_tenant(user_tenant_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User tenant link not found")
    return row


@router.put("/{user_tenant_id}", response_model=UserTenantResponse)
def replace_user_tenant(
    user_tenant_id: UserTenantId,
    body: UserTenantReplace,
    use_cases: UserTenantUseCases = Depends(get_user_tenant_use_cases),
):
    try:
        return use_cases.replace_user_tenant(
            user_tenant_id=user_tenant_id,
            user_id=UserId(body.user_id),
            tenant_id=TenantId(body.tenant_id),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{user_tenant_id}", response_model=UserTenantResponse)
def update_user_tenant(
    user_tenant_id: UserTenantId,
    body: UserTenantUpdate,
    use_cases: UserTenantUseCases = Depends(get_user_tenant_use_cases),
):
    try:
        return use_cases.update_user_tenant(
            user_tenant_id=user_tenant_id,
            user_id=UserId(body.user_id) if body.user_id is not None else None,
            tenant_id=TenantId(body.tenant_id) if body.tenant_id is not None else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

@router.delete("/{user_tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_tenant(
    user_tenant_id: UserTenantId,
    use_cases: UserTenantUseCases = Depends(get_user_tenant_use_cases),
):
    try:
        use_cases.delete_user_tenant(user_tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return None


