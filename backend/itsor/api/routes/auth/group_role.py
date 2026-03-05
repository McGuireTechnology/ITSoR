from fastapi import APIRouter, status

from itsor.api.schemas.auth.group_role import (
    GroupRoleCreate,
    GroupRoleReplace,
    GroupRoleResponse,
    GroupRoleUpdate,
)

router = APIRouter(tags=["group_roles"])


@router.get("/group_roles", response_model=list[GroupRoleResponse])
def read_group_roles():
    pass


@router.post("/group_roles", response_model=GroupRoleResponse, status_code=status.HTTP_201_CREATED)
def create_group_role(body: GroupRoleCreate):
    pass


@router.get("/group_roles/{group_role_id}", response_model=GroupRoleResponse)
def read_group_role(group_role_id: str):
    pass


@router.put("/group_roles/{group_role_id}", response_model=GroupRoleResponse)
def replace_group_role(group_role_id: str, body: GroupRoleReplace):
    pass


@router.patch("/group_roles/{group_role_id}", response_model=GroupRoleResponse)
def update_group_role(group_role_id: str, body: GroupRoleUpdate):
    pass


@router.delete("/group_roles/{group_role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_role(group_role_id: str):
    pass


