from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_user_use_cases
from itsor.api.schemas.auth import LoginRequest, SignupRequest, TokenResponse
from itsor.use_cases.user_use_cases import UserUseCases

router = APIRouter(tags=["auth"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(body: SignupRequest, use_cases: UserUseCases = Depends(get_user_use_cases)):
    try:
        _, token = use_cases.signup(body.email, body.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, use_cases: UserUseCases = Depends(get_user_use_cases)):
    try:
        _, token = use_cases.login(body.email, body.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    return TokenResponse(access_token=token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout():
    return None
