from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from itsor.api.deps import get_current_user
from itsor.api.schemas.idm_users_schemas import IdmUserCreate, IdmUserResponse, IdmUserUpdate
from itsor.domain.models import PlatformUser
from itsor.infrastructure.container.database import get_db
from itsor.infrastructure.models.sqlalchemy_idm_person_model import IdmPersonModel
from itsor.infrastructure.models.sqlalchemy_idm_user_model import IdmUserModel

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[IdmUserResponse])
def list_idm_users(db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    return db.query(IdmUserModel).all()


@router.post("", response_model=IdmUserResponse, status_code=status.HTTP_201_CREATED)
def create_idm_user(body: IdmUserCreate, db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    person = db.query(IdmPersonModel).filter(IdmPersonModel.id == body.person_id).first()
    if not person:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Person not found")

    user = IdmUserModel(
        person_id=body.person_id,
        username=body.username,
        account_status=body.account_status,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("/{user_id}", response_model=IdmUserResponse)
def get_idm_user(user_id: str, db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    user = db.query(IdmUserModel).filter(IdmUserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IDM user not found")
    return user


@router.patch("/{user_id}", response_model=IdmUserResponse)
def update_idm_user(user_id: str, body: IdmUserUpdate, db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    user = db.query(IdmUserModel).filter(IdmUserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IDM user not found")

    if body.username is not None:
        setattr(user, "username", body.username)
    if body.account_status is not None:
        setattr(user, "account_status", body.account_status)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_idm_user(user_id: str, db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    user = db.query(IdmUserModel).filter(IdmUserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IDM user not found")

    db.delete(user)
    db.commit()
