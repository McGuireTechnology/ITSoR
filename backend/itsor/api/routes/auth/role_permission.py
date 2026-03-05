from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_role_permission_use_cases
from itsor.api.schemas.auth.role_permission import (
    RolePermissionCreate,
    RolePermissionReplace,
    RolePermissionResponse,
    RolePermissionUpdate,
)
from itsor.application.use_cases.auth import RolePermissionUseCases
from itsor.domain.ids import PermissionId, RoleId, RolePermissionId

router = APIRouter(prefix="/role_permissions", tags=["role_permissions"])


@router.get("/", response_model=list[RolePermissionResponse])
def read_role_permissions(use_cases: RolePermissionUseCases = Depends(get_role_permission_use_cases)):
    return use_cases.list_role_permissions()


@router.post("/", response_model=RolePermissionResponse, status_code=status.HTTP_201_CREATED)
def create_role_permission(body: RolePermissionCreate, use_cases: RolePermissionUseCases = Depends(get_role_permission_use_cases)):
    return use_cases.create_role_permission(role_id=RoleId(body.role_id), permission_id=PermissionId(body.permission_id))


@router.get("/{role_permission_id}", response_model=RolePermissionResponse)
def read_role_permission(
    role_permission_id: RolePermissionId,
    use_cases: RolePermissionUseCases = Depends(get_role_permission_use_cases),
):
    row = use_cases.get_role_permission(role_permission_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role permission link not found")
    return row


@router.put("/{role_permission_id}", response_model=RolePermissionResponse)
def replace_role_permission(
    role_permission_id: RolePermissionId,
    body: RolePermissionReplace,
    use_cases: RolePermissionUseCases = Depends(get_role_permission_use_cases),
):
    try:
        return use_cases.replace_role_permission(
            role_permission_id=role_permission_id,
            role_id=RoleId(body.role_id),
            permission_id=PermissionId(body.permission_id),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{role_permission_id}", response_model=RolePermissionResponse)
def update_role_permission(
    role_permission_id: RolePermissionId,
    body: RolePermissionUpdate,
    use_cases: RolePermissionUseCases = Depends(get_role_permission_use_cases),
):
    try:
        return use_cases.update_role_permission(
            role_permission_id=role_permission_id,
            role_id=RoleId(body.role_id) if body.role_id is not None else None,
            permission_id=PermissionId(body.permission_id) if body.permission_id is not None else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{role_permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role_permission(
    role_permission_id: RolePermissionId,
    use_cases: RolePermissionUseCases = Depends(get_role_permission_use_cases),
):
    try:
        use_cases.delete_role_permission(role_permission_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return None


