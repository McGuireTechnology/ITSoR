from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from itsor.common.security import User, get_user_by_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    return get_user_by_token(token)
