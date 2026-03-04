from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from itsor.api.deps import AuthorizationService, get_authorization_service, get_current_user
from itsor.api.schemas.platform_group_memberships_schemas import (
    PlatformGroupMembershipCreate,
    PlatformGroupMembershipResponse,
    PlatformGroupMembershipUpdate,
)
from itsor.domain.models import User
from itsor.infrastructure.container.database import get_db
from itsor.infrastructure.models.sqlalchemy_group_model import GroupModel
from itsor.infrastructure.models.sqlalchemy_platform_group_membership_model import (
    PlatformGroupMembershipModel,
)
from itsor.infrastructure.models.sqlalchemy_user_model import UserModel

router = APIRouter(prefix="/group-memberships", tags=["group-memberships"])


def _authorize(current_user: User, authz: AuthorizationService, action: str) -> None:
    authz.authorize_platform_endpoint(
        current_user=current_user,
        endpoint_name="group-memberships",
        action=action,
    )


def _validate_member_ref(
    db: Session, member_type: str, member_user_id: str | None, member_group_id: str | None
):
    if member_type not in {"user", "group"}:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="member_type must be 'user' or 'group'"
        )

    if member_type == "user":
        if not member_user_id or member_group_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="user membership requires member_user_id only",
            )
        user = db.query(UserModel).filter(UserModel.id == member_user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Member user not found"
            )
        return

    if not member_group_id or member_user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="group membership requires member_group_id only",
        )
    group = db.query(GroupModel).filter(GroupModel.id == member_group_id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Member group not found")


@router.get("", response_model=list[PlatformGroupMembershipResponse])
def list_group_memberships(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authorize(current_user, authz, "read")
    return db.query(PlatformGroupMembershipModel).all()


@router.post(
    "", response_model=PlatformGroupMembershipResponse, status_code=status.HTTP_201_CREATED
)
def create_group_membership(
    body: PlatformGroupMembershipCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authorize(current_user, authz, "write")
    group = db.query(GroupModel).filter(GroupModel.id == body.group_id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Group not found")

    _validate_member_ref(db, body.member_type, body.member_user_id, body.member_group_id)

    if body.member_type == "group" and body.member_group_id == body.group_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Group cannot directly contain itself"
        )

    membership = PlatformGroupMembershipModel(
        group_id=body.group_id,
        member_type=body.member_type,
        member_user_id=body.member_user_id,
        member_group_id=body.member_group_id,
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


@router.get("/{membership_id}", response_model=PlatformGroupMembershipResponse)
def get_group_membership(
    membership_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authorize(current_user, authz, "read")
    membership = (
        db.query(PlatformGroupMembershipModel)
        .filter(PlatformGroupMembershipModel.id == membership_id)
        .first()
    )
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group membership not found"
        )
    return membership


@router.patch("/{membership_id}", response_model=PlatformGroupMembershipResponse)
def update_group_membership(
    membership_id: str,
    body: PlatformGroupMembershipUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authorize(current_user, authz, "write")
    membership = (
        db.query(PlatformGroupMembershipModel)
        .filter(PlatformGroupMembershipModel.id == membership_id)
        .first()
    )
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group membership not found"
        )

    next_member_type = (
        body.member_type
        if body.member_type is not None
        else str(getattr(membership, "member_type", ""))
    )
    next_member_user_id = (
        body.member_user_id
        if body.member_user_id is not None
        else getattr(membership, "member_user_id", None)
    )
    next_member_group_id = (
        body.member_group_id
        if body.member_group_id is not None
        else getattr(membership, "member_group_id", None)
    )

    _validate_member_ref(db, next_member_type, next_member_user_id, next_member_group_id)

    if next_member_type == "group" and str(next_member_group_id) == str(
        getattr(membership, "group_id", "")
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Group cannot directly contain itself"
        )

    if body.member_type is not None:
        setattr(membership, "member_type", body.member_type)
    if body.member_user_id is not None:
        setattr(membership, "member_user_id", body.member_user_id)
    if body.member_group_id is not None:
        setattr(membership, "member_group_id", body.member_group_id)

    db.commit()
    db.refresh(membership)
    return membership


@router.delete("/{membership_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_membership(
    membership_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authorize(current_user, authz, "write")
    membership = (
        db.query(PlatformGroupMembershipModel)
        .filter(PlatformGroupMembershipModel.id == membership_id)
        .first()
    )
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group membership not found"
        )

    db.delete(membership)
    db.commit()
