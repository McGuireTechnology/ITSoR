from fastapi import APIRouter, status

from itsor.api.schemas.auth.role_permission import (
    RolePermissionCreate,
    RolePermissionReplace,
    RolePermissionResponse,
    RolePermissionUpdate,
)

router = APIRouter(tags=["role_permissions"])


@router.get("/role_permissions", response_model=list[RolePermissionResponse])
def read_role_permissions():
    pass


@router.post("/role_permissions", response_model=RolePermissionResponse, status_code=status.HTTP_201_CREATED)
def create_role_permission(body: RolePermissionCreate):
    pass


@router.get("/role_permissions/{role_permission_id}", response_model=RolePermissionResponse)
def read_role_permission(role_permission_id: str):
    pass


@router.put("/role_permissions/{role_permission_id}", response_model=RolePermissionResponse)
def replace_role_permission(role_permission_id: str, body: RolePermissionReplace):
    pass


@router.patch("/role_permissions/{role_permission_id}", response_model=RolePermissionResponse)
def update_role_permission(role_permission_id: str, body: RolePermissionUpdate):
    pass


@router.delete("/role_permissions/{role_permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role_permission(role_permission_id: str):
    pass


