import os
from dataclasses import dataclass
from typing import Any, Literal, Protocol, cast

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from itsor.application.use_cases.authorization_use_cases import Action, AuthorizationError, AuthorizationPrincipal, AuthorizationUseCases
try:
    from itsor.application.use_cases.custom_use_cases import EntityRecordUseCases, EntityTypeUseCases, NamespaceUseCases, WorkspaceUseCases
except ModuleNotFoundError:
    EntityRecordUseCases = EntityTypeUseCases = NamespaceUseCases = WorkspaceUseCases = Any

try:
    from itsor.application.use_cases.identity_use_cases import (
        IdmAccountUseCases,
        IdmGroupMembershipUseCases,
        IdmGroupUseCases,
        IdmIdentityUseCases,
        IdmPersonUseCases,
        IdmUserUseCases,
    )
except ModuleNotFoundError:
    IdmAccountUseCases = IdmGroupMembershipUseCases = IdmGroupUseCases = IdmIdentityUseCases = IdmPersonUseCases = IdmUserUseCases = Any
from itsor.application.use_cases.auth import (
    GroupMembershipUseCases,
    GroupRoleUseCases,
    NavigationAdminUseCases,
    GroupUseCases as AuthGroupUseCases,
    PermissionUseCases,
    RolePermissionUseCases,
    RoleUseCases,
    TenantUseCases as AuthTenantUseCases,
    UserRoleUseCases,
    UserTenantUseCases,
    UserUseCases as AuthUserUseCases,
)
from itsor.application.use_cases.auth_admin_use_cases import (
    AuthEndpointPermissionUseCases,
    AuthGroupMembershipUseCases,
    AuthModelCatalogUseCases,
    AuthRbacUseCases,
)
from itsor.application.use_cases.oscal import OscalDocumentUseCases
from itsor.infrastructure.database.sqlalchemy import get_db
from itsor.infrastructure.container import (
    get_entity_record_repository as container_get_entity_record_repository,
    get_entity_type_repository as container_get_entity_type_repository,
    get_group_membership_repository as container_get_group_membership_repository,
    get_group_repository as container_get_group_repository,
    get_group_role_repository as container_get_group_role_repository,
    get_navigation_module_repository as container_get_navigation_module_repository,
    get_navigation_resource_repository as container_get_navigation_resource_repository,
    get_navigation_view_repository as container_get_navigation_view_repository,
    get_idm_group_gateway as container_get_idm_group_gateway,
    get_namespace_repository as container_get_namespace_repository,
    get_password_hasher as container_get_password_hasher,
    get_permission_repository as container_get_permission_repository,
    get_platform_endpoint_permission_gateway as container_get_platform_endpoint_permission_gateway,
    get_platform_group_membership_gateway as container_get_platform_group_membership_gateway,
    get_role_permission_repository as container_get_role_permission_repository,
    get_role_repository as container_get_role_repository,
    get_tenant_repository as container_get_tenant_repository,
    get_user_role_repository as container_get_user_role_repository,
    get_user_repository as container_get_user_repository,
    get_user_tenant_repository as container_get_user_tenant_repository,
    get_workspace_repository as container_get_workspace_repository,
    get_token_codec as container_get_token_codec,
    get_oscal_document_repository as container_get_oscal_document_repository,
)

SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "itsor_session")
ROOT_TENANT_ID = os.getenv("ROOT_TENANT_ID", "").strip() or None
ROOT_TENANT_NAME = os.getenv("ROOT_TENANT_NAME", "Root").strip().lower()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/users/signin", auto_error=False)

CurrentUser = AuthorizationPrincipal


def get_user_repository(db=Depends(get_db)):
    return container_get_user_repository(db)


def get_tenant_repository(db=Depends(get_db)):
    return container_get_tenant_repository(db)


def get_group_repository(db=Depends(get_db)):
    return container_get_group_repository(db)


def get_group_membership_repository(db=Depends(get_db)):
    return container_get_group_membership_repository(db)


def get_navigation_module_repository(db=Depends(get_db)):
    return container_get_navigation_module_repository(db)


def get_navigation_resource_repository(db=Depends(get_db)):
    return container_get_navigation_resource_repository(db)


def get_navigation_view_repository(db=Depends(get_db)):
    return container_get_navigation_view_repository(db)


def get_workspace_repository(db=Depends(get_db)):
    return container_get_workspace_repository(db)


def get_namespace_repository(db=Depends(get_db)):
    return container_get_namespace_repository(db)


def get_entity_type_repository(db=Depends(get_db)):
    return container_get_entity_type_repository(db)


def get_entity_record_repository(db=Depends(get_db)):
    return container_get_entity_record_repository(db)


def get_oscal_document_repository(db=Depends(get_db)):
    return container_get_oscal_document_repository(db)


def get_role_repository(db=Depends(get_db)):
    return container_get_role_repository(db)


def get_permission_repository(db=Depends(get_db)):
    return container_get_permission_repository(db)


def get_user_tenant_repository(db=Depends(get_db)):
    return container_get_user_tenant_repository(db)


def get_user_role_repository(db=Depends(get_db)):
    return container_get_user_role_repository(db)


def get_group_role_repository(db=Depends(get_db)):
    return container_get_group_role_repository(db)


def get_role_permission_repository(db=Depends(get_db)):
    return container_get_role_permission_repository(db)


def get_platform_endpoint_permission_gateway(db=Depends(get_db)):
    return container_get_platform_endpoint_permission_gateway(db)


def get_platform_group_membership_gateway(db=Depends(get_db)):
    return container_get_platform_group_membership_gateway(db)


def get_idm_group_gateway(db=Depends(get_db)):
    return container_get_idm_group_gateway(db)


def get_password_hasher():
    return container_get_password_hasher()


def get_token_codec():
    return container_get_token_codec()


@dataclass
class AuthorizationService:
    use_cases: AuthorizationUseCases

    def authorize_resource_action(
        self,
        *,
        current_user: CurrentUser,
        resource: Any,
        action: Action,
        endpoint_name: str,
    ) -> None:
        try:
            self.use_cases.authorize_resource_action(
                current_user=current_user,
                resource=resource,
                action=action,
                endpoint_name=endpoint_name,
            )
        except AuthorizationError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))

    def authorize_tenant_scope(
        self,
        *,
        current_user: CurrentUser,
        tenant_id: str,
        action: Action,
        endpoint_name: str,
    ) -> None:
        try:
            self.use_cases.authorize_tenant_scope(
                current_user=current_user,
                tenant_id=tenant_id,
                action=action,
                endpoint_name=endpoint_name,
            )
        except AuthorizationError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))

    def authorize_platform_endpoint(self, *, current_user: CurrentUser, endpoint_name: str, action: Action) -> None:
        try:
            self.use_cases.authorize_platform_endpoint(
                current_user=current_user,
                endpoint_name=endpoint_name,
                action=action,
            )
        except AuthorizationError as exc:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(exc))

    def resolve_tenant_id_for_resource(self, resource: Any) -> str | None:
        return self.use_cases.resolve_tenant_id_for_resource(resource)

    def resolve_tenant_id_for_entity_type(self, entity_type_id: str) -> str | None:
        return self.use_cases.resolve_tenant_id_for_entity_type(entity_type_id)

    def resolve_tenant_id_for_namespace(self, namespace_id: str) -> str | None:
        return self.use_cases.resolve_tenant_id_for_namespace(namespace_id)

    def resolve_tenant_id_for_workspace(self, workspace_id: str) -> str | None:
        return self.use_cases.resolve_tenant_id_for_workspace(workspace_id)


def get_user_use_cases(
    repo=Depends(get_user_repository),
    tenant_repo=Depends(get_tenant_repository),
    group_repo=Depends(get_group_repository),
    password_hasher=Depends(get_password_hasher),
    token_codec=Depends(get_token_codec),
) -> AuthUserUseCases:
    return AuthUserUseCases(repo, tenant_repo, group_repo, password_hasher, token_codec)


def get_tenant_use_cases(
    repo=Depends(get_tenant_repository),
) -> AuthTenantUseCases:
    return AuthTenantUseCases(repo)


def get_group_use_cases(repo=Depends(get_group_repository)) -> AuthGroupUseCases:
    return AuthGroupUseCases(repo)


def get_role_use_cases(repo=Depends(get_role_repository)) -> RoleUseCases:
    return RoleUseCases(repo)


def get_permission_use_cases(repo=Depends(get_permission_repository)) -> PermissionUseCases:
    return PermissionUseCases(repo)


def get_user_tenant_use_cases(repo=Depends(get_user_tenant_repository)) -> UserTenantUseCases:
    return UserTenantUseCases(repo)


def get_user_role_use_cases(repo=Depends(get_user_role_repository)) -> UserRoleUseCases:
    return UserRoleUseCases(repo)


def get_group_role_use_cases(repo=Depends(get_group_role_repository)) -> GroupRoleUseCases:
    return GroupRoleUseCases(repo)


def get_role_permission_use_cases(repo=Depends(get_role_permission_repository)) -> RolePermissionUseCases:
    return RolePermissionUseCases(repo)


def get_group_membership_use_cases(repo=Depends(get_group_membership_repository)) -> GroupMembershipUseCases:
    return GroupMembershipUseCases(repo)


def get_navigation_admin_use_cases(
    module_repo=Depends(get_navigation_module_repository),
    resource_repo=Depends(get_navigation_resource_repository),
    view_repo=Depends(get_navigation_view_repository),
) -> NavigationAdminUseCases:
    return NavigationAdminUseCases(
        module_repo=module_repo,
        resource_repo=resource_repo,
        view_repo=view_repo,
    )


def get_auth_rbac_use_cases(
    user_repo=Depends(get_user_repository),
    group_repo=Depends(get_group_repository),
    tenant_repo=Depends(get_tenant_repository),
    role_repo=Depends(get_role_repository),
    permission_repo=Depends(get_permission_repository),
    user_tenant_repo=Depends(get_user_tenant_repository),
    user_role_repo=Depends(get_user_role_repository),
    group_role_repo=Depends(get_group_role_repository),
    role_permission_repo=Depends(get_role_permission_repository),
) -> AuthRbacUseCases:
    return AuthRbacUseCases(
        user_repo=user_repo,
        group_repo=group_repo,
        tenant_repo=tenant_repo,
        role_repo=role_repo,
        permission_repo=permission_repo,
        user_tenant_repo=user_tenant_repo,
        user_role_repo=user_role_repo,
        group_role_repo=group_role_repo,
        role_permission_repo=role_permission_repo,
    )


def get_auth_endpoint_permission_use_cases(
    gateway=Depends(get_platform_endpoint_permission_gateway),
    user_repo=Depends(get_user_repository),
    group_repo=Depends(get_group_repository),
) -> AuthEndpointPermissionUseCases:
    return AuthEndpointPermissionUseCases(
        gateway=gateway,
        user_repo=user_repo,
        group_repo=group_repo,
    )


def get_auth_group_membership_use_cases(
    gateway=Depends(get_platform_group_membership_gateway),
    user_repo=Depends(get_user_repository),
    group_repo=Depends(get_group_repository),
) -> AuthGroupMembershipUseCases:
    return AuthGroupMembershipUseCases(
        gateway=gateway,
        user_repo=user_repo,
        group_repo=group_repo,
    )


def get_auth_model_catalog_use_cases() -> AuthModelCatalogUseCases:
    return AuthModelCatalogUseCases()


get_platform_rbac_use_cases = get_auth_rbac_use_cases
get_platform_endpoint_permission_use_cases = get_auth_endpoint_permission_use_cases
get_platform_group_membership_use_cases = get_auth_group_membership_use_cases
get_platform_model_catalog_use_cases = get_auth_model_catalog_use_cases


def get_idm_group_use_cases(
    gateway=Depends(get_idm_group_gateway),
) -> IdmGroupUseCases:
    return IdmGroupUseCases(gateway)


def get_idm_user_use_cases(
    gateway=Depends(get_idm_group_gateway),
) -> IdmUserUseCases:
    return IdmUserUseCases(gateway)


def get_idm_account_use_cases(
    gateway=Depends(get_idm_group_gateway),
) -> IdmAccountUseCases:
    return IdmAccountUseCases(gateway)


def get_idm_person_use_cases(
    gateway=Depends(get_idm_group_gateway),
) -> IdmPersonUseCases:
    return IdmPersonUseCases(gateway)


def get_idm_identity_use_cases(
    gateway=Depends(get_idm_group_gateway),
) -> IdmIdentityUseCases:
    return IdmIdentityUseCases(gateway)


def get_idm_group_membership_use_cases(
    gateway=Depends(get_idm_group_gateway),
) -> IdmGroupMembershipUseCases:
    return IdmGroupMembershipUseCases(gateway)


def get_workspace_use_cases(
    repo=Depends(get_workspace_repository),
    namespace_repo=Depends(get_namespace_repository),
    entity_type_repo=Depends(get_entity_type_repository),
    entity_record_repo=Depends(get_entity_record_repository),
) -> WorkspaceUseCases:
    return WorkspaceUseCases(
        repo,
        namespace_repo,
        entity_type_repo,
        entity_record_repo,
    )


def get_namespace_use_cases(
    repo=Depends(get_namespace_repository),
    workspace_repo=Depends(get_workspace_repository),
    entity_type_repo=Depends(get_entity_type_repository),
    entity_record_repo=Depends(get_entity_record_repository),
) -> NamespaceUseCases:
    return NamespaceUseCases(
        repo,
        workspace_repo,
        entity_type_repo,
        entity_record_repo,
    )


def get_entity_type_use_cases(
    repo=Depends(get_entity_type_repository),
    namespace_repo=Depends(get_namespace_repository),
    entity_record_repo=Depends(get_entity_record_repository),
) -> EntityTypeUseCases:
    return EntityTypeUseCases(repo, namespace_repo, entity_record_repo)


def get_entity_record_use_cases(
    repo=Depends(get_entity_record_repository),
    entity_type_repo=Depends(get_entity_type_repository),
) -> EntityRecordUseCases:
    return EntityRecordUseCases(repo, entity_type_repo)


def get_oscal_document_use_cases(
    repo=Depends(get_oscal_document_repository),
) -> OscalDocumentUseCases:
    return OscalDocumentUseCases(repo)


def get_authorization_service(
    user_repo=Depends(get_user_repository),
    tenant_repo=Depends(get_tenant_repository),
    group_repo=Depends(get_group_repository),
    endpoint_permission_gateway=Depends(get_platform_endpoint_permission_gateway),
    workspace_repo=Depends(get_workspace_repository),
    namespace_repo=Depends(get_namespace_repository),
    entity_type_repo=Depends(get_entity_type_repository),
    entity_record_repo=Depends(get_entity_record_repository),
) -> AuthorizationService:
    use_cases = AuthorizationUseCases(
        user_repo=user_repo,
        tenant_repo=tenant_repo,
        group_repo=group_repo,
        endpoint_permission_gateway=endpoint_permission_gateway,
        workspace_repo=workspace_repo,
        namespace_repo=namespace_repo,
        entity_type_repo=entity_type_repo,
        entity_record_repo=entity_record_repo,
        root_tenant_id=ROOT_TENANT_ID,
        root_tenant_name=ROOT_TENANT_NAME,
    )
    return AuthorizationService(
        use_cases=use_cases,
    )


def get_current_user(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    use_cases: AuthUserUseCases = Depends(get_user_use_cases),
) -> CurrentUser:
    auth_token = request.cookies.get(SESSION_COOKIE_NAME) or token
    if not auth_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = use_cases.get_current_user(auth_token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return cast(CurrentUser, user)
