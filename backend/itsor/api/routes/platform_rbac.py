"""DB-backed platform RBAC routes."""

# noqa: E501

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import AuthorizationService, get_authorization_service, get_current_user
from itsor.api.schemas.platform_rbac_schemas import (
    PlatformGroupRoleCreate,
    PlatformGroupRoleResponse,
    PlatformGroupRoleUpdate,
    PlatformPermissionCreate,
    PlatformPermissionResponse,
    PlatformPermissionUpdate,
    PlatformRoleCreate,
    PlatformRolePermissionCreate,
    PlatformRolePermissionResponse,
    PlatformRolePermissionUpdate,
    PlatformRoleResponse,
    PlatformRoleUpdate,
    PlatformUserRoleCreate,
    PlatformUserRoleResponse,
    PlatformUserRoleUpdate,
    PlatformUserTenantCreate,
    PlatformUserTenantResponse,
    PlatformUserTenantUpdate,
)
from itsor.domain.models import PlatformUser
from itsor.infrastructure.container.database import get_db
from itsor.infrastructure.models.sqlalchemy_group_model import GroupModel
from itsor.infrastructure.models.sqlalchemy_platform_rbac_models import (
    PlatformGroupRoleModel,
    PlatformPermissionModel,
    PlatformRoleModel,
    PlatformRolePermissionModel,
    PlatformUserRoleModel,
    PlatformUserTenantModel,
)
from itsor.infrastructure.models.sqlalchemy_tenant_model import TenantModel
from itsor.infrastructure.models.sqlalchemy_user_model import UserModel

router = APIRouter(tags=["platform-rbac"])


def _authz(
    current_user: PlatformUser,
    authz: AuthorizationService,
    endpoint_name: str,
    action: Literal["read", "write"],
) -> None:
    authz.authorize_platform_endpoint(
        current_user=current_user,
        endpoint_name=endpoint_name,
        action=action,
    )


def _ensure_user_exists(db, user_id: str) -> None:
    if not db.query(UserModel).filter(UserModel.id == user_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


def _ensure_group_exists(db, group_id: str) -> None:
    if not db.query(GroupModel).filter(GroupModel.id == group_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")


def _ensure_tenant_exists(db, tenant_id: str) -> None:
    if not db.query(TenantModel).filter(TenantModel.id == tenant_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")


def _ensure_role_exists(db, role_id: str) -> None:
    if not db.query(PlatformRoleModel).filter(PlatformRoleModel.id == role_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")


def _ensure_permission_exists(db, permission_id: str) -> None:
    if (
        not db.query(PlatformPermissionModel)
        .filter(PlatformPermissionModel.id == permission_id)
        .first()
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")


@router.get("/roles", response_model=list[PlatformRoleResponse])
def list_roles(
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "roles", "read")
    return db.query(PlatformRoleModel).order_by(PlatformRoleModel.name.asc()).all()


@router.post("/roles", response_model=PlatformRoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    body: PlatformRoleCreate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "roles", "write")
    if body.tenant_id:
        _ensure_tenant_exists(db, body.tenant_id)

    model = PlatformRoleModel(
        name=body.name,
        tenant_id=body.tenant_id,
        description=body.description,
    )
    db.add(model)
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(model)
    return model


@router.get("/roles/{role_id}", response_model=PlatformRoleResponse)
def get_role(
    role_id: str,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "roles", "read")
    row = db.query(PlatformRoleModel).filter(PlatformRoleModel.id == role_id).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return row


@router.put("/roles/{role_id}", response_model=PlatformRoleResponse)
def put_role(
    role_id: str,
    body: PlatformRoleCreate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "roles", "write")
    row = db.query(PlatformRoleModel).filter(PlatformRoleModel.id == role_id).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    if body.tenant_id:
        _ensure_tenant_exists(db, body.tenant_id)

    row.name = body.name
    row.tenant_id = body.tenant_id
    row.description = body.description
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.patch("/roles/{role_id}", response_model=PlatformRoleResponse)
def patch_role(
    role_id: str,
    body: PlatformRoleUpdate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "roles", "write")
    row = db.query(PlatformRoleModel).filter(PlatformRoleModel.id == role_id).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")

    if body.tenant_id is not None:
        _ensure_tenant_exists(db, body.tenant_id)
        row.tenant_id = body.tenant_id
    if body.name is not None:
        row.name = body.name
    if body.description is not None:
        row.description = body.description

    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: str,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "roles", "write")
    row = db.query(PlatformRoleModel).filter(PlatformRoleModel.id == role_id).first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    db.delete(row)
    db.commit()


@router.get("/permissions", response_model=list[PlatformPermissionResponse])
def list_permissions(
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "permissions", "read")
    return db.query(PlatformPermissionModel).order_by(PlatformPermissionModel.name.asc()).all()


@router.post(
    "/permissions", response_model=PlatformPermissionResponse, status_code=status.HTTP_201_CREATED
)
def create_permission(
    body: PlatformPermissionCreate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    pass


@router.get("/permissions/{permission_id}", response_model=PlatformPermissionResponse)
def get_permission(
    permission_id: str,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "permissions", "read")
    row = (
        db.query(PlatformPermissionModel)
        .filter(PlatformPermissionModel.id == permission_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return row


@router.put("/permissions/{permission_id}", response_model=PlatformPermissionResponse)
def put_permission(
    permission_id: str,
    body: PlatformPermissionCreate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "permissions", "write")
    row = (
        db.query(PlatformPermissionModel)
        .filter(PlatformPermissionModel.id == permission_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    row.name = body.name
    row.resource = body.resource
    row.action = body.action.to_verb()
    row.effect = body.effect.value
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.patch("/permissions/{permission_id}", response_model=PlatformPermissionResponse)
def patch_permission(
    permission_id: str,
    body: PlatformPermissionUpdate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "permissions", "write")
    row = (
        db.query(PlatformPermissionModel)
        .filter(PlatformPermissionModel.id == permission_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    if body.name is not None:
        row.name = body.name
    if body.resource is not None:
        row.resource = body.resource
    if body.action is not None:
        row.action = body.action.to_verb()
    if body.effect is not None:
        row.effect = body.effect.value

    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.delete("/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    permission_id: str,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "permissions", "write")
    row = (
        db.query(PlatformPermissionModel)
        .filter(PlatformPermissionModel.id == permission_id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    db.delete(row)
    db.commit()


@router.get("/user-tenants", response_model=list[PlatformUserTenantResponse])
def list_user_tenants(
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-tenants", "read")
    return db.query(PlatformUserTenantModel).all()


@router.post(
    "/user-tenants", response_model=PlatformUserTenantResponse, status_code=status.HTTP_201_CREATED
)
def create_user_tenant(
    body: PlatformUserTenantCreate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-tenants", "write")
    _ensure_user_exists(db, body.user_id)
    _ensure_tenant_exists(db, body.tenant_id)
    model = PlatformUserTenantModel(
        user_id=body.user_id, tenant_id=body.tenant_id
    )
    db.add(model)
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(model)
    return model


@router.get("/user-tenants/{user_tenant_id}", response_model=PlatformUserTenantResponse)
def get_user_tenant(
    user_tenant_id: str,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-tenants", "read")
    row = (
        db.query(PlatformUserTenantModel)
        .filter(PlatformUserTenantModel.id == user_tenant_id)
        .first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User-tenant link not found"
        )
    return row


@router.put("/user-tenants/{user_tenant_id}", response_model=PlatformUserTenantResponse)
def put_user_tenant(
    user_tenant_id: str,
    body: PlatformUserTenantCreate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-tenants", "write")
    row = (
        db.query(PlatformUserTenantModel)
        .filter(PlatformUserTenantModel.id == user_tenant_id)
        .first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User-tenant link not found"
        )
    _ensure_user_exists(db, body.user_id)
    _ensure_tenant_exists(db, body.tenant_id)

    row.user_id = body.user_id
    row.tenant_id = body.tenant_id
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.patch("/user-tenants/{user_tenant_id}", response_model=PlatformUserTenantResponse)
def patch_user_tenant(
    user_tenant_id: str,
    body: PlatformUserTenantUpdate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-tenants", "write")
    row = (
        db.query(PlatformUserTenantModel)
        .filter(PlatformUserTenantModel.id == user_tenant_id)
        .first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User-tenant link not found"
        )

    if body.user_id is not None:
        _ensure_user_exists(db, body.user_id)
        row.user_id = body.user_id
    if body.tenant_id is not None:
        _ensure_tenant_exists(db, body.tenant_id)
        row.tenant_id = body.tenant_id

    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.delete("/user-tenants/{user_tenant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_tenant(
    user_tenant_id: str,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-tenants", "write")
    row = (
        db.query(PlatformUserTenantModel)
        .filter(PlatformUserTenantModel.id == user_tenant_id)
        .first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User-tenant link not found"
        )
    db.delete(row)
    db.commit()


@router.get("/user-roles", response_model=list[PlatformUserRoleResponse])
def list_user_roles(
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-roles", "read")
    return db.query(PlatformUserRoleModel).all()


@router.post(
    "/user-roles", response_model=PlatformUserRoleResponse, status_code=status.HTTP_201_CREATED
)
def create_user_role(
    body: PlatformUserRoleCreate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-roles", "write")
    _ensure_user_exists(db, body.user_id)
    _ensure_role_exists(db, body.role_id)
    model = PlatformUserRoleModel(user_id=body.user_id, role_id=body.role_id)
    db.add(model)
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(model)
    return model


@router.get("/user-roles/{user_role_id}", response_model=PlatformUserRoleResponse)
def get_user_role(
    user_role_id: str,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-roles", "read")
    row = db.query(PlatformUserRoleModel).filter(PlatformUserRoleModel.id == user_role_id).first()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User-role link not found"
        )
    return row


@router.put("/user-roles/{user_role_id}", response_model=PlatformUserRoleResponse)
def put_user_role(
    user_role_id: str,
    body: PlatformUserRoleCreate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-roles", "write")
    row = db.query(PlatformUserRoleModel).filter(PlatformUserRoleModel.id == user_role_id).first()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User-role link not found"
        )
    _ensure_user_exists(db, body.user_id)
    _ensure_role_exists(db, body.role_id)

    row.user_id = body.user_id
    row.role_id = body.role_id
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.patch("/user-roles/{user_role_id}", response_model=PlatformUserRoleResponse)
def patch_user_role(
    user_role_id: str,
    body: PlatformUserRoleUpdate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-roles", "write")
    row = db.query(PlatformUserRoleModel).filter(PlatformUserRoleModel.id == user_role_id).first()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User-role link not found"
        )

    if body.user_id is not None:
        _ensure_user_exists(db, body.user_id)
        row.user_id = body.user_id
    if body.role_id is not None:
        _ensure_role_exists(db, body.role_id)
        row.role_id = body.role_id

    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.delete("/user-roles/{user_role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_role(
    user_role_id: str,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-roles", "write")
    row = db.query(PlatformUserRoleModel).filter(PlatformUserRoleModel.id == user_role_id).first()
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User-role link not found"
        )
    db.delete(row)
    db.commit()


@router.get("/group-roles", response_model=list[PlatformGroupRoleResponse])
def list_group_roles(
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "group-roles", "read")
    return db.query(PlatformGroupRoleModel).all()


@router.post(
    "/group-roles", response_model=PlatformGroupRoleResponse, status_code=status.HTTP_201_CREATED
)
def create_group_role(
    body: PlatformGroupRoleCreate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "group-roles", "write")
    _ensure_group_exists(db, body.group_id)
    _ensure_role_exists(db, body.role_id)
    model = PlatformGroupRoleModel(group_id=body.group_id, role_id=body.role_id)
    db.add(model)
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(model)
    return model


@router.get("/group-roles/{group_role_id}", response_model=PlatformGroupRoleResponse)
def get_group_role(
    group_role_id: str,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "group-roles", "read")
    row = (
        db.query(PlatformGroupRoleModel).filter(PlatformGroupRoleModel.id == group_role_id).first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group-role link not found"
        )
    return row


@router.put("/group-roles/{group_role_id}", response_model=PlatformGroupRoleResponse)
def put_group_role(
    group_role_id: str,
    body: PlatformGroupRoleCreate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "group-roles", "write")
    row = (
        db.query(PlatformGroupRoleModel).filter(PlatformGroupRoleModel.id == group_role_id).first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group-role link not found"
        )
    _ensure_group_exists(db, body.group_id)
    _ensure_role_exists(db, body.role_id)

    row.group_id = body.group_id
    row.role_id = body.role_id
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.patch("/group-roles/{group_role_id}", response_model=PlatformGroupRoleResponse)
def patch_group_role(
    group_role_id: str,
    body: PlatformGroupRoleUpdate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "group-roles", "write")
    row = (
        db.query(PlatformGroupRoleModel).filter(PlatformGroupRoleModel.id == group_role_id).first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group-role link not found"
        )

    if body.group_id is not None:
        _ensure_group_exists(db, body.group_id)
        row.group_id = body.group_id
    if body.role_id is not None:
        _ensure_role_exists(db, body.role_id)
        row.role_id = body.role_id

    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.delete("/group-roles/{group_role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_role(
    group_role_id: str,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "group-roles", "write")
    row = (
        db.query(PlatformGroupRoleModel).filter(PlatformGroupRoleModel.id == group_role_id).first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group-role link not found"
        )
    db.delete(row)
    db.commit()


@router.get("/role-permissions", response_model=list[PlatformRolePermissionResponse])
def list_role_permissions(
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "role-permissions", "read")
    return db.query(PlatformRolePermissionModel).all()


@router.post(
    "/role-permissions",
    response_model=PlatformRolePermissionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_role_permission(
    body: PlatformRolePermissionCreate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "role-permissions", "write")
    _ensure_role_exists(db, body.role_id)
    _ensure_permission_exists(db, body.permission_id)
    model = PlatformRolePermissionModel(
        role_id=body.role_id,
        permission_id=body.permission_id,
    )
    db.add(model)
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(model)
    return model


@router.get("/role-permissions/{role_permission_id}", response_model=PlatformRolePermissionResponse)
def get_role_permission(
    role_permission_id: str,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "role-permissions", "read")
    row = (
        db.query(PlatformRolePermissionModel)
        .filter(PlatformRolePermissionModel.id == role_permission_id)
        .first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role-permission link not found"
        )
    return row


@router.put("/role-permissions/{role_permission_id}", response_model=PlatformRolePermissionResponse)
def put_role_permission(
    role_permission_id: str,
    body: PlatformRolePermissionCreate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "role-permissions", "write")
    row = (
        db.query(PlatformRolePermissionModel)
        .filter(PlatformRolePermissionModel.id == role_permission_id)
        .first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role-permission link not found"
        )
    _ensure_role_exists(db, body.role_id)
    _ensure_permission_exists(db, body.permission_id)

    row.role_id = body.role_id
    row.permission_id = body.permission_id
    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.patch(
    "/role-permissions/{role_permission_id}", response_model=PlatformRolePermissionResponse
)
def patch_role_permission(
    role_permission_id: str,
    body: PlatformRolePermissionUpdate,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "role-permissions", "write")
    row = (
        db.query(PlatformRolePermissionModel)
        .filter(PlatformRolePermissionModel.id == role_permission_id)
        .first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role-permission link not found"
        )

    if body.role_id is not None:
        _ensure_role_exists(db, body.role_id)
        row.role_id = body.role_id
    if body.permission_id is not None:
        _ensure_permission_exists(db, body.permission_id)
        row.permission_id = body.permission_id

    try:
        db.commit()
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    db.refresh(row)
    return row


@router.delete("/role-permissions/{role_permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role_permission(
    role_permission_id: str,
    db=Depends(get_db),
    current_user: PlatformUser = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "role-permissions", "write")
    row = (
        db.query(PlatformRolePermissionModel)
        .filter(PlatformRolePermissionModel.id == role_permission_id)
        .first()
    )
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Role-permission link not found"
        )
    db.delete(row)
    db.commit()
