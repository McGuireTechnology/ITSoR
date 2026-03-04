from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import CurrentUser as User, get_current_user, get_idm_user_use_cases
from itsor.api.schemas.idm_users_schemas import IdmUserCreate, IdmUserResponse, IdmUserUpdate
from itsor.application.use_cases.identity_use_cases import IdmUserUseCases

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[IdmUserResponse])
def list_idm_users(_: User = Depends(get_current_user), use_cases: IdmUserUseCases = Depends(get_idm_user_use_cases)):
    return use_cases.list_users()


@router.post("", response_model=IdmUserResponse, status_code=status.HTTP_201_CREATED)
def create_idm_user(body: IdmUserCreate, _: User = Depends(get_current_user), use_cases: IdmUserUseCases = Depends(get_idm_user_use_cases)):
    try:
        return use_cases.create_user(
            person_id=body.person_id,
            username=body.username,
            account_status=body.account_status,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{user_id}", response_model=IdmUserResponse)
def get_idm_user(user_id: str, _: User = Depends(get_current_user), use_cases: IdmUserUseCases = Depends(get_idm_user_use_cases)):
    user = use_cases.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IDM user not found")
    return user


@router.patch("/{user_id}", response_model=IdmUserResponse)
def update_idm_user(user_id: str, body: IdmUserUpdate, _: User = Depends(get_current_user), use_cases: IdmUserUseCases = Depends(get_idm_user_use_cases)):
    try:
        return use_cases.update_user(
            user_id=user_id,
            username=body.username,
            account_status=body.account_status,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_idm_user(user_id: str, _: User = Depends(get_current_user), use_cases: IdmUserUseCases = Depends(get_idm_user_use_cases)):
    try:
        use_cases.delete_user(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
