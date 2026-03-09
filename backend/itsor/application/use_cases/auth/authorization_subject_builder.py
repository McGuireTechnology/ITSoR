from __future__ import annotations

from dataclasses import dataclass

from itsor.application.ports.auth.repositories import (
    GroupMembershipRepository,
    GroupRoleRepository,
    UserRoleRepository,
    UserTenantRepository,
)
from itsor.domain.models import GroupMembership
from itsor.domain.policy import AuthorizationSubject


@dataclass
class AuthorizationSubjectBuilder:
    user_tenant_repo: UserTenantRepository
    group_membership_repo: GroupMembershipRepository
    user_role_repo: UserRoleRepository
    group_role_repo: GroupRoleRepository

    def build_for_user(
        self,
        *,
        user_id: str,
        primary_group_id: str | None = None,
        direct_tenant_id: str | None = None,
        acts_for_user_ids: frozenset[str] = frozenset(),
        include_nested_groups: bool = True,
    ) -> AuthorizationSubject:
        direct_group_ids, effective_group_ids = self._resolve_groups(
            user_id=user_id,
            primary_group_id=primary_group_id,
            include_nested_groups=include_nested_groups,
        )

        role_ids = self._resolve_role_ids(
            user_id=user_id,
            all_group_ids=frozenset({*direct_group_ids, *effective_group_ids}),
        )

        tenant_ids = self._resolve_tenant_ids(user_id=user_id)
        tenant_id = self._resolve_primary_tenant_id(
            direct_tenant_id=direct_tenant_id,
            tenant_ids=tenant_ids,
        )

        return AuthorizationSubject(
            user_id=user_id,
            effective_user_ids=acts_for_user_ids,
            tenant_id=tenant_id,
            tenant_ids=tenant_ids,
            group_ids=direct_group_ids,
            effective_group_ids=effective_group_ids,
            role_ids=role_ids,
        )

    def _resolve_tenant_ids(self, *, user_id: str) -> frozenset[str]:
        tenant_ids = {
            str(link.tenant_id)
            for link in self.user_tenant_repo.list()
            if str(link.user_id) == user_id
        }
        return frozenset(tenant_ids)

    @staticmethod
    def _resolve_primary_tenant_id(*, direct_tenant_id: str | None, tenant_ids: frozenset[str]) -> str | None:
        if direct_tenant_id is not None:
            return direct_tenant_id
        if not tenant_ids:
            return None
        return sorted(tenant_ids)[0]

    def _resolve_groups(
        self,
        *,
        user_id: str,
        primary_group_id: str | None,
        include_nested_groups: bool,
    ) -> tuple[frozenset[str], frozenset[str]]:
        memberships = self.group_membership_repo.list()
        direct_group_ids = {
            str(membership.group_id)
            for membership in memberships
            if membership.member_type == "user" and str(membership.member_user_id) == user_id
        }
        if primary_group_id is not None:
            direct_group_ids.add(primary_group_id)

        all_group_ids = set(direct_group_ids)
        if include_nested_groups:
            all_group_ids.update(self._expand_parent_groups(seed_group_ids=direct_group_ids, memberships=memberships))

        effective_group_ids = all_group_ids.difference(direct_group_ids)
        return frozenset(direct_group_ids), frozenset(effective_group_ids)

    @staticmethod
    def _expand_parent_groups(
        *,
        seed_group_ids: set[str],
        memberships: list[GroupMembership],
    ) -> set[str]:
        expanded = set(seed_group_ids)
        frontier = set(seed_group_ids)

        while frontier:
            next_frontier: set[str] = set()
            for membership in memberships:
                if membership.member_type != "group":
                    continue
                member_group_id = str(membership.member_group_id)
                if member_group_id not in frontier:
                    continue
                parent_group_id = str(membership.group_id)
                if parent_group_id in expanded:
                    continue
                expanded.add(parent_group_id)
                next_frontier.add(parent_group_id)
            frontier = next_frontier

        return expanded

    def _resolve_role_ids(self, *, user_id: str, all_group_ids: frozenset[str]) -> frozenset[str]:
        role_ids = {
            str(assignment.role_id)
            for assignment in self.user_role_repo.list_for_user(user_id)
        }

        for group_id in all_group_ids:
            for assignment in self.group_role_repo.list_for_group(group_id):
                role_ids.add(str(assignment.role_id))

        return frozenset(role_ids)


__all__ = ["AuthorizationSubjectBuilder"]
