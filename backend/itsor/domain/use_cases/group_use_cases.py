from typing import List, Optional

from itsor.domain.ids import generate_ulid
from itsor.domain.models import Group
from itsor.domain.ports.group_repository import GroupRepository
from itsor.domain.use_cases.base_use_case import BaseUseCase


class GroupUseCases(BaseUseCase):
    def __init__(self, repo: GroupRepository) -> None:
        self._repo = repo

    def list_groups(self) -> List[Group]:
        return self._repo.list()

    def get_group(self, group_id: str) -> Optional[Group]:
        return self._repo.get_by_id(group_id)

    def create_group(self, name: str, tenant_id: str | None = None) -> Group:
        existing = self._repo.get_by_name(name, tenant_id)
        if existing:
            raise ValueError("Group name already registered")
        group = Group(id=generate_ulid(), name=name, tenant_id=tenant_id)
        return self._repo.create(group)

    def update_group(self, group_id: str, name: Optional[str] = None) -> Group:
        group = self._repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")
        if name is not None and name != group.name:
            existing = self._repo.get_by_name(name, group.tenant_id)
            if existing:
                raise ValueError("Group name already in use")
            group.name = name
        return self._repo.update(group)

    def replace_group(self, group_id: str, name: str) -> Group:
        group = self._repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")
        if name != group.name:
            existing = self._repo.get_by_name(name, group.tenant_id)
            if existing:
                raise ValueError("Group name already in use")
        group.name = name
        return self._repo.update(group)

    def delete_group(self, group_id: str) -> None:
        group = self._repo.get_by_id(group_id)
        if not group:
            raise ValueError("Group not found")
        self._repo.delete(group_id)
