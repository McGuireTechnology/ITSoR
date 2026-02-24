from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated

from itsor.common import security
from itsor.common.security import User
from itsor.core.api.deps.auth import get_current_user

router = APIRouter(tags=["records"])


@router.get("/records")
def list_records(current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    visible_records = [
        record
        for record in security.list_records()
        if security.has_record_permission(
            current_user,
            security.get_record(record["id"]),
            "read",
        )
    ]
    return {
        "resource": "record",
        "status": "listed",
        "items": visible_records,
    }


@router.post("/records")
def create_record(payload: dict, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {
        "resource": "record",
        "status": "created",
        "item": security.create_record(payload, owner_user_id=current_user.id),
    }


@router.get("/records/{record_id}")
def get_record(record_id: str, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    record = security.require_record_permission(current_user, record_id, "read")
    return {
        "resource": "record",
        "id": record_id,
        "status": "retrieved",
        "item": {
            "id": record.id,
            "entity_id": record.entity_id,
            "data": record.data,
            "acl": {
                "owner_user_id": record.owner_user_id,
                "owner_perms": record.owner_perms,
                "group_perms": record.group_perms,
                "tenant_perms": record.tenant_perms,
                "public_perms": record.public_perms,
            },
        },
    }


@router.put("/records/{record_id}")
def replace_record(
    record_id: str,
    payload: dict,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    security.require_record_permission(current_user, record_id, "update")
    return {
        "resource": "record",
        "id": record_id,
        "status": "replaced",
        "item": security.replace_record(record_id, payload, owner_user_id=current_user.id),
    }


@router.patch("/records/{record_id}")
def update_record(
    record_id: str,
    payload: dict,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    security.require_record_permission(current_user, record_id, "update")
    return {
        "resource": "record",
        "id": record_id,
        "status": "updated",
        "item": security.update_record(record_id, payload),
    }


@router.delete("/records/{record_id}")
def delete_record(record_id: str, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    security.require_record_permission(current_user, record_id, "delete")
    deleted = security.delete_record(record_id)
    return {
        "resource": "record",
        "id": record_id,
        "status": deleted["status"],
    }
