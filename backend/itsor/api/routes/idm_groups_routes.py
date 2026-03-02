from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from itsor.api.deps import get_current_user
from itsor.api.schemas.idm_groups_schemas import IdmGroupCreate, IdmGroupResponse, IdmGroupUpdate
from itsor.domain.ids import generate_ulid
from itsor.domain.models import PlatformUser
from itsor.infrastructure.container.database import get_db
from itsor.infrastructure.models.sqlalchemy_idm_group_model import IdmGroupModel

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("", response_model=list[IdmGroupResponse])
def list_idm_groups(db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    return db.query(IdmGroupModel).all()


@router.post("", response_model=IdmGroupResponse, status_code=status.HTTP_201_CREATED)
def create_idm_group(body: IdmGroupCreate, db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    group = IdmGroupModel(
        id=generate_ulid(),
        name=body.name,
        description=body.description,
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


@router.get("/{group_id}", response_model=IdmGroupResponse)
def get_idm_group(group_id: str, db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    group = db.query(IdmGroupModel).filter(IdmGroupModel.id == group_id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IDM group not found")
    return group


@router.patch("/{group_id}", response_model=IdmGroupResponse)
def update_idm_group(group_id: str, body: IdmGroupUpdate, db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    group = db.query(IdmGroupModel).filter(IdmGroupModel.id == group_id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IDM group not found")

    if body.name is not None:
        setattr(group, "name", body.name)
    if body.description is not None:
        setattr(group, "description", body.description)

    db.commit()
    db.refresh(group)
    return group


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_idm_group(group_id: str, db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    group = db.query(IdmGroupModel).filter(IdmGroupModel.id == group_id).first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IDM group not found")

    db.delete(group)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="IDM group is referenced by memberships")
