from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_group_role_use_cases
from itsor.api.schemas.auth.group_role import (
    GroupRoleCreate,
    GroupRoleReplace,
    GroupRoleResponse,
    GroupRoleUpdate,
)
from itsor.application.use_cases.auth import GroupRoleUseCases
from itsor.domain.ids import GroupId, GroupRoleId, RoleId

router = APIRouter(prefix="/group_roles", tags=["group_roles"])


@router.get("/", response_model=list[GroupRoleResponse])
def read_group_roles(use_cases: GroupRoleUseCases = Depends(get_group_role_use_cases)):
    return use_cases.list_group_roles()


@router.post("/", response_model=GroupRoleResponse, status_code=status.HTTP_201_CREATED)
def create_group_role(body: GroupRoleCreate, use_cases: GroupRoleUseCases = Depends(get_group_role_use_cases)):
    return use_cases.create_group_role(group_id=GroupId(body.group_id), role_id=RoleId(body.role_id))


@router.get("/{group_role_id}", response_model=GroupRoleResponse)
def read_group_role(group_role_id: GroupRoleId, use_cases: GroupRoleUseCases = Depends(get_group_role_use_cases)):
    row = use_cases.get_group_role(group_role_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group role assignment not found")
    return row


@router.put("/{group_role_id}", response_model=GroupRoleResponse)
def replace_group_role(
    group_role_id: GroupRoleId,
    body: GroupRoleReplace,
    use_cases: GroupRoleUseCases = Depends(get_group_role_use_cases),
):
    try:
        return use_cases.replace_group_role(
            group_role_id=group_role_id,
            group_id=GroupId(body.group_id),
            role_id=RoleId(body.role_id),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{group_role_id}", response_model=GroupRoleResponse)
def update_group_role(
    group_role_id: GroupRoleId,
    body: GroupRoleUpdate,
    use_cases: GroupRoleUseCases = Depends(get_group_role_use_cases),
):
    try:
        return use_cases.update_group_role(
            group_role_id=group_role_id,
            group_id=GroupId(body.group_id) if body.group_id is not None else None,
            role_id=RoleId(body.role_id) if body.role_id is not None else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{group_role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_role(group_role_id: GroupRoleId, use_cases: GroupRoleUseCases = Depends(get_group_role_use_cases)):
    try:
        use_cases.delete_group_role(group_role_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return None


