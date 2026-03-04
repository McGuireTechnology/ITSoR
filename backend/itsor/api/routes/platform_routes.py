"""Consolidated platform routes module."""

from typing import Any, Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from itsor.api.deps import (
    AuthorizationService,
    CurrentUser as User,
    get_authorization_service,
    get_current_user,
    get_group_use_cases,
    get_platform_endpoint_permission_use_cases,
    get_platform_group_membership_use_cases,
    get_platform_model_catalog_use_cases,
    get_platform_rbac_use_cases,
    get_tenant_use_cases,
    get_user_use_cases,
)
from itsor.api.schemas.platform_schemas import (
    GroupCreate,
    GroupReplace,
    GroupResponse,
    GroupUpdate,
    PlatformGroupMembershipCreate,
    PlatformGroupMembershipResponse,
    PlatformGroupMembershipUpdate,
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
    TenantCreate,
    TenantReplace,
    TenantResponse,
    TenantUpdate,
    UserCreate,
    UserReplace,
    UserResponse,
    UserUpdate,
)
from itsor.application.use_cases.platform_use_cases import (
    EndpointAction,
    PlatformEndpointPermissionUseCases,
    PlatformGroupMembershipUseCases,
    PlatformModelCatalogUseCases,
    PrincipalType,
)
from itsor.application.use_cases.platform_use_cases import (
    GroupUseCases,
    PlatformRbacUseCases,
    TenantUseCases,
    UserUseCases,
)

router = APIRouter(tags=["platform"])


class PlatformEndpointPermissionEntry(BaseModel):
    principal_type: PrincipalType
    principal_id: str
    endpoint_name: str
    action: EndpointAction


class PlatformEndpointPermissionUpdateRequest(BaseModel):
    principal_type: PrincipalType
    principal_id: str
    endpoint_name: str
    action: EndpointAction


class PlatformEndpointPermissionPatchRequest(BaseModel):
    principal_type: PrincipalType | None = None
    principal_id: str | None = None
    endpoint_name: str | None = None
    action: EndpointAction | None = None


class PlatformEndpointPermissionEntryResponse(BaseModel):
    id: int
    principal_type: PrincipalType
    principal_id: str
    endpoint_name: str
    action: EndpointAction

    model_config = {"from_attributes": True}


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


@router.get(
    "/endpoint-permissions",
    response_model=list[PlatformEndpointPermissionEntryResponse],
    tags=["endpoint-permissions"],
)
def list_platform_endpoint_permission_rows(
    principal_type: PrincipalType | None = None,
    principal_id: str | None = None,
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
    use_cases: PlatformEndpointPermissionUseCases = Depends(get_platform_endpoint_permission_use_cases),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="endpoint-permissions", action="read")
    return use_cases.list_rows(principal_type=principal_type, principal_id=principal_id)


@router.post(
    "/endpoint-permissions",
    response_model=PlatformEndpointPermissionEntryResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["endpoint-permissions"],
)
def create_platform_endpoint_permission_row(
    body: PlatformEndpointPermissionEntry,
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
    use_cases: PlatformEndpointPermissionUseCases = Depends(get_platform_endpoint_permission_use_cases),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="endpoint-permissions", action="write")
    try:
        return use_cases.create_row(
            principal_type=body.principal_type,
            principal_id=body.principal_id,
            endpoint_name=body.endpoint_name,
            action=body.action,
        )
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if detail in {"User not found", "Group not found"} else status.HTTP_409_CONFLICT
        raise HTTPException(status_code=status_code, detail=detail)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get(
    "/endpoint-permissions/{endpoint_permission_id}",
    response_model=PlatformEndpointPermissionEntryResponse,
    tags=["endpoint-permissions"],
)
def get_platform_endpoint_permission_row(
    endpoint_permission_id: int,
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
    use_cases: PlatformEndpointPermissionUseCases = Depends(get_platform_endpoint_permission_use_cases),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="endpoint-permissions", action="read")
    row = use_cases.get_row(endpoint_permission_id)
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform endpoint permission row not found")
    return row


@router.put(
    "/endpoint-permissions/{endpoint_permission_id}",
    response_model=PlatformEndpointPermissionEntryResponse,
    tags=["endpoint-permissions"],
)
def put_platform_endpoint_permission_row(
    endpoint_permission_id: int,
    body: PlatformEndpointPermissionUpdateRequest,
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
    use_cases: PlatformEndpointPermissionUseCases = Depends(get_platform_endpoint_permission_use_cases),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="endpoint-permissions", action="write")
    try:
        return use_cases.replace_row(
            endpoint_permission_id=endpoint_permission_id,
            principal_type=body.principal_type,
            principal_id=body.principal_id,
            endpoint_name=body.endpoint_name,
            action=body.action,
        )
    except ValueError as exc:
        detail = str(exc)
        status_code = (
            status.HTTP_404_NOT_FOUND
            if detail in {"User not found", "Group not found", "Platform endpoint permission row not found"}
            else status.HTTP_409_CONFLICT
        )
        raise HTTPException(status_code=status_code, detail=detail)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.patch(
    "/endpoint-permissions/{endpoint_permission_id}",
    response_model=PlatformEndpointPermissionEntryResponse,
    tags=["endpoint-permissions"],
)
def patch_platform_endpoint_permission_row(
    endpoint_permission_id: int,
    body: PlatformEndpointPermissionPatchRequest,
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
    use_cases: PlatformEndpointPermissionUseCases = Depends(get_platform_endpoint_permission_use_cases),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="endpoint-permissions", action="write")
    try:
        return use_cases.patch_row(
            endpoint_permission_id=endpoint_permission_id,
            principal_type=body.principal_type,
            principal_id=body.principal_id,
            endpoint_name=body.endpoint_name,
            action=body.action,
        )
    except ValueError as exc:
        detail = str(exc)
        if detail == "No fields provided for patch":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
        status_code = (
            status.HTTP_404_NOT_FOUND
            if detail in {"User not found", "Group not found", "Platform endpoint permission row not found"}
            else status.HTTP_409_CONFLICT
        )
        raise HTTPException(status_code=status_code, detail=detail)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.delete(
    "/endpoint-permissions/{endpoint_permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["endpoint-permissions"],
)
def delete_platform_endpoint_permission_row(
    endpoint_permission_id: int,
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
    use_cases: PlatformEndpointPermissionUseCases = Depends(get_platform_endpoint_permission_use_cases),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="endpoint-permissions", action="write")
    try:
        use_cases.delete_row(endpoint_permission_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get(
    "/group-memberships",
    response_model=list[PlatformGroupMembershipResponse],
    tags=["group-memberships"],
)
def list_group_memberships(
    _: User = Depends(get_current_user),
    use_cases: PlatformGroupMembershipUseCases = Depends(get_platform_group_membership_use_cases),
):
    return use_cases.list_memberships()


@router.post(
    "/group-memberships",
    response_model=PlatformGroupMembershipResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["group-memberships"],
)
def create_group_membership(
    body: PlatformGroupMembershipCreate,
    _: User = Depends(get_current_user),
    use_cases: PlatformGroupMembershipUseCases = Depends(get_platform_group_membership_use_cases),
):
    try:
        return use_cases.create_membership(
            group_id=body.group_id,
            member_type=body.member_type,
            member_user_id=body.member_user_id,
            member_group_id=body.member_group_id,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get(
    "/group-memberships/{membership_id}",
    response_model=PlatformGroupMembershipResponse,
    tags=["group-memberships"],
)
def get_group_membership(
    membership_id: str,
    _: User = Depends(get_current_user),
    use_cases: PlatformGroupMembershipUseCases = Depends(get_platform_group_membership_use_cases),
):
    membership = use_cases.get_membership(membership_id)
    if not membership:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group membership not found")
    return membership


@router.patch(
    "/group-memberships/{membership_id}",
    response_model=PlatformGroupMembershipResponse,
    tags=["group-memberships"],
)
def update_group_membership(
    membership_id: str,
    body: PlatformGroupMembershipUpdate,
    _: User = Depends(get_current_user),
    use_cases: PlatformGroupMembershipUseCases = Depends(get_platform_group_membership_use_cases),
):
    try:
        return use_cases.patch_membership(
            membership_id=membership_id,
            member_type=body.member_type,
            member_user_id=body.member_user_id,
            member_group_id=body.member_group_id,
        )
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if detail == "Group membership not found" else status.HTTP_409_CONFLICT
        raise HTTPException(status_code=status_code, detail=detail)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.delete(
    "/group-memberships/{membership_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["group-memberships"],
)
def delete_group_membership(
    membership_id: str,
    _: User = Depends(get_current_user),
    use_cases: PlatformGroupMembershipUseCases = Depends(get_platform_group_membership_use_cases),
):
    try:
        use_cases.delete_membership(membership_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/models", response_model=list[str], tags=["platform-models"])
def list_platform_models(
    use_cases: PlatformModelCatalogUseCases = Depends(get_platform_model_catalog_use_cases),
) -> list[str]:
    return use_cases.list_models()


@router.get("/models/{model_name}", tags=["platform-models"])
def get_platform_model_details(
    model_name: str,
    use_cases: PlatformModelCatalogUseCases = Depends(get_platform_model_catalog_use_cases),
) -> dict[str, Any]:
    try:
        return use_cases.get_model_details(model_name)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    except RuntimeError as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))


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


@router.get("/users", response_model=list[UserResponse], tags=["users"])
def list_users(
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="users", action="read")
    return use_cases.list_users()


@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(
    body: UserCreate,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="users", action="write")
    try:
        return use_cases.create_user(
            body.username,
            body.email,
            body.password,
            invite_group_id=body.invite_group_id,
            create_tenant_name=body.create_tenant_name,
            platform_endpoint_permissions=body.platform_endpoint_permissions,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/users/{user_id}", response_model=UserResponse, tags=["users"])
def get_user(
    user_id: str,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="users", action="read")
    user = use_cases.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/users/{user_id}", response_model=UserResponse, tags=["users"])
def update_user(
    user_id: str,
    body: UserUpdate,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="users", action="write")
    try:
        return use_cases.update_user(user_id, body.username, body.email, body.password, body.platform_endpoint_permissions)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.put("/users/{user_id}", response_model=UserResponse, tags=["users"])
def replace_user(
    user_id: str,
    body: UserReplace,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="users", action="write")
    try:
        return use_cases.replace_user(user_id, body.username, body.email, body.password, body.platform_endpoint_permissions)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
def delete_user(
    user_id: str,
    use_cases: UserUseCases = Depends(get_user_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    authz.authorize_platform_endpoint(current_user=current_user, endpoint_name="users", action="write")
    try:
        use_cases.delete_user(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/tenants", response_model=list[TenantResponse], tags=["tenants"])
def list_tenants(
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
    _: User = Depends(get_current_user),
):
    return use_cases.list_tenants()


@router.post("/tenants", response_model=TenantResponse, status_code=status.HTTP_201_CREATED, tags=["tenants"])
def create_tenant(
    body: TenantCreate,
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
    current_user: User = Depends(get_current_user),
):
    try:
        return use_cases.create_tenant(body.name, creator_user_id=current_user.id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/tenants/{tenant_id}", response_model=TenantResponse, tags=["tenants"])
def get_tenant(
    tenant_id: str,
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    tenant = use_cases.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    authz.authorize_resource_action(current_user=current_user, resource=tenant, action="read", endpoint_name="tenants")
    return tenant


@router.patch("/tenants/{tenant_id}", response_model=TenantResponse, tags=["tenants"])
def update_tenant(
    tenant_id: str,
    body: TenantUpdate,
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    tenant = use_cases.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    authz.authorize_resource_action(current_user=current_user, resource=tenant, action="write", endpoint_name="tenants")

    try:
        return use_cases.update_tenant(tenant_id, body.name)
    except ValueError as exc:
        error_detail = str(exc)
        if error_detail == "Tenant not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_detail)


@router.put("/tenants/{tenant_id}", response_model=TenantResponse, tags=["tenants"])
def replace_tenant(
    tenant_id: str,
    body: TenantReplace,
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    tenant = use_cases.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    authz.authorize_resource_action(current_user=current_user, resource=tenant, action="write", endpoint_name="tenants")

    try:
        return use_cases.replace_tenant(tenant_id, body.name)
    except ValueError as exc:
        error_detail = str(exc)
        if error_detail == "Tenant not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_detail)


@router.delete("/tenants/{tenant_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tenants"])
def delete_tenant(
    tenant_id: str,
    use_cases: TenantUseCases = Depends(get_tenant_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    tenant = use_cases.get_tenant(tenant_id)
    if not tenant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tenant not found")
    authz.authorize_resource_action(current_user=current_user, resource=tenant, action="write", endpoint_name="tenants")

    try:
        use_cases.delete_tenant(tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.get("/groups", response_model=list[GroupResponse], tags=["groups"])
def list_groups(
    use_cases: GroupUseCases = Depends(get_group_use_cases),
    _: User = Depends(get_current_user),
):
    return use_cases.list_groups()


@router.post("/groups", response_model=GroupResponse, status_code=status.HTTP_201_CREATED, tags=["groups"])
def create_group(
    body: GroupCreate,
    use_cases: GroupUseCases = Depends(get_group_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    if body.tenant_id:
        authz.authorize_tenant_scope(
            current_user=current_user,
            tenant_id=body.tenant_id,
            action="write",
            endpoint_name="groups",
        )

    try:
        return use_cases.create_group(
            body.name,
            body.tenant_id,
            creator_user_id=current_user.id,
            platform_endpoint_permissions=body.platform_endpoint_permissions,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/groups/{group_id}", response_model=GroupResponse, tags=["groups"])
def get_group(
    group_id: str,
    use_cases: GroupUseCases = Depends(get_group_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    group = use_cases.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    authz.authorize_resource_action(current_user=current_user, resource=group, action="read", endpoint_name="groups")
    return group


@router.patch("/groups/{group_id}", response_model=GroupResponse, tags=["groups"])
def update_group(
    group_id: str,
    body: GroupUpdate,
    use_cases: GroupUseCases = Depends(get_group_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    group = use_cases.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    authz.authorize_resource_action(current_user=current_user, resource=group, action="write", endpoint_name="groups")

    try:
        return use_cases.update_group(group_id, body.name, body.platform_endpoint_permissions)
    except ValueError as exc:
        error_detail = str(exc)
        if error_detail == "Group not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_detail)


@router.put("/groups/{group_id}", response_model=GroupResponse, tags=["groups"])
def replace_group(
    group_id: str,
    body: GroupReplace,
    use_cases: GroupUseCases = Depends(get_group_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    group = use_cases.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    authz.authorize_resource_action(current_user=current_user, resource=group, action="write", endpoint_name="groups")

    try:
        return use_cases.replace_group(group_id, body.name, body.platform_endpoint_permissions)
    except ValueError as exc:
        error_detail = str(exc)
        if error_detail == "Group not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_detail)


@router.delete("/groups/{group_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["groups"])
def delete_group(
    group_id: str,
    use_cases: GroupUseCases = Depends(get_group_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    group = use_cases.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    authz.authorize_resource_action(current_user=current_user, resource=group, action="write", endpoint_name="groups")

    try:
        use_cases.delete_group(group_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
