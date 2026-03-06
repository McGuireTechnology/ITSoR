from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_current_user, get_user_role_use_cases
from itsor.api.schemas.auth.user_role import (
    UserRoleCreate,
    UserRoleReplace,
    UserRoleResponse,
    UserRoleUpdate,
)
from itsor.application.use_cases.auth import UserRoleUseCases
from itsor.domain.ids import RoleId, UserId, UserRoleId

router = APIRouter(prefix="/user_roles", tags=["user_roles"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[UserRoleResponse])
def read_user_roles(use_cases: UserRoleUseCases = Depends(get_user_role_use_cases)):
    return use_cases.list_user_roles()


@router.post("/", response_model=UserRoleResponse, status_code=status.HTTP_201_CREATED)
def create_user_role(body: UserRoleCreate, use_cases: UserRoleUseCases = Depends(get_user_role_use_cases)):
    return use_cases.create_user_role(user_id=UserId(body.user_id), role_id=RoleId(body.role_id))


@router.get("/{user_role_id}", response_model=UserRoleResponse)
def read_user_role(user_role_id: UserRoleId, use_cases: UserRoleUseCases = Depends(get_user_role_use_cases)):
    row = use_cases.get_user_role(user_role_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User role assignment not found")
    return row


@router.put("/{user_role_id}", response_model=UserRoleResponse)
def replace_user_role(
    user_role_id: UserRoleId,
    body: UserRoleReplace,
    use_cases: UserRoleUseCases = Depends(get_user_role_use_cases),
):
    try:
        return use_cases.replace_user_role(
            user_role_id=user_role_id,
            user_id=UserId(body.user_id),
            role_id=RoleId(body.role_id),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{user_role_id}", response_model=UserRoleResponse)
def update_user_role(
    user_role_id: UserRoleId,
    body: UserRoleUpdate,
    use_cases: UserRoleUseCases = Depends(get_user_role_use_cases),
):
    try:
        return use_cases.update_user_role(
            user_role_id=user_role_id,
            user_id=UserId(body.user_id) if body.user_id is not None else None,
            role_id=RoleId(body.role_id) if body.role_id is not None else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{user_role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_role(user_role_id: UserRoleId, use_cases: UserRoleUseCases = Depends(get_user_role_use_cases)):
    try:
        use_cases.delete_user_role(user_role_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return None


