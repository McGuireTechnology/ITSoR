from typing import Annotated

from fastapi import APIRouter, Depends

from itsor.common import security
from itsor.common.security import User
from itsor.core.api.deps.auth import get_current_user

router = APIRouter(tags=["users"])


@router.get("/users")
def list_users(current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {"resource": "user", "status": "listed", "items": security.list_users()}


@router.post("/users")
def create_user(payload: dict, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {"resource": "user", "status": "created", "item": security.create_user(payload)}


@router.get("/users/{user_id}")
def get_user(user_id: str, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {"resource": "user", "id": user_id, "status": "retrieved", "item": security.get_user(user_id)}


@router.put("/users/{user_id}")
def replace_user(user_id: str, payload: dict, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {
        "resource": "user",
        "id": user_id,
        "status": "replaced",
        "item": security.replace_user(user_id, payload),
    }


@router.patch("/users/{user_id}")
def update_user(user_id: str, payload: dict, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {
        "resource": "user",
        "id": user_id,
        "status": "updated",
        "item": security.update_user(user_id, payload),
    }


@router.delete("/users/{user_id}")
def delete_user(user_id: str, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    result = security.delete_user(user_id)
    return {"resource": "user", "id": user_id, "status": result["status"]}
