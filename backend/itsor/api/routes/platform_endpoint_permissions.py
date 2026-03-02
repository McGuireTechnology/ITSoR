from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import AuthorizationService, get_authorization_service, get_current_user
from itsor.api.schemas.platform_endpoint_permissions_schemas import (
    PlatformEndpointPermissionEntry,
    PlatformEndpointPermissionPatchRequest,
    PlatformEndpointPermissionEntryResponse,
    PlatformEndpointPermissionUpdateRequest,
)
from itsor.domain.models import PlatformUser
from itsor.infrastructure.container.database import get_db
from itsor.infrastructure.models.sqlalchemy_platform_endpoint_permission_model import PlatformEndpointPermissionModel

router = APIRouter(prefix="/endpoint-permissions", tags=["endpoint-permissions"])
PrincipalType = Literal["user", "group"]


def _validate_principal(principal_type: PrincipalType, principal_id: str, authz: AuthorizationService) -> None:
    if principal_type == "user":
        principal = authz.user_repo.get_by_id(principal_id)
        if not principal:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return

    principal = authz.group_repo.get_by_id(principal_id)
    if not principal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")

@router.get("", response_model=list[PlatformEndpointPermissionEntryResponse])
def list_platform_endpoint_permission_rows(
    principal_type: PrincipalType | None = None,
    principal_id: str | None = None,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="endpoint-permissions", action="read")
    query = db.query(PlatformEndpointPermissionModel)
    if principal_type:
        query = query.filter(PlatformEndpointPermissionModel.principal_type == principal_type)
    if principal_id:
        query = query.filter(PlatformEndpointPermissionModel.principal_id == principal_id)
    return query.order_by(PlatformEndpointPermissionModel.id.asc()).all()


@router.post("", response_model=PlatformEndpointPermissionEntryResponse, status_code=status.HTTP_201_CREATED)
def create_platform_endpoint_permission_row(
    body: PlatformEndpointPermissionEntry,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="endpoint-permissions", action="write")
    _validate_principal(body.principal_type, body.principal_id, authz)

    model = PlatformEndpointPermissionModel(
        principal_type=body.principal_type,
        principal_id=body.principal_id,
        endpoint_name=body.endpoint_name,
        action=body.action,
    )
    db.add(model)
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(model)
    return model


@router.get("/{endpoint_permission_id}", response_model=PlatformEndpointPermissionEntryResponse)
def get_platform_endpoint_permission_row(
    endpoint_permission_id: int,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="endpoint-permissions", action="read")
    row = db.query(PlatformEndpointPermissionModel).filter(PlatformEndpointPermissionModel.id == endpoint_permission_id).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform endpoint permission row not found")
    return row


@router.put("/{endpoint_permission_id}", response_model=PlatformEndpointPermissionEntryResponse)
def put_platform_endpoint_permission_row(
    endpoint_permission_id: int,
    body: PlatformEndpointPermissionUpdateRequest,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="endpoint-permissions", action="write")
    _validate_principal(body.principal_type, body.principal_id, authz)
    row = db.query(PlatformEndpointPermissionModel).filter(PlatformEndpointPermissionModel.id == endpoint_permission_id).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform endpoint permission row not found")
    row.principal_type = body.principal_type
    row.principal_id = body.principal_id
    row.endpoint_name = body.endpoint_name
    row.action = body.action
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.patch("/{endpoint_permission_id}", response_model=PlatformEndpointPermissionEntryResponse)
def patch_platform_endpoint_permission_row(
    endpoint_permission_id: int,
    body: PlatformEndpointPermissionPatchRequest,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="endpoint-permissions", action="write")
    row = db.query(PlatformEndpointPermissionModel).filter(PlatformEndpointPermissionModel.id == endpoint_permission_id).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform endpoint permission row not found")

    if (
        body.principal_type is None
        and body.principal_id is None
        and body.endpoint_name is None
        and body.action is None
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No fields provided for patch")

    effective_principal_type = body.principal_type or row.principal_type
    effective_principal_id = body.principal_id or row.principal_id
    _validate_principal(effective_principal_type, effective_principal_id, authz)

    if body.principal_type is not None:
        row.principal_type = body.principal_type
    if body.principal_id is not None:
        row.principal_id = body.principal_id
    if body.endpoint_name is not None:
        row.endpoint_name = body.endpoint_name
    if body.action is not None:
        row.action = body.action

    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row





@router.delete("/{endpoint_permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_platform_endpoint_permission_row(
    endpoint_permission_id: int,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="endpoint-permissions", action="write")
    row = db.query(PlatformEndpointPermissionModel).filter(PlatformEndpointPermissionModel.id == endpoint_permission_id).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform endpoint permission row not found")
    db.delete(row)
    db.commit()
