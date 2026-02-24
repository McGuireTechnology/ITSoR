from typing import Annotated

from fastapi import APIRouter, Depends

from itsor.common import security
from itsor.common.security import User
from itsor.core.api.deps.auth import get_current_user

router = APIRouter(tags=["tenants"])


@router.get("/tenants")
def list_tenants(current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {"resource": "tenant", "status": "listed", "items": security.list_tenants()}


@router.post("/tenants")
def create_tenant(payload: dict, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {"resource": "tenant", "status": "created", "item": security.create_tenant(payload)}


@router.get("/tenants/{tenant_id}")
def get_tenant(tenant_id: str, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    return {
        "resource": "tenant",
        "id": tenant_id,
        "status": "retrieved",
        "item": security.get_tenant(tenant_id),
    }


@router.put("/tenants/{tenant_id}")
def replace_tenant(
    tenant_id: str,
    payload: dict,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    return {
        "resource": "tenant",
        "id": tenant_id,
        "status": "replaced",
        "item": security.replace_tenant(tenant_id, payload),
    }


@router.patch("/tenants/{tenant_id}")
def update_tenant(
    tenant_id: str,
    payload: dict,
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    return {
        "resource": "tenant",
        "id": tenant_id,
        "status": "updated",
        "item": security.update_tenant(tenant_id, payload),
    }


@router.delete("/tenants/{tenant_id}")
def delete_tenant(tenant_id: str, current_user: Annotated[User, Depends(get_current_user)]) -> dict:
    result = security.delete_tenant(tenant_id)
    return {"resource": "tenant", "id": tenant_id, "status": result["status"]}
