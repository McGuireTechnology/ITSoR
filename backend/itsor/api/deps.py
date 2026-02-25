import os

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from itsor.domain.models.user import User
from itsor.domain.use_cases.tenant_use_cases import TenantUseCases
from itsor.domain.use_cases.user_use_cases import UserUseCases
from itsor.infrastructure.container.repositories import get_tenant_repository, get_user_repository

SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "itsor_session")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)


def get_user_use_cases(repo=Depends(get_user_repository)) -> UserUseCases:
    return UserUseCases(repo)


def get_tenant_use_cases(repo=Depends(get_tenant_repository)) -> TenantUseCases:
    return TenantUseCases(repo)


def get_current_user(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    use_cases: UserUseCases = Depends(get_user_use_cases),
) -> User:
    auth_token = request.cookies.get(SESSION_COOKIE_NAME) or token
    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = use_cases.get_current_user(auth_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
