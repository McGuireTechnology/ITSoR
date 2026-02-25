from typing import List, Optional

from itsor.domain.ids import generate_ulid
from itsor.domain.models import Group, Tenant
from itsor.domain.ports.group_repository import GroupRepository
from itsor.domain.ports.tenant_repository import TenantRepository
from itsor.domain.ports.user_repository import UserRepository
from itsor.domain.use_cases.base_use_case import BaseUseCase


class TenantUseCases(BaseUseCase):
    def __init__(self, repo: TenantRepository, group_repo: GroupRepository, user_repo: UserRepository) -> None:
        self._repo = repo
        self._group_repo = group_repo
        self._user_repo = user_repo

    def list_tenants(self) -> List[Tenant]:
        return self._repo.list()

    def get_tenant(self, tenant_id: str) -> Optional[Tenant]:
        return self._repo.get_by_id(tenant_id)

    def create_tenant(self, name: str, creator_user_id: str | None = None) -> Tenant:
        existing = self._repo.get_by_name(name)
        if existing:
            raise ValueError("Tenant name already registered")
        tenant = Tenant(id=generate_ulid(), name=name, owner_id=creator_user_id)
        created_tenant = self._repo.create(tenant)

        admins_group = Group(
            id=generate_ulid(),
            name="Tenant Admins",
            tenant_id=created_tenant.id,
            owner_id=creator_user_id,
        )
        self._group_repo.create(admins_group)

        users_group = Group(
            id=generate_ulid(),
            name="Tenant Users",
            tenant_id=created_tenant.id,
            owner_id=creator_user_id,
        )
        created_users_group = self._group_repo.create(users_group)

        if creator_user_id:
            creator = self._user_repo.get_by_id(creator_user_id)
            if creator:
                creator.group_id = created_users_group.id
                self._user_repo.update(creator)

        return created_tenant

    def update_tenant(self, tenant_id: str, name: Optional[str] = None) -> Tenant:
        tenant = self._repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        if name is not None and name != tenant.name:
            existing = self._repo.get_by_name(name)
            if existing:
                raise ValueError("Tenant name already in use")
            tenant.name = name
        return self._repo.update(tenant)

    def replace_tenant(self, tenant_id: str, name: str) -> Tenant:
        tenant = self._repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        if name != tenant.name:
            existing = self._repo.get_by_name(name)
            if existing:
                raise ValueError("Tenant name already in use")
        tenant.name = name
        return self._repo.update(tenant)

    def delete_tenant(self, tenant_id: str) -> None:
        tenant = self._repo.get_by_id(tenant_id)
        if not tenant:
            raise ValueError("Tenant not found")
        self._repo.delete(tenant_id)
