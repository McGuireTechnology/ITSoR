from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import CurrentUser as User, get_current_user, get_idm_group_membership_use_cases
from itsor.api.schemas.idm_group_memberships_schemas import (
    IdmGroupMembershipCreate,
    IdmGroupMembershipResponse,
    IdmGroupMembershipUpdate,
)
from itsor.application.use_cases.identity_use_cases import IdmGroupMembershipUseCases

router = APIRouter(prefix="/group-memberships", tags=["group-memberships"])


@router.get("", response_model=list[IdmGroupMembershipResponse])
def list_group_memberships(_: User = Depends(get_current_user), use_cases: IdmGroupMembershipUseCases = Depends(get_idm_group_membership_use_cases)):
    return use_cases.list_group_memberships()


@router.post("", response_model=IdmGroupMembershipResponse, status_code=status.HTTP_201_CREATED)
def create_group_membership(body: IdmGroupMembershipCreate, _: User = Depends(get_current_user), use_cases: IdmGroupMembershipUseCases = Depends(get_idm_group_membership_use_cases)):
    try:
        return use_cases.create_group_membership(
            group_id=body.group_id,
            member_type=body.member_type,
            member_user_id=body.member_user_id,
            member_group_id=body.member_group_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{membership_id}", response_model=IdmGroupMembershipResponse)
def get_group_membership(membership_id: str, _: User = Depends(get_current_user), use_cases: IdmGroupMembershipUseCases = Depends(get_idm_group_membership_use_cases)):
    membership = use_cases.get_group_membership(membership_id)
    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group membership not found")
    return membership


@router.patch("/{membership_id}", response_model=IdmGroupMembershipResponse)
def update_group_membership(
    membership_id: str,
    body: IdmGroupMembershipUpdate,
    _: User = Depends(get_current_user),
    use_cases: IdmGroupMembershipUseCases = Depends(get_idm_group_membership_use_cases),
):
    try:
        return use_cases.update_group_membership(
            membership_id=membership_id,
            member_type=body.member_type,
            member_user_id=body.member_user_id,
            member_group_id=body.member_group_id,
        )
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if detail == "Group membership not found" else status.HTTP_409_CONFLICT
        raise HTTPException(status_code=status_code, detail=detail)


@router.delete("/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_membership(membership_id: str, _: User = Depends(get_current_user), use_cases: IdmGroupMembershipUseCases = Depends(get_idm_group_membership_use_cases)):
    try:
        use_cases.delete_group_membership(membership_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
