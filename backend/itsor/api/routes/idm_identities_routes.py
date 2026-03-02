import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from itsor.api.deps import get_current_user
from itsor.api.schemas.idm_identities_schemas import IdmIdentityCreate, IdmIdentityResponse, IdmIdentityUpdate
from itsor.domain.ids import generate_ulid
from itsor.domain.models import PlatformUser
from itsor.infrastructure.container.database import get_db
from itsor.infrastructure.models.sqlalchemy_idm_identity_model import IdmIdentityModel
from itsor.infrastructure.models.sqlalchemy_idm_person_model import IdmPersonModel

router = APIRouter(prefix="/identities", tags=["identities"])


def _parse_payload(raw_payload: str | None) -> dict:
    if not raw_payload:
        return {}
    try:
        parsed = json.loads(raw_payload)
    except (TypeError, ValueError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _identity_response(model: IdmIdentityModel) -> IdmIdentityResponse:
    return IdmIdentityResponse(
        id=str(getattr(model, "id", "")),
        person_id=str(getattr(model, "person_id", "")),
        source_system=str(getattr(model, "source_system", "")),
        source_record_id=str(getattr(model, "source_record_id", "")),
        demographic_payload=_parse_payload(str(getattr(model, "demographic_payload", "{}"))),
        valid_from=getattr(model, "valid_from", None),
        valid_to=getattr(model, "valid_to", None),
        superseded_at=getattr(model, "superseded_at", None),
    )


@router.get("", response_model=list[IdmIdentityResponse])
def list_identities(db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    rows = db.query(IdmIdentityModel).all()
    return [_identity_response(row) for row in rows]


@router.post("", response_model=IdmIdentityResponse, status_code=status.HTTP_201_CREATED)
def create_identity(body: IdmIdentityCreate, db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    person = db.query(IdmPersonModel).filter(IdmPersonModel.id == body.person_id).first()
    if not person:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Person not found")

    identity = IdmIdentityModel(
        id=generate_ulid(),
        person_id=body.person_id,
        source_system=body.source_system,
        source_record_id=body.source_record_id,
        demographic_payload=json.dumps(body.demographic_payload or {}),
        valid_from=body.valid_from,
        valid_to=body.valid_to,
        superseded_at=body.superseded_at,
    )
    db.add(identity)
    db.commit()
    db.refresh(identity)
    return _identity_response(identity)


@router.get("/{identity_id}", response_model=IdmIdentityResponse)
def get_identity(identity_id: str, db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    identity = db.query(IdmIdentityModel).filter(IdmIdentityModel.id == identity_id).first()
    if not identity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Identity not found")
    return _identity_response(identity)


@router.patch("/{identity_id}", response_model=IdmIdentityResponse)
def update_identity(identity_id: str, body: IdmIdentityUpdate, db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    identity = db.query(IdmIdentityModel).filter(IdmIdentityModel.id == identity_id).first()
    if not identity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Identity not found")

    if body.source_system is not None:
        setattr(identity, "source_system", body.source_system)
    if body.source_record_id is not None:
        setattr(identity, "source_record_id", body.source_record_id)
    if body.demographic_payload is not None:
        setattr(identity, "demographic_payload", json.dumps(body.demographic_payload))
    if body.valid_from is not None:
        setattr(identity, "valid_from", body.valid_from)
    if body.valid_to is not None:
        setattr(identity, "valid_to", body.valid_to)
    if body.superseded_at is not None:
        setattr(identity, "superseded_at", body.superseded_at)

    db.commit()
    db.refresh(identity)
    return _identity_response(identity)


@router.delete("/{identity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_identity(identity_id: str, db: Session = Depends(get_db), _: PlatformUser = Depends(get_current_user)):
    identity = db.query(IdmIdentityModel).filter(IdmIdentityModel.id == identity_id).first()
    if not identity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Identity not found")

    db.delete(identity)
    db.commit()
