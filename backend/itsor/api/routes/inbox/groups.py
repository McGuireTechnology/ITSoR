from typing import Annotated

from fastapi import APIRouter, Depends

from itsor.common import security
from itsor.common.security import User
from itsor.core.api.deps.auth import get_current_user

router = APIRouter(tags=["groups"])


@router.get("/groups")
def list_groups(current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {"resource": "group", "status": "listed", "items": security.list_groups()}


@router.post("/groups")
def create_group(payload: dict, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {"resource": "group", "status": "created", "item": security.create_group(payload)}


@router.get("/groups/{group_id}")
def get_group(group_id: str, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {
        "resource": "group",
        "id": group_id,
        "status": "retrieved",
        "item": security.get_group(group_id),
    }


@router.put("/groups/{group_id}")
def replace_group(
    group_id: str,
    payload: dict,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    return {
        "resource": "group",
        "id": group_id,
        "status": "replaced",
        "item": security.replace_group(group_id, payload),
    }


@router.patch("/groups/{group_id}")
def update_group(
    group_id: str,
    payload: dict,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    return {
        "resource": "group",
        "id": group_id,
        "status": "updated",
        "item": security.update_group(group_id, payload),
    }


@router.delete("/groups/{group_id}")
def delete_group(group_id: str, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    result = security.delete_group(group_id)
    return {"resource": "group", "id": group_id, "status": result["status"]}
