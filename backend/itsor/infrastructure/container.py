import os

from itsor.application.ports.inbox.custom_ports import EntityRecordRepository, EntityTypeRepository, NamespaceRepository, WorkspaceRepository
from itsor.application.ports.auth import (
    GroupMembershipRepository,
    GroupRepository,
    TenantRepository,
    UserRepository,
    GroupRoleRepository,
    NavigationModuleRepository,
    NavigationResourceRepository,
    NavigationViewRepository,
    PasswordHasher,
    PermissionRepository,
    RolePermissionRepository,
    RoleRepository,
    TokenCodec,
    UserRoleRepository,
    UserTenantRepository,
)
from itsor.infrastructure.adapters.in_memory_entity_record_repository import InMemoryEntityRecordRepository
from itsor.infrastructure.adapters.in_memory_entity_type_repository import InMemoryEntityTypeRepository
from itsor.infrastructure.adapters.in_memory_namespace_repository import InMemoryNamespaceRepository
from itsor.infrastructure.adapters.in_memory_workspace_repository import InMemoryWorkspaceRepository
from itsor.infrastructure.adapters.memory.auth_repository import (
    InMemoryGroupRepository,
    InMemoryTenantRepository,
    InMemoryUserRepository,
)
from itsor.infrastructure.adapters.sqlalchemy.auth_repository import (
    BcryptPasswordHasher,
    JwtTokenCodec,
    SQLAlchemyGroupMembershipRepository,
    SQLAlchemyGroupRepository,
    SQLAlchemyGroupRoleRepository,
    SQLAlchemyNavigationModuleRepository,
    SQLAlchemyNavigationResourceRepository,
    SQLAlchemyNavigationViewRepository,
    SQLAlchemyPermissionRepository,
    SQLAlchemyPlatformEndpointPermissionGateway,
    SQLAlchemyPlatformGroupMembershipGateway,
    SQLAlchemyRolePermissionRepository,
    SQLAlchemyRoleRepository,
    SQLAlchemyTenantRepository,
    SQLAlchemyUserRepository,
    SQLAlchemyUserRoleRepository,
    SQLAlchemyUserTenantRepository,
)
from itsor.infrastructure.adapters.sqlalchemy.identity_gateway import SQLAlchemyIdmGroupGateway
from itsor.infrastructure.adapters.sqlalchemy_entity_record_repository import SQLAlchemyEntityRecordRepository
from itsor.infrastructure.adapters.sqlalchemy_entity_type_repository import SQLAlchemyEntityTypeRepository
from itsor.infrastructure.adapters.sqlalchemy_namespace_repository import SQLAlchemyNamespaceRepository
from itsor.infrastructure.adapters.sqlalchemy_workspace_repository import SQLAlchemyWorkspaceRepository


BACKEND = os.getenv("USER_REPOSITORY_BACKEND", "sqlalchemy").lower()


def _unsupported_backend() -> RuntimeError:
    return RuntimeError(f"Unsupported USER_REPOSITORY_BACKEND: {BACKEND}")


def _raise_platform_sqlalchemy_required() -> RuntimeError:
    return RuntimeError("Platform RBAC repositories require USER_REPOSITORY_BACKEND=sqlalchemy")


def _raise_platform_gateway_sqlalchemy_required() -> RuntimeError:
    return RuntimeError("Platform admin gateways require USER_REPOSITORY_BACKEND=sqlalchemy")


def _get_user_repository_sqlalchemy(db=None) -> UserRepository:
    return SQLAlchemyUserRepository(db)


def _get_tenant_repository_sqlalchemy(db=None) -> TenantRepository:
    return SQLAlchemyTenantRepository(db)


def _get_group_repository_sqlalchemy(db=None) -> GroupRepository:
    return SQLAlchemyGroupRepository(db)


def _get_group_membership_repository_sqlalchemy(db=None) -> GroupMembershipRepository:
    return SQLAlchemyGroupMembershipRepository(db)


def _get_navigation_module_repository_sqlalchemy(db=None) -> NavigationModuleRepository:
    return SQLAlchemyNavigationModuleRepository(db)


def _get_navigation_resource_repository_sqlalchemy(db=None) -> NavigationResourceRepository:
    return SQLAlchemyNavigationResourceRepository(db)


def _get_navigation_view_repository_sqlalchemy(db=None) -> NavigationViewRepository:
    return SQLAlchemyNavigationViewRepository(db)


def _get_workspace_repository_sqlalchemy(db=None) -> WorkspaceRepository:
    return SQLAlchemyWorkspaceRepository(db)


def _get_namespace_repository_sqlalchemy(db=None) -> NamespaceRepository:
    return SQLAlchemyNamespaceRepository(db)


def _get_entity_type_repository_sqlalchemy(db=None) -> EntityTypeRepository:
    return SQLAlchemyEntityTypeRepository(db)


def _get_entity_record_repository_sqlalchemy(db=None) -> EntityRecordRepository:
    return SQLAlchemyEntityRecordRepository(db)


def _get_role_repository_sqlalchemy(db=None) -> RoleRepository:
    return SQLAlchemyRoleRepository(db)


def _get_permission_repository_sqlalchemy(db=None) -> PermissionRepository:
    return SQLAlchemyPermissionRepository(db)


def _get_user_tenant_repository_sqlalchemy(db=None) -> UserTenantRepository:
    return SQLAlchemyUserTenantRepository(db)


def _get_user_role_repository_sqlalchemy(db=None) -> UserRoleRepository:
    return SQLAlchemyUserRoleRepository(db)


def _get_group_role_repository_sqlalchemy(db=None) -> GroupRoleRepository:
    return SQLAlchemyGroupRoleRepository(db)


def _get_role_permission_repository_sqlalchemy(db=None) -> RolePermissionRepository:
    return SQLAlchemyRolePermissionRepository(db)


def _get_platform_endpoint_permission_gateway_sqlalchemy(db=None):
    return SQLAlchemyPlatformEndpointPermissionGateway(db)


def _get_platform_group_membership_gateway_sqlalchemy(db=None):
    return SQLAlchemyPlatformGroupMembershipGateway(db)


def _get_idm_group_gateway_sqlalchemy(db=None):
    return SQLAlchemyIdmGroupGateway(db)


def _get_password_hasher_sqlalchemy() -> PasswordHasher:
    return BcryptPasswordHasher()


def _get_token_codec_sqlalchemy() -> TokenCodec:
    return JwtTokenCodec()


_MEMORY_USER_REPOSITORY = InMemoryUserRepository()
_MEMORY_TENANT_REPOSITORY = InMemoryTenantRepository()
_MEMORY_GROUP_REPOSITORY = InMemoryGroupRepository()
_MEMORY_WORKSPACE_REPOSITORY = InMemoryWorkspaceRepository()
_MEMORY_NAMESPACE_REPOSITORY = InMemoryNamespaceRepository()
_MEMORY_ENTITY_TYPE_REPOSITORY = InMemoryEntityTypeRepository()
_MEMORY_ENTITY_RECORD_REPOSITORY = InMemoryEntityRecordRepository()


def _get_user_repository_memory() -> UserRepository:
    return _MEMORY_USER_REPOSITORY


def _get_tenant_repository_memory() -> TenantRepository:
    return _MEMORY_TENANT_REPOSITORY


def _get_group_repository_memory() -> GroupRepository:
    return _MEMORY_GROUP_REPOSITORY


def _get_group_membership_repository_memory() -> GroupMembershipRepository:
    raise _raise_platform_sqlalchemy_required()


def _get_navigation_module_repository_memory() -> NavigationModuleRepository:
    raise _raise_platform_sqlalchemy_required()


def _get_navigation_resource_repository_memory() -> NavigationResourceRepository:
    raise _raise_platform_sqlalchemy_required()


def _get_navigation_view_repository_memory() -> NavigationViewRepository:
    raise _raise_platform_sqlalchemy_required()


def _get_workspace_repository_memory() -> WorkspaceRepository:
    return _MEMORY_WORKSPACE_REPOSITORY


def _get_namespace_repository_memory() -> NamespaceRepository:
    return _MEMORY_NAMESPACE_REPOSITORY


def _get_entity_type_repository_memory() -> EntityTypeRepository:
    return _MEMORY_ENTITY_TYPE_REPOSITORY


def _get_entity_record_repository_memory() -> EntityRecordRepository:
    return _MEMORY_ENTITY_RECORD_REPOSITORY


def _get_role_repository_memory() -> RoleRepository:
    raise _raise_platform_sqlalchemy_required()


def _get_permission_repository_memory() -> PermissionRepository:
    raise _raise_platform_sqlalchemy_required()


def _get_user_tenant_repository_memory() -> UserTenantRepository:
    raise _raise_platform_sqlalchemy_required()


def _get_user_role_repository_memory() -> UserRoleRepository:
    raise _raise_platform_sqlalchemy_required()


def _get_group_role_repository_memory() -> GroupRoleRepository:
    raise _raise_platform_sqlalchemy_required()


def _get_role_permission_repository_memory() -> RolePermissionRepository:
    raise _raise_platform_sqlalchemy_required()


def _get_platform_endpoint_permission_gateway_memory():
    raise _raise_platform_gateway_sqlalchemy_required()


def _get_platform_group_membership_gateway_memory():
    raise _raise_platform_gateway_sqlalchemy_required()


def _get_idm_group_gateway_memory():
    raise _raise_platform_gateway_sqlalchemy_required()


def _get_password_hasher_memory() -> PasswordHasher:
    return BcryptPasswordHasher()


def _get_token_codec_memory() -> TokenCodec:
    return JwtTokenCodec()


def _get_user_repository_unsupported() -> UserRepository:
    raise _unsupported_backend()


def _get_tenant_repository_unsupported() -> TenantRepository:
    raise _unsupported_backend()


def _get_group_repository_unsupported() -> GroupRepository:
    raise _unsupported_backend()


def _get_group_membership_repository_unsupported() -> GroupMembershipRepository:
    raise _unsupported_backend()


def _get_navigation_module_repository_unsupported() -> NavigationModuleRepository:
    raise _unsupported_backend()


def _get_navigation_resource_repository_unsupported() -> NavigationResourceRepository:
    raise _unsupported_backend()


def _get_navigation_view_repository_unsupported() -> NavigationViewRepository:
    raise _unsupported_backend()


def _get_workspace_repository_unsupported() -> WorkspaceRepository:
    raise _unsupported_backend()


def _get_namespace_repository_unsupported() -> NamespaceRepository:
    raise _unsupported_backend()


def _get_entity_type_repository_unsupported() -> EntityTypeRepository:
    raise _unsupported_backend()


def _get_entity_record_repository_unsupported() -> EntityRecordRepository:
    raise _unsupported_backend()


def _get_role_repository_unsupported() -> RoleRepository:
    raise _unsupported_backend()


def _get_permission_repository_unsupported() -> PermissionRepository:
    raise _unsupported_backend()


def _get_user_tenant_repository_unsupported() -> UserTenantRepository:
    raise _unsupported_backend()


def _get_user_role_repository_unsupported() -> UserRoleRepository:
    raise _unsupported_backend()


def _get_group_role_repository_unsupported() -> GroupRoleRepository:
    raise _unsupported_backend()


def _get_role_permission_repository_unsupported() -> RolePermissionRepository:
    raise _unsupported_backend()


def _get_platform_endpoint_permission_gateway_unsupported():
    raise _unsupported_backend()


def _get_platform_group_membership_gateway_unsupported():
    raise _unsupported_backend()


def _get_idm_group_gateway_unsupported():
    raise _unsupported_backend()


def _get_password_hasher_unsupported() -> PasswordHasher:
    raise _unsupported_backend()


def _get_token_codec_unsupported() -> TokenCodec:
    raise _unsupported_backend()


if BACKEND == "sqlalchemy":
    get_user_repository = _get_user_repository_sqlalchemy
    get_tenant_repository = _get_tenant_repository_sqlalchemy
    get_group_repository = _get_group_repository_sqlalchemy
    get_group_membership_repository = _get_group_membership_repository_sqlalchemy
    get_navigation_module_repository = _get_navigation_module_repository_sqlalchemy
    get_navigation_resource_repository = _get_navigation_resource_repository_sqlalchemy
    get_navigation_view_repository = _get_navigation_view_repository_sqlalchemy
    get_workspace_repository = _get_workspace_repository_sqlalchemy
    get_namespace_repository = _get_namespace_repository_sqlalchemy
    get_entity_type_repository = _get_entity_type_repository_sqlalchemy
    get_entity_record_repository = _get_entity_record_repository_sqlalchemy
    get_role_repository = _get_role_repository_sqlalchemy
    get_permission_repository = _get_permission_repository_sqlalchemy
    get_user_tenant_repository = _get_user_tenant_repository_sqlalchemy
    get_user_role_repository = _get_user_role_repository_sqlalchemy
    get_group_role_repository = _get_group_role_repository_sqlalchemy
    get_role_permission_repository = _get_role_permission_repository_sqlalchemy
    get_platform_endpoint_permission_gateway = _get_platform_endpoint_permission_gateway_sqlalchemy
    get_platform_group_membership_gateway = _get_platform_group_membership_gateway_sqlalchemy
    get_idm_group_gateway = _get_idm_group_gateway_sqlalchemy
    get_password_hasher = _get_password_hasher_sqlalchemy
    get_token_codec = _get_token_codec_sqlalchemy
elif BACKEND == "memory":
    get_user_repository = _get_user_repository_memory
    get_tenant_repository = _get_tenant_repository_memory
    get_group_repository = _get_group_repository_memory
    get_group_membership_repository = _get_group_membership_repository_memory
    get_navigation_module_repository = _get_navigation_module_repository_memory
    get_navigation_resource_repository = _get_navigation_resource_repository_memory
    get_navigation_view_repository = _get_navigation_view_repository_memory
    get_workspace_repository = _get_workspace_repository_memory
    get_namespace_repository = _get_namespace_repository_memory
    get_entity_type_repository = _get_entity_type_repository_memory
    get_entity_record_repository = _get_entity_record_repository_memory
    get_role_repository = _get_role_repository_memory
    get_permission_repository = _get_permission_repository_memory
    get_user_tenant_repository = _get_user_tenant_repository_memory
    get_user_role_repository = _get_user_role_repository_memory
    get_group_role_repository = _get_group_role_repository_memory
    get_role_permission_repository = _get_role_permission_repository_memory
    get_platform_endpoint_permission_gateway = _get_platform_endpoint_permission_gateway_memory
    get_platform_group_membership_gateway = _get_platform_group_membership_gateway_memory
    get_idm_group_gateway = _get_idm_group_gateway_memory
    get_password_hasher = _get_password_hasher_memory
    get_token_codec = _get_token_codec_memory
else:
    get_user_repository = _get_user_repository_unsupported
    get_tenant_repository = _get_tenant_repository_unsupported
    get_group_repository = _get_group_repository_unsupported
    get_group_membership_repository = _get_group_membership_repository_unsupported
    get_navigation_module_repository = _get_navigation_module_repository_unsupported
    get_navigation_resource_repository = _get_navigation_resource_repository_unsupported
    get_navigation_view_repository = _get_navigation_view_repository_unsupported
    get_workspace_repository = _get_workspace_repository_unsupported
    get_namespace_repository = _get_namespace_repository_unsupported
    get_entity_type_repository = _get_entity_type_repository_unsupported
    get_entity_record_repository = _get_entity_record_repository_unsupported
    get_role_repository = _get_role_repository_unsupported
    get_permission_repository = _get_permission_repository_unsupported
    get_user_tenant_repository = _get_user_tenant_repository_unsupported
    get_user_role_repository = _get_user_role_repository_unsupported
    get_group_role_repository = _get_group_role_repository_unsupported
    get_role_permission_repository = _get_role_permission_repository_unsupported
    get_platform_endpoint_permission_gateway = _get_platform_endpoint_permission_gateway_unsupported
    get_platform_group_membership_gateway = _get_platform_group_membership_gateway_unsupported
    get_idm_group_gateway = _get_idm_group_gateway_unsupported
    get_password_hasher = _get_password_hasher_unsupported
    get_token_codec = _get_token_codec_unsupported


__all__ = [
    "get_entity_record_repository",
    "get_entity_type_repository",
    "get_group_repository",
    "get_navigation_module_repository",
    "get_navigation_resource_repository",
    "get_navigation_view_repository",
    "get_group_role_repository",
    "get_idm_group_gateway",
    "get_namespace_repository",
    "get_password_hasher",
    "get_permission_repository",
    "get_platform_endpoint_permission_gateway",
    "get_platform_group_membership_gateway",
    "get_role_permission_repository",
    "get_role_repository",
    "get_tenant_repository",
    "get_token_codec",
    "get_user_repository",
    "get_user_role_repository",
    "get_user_tenant_repository",
    "get_workspace_repository",
]
