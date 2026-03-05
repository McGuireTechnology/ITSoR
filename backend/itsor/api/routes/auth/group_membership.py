from fastapi import APIRouter, status

from itsor.api.schemas.auth.group_membership import (
    GroupMembershipCreate,
    GroupMembershipReplace,
    GroupMembershipResponse,
    GroupMembershipUpdate,
)

router = APIRouter(tags=["group_memberships"])


@router.get("/group_memberships", response_model=list[GroupMembershipResponse])
def read_group_memberships():
    pass


@router.post(
    "/group_memberships",
    response_model=GroupMembershipResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_group_membership(body: GroupMembershipCreate):
    pass


@router.get("/group_memberships/{group_membership_id}", response_model=GroupMembershipResponse)
def read_group_membership(group_membership_id: str):
    pass


@router.put("/group_memberships/{group_membership_id}", response_model=GroupMembershipResponse)
def replace_group_membership(group_membership_id: str, body: GroupMembershipReplace):
    pass


@router.patch("/group_memberships/{group_membership_id}", response_model=GroupMembershipResponse)
def update_group_membership(group_membership_id: str, body: GroupMembershipUpdate):
    pass


@router.delete("/group_memberships/{group_membership_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_membership(group_membership_id: str):
    pass


