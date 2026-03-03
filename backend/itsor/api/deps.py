import os
from dataclasses import dataclass
from typing import Literal

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from itsor.domain.models import BaseModel, PermissionLevel, PlatformResourceAction, PlatformTenant, PlatformUser
from itsor.domain.use_cases.entity_record_use_cases import EntityRecordUseCases
from itsor.domain.use_cases.entity_type_use_cases import EntityTypeUseCases
from itsor.domain.use_cases.group_use_cases import GroupUseCases
from itsor.domain.use_cases.namespace_use_cases import NamespaceUseCases
from itsor.domain.use_cases.tenant_use_cases import TenantUseCases
from itsor.domain.use_cases.user_use_cases import UserUseCases
from itsor.domain.use_cases.workspace_use_cases import WorkspaceUseCases
from itsor.domain.ports.entity_record_repository import EntityRecordRepository
from itsor.domain.ports.entity_type_repository import EntityTypeRepository
from itsor.domain.ports.group_repository import GroupRepository
from itsor.domain.ports.namespace_repository import NamespaceRepository
from itsor.domain.ports.tenant_repository import TenantRepository
from itsor.domain.ports.user_repository import UserRepository
from itsor.domain.ports.workspace_repository import WorkspaceRepository
from itsor.infrastructure.container.repositories import (
    get_entity_record_repository,
    get_entity_type_repository,
    get_group_repository,
    get_namespace_repository,
    get_tenant_repository,
    get_user_repository,
    get_workspace_repository,
)

SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "itsor_session")
ROOT_TENANT_ID = os.getenv("ROOT_TENANT_ID", "").strip() or None
ROOT_TENANT_NAME = os.getenv("ROOT_TENANT_NAME", "Root").strip().lower()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)

Action = PlatformResourceAction | Literal["read", "write"]


@dataclass
class AuthorizationService:
    user_repo: UserRepository
    tenant_repo: TenantRepository
    group_repo: GroupRepository
    workspace_repo: WorkspaceRepository
    namespace_repo: NamespaceRepository
    entity_type_repo: EntityTypeRepository
    entity_record_repo: EntityRecordRepository

    def authorize_resource_action(
        self,
        *,
        current_user: PlatformUser,
        resource: BaseModel,
        action: Action,
        endpoint_name: str,
    ) -> None:
        if self._is_root_tenant_operator(current_user):
            return

        if resource.owner_id and str(resource.owner_id) == str(current_user.id):
            return

        if not self._resource_permission_allows(resource, current_user, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Resource permission bytes are insufficient for this action",
            )

        tenant_id = self.resolve_tenant_id_for_resource(resource)
        if tenant_id is None:
            return

        self.authorize_tenant_scope(current_user=current_user, tenant_id=tenant_id, action=action, endpoint_name=endpoint_name)

    def authorize_tenant_scope(
        self,
        *,
        current_user: PlatformUser,
        tenant_id: str,
        action: Action,
        endpoint_name: str,
    ) -> None:
        if self._is_root_tenant_operator(current_user):
            return

        if not self._endpoint_permission_allows(current_user, endpoint_name, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No permission for endpoint '{endpoint_name}' in tenant",
            )

        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            return

        if tenant.owner_id and str(tenant.owner_id) == str(current_user.id):
            return

        user_tenant_id = self._resolve_user_tenant_id(current_user)
        if not user_tenant_id or str(user_tenant_id) != str(tenant.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No permission for endpoint '{endpoint_name}' in tenant",
            )

        if not self._resource_permission_allows(tenant, current_user, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient tenant permissions for this action",
            )

    def authorize_platform_endpoint(self, *, current_user: PlatformUser, endpoint_name: str, action: Action) -> None:
        if self._is_root_tenant_operator(current_user):
            return
        if not self._endpoint_permission_allows(current_user, endpoint_name, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No platform endpoint permission for '{endpoint_name}'",
            )

    def resolve_tenant_id_for_resource(self, resource: BaseModel) -> str | None:
        tenant_id = getattr(resource, "tenant_id", None)
        if tenant_id:
            return str(tenant_id)

        workspace_id = getattr(resource, "workspace_id", None)
        if workspace_id:
            workspace = self.workspace_repo.get_by_id(str(workspace_id))
            return str(workspace.tenant_id) if workspace and workspace.tenant_id else None

        namespace_id = getattr(resource, "namespace_id", None)
        if namespace_id:
            namespace = self.namespace_repo.get_by_id(str(namespace_id))
            if not namespace:
                return None
            workspace = self.workspace_repo.get_by_id(str(namespace.workspace_id))
            return str(workspace.tenant_id) if workspace and workspace.tenant_id else None

        entity_type_id = getattr(resource, "entity_type_id", None)
        if entity_type_id:
            entity_type = self.entity_type_repo.get_by_id(str(entity_type_id))
            if not entity_type:
                return None
            namespace = self.namespace_repo.get_by_id(str(entity_type.namespace_id))
            if not namespace:
                return None
            workspace = self.workspace_repo.get_by_id(str(namespace.workspace_id))
            return str(workspace.tenant_id) if workspace and workspace.tenant_id else None

        return None

    def resolve_tenant_id_for_entity_type(self, entity_type_id: str) -> str | None:
        entity_type = self.entity_type_repo.get_by_id(entity_type_id)
        if not entity_type:
            return None
        return self.resolve_tenant_id_for_resource(entity_type)

    def resolve_tenant_id_for_namespace(self, namespace_id: str) -> str | None:
        namespace = self.namespace_repo.get_by_id(namespace_id)
        if not namespace:
            return None
        return self.resolve_tenant_id_for_resource(namespace)

    def resolve_tenant_id_for_workspace(self, workspace_id: str) -> str | None:
        workspace = self.workspace_repo.get_by_id(workspace_id)
        if not workspace:
            return None
        return self.resolve_tenant_id_for_resource(workspace)

    def _is_root_tenant_operator(self, current_user: PlatformUser) -> bool:
        root_tenant_id = self._resolve_root_tenant_id()
        if not root_tenant_id:
            return False
        user_tenant_id = self._resolve_user_tenant_id(current_user)
        return bool(user_tenant_id and str(user_tenant_id) == str(root_tenant_id))

    def _resolve_root_tenant_id(self) -> str | None:
        if ROOT_TENANT_ID:
            root = self.tenant_repo.get_by_id(ROOT_TENANT_ID)
            if root:
                return str(root.id)

        for tenant in self.tenant_repo.list():
            if tenant.name and str(tenant.name).strip().lower() == ROOT_TENANT_NAME:
                return str(tenant.id)
        return None

    def _resolve_user_tenant_id(self, current_user: PlatformUser) -> str | None:
        if not current_user.group_id:
            return None
        group = self.group_repo.get_by_id(str(current_user.group_id))
        if not group or not group.tenant_id:
            return None
        return str(group.tenant_id)

    def _resource_permission_allows(self, resource: BaseModel | PlatformTenant, current_user: PlatformUser, action: Action) -> bool:
        granted = self._granted_permission_level(resource, current_user)
        required = int(PermissionLevel.READ if action == "read" else PermissionLevel.WRITE)
        return (int(granted) & required) == required

    def _endpoint_permission_allows(self, current_user: PlatformUser, endpoint_name: str, action: Action) -> bool:
        endpoint = str(endpoint_name).strip().lower()
        op = action.value if isinstance(action, PlatformResourceAction) else str(action).strip().lower()

        policies: list[dict[str, list[str]]] = []

        if isinstance(current_user.platform_endpoint_permissions, dict):
            policies.append(current_user.platform_endpoint_permissions)

        if current_user.group_id:
            group = self.group_repo.get_by_id(str(current_user.group_id))
            group_policy = getattr(group, "platform_endpoint_permissions", None) if group else None
            if isinstance(group_policy, dict):
                policies.append(group_policy)

        if not policies:
            return True

        if not any(policy for policy in policies):
            return True

        for policy in policies:
            if self._policy_allows(policy, endpoint, op):
                return True
        return False

    @staticmethod
    def _policy_allows(policy: dict[str, list[str]], endpoint: str, action: str) -> bool:
        candidates = [endpoint, "*"]
        for key in candidates:
            allowed = policy.get(key)
            if not isinstance(allowed, list):
                continue
            normalized = {
                item.value if isinstance(item, PlatformResourceAction) else str(item).strip().lower()
                for item in allowed
            }
            if "*" in normalized or action in normalized:
                return True
        return False

    def _granted_permission_level(self, resource: BaseModel | PlatformTenant, current_user: PlatformUser) -> int:
        if resource.owner_id and str(resource.owner_id) == str(current_user.id):
            return int(resource.owner_permissions)
        if resource.group_id and current_user.group_id and str(resource.group_id) == str(current_user.group_id):
            return int(resource.group_permissions)
        return int(resource.world_permissions)


def get_user_use_cases(
    repo=Depends(get_user_repository),
    tenant_repo=Depends(get_tenant_repository),
    group_repo=Depends(get_group_repository),
) -> UserUseCases:
    return UserUseCases(repo, tenant_repo, group_repo)


def get_tenant_use_cases(
    repo=Depends(get_tenant_repository),
    group_repo=Depends(get_group_repository),
    user_repo=Depends(get_user_repository),
) -> TenantUseCases:
    return TenantUseCases(repo, group_repo, user_repo)


def get_group_use_cases(repo=Depends(get_group_repository)) -> GroupUseCases:
    return GroupUseCases(repo)


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


def get_authorization_service(
    user_repo: UserRepository = Depends(get_user_repository),
    tenant_repo: TenantRepository = Depends(get_tenant_repository),
    group_repo: GroupRepository = Depends(get_group_repository),
    workspace_repo: WorkspaceRepository = Depends(get_workspace_repository),
    namespace_repo: NamespaceRepository = Depends(get_namespace_repository),
    entity_type_repo: EntityTypeRepository = Depends(get_entity_type_repository),
    entity_record_repo: EntityRecordRepository = Depends(get_entity_record_repository),
) -> AuthorizationService:
    return AuthorizationService(
        user_repo=user_repo,
        tenant_repo=tenant_repo,
        group_repo=group_repo,
        workspace_repo=workspace_repo,
        namespace_repo=namespace_repo,
        entity_type_repo=entity_type_repo,
        entity_record_repo=entity_record_repo,
    )


def get_current_user(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    use_cases: UserUseCases = Depends(get_user_use_cases),
) -> PlatformUser:
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
    return user
