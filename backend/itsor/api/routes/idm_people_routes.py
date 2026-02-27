from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from itsor.api.deps import get_current_user
from itsor.api.schemas.idm_people_schemas import IdmPersonCreate, IdmPersonResponse, IdmPersonUpdate
from itsor.domain.ids import generate_ulid
from itsor.domain.models import User
from itsor.infrastructure.container.database import get_db
from itsor.infrastructure.models.sqlalchemy_idm_identity_model import IdmIdentityModel
from itsor.infrastructure.models.sqlalchemy_idm_person_model import IdmPersonModel

router = APIRouter(prefix="/people", tags=["people"])


@router.get("", response_model=list[IdmPersonResponse])
def list_people(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(IdmPersonModel).all()


@router.post("", response_model=IdmPersonResponse, status_code=status.HTTP_201_CREATED)
def create_person(body: IdmPersonCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    if body.current_identity_id:
        current_identity = db.query(IdmIdentityModel).filter(IdmIdentityModel.id == body.current_identity_id).first()
        if not current_identity:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Current identity not found")

    person = IdmPersonModel(
        id=generate_ulid(),
        display_name=body.display_name,
        current_identity_id=body.current_identity_id,
    )
    db.add(person)
    db.commit()
    db.refresh(person)
    return person


@router.get("/{person_id}", response_model=IdmPersonResponse)
def get_person(person_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    person = db.query(IdmPersonModel).filter(IdmPersonModel.id == person_id).first()
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person


@router.patch("/{person_id}", response_model=IdmPersonResponse)
def update_person(person_id: str, body: IdmPersonUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    person = db.query(IdmPersonModel).filter(IdmPersonModel.id == person_id).first()
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    if body.display_name is not None:
        setattr(person, "display_name", body.display_name)

    if body.current_identity_id is not None:
        identity = db.query(IdmIdentityModel).filter(IdmIdentityModel.id == body.current_identity_id).first()
        if not identity:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Current identity not found")
        if str(getattr(identity, "person_id", "")) != str(getattr(person, "id", "")):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Current identity must reference the same person")
        setattr(person, "current_identity_id", body.current_identity_id)

    db.commit()
    db.refresh(person)
    return person


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(person_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    person = db.query(IdmPersonModel).filter(IdmPersonModel.id == person_id).first()
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")

    db.delete(person)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Person is referenced by identities or users")
