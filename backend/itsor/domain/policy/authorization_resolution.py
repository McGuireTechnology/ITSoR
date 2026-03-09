from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Sequence

from itsor.domain.models.permission_models import (
    AclPolicy,
    AclPrincipalType,
    AclRowPredicate,
    AclScope,
    AclValue,
    GroupAclPolicy,
    OwnerAclPolicy,
    PermissionEffect,
    ResourceAclPolicy,
    RowAclPolicy,
)
from itsor.domain.models.resource_models import Resource, ResourceAction


_PRINCIPAL_PRECEDENCE: dict[AclPrincipalType, int] = {
    AclPrincipalType.USER: 0,
    AclPrincipalType.GROUP: 1,
    AclPrincipalType.ROLE: 2,
    AclPrincipalType.TENANT: 3,
    AclPrincipalType.AUTHENTICATED: 4,
    AclPrincipalType.PUBLIC: 5,
}

_COARSE_SCOPE_PRECEDENCE: dict[AclScope, int] = {
    AclScope.OWNER: 0,
    AclScope.GROUP: 0,
}


class RowAccessMode(str, Enum):
    ALL = "all"
    FILTERED = "filtered"
    NONE = "none"


@dataclass(frozen=True)
class AuthorizationSubject:
    user_id: str | None = None
    effective_user_ids: frozenset[str] = field(default_factory=frozenset)
    tenant_id: str | None = None
    tenant_ids: frozenset[str] = field(default_factory=frozenset)
    group_ids: frozenset[str] = field(default_factory=frozenset)
    effective_group_ids: frozenset[str] = field(default_factory=frozenset)
    role_ids: frozenset[str] = field(default_factory=frozenset)

    @property
    def is_authenticated(self) -> bool:
        return self.user_id is not None

    @property
    def all_user_ids(self) -> frozenset[str]:
        if self.user_id is None:
            return self.effective_user_ids
        return frozenset({self.user_id, *self.effective_user_ids})

    @property
    def all_group_ids(self) -> frozenset[str]:
        return frozenset({*self.group_ids, *self.effective_group_ids})


@dataclass(frozen=True)
class RowAccessResolution:
    mode: RowAccessMode
    resource_ids: tuple[str, ...] = ()
    predicates: tuple[AclRowPredicate, ...] = ()


@dataclass(frozen=True)
class AuthorizationDecision:
    is_allowed: bool
    coarse_effect: PermissionEffect | None
    winning_scope: AclScope | None
    winning_principal: AclPrincipalType | None
    row_access: RowAccessResolution


def resolve_authorization(
    *,
    subject: AuthorizationSubject,
    resource: Resource,
    action: ResourceAction,
    policies: Sequence[AclPolicy],
    resource_tenant_id: str | None = None,
    superuser_role_ids: frozenset[str] = frozenset({"superuser"}),
    resource_id: str | None = None,
    row_values: dict[str, AclValue] | None = None,
) -> AuthorizationDecision:
    if _is_superuser(subject, superuser_role_ids):
        return AuthorizationDecision(
            is_allowed=True,
            coarse_effect=PermissionEffect.ALLOW,
            winning_scope=AclScope.RESOURCE,
            winning_principal=AclPrincipalType.ROLE,
            row_access=RowAccessResolution(mode=RowAccessMode.ALL),
        )

    if not _is_tenant_authorized(subject, resource_tenant_id):
        return AuthorizationDecision(
            is_allowed=False,
            coarse_effect=PermissionEffect.DENY,
            winning_scope=AclScope.RESOURCE,
            winning_principal=AclPrincipalType.TENANT,
            row_access=RowAccessResolution(mode=RowAccessMode.NONE),
        )

    scoped = [policy for policy in policies if policy.resource == resource and policy.action == action]

    resource_type_decision = _resolve_resource_type(
        subject=subject,
        policies=[policy for policy in scoped if policy.scope == AclScope.RESOURCE],
    )
    if resource_type_decision is None or resource_type_decision.effect == PermissionEffect.DENY:
        return AuthorizationDecision(
            is_allowed=False,
            coarse_effect=resource_type_decision.effect if resource_type_decision else None,
            winning_scope=resource_type_decision.scope if resource_type_decision else None,
            winning_principal=(
                resource_type_decision.principal.principal_type
                if resource_type_decision
                else None
            ),
            row_access=RowAccessResolution(mode=RowAccessMode.NONE),
        )

    owner_group_decision = _resolve_owner_group(
        subject=subject,
        policies=[
            policy
            for policy in scoped
            if policy.scope in {AclScope.OWNER, AclScope.GROUP}
        ],
        resource_id=resource_id,
        row_values=row_values,
    )
    if owner_group_decision is not None and owner_group_decision.effect == PermissionEffect.DENY:
        return AuthorizationDecision(
            is_allowed=False,
            coarse_effect=owner_group_decision.effect,
            winning_scope=owner_group_decision.scope,
            winning_principal=owner_group_decision.principal.principal_type,
            row_access=RowAccessResolution(mode=RowAccessMode.NONE),
        )

    row_policies = [policy for policy in scoped if policy.scope == AclScope.ROW]
    row_resolution = _resolve_row(
        subject=subject,
        policies=row_policies,
        resource_id=resource_id,
        row_values=row_values,
    )
    if row_resolution.mode == RowAccessMode.NONE:
        return AuthorizationDecision(
            is_allowed=False,
            coarse_effect=(
                owner_group_decision.effect
                if owner_group_decision is not None
                else resource_type_decision.effect
            ),
            winning_scope=(
                owner_group_decision.scope
                if owner_group_decision is not None
                else resource_type_decision.scope
            ),
            winning_principal=(
                owner_group_decision.principal.principal_type
                if owner_group_decision is not None
                else resource_type_decision.principal.principal_type
            ),
            row_access=row_resolution,
        )

    return AuthorizationDecision(
        is_allowed=True,
        coarse_effect=(
            owner_group_decision.effect
            if owner_group_decision is not None
            else resource_type_decision.effect
        ),
        winning_scope=(
            owner_group_decision.scope
            if owner_group_decision is not None
            else resource_type_decision.scope
        ),
        winning_principal=(
            owner_group_decision.principal.principal_type
            if owner_group_decision is not None
            else resource_type_decision.principal.principal_type
        ),
        row_access=row_resolution,
    )


def _resolve_resource_type(
    *,
    subject: AuthorizationSubject,
    policies: Sequence[AclPolicy],
) -> ResourceAclPolicy | None:
    candidates: list[ResourceAclPolicy] = []
    for policy in policies:
        if policy.scope != AclScope.RESOURCE:
            continue
        if _matches_principal(policy.principal.principal_type, policy.principal.principal_id, subject):
            candidates.append(policy)

    if not candidates:
        return None

    winner_rank = min(_resource_type_rank(policy) for policy in candidates)
    tied = [policy for policy in candidates if _resource_type_rank(policy) == winner_rank]
    deny = next((policy for policy in tied if policy.effect == PermissionEffect.DENY), None)
    return deny or tied[0]


def _resolve_owner_group(
    *,
    subject: AuthorizationSubject,
    policies: Sequence[AclPolicy],
    resource_id: str | None,
    row_values: dict[str, AclValue] | None,
) -> OwnerAclPolicy | GroupAclPolicy | None:
    candidates: list[OwnerAclPolicy | GroupAclPolicy] = []
    for policy in policies:
        if policy.scope == AclScope.OWNER:
            typed = policy
        elif policy.scope == AclScope.GROUP:
            typed = policy
        else:
            continue

        if _matches_coarse_policy(
            policy=typed,
            subject=subject,
            resource_id=resource_id,
            row_values=row_values,
        ):
            candidates.append(typed)

    if not candidates:
        return None

    winner_rank = min(_coarse_rank(policy) for policy in candidates)
    tied = [policy for policy in candidates if _coarse_rank(policy) == winner_rank]
    deny = next((policy for policy in tied if policy.effect == PermissionEffect.DENY), None)
    return deny or tied[0]


def _resolve_row(
    *,
    subject: AuthorizationSubject,
    policies: Sequence[AclPolicy],
    resource_id: str | None,
    row_values: dict[str, AclValue] | None,
) -> RowAccessResolution:
    row_candidates: list[RowAclPolicy] = []
    for policy in policies:
        if policy.scope != AclScope.ROW:
            continue
        if _matches_principal(policy.principal.principal_type, policy.principal.principal_id, subject):
            row_candidates.append(policy)

    if not row_candidates:
        return RowAccessResolution(mode=RowAccessMode.ALL)

    if resource_id is not None or row_values is not None:
        targeted = [
            policy
            for policy in row_candidates
            if _matches_row_policy(policy, resource_id=resource_id, row_values=row_values)
        ]
        if not targeted:
            return RowAccessResolution(mode=RowAccessMode.NONE)

        winner_rank = min(_row_rank(policy) for policy in targeted)
        tied = [policy for policy in targeted if _row_rank(policy) == winner_rank]
        winning_effect = (
            PermissionEffect.DENY
            if any(policy.effect == PermissionEffect.DENY for policy in tied)
            else PermissionEffect.ALLOW
        )
        if winning_effect == PermissionEffect.DENY:
            return RowAccessResolution(mode=RowAccessMode.NONE)

        return RowAccessResolution(mode=RowAccessMode.FILTERED)

    winner_rank = min(_row_rank(policy) for policy in row_candidates)
    tied = [policy for policy in row_candidates if _row_rank(policy) == winner_rank]
    if any(policy.effect == PermissionEffect.DENY for policy in tied):
        return RowAccessResolution(mode=RowAccessMode.NONE)

    allow_policies = [policy for policy in row_candidates if policy.effect == PermissionEffect.ALLOW]
    if not allow_policies:
        return RowAccessResolution(mode=RowAccessMode.NONE)

    allow_resource_ids = tuple(
        sorted(
            {
                policy.resource_id
                for policy in allow_policies
                if policy.resource_id is not None
            }
        )
    )
    predicates = tuple(
        predicate
        for policy in allow_policies
        for predicate in policy.predicates
    )
    return RowAccessResolution(
        mode=RowAccessMode.FILTERED,
        resource_ids=allow_resource_ids,
        predicates=predicates,
    )


def _matches_coarse_policy(
    *,
    policy: ResourceAclPolicy | OwnerAclPolicy | GroupAclPolicy,
    subject: AuthorizationSubject,
    resource_id: str | None,
    row_values: dict[str, AclValue] | None,
) -> bool:
    if not _matches_principal(policy.principal.principal_type, policy.principal.principal_id, subject):
        return False

    if isinstance(policy, OwnerAclPolicy):
        if policy.owner_user_id is not None and str(policy.owner_user_id) not in subject.all_user_ids:
            return False
        if row_values is None:
            return policy.owner_user_id is not None
        owner_value = row_values.get(policy.owner_field)
        return owner_value in subject.all_user_ids

    if isinstance(policy, GroupAclPolicy):
        if policy.allowed_group_ids:
            if not set(map(str, policy.allowed_group_ids)).intersection(subject.all_group_ids):
                return False
        if row_values is None:
            return True
        row_group = row_values.get(policy.group_field)
        return row_group in subject.all_group_ids

    return True


def _matches_row_policy(
    policy: RowAclPolicy,
    *,
    resource_id: str | None,
    row_values: dict[str, AclValue] | None,
) -> bool:
    if policy.resource_id is not None and policy.resource_id != resource_id:
        return False
    if not policy.predicates:
        return True
    if row_values is None:
        return True
    return all(_matches_predicate(predicate, row_values) for predicate in policy.predicates)


def _matches_predicate(predicate: AclRowPredicate, row_values: dict[str, AclValue]) -> bool:
    row_value = row_values.get(predicate.field)
    expected = predicate.value
    if isinstance(expected, list):
        return row_value in expected
    return row_value == expected


def _matches_principal(
    principal_type: AclPrincipalType,
    principal_id: str | None,
    subject: AuthorizationSubject,
) -> bool:
    if principal_type == AclPrincipalType.PUBLIC:
        return True
    if principal_type == AclPrincipalType.AUTHENTICATED:
        return subject.is_authenticated
    if principal_type == AclPrincipalType.USER:
        return principal_id is not None and principal_id in subject.all_user_ids
    if principal_type == AclPrincipalType.GROUP:
        return principal_id is not None and principal_id in subject.all_group_ids
    if principal_type == AclPrincipalType.ROLE:
        return principal_id is not None and principal_id in subject.role_ids
    if principal_type == AclPrincipalType.TENANT:
        return principal_id is not None and subject.tenant_id == principal_id
    return False


def _coarse_rank(policy: OwnerAclPolicy | GroupAclPolicy) -> tuple[int, int, int]:
    scope_rank = _COARSE_SCOPE_PRECEDENCE[policy.scope]
    principal_rank = _PRINCIPAL_PRECEDENCE[policy.principal.principal_type]
    specificity_rank = 0 if _has_specific_constraint(policy) else 1
    return scope_rank, principal_rank, specificity_rank


def _resource_type_rank(policy: ResourceAclPolicy) -> tuple[int, int]:
    principal_rank = _PRINCIPAL_PRECEDENCE[policy.principal.principal_type]
    specificity_rank = 0
    return principal_rank, specificity_rank


def _is_superuser(subject: AuthorizationSubject, superuser_role_ids: frozenset[str]) -> bool:
    if not superuser_role_ids:
        return False
    return bool(subject.role_ids.intersection(superuser_role_ids))


def _is_tenant_authorized(subject: AuthorizationSubject, resource_tenant_id: str | None) -> bool:
    if resource_tenant_id is None:
        return True

    if subject.tenant_ids:
        return resource_tenant_id in subject.tenant_ids

    return subject.tenant_id == resource_tenant_id


def _row_rank(policy: RowAclPolicy) -> tuple[int, int]:
    principal_rank = _PRINCIPAL_PRECEDENCE[policy.principal.principal_type]
    specificity_rank = 0 if (policy.resource_id is not None or policy.predicates) else 1
    return principal_rank, specificity_rank


def _has_specific_constraint(policy: OwnerAclPolicy | GroupAclPolicy) -> bool:
    if isinstance(policy, OwnerAclPolicy):
        return policy.owner_user_id is not None
    return bool(policy.allowed_group_ids)


__all__ = [
    "AuthorizationDecision",
    "AuthorizationSubject",
    "RowAccessMode",
    "RowAccessResolution",
    "resolve_authorization",
]
