from fastapi import APIRouter, status

from itsor.api.schemas.auth.permission import (
    PermissionCreate,
    PermissionReplace,
    PermissionResponse,
    PermissionUpdate,
)

router = APIRouter(tags=["permissions"])


@router.get("/permissions", response_model=list[PermissionResponse])
def read_permissions():
    pass


@router.post("/permissions", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
def create_permission(body: PermissionCreate):
    pass


@router.get("/permissions/{permission_id}", response_model=PermissionResponse)
def read_permission(permission_id: str):
    pass


@router.put("/permissions/{permission_id}", response_model=PermissionResponse)
def replace_permission(permission_id: str, body: PermissionReplace):
    pass


@router.patch("/permissions/{permission_id}", response_model=PermissionResponse)
def update_permission(permission_id: str, body: PermissionUpdate):
    pass


@router.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(permission_id: str):
    pass


