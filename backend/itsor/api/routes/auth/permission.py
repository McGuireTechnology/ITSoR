from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_current_user, get_permission_use_cases
from itsor.api.schemas.auth.permission import (
    PermissionCreate,
    PermissionReplace,
    PermissionResponse,
    PermissionUpdate,
)
from itsor.application.use_cases.auth import PermissionUseCases
from itsor.domain.ids import PermissionId

router = APIRouter(prefix="/permissions", tags=["permissions"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[PermissionResponse])
def read_permissions(use_cases: PermissionUseCases = Depends(get_permission_use_cases)):
    return use_cases.list_permissions()


@router.post("/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
def create_permission(body: PermissionCreate, use_cases: PermissionUseCases = Depends(get_permission_use_cases)):
    return use_cases.create_permission(name=body.name, resource=body.resource, action=body.action)


@router.get("/{permission_id}", response_model=PermissionResponse)
def read_permission(permission_id: PermissionId, use_cases: PermissionUseCases = Depends(get_permission_use_cases)):
    permission = use_cases.get_permission(permission_id)
    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return permission


@router.put("/{permission_id}", response_model=PermissionResponse)
def replace_permission(
    permission_id: PermissionId,
    body: PermissionReplace,
    use_cases: PermissionUseCases = Depends(get_permission_use_cases),
):
    try:
        return use_cases.replace_permission(
            permission_id=permission_id,
            name=body.name,
            resource=body.resource,
            action=body.action,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{permission_id}", response_model=PermissionResponse)
def update_permission(
    permission_id: PermissionId,
    body: PermissionUpdate,
    use_cases: PermissionUseCases = Depends(get_permission_use_cases),
):
    try:
        return use_cases.update_permission(
            permission_id=permission_id,
            name=body.name,
            resource=body.resource,
            action=body.action,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(permission_id: PermissionId, use_cases: PermissionUseCases = Depends(get_permission_use_cases)):
    try:
        use_cases.delete_permission(permission_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return None


