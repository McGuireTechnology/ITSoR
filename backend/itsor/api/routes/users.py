from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_current_user, get_user_use_cases
from itsor.api.schemas.user import UserCreate, UserUpdate, UserReplace, UserResponse
from itsor.domain.models.user import User
from itsor.domain.use_cases.user_use_cases import UserUseCases

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=List[UserResponse])
def list_users(
    use_cases: UserUseCases = Depends(get_user_use_cases),
    _: User = Depends(get_current_user),
):
    return use_cases.list_users()


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    body: UserCreate,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.create_user(body.username, body.email, body.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: str,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    _: User = Depends(get_current_user),
):
    user = use_cases.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: str,
    body: UserUpdate,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.update_user(user_id, body.username, body.email, body.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.put("/{user_id}", response_model=UserResponse)
def replace_user(
    user_id: str,
    body: UserReplace,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.replace_user(user_id, body.username, body.email, body.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        use_cases.delete_user(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
