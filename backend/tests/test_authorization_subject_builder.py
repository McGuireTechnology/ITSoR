from typing import Generic, TypeVar

from itsor.application.use_cases.auth.authorization_subject_builder import (
    AuthorizationSubjectBuilder,
)
from itsor.domain.models import GroupMembership, RoleAssignment, UserTenant


TModel = TypeVar("TModel")


class _ListRepo(Generic[TModel]):
    def __init__(self, items: list[TModel]) -> None:
        self._items = items

    def list(self) -> list[TModel]:
        return list(self._items)


class _UserRoleRepo:
    def __init__(self, assignments: list[RoleAssignment]) -> None:
        self._assignments = assignments

    def list_for_user(self, user_id: str) -> list[RoleAssignment]:
        return [
            assignment
            for assignment in self._assignments
            if assignment.assignee_type == "user" and str(assignment.user_id) == user_id
        ]


class _GroupRoleRepo:
    def __init__(self, assignments: list[RoleAssignment]) -> None:
        self._assignments = assignments

    def list_for_group(self, group_id: str) -> list[RoleAssignment]:
        return [
            assignment
            for assignment in self._assignments
            if assignment.assignee_type == "group" and str(assignment.group_id) == group_id
        ]


def test_builder_collects_tenants_groups_roles_and_effective_identities() -> None:
    memberships = [
        GroupMembership(group_id="g-direct", member_type="user", member_user_id="u-1"),
        GroupMembership(group_id="g-parent", member_type="group", member_group_id="g-direct"),
    ]
    user_tenants = [
        UserTenant(user_id="u-1", tenant_id="t-2"),
        UserTenant(user_id="u-1", tenant_id="t-1"),
        UserTenant(user_id="u-other", tenant_id="t-x"),
    ]
    user_roles = [
        RoleAssignment(user_id="u-1", role_id="r-user"),
        RoleAssignment(user_id="u-other", role_id="r-ignored"),
    ]
    group_roles = [
        RoleAssignment(group_id="g-parent", role_id="r-parent"),
        RoleAssignment(group_id="g-direct", role_id="r-direct"),
        RoleAssignment(group_id="g-other", role_id="r-ignored"),
    ]

    builder = AuthorizationSubjectBuilder(
        user_tenant_repo=_ListRepo(user_tenants),
        group_membership_repo=_ListRepo(memberships),
        user_role_repo=_UserRoleRepo(user_roles),
        group_role_repo=_GroupRoleRepo(group_roles),
    )

    subject = builder.build_for_user(
        user_id="u-1",
        primary_group_id="g-primary",
        acts_for_user_ids=frozenset({"u-delegate"}),
    )

    assert subject.user_id == "u-1"
    assert subject.effective_user_ids == frozenset({"u-delegate"})
    assert subject.group_ids == frozenset({"g-direct", "g-primary"})
    assert subject.effective_group_ids == frozenset({"g-parent"})
    assert subject.tenant_ids == frozenset({"t-1", "t-2"})
    assert subject.tenant_id == "t-1"
    assert subject.role_ids == frozenset({"r-user", "r-parent", "r-direct"})


def test_builder_can_disable_nested_group_expansion() -> None:
    memberships = [
        GroupMembership(group_id="g-direct", member_type="user", member_user_id="u-1"),
        GroupMembership(group_id="g-parent", member_type="group", member_group_id="g-direct"),
    ]
    builder = AuthorizationSubjectBuilder(
        user_tenant_repo=_ListRepo([]),
        group_membership_repo=_ListRepo(memberships),
        user_role_repo=_UserRoleRepo([]),
        group_role_repo=_GroupRoleRepo([]),
    )

    subject = builder.build_for_user(
        user_id="u-1",
        include_nested_groups=False,
    )

    assert subject.group_ids == frozenset({"g-direct"})
    assert subject.effective_group_ids == frozenset()
