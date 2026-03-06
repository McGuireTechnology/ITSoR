from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_current_user, get_role_use_cases
from itsor.api.schemas.auth.role import RoleCreate, RoleReplace, RoleResponse, RoleUpdate
from itsor.application.use_cases.auth import RoleUseCases
from itsor.domain.ids import RoleId, TenantId

router = APIRouter(prefix="/roles", tags=["roles"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[RoleResponse])
def read_roles(use_cases: RoleUseCases = Depends(get_role_use_cases)):
    return use_cases.list_roles()


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(body: RoleCreate, use_cases: RoleUseCases = Depends(get_role_use_cases)):
    try:
        tenant_id = TenantId(body.tenant_id) if body.tenant_id else None
        return use_cases.create_role(name=body.name, tenant_id=tenant_id, description=body.description)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{role_id}", response_model=RoleResponse)
def read_role(role_id: RoleId, use_cases: RoleUseCases = Depends(get_role_use_cases)):
    role = use_cases.get_role(role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role


@router.put("/{role_id}", response_model=RoleResponse)
def replace_role(role_id: RoleId, body: RoleReplace, use_cases: RoleUseCases = Depends(get_role_use_cases)):
    try:
        tenant_id = TenantId(body.tenant_id) if body.tenant_id else None
        return use_cases.replace_role(
            role_id=role_id,
            name=body.name,
            tenant_id=tenant_id,
            description=body.description,
        )
    except ValueError as exc:
        message = str(exc)
        code = status.HTTP_409_CONFLICT if "already" in message.lower() else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=code, detail=message)


@router.patch("/{role_id}", response_model=RoleResponse)
def update_role(role_id: RoleId, body: RoleUpdate, use_cases: RoleUseCases = Depends(get_role_use_cases)):
    try:
        tenant_id = TenantId(body.tenant_id) if body.tenant_id else None
        return use_cases.update_role(
            role_id=role_id,
            name=body.name,
            tenant_id=tenant_id,
            description=body.description,
        )
    except ValueError as exc:
        message = str(exc)
        code = status.HTTP_409_CONFLICT if "already" in message.lower() else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=code, detail=message)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: RoleId, use_cases: RoleUseCases = Depends(get_role_use_cases)):
    try:
        use_cases.delete_role(role_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return None


