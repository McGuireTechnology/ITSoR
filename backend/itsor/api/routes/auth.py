import os

from fastapi import APIRouter, Depends, HTTPException, Response, status

from itsor.api.deps import get_current_user, get_user_use_cases
from itsor.api.schemas.auth import LoginRequest, SignupRequest, TokenResponse
from itsor.domain.models.user import User
from itsor.domain.use_cases.user_use_cases import UserUseCases

router = APIRouter(tags=["auth"])

SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "itsor_session")
SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "lax").lower()
SESSION_COOKIE_MAX_AGE = int(os.getenv("SESSION_COOKIE_MAX_AGE", "3600"))


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=SESSION_COOKIE_SECURE,
        samesite=SESSION_COOKIE_SAMESITE,
        max_age=SESSION_COOKIE_MAX_AGE,
        path="/",
    )


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(body: SignupRequest, response: Response, use_cases: UserUseCases = Depends(get_user_use_cases)):
    try:
        _, token = use_cases.signup(body.username, body.email, body.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    _set_session_cookie(response, token)
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, response: Response, use_cases: UserUseCases = Depends(get_user_use_cases)):
    try:
        _, token = use_cases.login(body.identifier, body.password)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))
    _set_session_cookie(response, token)
    return TokenResponse(access_token=token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(response: Response, _: User = Depends(get_current_user)):
    response.delete_cookie(key=SESSION_COOKIE_NAME, path="/")
    return None
