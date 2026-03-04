import json
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import CurrentUser as User, get_current_user, get_idm_identity_use_cases
from itsor.api.schemas.idm_identities_schemas import IdmIdentityCreate, IdmIdentityResponse, IdmIdentityUpdate
from itsor.application.use_cases.identity_use_cases import IdmIdentityUseCases

router = APIRouter(prefix="/identities", tags=["identities"])


def _parse_payload(raw_payload: str | None) -> dict:
    if not raw_payload:
        return {}
    try:
        parsed = json.loads(raw_payload)
    except (TypeError, ValueError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _identity_response(model: Any) -> IdmIdentityResponse:
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
def list_identities(_: User = Depends(get_current_user), use_cases: IdmIdentityUseCases = Depends(get_idm_identity_use_cases)):
    rows = use_cases.list_identities()
    return [_identity_response(row) for row in rows]


@router.post("", response_model=IdmIdentityResponse, status_code=status.HTTP_201_CREATED)
def create_identity(body: IdmIdentityCreate, _: User = Depends(get_current_user), use_cases: IdmIdentityUseCases = Depends(get_idm_identity_use_cases)):
    try:
        identity = use_cases.create_identity(
            person_id=body.person_id,
            source_system=body.source_system,
            source_record_id=body.source_record_id,
            demographic_payload=body.demographic_payload,
            valid_from=body.valid_from,
            valid_to=body.valid_to,
            superseded_at=body.superseded_at,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return _identity_response(identity)


@router.get("/{identity_id}", response_model=IdmIdentityResponse)
def get_identity(identity_id: str, _: User = Depends(get_current_user), use_cases: IdmIdentityUseCases = Depends(get_idm_identity_use_cases)):
    identity = use_cases.get_identity(identity_id)
    if not identity:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Identity not found")
    return _identity_response(identity)


@router.patch("/{identity_id}", response_model=IdmIdentityResponse)
def update_identity(identity_id: str, body: IdmIdentityUpdate, _: User = Depends(get_current_user), use_cases: IdmIdentityUseCases = Depends(get_idm_identity_use_cases)):
    try:
        identity = use_cases.update_identity(
            identity_id=identity_id,
            source_system=body.source_system,
            source_record_id=body.source_record_id,
            demographic_payload=body.demographic_payload,
            valid_from=body.valid_from,
            valid_to=body.valid_to,
            superseded_at=body.superseded_at,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return _identity_response(identity)


@router.delete("/{identity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_identity(identity_id: str, _: User = Depends(get_current_user), use_cases: IdmIdentityUseCases = Depends(get_idm_identity_use_cases)):
    try:
        use_cases.delete_identity(identity_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
