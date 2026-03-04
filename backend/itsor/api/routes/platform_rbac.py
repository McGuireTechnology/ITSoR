"""Platform RBAC routes backed by repository-driven use cases."""

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
from itsor.domain.models import User
from itsor.domain.use_cases.platform_use_cases import PlatformRbacUseCases
from itsor.infrastructure.adapters.platform_rbac_repositories import (
    SQLAlchemyGroupRoleRepository,
    SQLAlchemyPermissionRepository,
    SQLAlchemyRolePermissionRepository,
    SQLAlchemyRoleRepository,
    SQLAlchemyUserRoleRepository,
    SQLAlchemyUserTenantRepository,
)
from itsor.infrastructure.adapters.sqlalchemy_group_repository import SQLAlchemyGroupRepository
from itsor.infrastructure.adapters.sqlalchemy_tenant_repository import SQLAlchemyTenantRepository
from itsor.infrastructure.adapters.sqlalchemy_user_repository import SQLAlchemyUserRepository
from itsor.infrastructure.container.database import get_db

router = APIRouter()

_NOT_FOUND_MESSAGES = {
    "User not found",
    "Group not found",
    "Tenant not found",
    "Role not found",
    "Permission not found",
    "User-tenant link not found",
    "User-role link not found",
    "Group-role link not found",
    "Role-permission link not found",
}


def _authz(
    current_user: User,
    authz: AuthorizationService,
    endpoint_name: str,
    action: Literal["read", "write"],
) -> None:
    authz.authorize_platform_endpoint(
        current_user=current_user,
        endpoint_name=endpoint_name,
        action=action,
    )


def _raise_http_for_value_error(exc: ValueError) -> None:
    message = str(exc)
    if message in _NOT_FOUND_MESSAGES or message.endswith(" not found"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=message)


def _raise_conflict(exc: Exception) -> None:
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


def get_platform_rbac_use_cases(db=Depends(get_db)) -> PlatformRbacUseCases:
    return PlatformRbacUseCases(
        user_repo=SQLAlchemyUserRepository(db),
        group_repo=SQLAlchemyGroupRepository(db),
        tenant_repo=SQLAlchemyTenantRepository(db),
        role_repo=SQLAlchemyRoleRepository(db),
        permission_repo=SQLAlchemyPermissionRepository(db),
        user_tenant_repo=SQLAlchemyUserTenantRepository(db),
        user_role_repo=SQLAlchemyUserRoleRepository(db),
        group_role_repo=SQLAlchemyGroupRoleRepository(db),
        role_permission_repo=SQLAlchemyRolePermissionRepository(db),
    )


@router.get("/roles", response_model=list[PlatformRoleResponse], tags=["roles"])
def list_roles(
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "roles", "read")
    return use_cases.list_roles()


@router.post(
    "/roles",
    response_model=PlatformRoleResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["roles"],
)
def create_role(
    body: PlatformRoleCreate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "roles", "write")
    try:
        return use_cases.create_role(
            name=body.name,
            tenant_id=body.tenant_id,
            description=body.description,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.get("/roles/{role_id}", response_model=PlatformRoleResponse, tags=["roles"])
def get_role(
    role_id: str,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "roles", "read")
    row = use_cases.get_role(role_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return row


@router.put("/roles/{role_id}", response_model=PlatformRoleResponse, tags=["roles"])
def put_role(
    role_id: str,
    body: PlatformRoleCreate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "roles", "write")
    try:
        return use_cases.replace_role(
            role_id=role_id,
            name=body.name,
            tenant_id=body.tenant_id,
            description=body.description,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.patch("/roles/{role_id}", response_model=PlatformRoleResponse, tags=["roles"])
def patch_role(
    role_id: str,
    body: PlatformRoleUpdate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "roles", "write")
    try:
        return use_cases.update_role(
            role_id=role_id,
            name=body.name,
            tenant_id=body.tenant_id,
            description=body.description,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["roles"])
def delete_role(
    role_id: str,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "roles", "write")
    try:
        use_cases.delete_role(role_id)
    except ValueError as exc:
        _raise_http_for_value_error(exc)


@router.get("/permissions", response_model=list[PlatformPermissionResponse], tags=["permissions"])
def list_permissions(
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "permissions", "read")
    return use_cases.list_permissions()


@router.post(
    "/permissions",
    response_model=PlatformPermissionResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["permissions"],
)
def create_permission(
    body: PlatformPermissionCreate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "permissions", "write")
    try:
        return use_cases.create_permission(
            name=body.name,
            resource=body.resource,
            action=body.action,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.get(
    "/permissions/{permission_id}", response_model=PlatformPermissionResponse, tags=["permissions"]
)
def get_permission(
    permission_id: str,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "permissions", "read")
    row = use_cases.get_permission(permission_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return row


@router.put(
    "/permissions/{permission_id}", response_model=PlatformPermissionResponse, tags=["permissions"]
)
def put_permission(
    permission_id: str,
    body: PlatformPermissionCreate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "permissions", "write")
    try:
        return use_cases.replace_permission(
            permission_id=permission_id,
            name=body.name,
            resource=body.resource,
            action=body.action,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.patch(
    "/permissions/{permission_id}", response_model=PlatformPermissionResponse, tags=["permissions"]
)
def patch_permission(
    permission_id: str,
    body: PlatformPermissionUpdate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "permissions", "write")
    try:
        return use_cases.update_permission(
            permission_id=permission_id,
            name=body.name,
            resource=body.resource,
            action=body.action,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.delete(
    "/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["permissions"]
)
def delete_permission(
    permission_id: str,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "permissions", "write")
    try:
        use_cases.delete_permission(permission_id)
    except ValueError as exc:
        _raise_http_for_value_error(exc)


@router.get("/user-tenants", response_model=list[PlatformUserTenantResponse], tags=["user-tenants"])
def list_user_tenants(
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-tenants", "read")
    return use_cases.list_user_tenants()


@router.post(
    "/user-tenants",
    response_model=PlatformUserTenantResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["user-tenants"],
)
def create_user_tenant(
    body: PlatformUserTenantCreate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-tenants", "write")
    try:
        return use_cases.create_user_tenant(user_id=body.user_id, tenant_id=body.tenant_id)
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.get(
    "/user-tenants/{user_tenant_id}",
    response_model=PlatformUserTenantResponse,
    tags=["user-tenants"],
)
def get_user_tenant(
    user_tenant_id: str,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-tenants", "read")
    row = use_cases.get_user_tenant(user_tenant_id)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User-tenant link not found",
        )
    return row


@router.put(
    "/user-tenants/{user_tenant_id}",
    response_model=PlatformUserTenantResponse,
    tags=["user-tenants"],
)
def put_user_tenant(
    user_tenant_id: str,
    body: PlatformUserTenantCreate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-tenants", "write")
    try:
        return use_cases.replace_user_tenant(
            user_tenant_id=user_tenant_id,
            user_id=body.user_id,
            tenant_id=body.tenant_id,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.patch(
    "/user-tenants/{user_tenant_id}",
    response_model=PlatformUserTenantResponse,
    tags=["user-tenants"],
)
def patch_user_tenant(
    user_tenant_id: str,
    body: PlatformUserTenantUpdate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-tenants", "write")
    try:
        return use_cases.update_user_tenant(
            user_tenant_id=user_tenant_id,
            user_id=body.user_id,
            tenant_id=body.tenant_id,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.delete(
    "/user-tenants/{user_tenant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["user-tenants"],
)
def delete_user_tenant(
    user_tenant_id: str,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-tenants", "write")
    try:
        use_cases.delete_user_tenant(user_tenant_id)
    except ValueError as exc:
        _raise_http_for_value_error(exc)


@router.get("/user-roles", response_model=list[PlatformUserRoleResponse], tags=["user-roles"])
def list_user_roles(
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-roles", "read")
    return use_cases.list_user_roles()


@router.post(
    "/user-roles",
    response_model=PlatformUserRoleResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["user-roles"],
)
def create_user_role(
    body: PlatformUserRoleCreate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-roles", "write")
    try:
        return use_cases.create_user_role(user_id=body.user_id, role_id=body.role_id)
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.get(
    "/user-roles/{user_role_id}", response_model=PlatformUserRoleResponse, tags=["user-roles"]
)
def get_user_role(
    user_role_id: str,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-roles", "read")
    row = use_cases.get_user_role(user_role_id)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User-role link not found",
        )
    return row


@router.put(
    "/user-roles/{user_role_id}", response_model=PlatformUserRoleResponse, tags=["user-roles"]
)
def put_user_role(
    user_role_id: str,
    body: PlatformUserRoleCreate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-roles", "write")
    try:
        return use_cases.replace_user_role(
            user_role_id=user_role_id,
            user_id=body.user_id,
            role_id=body.role_id,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.patch(
    "/user-roles/{user_role_id}", response_model=PlatformUserRoleResponse, tags=["user-roles"]
)
def patch_user_role(
    user_role_id: str,
    body: PlatformUserRoleUpdate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-roles", "write")
    try:
        return use_cases.update_user_role(
            user_role_id=user_role_id,
            user_id=body.user_id,
            role_id=body.role_id,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.delete(
    "/user-roles/{user_role_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["user-roles"]
)
def delete_user_role(
    user_role_id: str,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "user-roles", "write")
    try:
        use_cases.delete_user_role(user_role_id)
    except ValueError as exc:
        _raise_http_for_value_error(exc)


@router.get("/group-roles", response_model=list[PlatformGroupRoleResponse], tags=["group-roles"])
def list_group_roles(
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "group-roles", "read")
    return use_cases.list_group_roles()


@router.post(
    "/group-roles",
    response_model=PlatformGroupRoleResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["group-roles"],
)
def create_group_role(
    body: PlatformGroupRoleCreate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "group-roles", "write")
    try:
        return use_cases.create_group_role(group_id=body.group_id, role_id=body.role_id)
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.get(
    "/group-roles/{group_role_id}", response_model=PlatformGroupRoleResponse, tags=["group-roles"]
)
def get_group_role(
    group_role_id: str,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "group-roles", "read")
    row = use_cases.get_group_role(group_role_id)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group-role link not found",
        )
    return row


@router.put(
    "/group-roles/{group_role_id}", response_model=PlatformGroupRoleResponse, tags=["group-roles"]
)
def put_group_role(
    group_role_id: str,
    body: PlatformGroupRoleCreate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "group-roles", "write")
    try:
        return use_cases.replace_group_role(
            group_role_id=group_role_id,
            group_id=body.group_id,
            role_id=body.role_id,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.patch(
    "/group-roles/{group_role_id}", response_model=PlatformGroupRoleResponse, tags=["group-roles"]
)
def patch_group_role(
    group_role_id: str,
    body: PlatformGroupRoleUpdate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "group-roles", "write")
    try:
        return use_cases.update_group_role(
            group_role_id=group_role_id,
            group_id=body.group_id,
            role_id=body.role_id,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.delete(
    "/group-roles/{group_role_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["group-roles"]
)
def delete_group_role(
    group_role_id: str,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "group-roles", "write")
    try:
        use_cases.delete_group_role(group_role_id)
    except ValueError as exc:
        _raise_http_for_value_error(exc)


@router.get(
    "/role-permissions",
    response_model=list[PlatformRolePermissionResponse],
    tags=["role-permissions"],
)
def list_role_permissions(
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "role-permissions", "read")
    return use_cases.list_role_permissions()


@router.post(
    "/role-permissions",
    response_model=PlatformRolePermissionResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["role-permissions"],
)
def create_role_permission(
    body: PlatformRolePermissionCreate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "role-permissions", "write")
    try:
        return use_cases.create_role_permission(
            role_id=body.role_id,
            permission_id=body.permission_id,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.get(
    "/role-permissions/{role_permission_id}",
    response_model=PlatformRolePermissionResponse,
    tags=["role-permissions"],
)
def get_role_permission(
    role_permission_id: str,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "role-permissions", "read")
    row = use_cases.get_role_permission(role_permission_id)
    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role-permission link not found",
        )
    return row


@router.put(
    "/role-permissions/{role_permission_id}",
    response_model=PlatformRolePermissionResponse,
    tags=["role-permissions"],
)
def put_role_permission(
    role_permission_id: str,
    body: PlatformRolePermissionCreate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "role-permissions", "write")
    try:
        return use_cases.replace_role_permission(
            role_permission_id=role_permission_id,
            role_id=body.role_id,
            permission_id=body.permission_id,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.patch(
    "/role-permissions/{role_permission_id}",
    response_model=PlatformRolePermissionResponse,
    tags=["role-permissions"],
)
def patch_role_permission(
    role_permission_id: str,
    body: PlatformRolePermissionUpdate,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "role-permissions", "write")
    try:
        return use_cases.update_role_permission(
            role_permission_id=role_permission_id,
            role_id=body.role_id,
            permission_id=body.permission_id,
        )
    except ValueError as exc:
        _raise_http_for_value_error(exc)
    except Exception as exc:
        _raise_conflict(exc)


@router.delete(
    "/role-permissions/{role_permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["role-permissions"],
)
def delete_role_permission(
    role_permission_id: str,
    use_cases: PlatformRbacUseCases = Depends(get_platform_rbac_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    _authz(current_user, authz, "role-permissions", "write")
    try:
        use_cases.delete_role_permission(role_permission_id)
    except ValueError as exc:
        _raise_http_for_value_error(exc)
