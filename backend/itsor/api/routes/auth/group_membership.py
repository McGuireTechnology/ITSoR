from typing import Literal, cast

from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_current_user, get_group_membership_use_cases
from itsor.api.schemas.auth.group_membership import (
    GroupMembershipCreate,
    GroupMembershipReplace,
    GroupMembershipResponse,
    GroupMembershipUpdate,
)
from itsor.application.use_cases.auth import GroupMembershipUseCases
from itsor.domain.ids import GroupId, GroupMembershipId, UserId

router = APIRouter(
    prefix="/group_memberships",
    tags=["group_memberships"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=list[GroupMembershipResponse])
def read_group_memberships(use_cases: GroupMembershipUseCases = Depends(get_group_membership_use_cases)):
    return use_cases.list_group_memberships()


@router.post(
    "/",
    response_model=GroupMembershipResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_group_membership(
    body: GroupMembershipCreate,
    use_cases: GroupMembershipUseCases = Depends(get_group_membership_use_cases),
):
    try:
        return use_cases.create_group_membership(
            group_id=GroupId(body.group_id),
            member_type=cast(Literal["user", "group"], body.member_type),
            member_user_id=UserId(body.member_user_id) if body.member_user_id is not None else None,
            member_group_id=GroupId(body.member_group_id) if body.member_group_id is not None else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{group_membership_id}", response_model=GroupMembershipResponse)
def read_group_membership(
    group_membership_id: GroupMembershipId,
    use_cases: GroupMembershipUseCases = Depends(get_group_membership_use_cases),
):
    membership = use_cases.get_group_membership(group_membership_id)
    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group membership not found")
    return membership


@router.put("/{group_membership_id}", response_model=GroupMembershipResponse)
def replace_group_membership(
    group_membership_id: GroupMembershipId,
    body: GroupMembershipReplace,
    use_cases: GroupMembershipUseCases = Depends(get_group_membership_use_cases),
):
    try:
        return use_cases.replace_group_membership(
            membership_id=group_membership_id,
            group_id=GroupId(body.group_id),
            member_type=cast(Literal["user", "group"], body.member_type),
            member_user_id=UserId(body.member_user_id) if body.member_user_id is not None else None,
            member_group_id=GroupId(body.member_group_id) if body.member_group_id is not None else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.patch("/{group_membership_id}", response_model=GroupMembershipResponse)
def update_group_membership(
    group_membership_id: GroupMembershipId,
    body: GroupMembershipUpdate,
    use_cases: GroupMembershipUseCases = Depends(get_group_membership_use_cases),
):
    try:
        return use_cases.update_group_membership(
            membership_id=group_membership_id,
            member_type=(
                cast(Literal["user", "group"], body.member_type)
                if body.member_type is not None
                else None
            ),
            member_user_id=UserId(body.member_user_id) if body.member_user_id is not None else None,
            member_group_id=GroupId(body.member_group_id) if body.member_group_id is not None else None,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{group_membership_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_membership(
    group_membership_id: GroupMembershipId,
    use_cases: GroupMembershipUseCases = Depends(get_group_membership_use_cases),
):
    try:
        use_cases.delete_group_membership(group_membership_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return None


