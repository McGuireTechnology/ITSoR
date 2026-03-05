from fastapi import APIRouter, status

from itsor.api.schemas.auth.role import RoleCreate, RoleReplace, RoleResponse, RoleUpdate

router = APIRouter(tags=["roles"])


@router.get("/roles", response_model=list[RoleResponse])
def read_roles():
    pass


@router.post("/roles", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(body: RoleCreate):
    pass


@router.get("/roles/{role_id}", response_model=RoleResponse)
def read_role(role_id: str):
    pass


@router.put("/roles/{role_id}", response_model=RoleResponse)
def replace_role(role_id: str, body: RoleReplace):
    pass


@router.patch("/roles/{role_id}", response_model=RoleResponse)
def update_role(role_id: str, body: RoleUpdate):
    pass


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: str):
    pass


