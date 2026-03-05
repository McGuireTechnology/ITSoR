from fastapi import APIRouter, status

from itsor.api.schemas.auth.group import GroupCreate, GroupReplace, GroupResponse, GroupUpdate

router = APIRouter(tags=["groups"])


@router.get("/groups", response_model=list[GroupResponse])
def read_groups():
    pass


@router.post("/groups", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(body: GroupCreate):
    pass


@router.get("/groups/{group_id}", response_model=GroupResponse)
def read_group(group_id: str):
    pass


@router.put("/groups/{group_id}", response_model=GroupResponse)
def replace_group(group_id: str, body: GroupReplace):
    pass


@router.patch("/groups/{group_id}", response_model=GroupResponse)
def update_group(group_id: str, body: GroupUpdate):
    pass


@router.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: str):
    pass


