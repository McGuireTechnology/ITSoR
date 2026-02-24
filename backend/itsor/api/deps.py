from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from itsor.infrastructure.container.database import get_db
from itsor.infrastructure.adapters.user_repository import SQLAlchemyUserRepository
from itsor.use_cases.user_use_cases import UserUseCases
from itsor.domain.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_user_use_cases(db: Session = Depends(get_db)) -> UserUseCases:
    repo = SQLAlchemyUserRepository(db)
    return UserUseCases(repo)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    use_cases: UserUseCases = Depends(get_user_use_cases),
) -> User:
    user = use_cases.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
