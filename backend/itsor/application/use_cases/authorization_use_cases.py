from dataclasses import dataclass
from typing import Any, Literal, Protocol


Action = Literal["read", "write"]

PERMISSION_READ = 0b01
PERMISSION_WRITE = 0b10


class AuthorizationPrincipal(Protocol):
    id: str
    group_id: str | None


class AuthorizationError(Exception):
    pass


@dataclass
class AuthorizationUseCases:
    user_repo: Any
    tenant_repo: Any
    group_repo: Any
    workspace_repo: Any
    namespace_repo: Any
    entity_type_repo: Any
    entity_record_repo: Any
    endpoint_permission_gateway: Any | None = None
    root_tenant_id: str | None = None
    root_tenant_name: str = "root"

    def authorize_resource_action(
        self,
        *,
        current_user: AuthorizationPrincipal,
        resource: Any,
        action: Action,
        endpoint_name: str,
    ) -> None:
        if self._is_root_tenant_operator(current_user):
            return

        if resource.owner_id and str(resource.owner_id) == str(current_user.id):
            return

        if not self._resource_permission_allows(resource, current_user, action):
            raise AuthorizationError("Resource permission bytes are insufficient for this action")

        tenant_id = self.resolve_tenant_id_for_resource(resource)
        if tenant_id is None:
            return

        self.authorize_tenant_scope(current_user=current_user, tenant_id=tenant_id, action=action, endpoint_name=endpoint_name)

    def authorize_tenant_scope(
        self,
        *,
        current_user: AuthorizationPrincipal,
        tenant_id: str,
        action: Action,
        endpoint_name: str,
    ) -> None:
        if self._is_root_tenant_operator(current_user):
            return

        if not self._endpoint_permission_allows(current_user, endpoint_name, action):
            raise AuthorizationError(f"No permission for endpoint '{endpoint_name}' in tenant")

        tenant = self.tenant_repo.get_by_id(tenant_id)
        if not tenant:
            return

        tenant_owner_id = getattr(tenant, "owner_id", None)
        if tenant_owner_id and str(tenant_owner_id) == str(current_user.id):
            return

        user_tenant_id = self._resolve_user_tenant_id(current_user)
        if not user_tenant_id or str(user_tenant_id) != str(tenant.id):
            raise AuthorizationError(f"No permission for endpoint '{endpoint_name}' in tenant")

        if not self._resource_permission_allows(tenant, current_user, action):
            raise AuthorizationError("Insufficient tenant permissions for this action")

    def authorize_platform_endpoint(
        self,
        *,
        current_user: AuthorizationPrincipal,
        endpoint_name: str,
        action: Action,
    ) -> None:
        if self._is_root_tenant_operator(current_user):
            return
        if not self._endpoint_permission_allows(current_user, endpoint_name, action):
            raise AuthorizationError(f"No platform endpoint permission for '{endpoint_name}'")

    def resolve_tenant_id_for_resource(self, resource: Any) -> str | None:
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

    def _is_root_tenant_operator(self, current_user: AuthorizationPrincipal) -> bool:
        root_tenant_id = self._resolve_root_tenant_id()
        if not root_tenant_id:
            return False
        user_tenant_id = self._resolve_user_tenant_id(current_user)
        return bool(user_tenant_id and str(user_tenant_id) == str(root_tenant_id))

    def _resolve_root_tenant_id(self) -> str | None:
        if self.root_tenant_id:
            root = self.tenant_repo.get_by_id(self.root_tenant_id)
            if root:
                return str(root.id)

        for tenant in self.tenant_repo.list():
            if tenant.name and str(tenant.name).strip().lower() == self.root_tenant_name:
                return str(tenant.id)
        return None

    def _resolve_user_tenant_id(self, current_user: AuthorizationPrincipal) -> str | None:
        if not current_user.group_id:
            return None
        group = self.group_repo.get_by_id(str(current_user.group_id))
        if not group or not group.tenant_id:
            return None
        return str(group.tenant_id)

    def _resource_permission_allows(self, resource: Any, current_user: AuthorizationPrincipal, action: Action) -> bool:
        granted = self._granted_permission_level(resource, current_user)
        required = PERMISSION_READ if action == "read" else PERMISSION_WRITE
        return (int(granted) & required) == required

    def _endpoint_permission_allows(self, current_user: AuthorizationPrincipal, endpoint_name: str, action: Action) -> bool:
        endpoint = str(endpoint_name).strip().lower()
        op = str(action).strip().lower()

        policies = self._load_endpoint_policies(
            principal_type="user",
            principal_id=str(current_user.id),
        )

        if current_user.group_id:
            policies.extend(
                self._load_endpoint_policies(
                    principal_type="group",
                    principal_id=str(current_user.group_id),
                )
            )

        if not policies:
            return True

        for policy in policies:
            if self._policy_allows(policy, endpoint, op):
                return True
        return False

    def _load_endpoint_policies(
        self,
        *,
        principal_type: str,
        principal_id: str,
    ) -> list[dict[str, list[str]]]:
        gateway = self.endpoint_permission_gateway
        list_rows = getattr(gateway, "list_rows", None)
        if not callable(list_rows):
            return []

        rows = list_rows(
            principal_type=principal_type,
            principal_id=principal_id,
        )

        policy: dict[str, list[str]] = {}
        for row in rows:
            endpoint = str(getattr(row, "endpoint_name", "")).strip().lower()
            operation = str(getattr(row, "action", "")).strip().lower()
            if not endpoint or not operation:
                continue
            allowed = policy.setdefault(endpoint, [])
            if operation not in allowed:
                allowed.append(operation)

        return [policy] if policy else []

    @staticmethod
    def _policy_allows(policy: dict[str, list[str]], endpoint: str, action: str) -> bool:
        candidates = [endpoint, "*"]
        for key in candidates:
            allowed = policy.get(key)
            if not isinstance(allowed, list):
                continue
            normalized = {
                str(item).strip().lower()
                for item in allowed
            }
            if "*" in normalized or action in normalized:
                return True
        return False

    def _granted_permission_level(self, resource: Any, current_user: AuthorizationPrincipal) -> int:
        if resource.owner_id and str(resource.owner_id) == str(current_user.id):
            return int(resource.owner_permissions)
        if resource.group_id and current_user.group_id and str(resource.group_id) == str(current_user.group_id):
            return int(resource.group_permissions)
        return int(resource.world_permissions)
