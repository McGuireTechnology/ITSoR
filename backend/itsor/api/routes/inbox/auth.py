from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from itsor.common.security import authenticate_user, issue_access_token

router = APIRouter(tags=["auth"])


@router.post("/auth/token")
def issue_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> dict:
    user = authenticate_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = issue_access_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
    }
