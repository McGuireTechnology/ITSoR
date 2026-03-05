from fastapi import APIRouter, status

from itsor.api.schemas.auth.user_role import (
    UserRoleCreate,
    UserRoleReplace,
    UserRoleResponse,
    UserRoleUpdate,
)

router = APIRouter(tags=["user_roles"])


@router.get("/user_roles", response_model=list[UserRoleResponse])
def read_user_roles():
    pass


@router.post("/user_roles", response_model=UserRoleResponse, status_code=status.HTTP_201_CREATED)
def create_user_role(body: UserRoleCreate):
    pass


@router.get("/user_roles/{user_role_id}", response_model=UserRoleResponse)
def read_user_role(user_role_id: str):
    pass


@router.put("/user_roles/{user_role_id}", response_model=UserRoleResponse)
def replace_user_role(user_role_id: str, body: UserRoleReplace):
    pass


@router.patch("/user_roles/{user_role_id}", response_model=UserRoleResponse)
def update_user_role(user_role_id: str, body: UserRoleUpdate):
    pass


@router.delete("/user_roles/{user_role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_role(user_role_id: str):
    pass


