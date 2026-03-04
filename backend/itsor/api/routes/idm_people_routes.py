from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import CurrentUser as User, get_current_user, get_idm_person_use_cases
from itsor.api.schemas.idm_people_schemas import IdmPersonCreate, IdmPersonResponse, IdmPersonUpdate
from itsor.application.use_cases.identity_use_cases import IdmPersonUseCases

router = APIRouter(prefix="/people", tags=["people"])


@router.get("", response_model=list[IdmPersonResponse])
def list_people(_: User = Depends(get_current_user), use_cases: IdmPersonUseCases = Depends(get_idm_person_use_cases)):
    return use_cases.list_people()


@router.post("", response_model=IdmPersonResponse, status_code=status.HTTP_201_CREATED)
def create_person(body: IdmPersonCreate, _: User = Depends(get_current_user), use_cases: IdmPersonUseCases = Depends(get_idm_person_use_cases)):
    try:
        return use_cases.create_person(
            display_name=body.display_name,
            current_identity_id=body.current_identity_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{person_id}", response_model=IdmPersonResponse)
def get_person(person_id: str, _: User = Depends(get_current_user), use_cases: IdmPersonUseCases = Depends(get_idm_person_use_cases)):
    person = use_cases.get_person(person_id)
    if not person:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    return person


@router.patch("/{person_id}", response_model=IdmPersonResponse)
def update_person(person_id: str, body: IdmPersonUpdate, _: User = Depends(get_current_user), use_cases: IdmPersonUseCases = Depends(get_idm_person_use_cases)):
    try:
        return use_cases.update_person(
            person_id=person_id,
            display_name=body.display_name,
            current_identity_id=body.current_identity_id,
        )
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if detail == "Person not found" else status.HTTP_409_CONFLICT
        raise HTTPException(status_code=status_code, detail=detail)


@router.delete("/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(person_id: str, _: User = Depends(get_current_user), use_cases: IdmPersonUseCases = Depends(get_idm_person_use_cases)):
    try:
        use_cases.delete_person(person_id)
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if detail == "Person not found" else status.HTTP_409_CONFLICT
        raise HTTPException(status_code=status_code, detail=detail)
