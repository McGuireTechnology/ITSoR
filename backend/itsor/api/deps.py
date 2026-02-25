import os

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from itsor.domain.models import User
from itsor.domain.use_cases.entity_record_use_cases import EntityRecordUseCases
from itsor.domain.use_cases.entity_type_use_cases import EntityTypeUseCases
from itsor.domain.use_cases.group_use_cases import GroupUseCases
from itsor.domain.use_cases.namespace_use_cases import NamespaceUseCases
from itsor.domain.use_cases.tenant_use_cases import TenantUseCases
from itsor.domain.use_cases.user_use_cases import UserUseCases
from itsor.domain.use_cases.workspace_use_cases import WorkspaceUseCases
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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", auto_error=False)


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


def get_current_user(
    request: Request,
    token: str | None = Depends(oauth2_scheme),
    use_cases: UserUseCases = Depends(get_user_use_cases),
) -> User:
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
