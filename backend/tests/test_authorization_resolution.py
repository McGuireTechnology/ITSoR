from itsor.domain.models.permission_models import (
    AclPrincipal,
    AclPrincipalType,
    AclRowPredicate,
    GroupAclPolicy,
    OwnerAclPolicy,
    PermissionEffect,
    ResourceAclPolicy,
    RowAclPolicy,
)
from itsor.domain.models.resource_models import Resource, ResourcePermissionAction
from itsor.domain.policy import AuthorizationSubject, RowAccessMode, resolve_authorization


def _legacy_unconstrained_row_allow(*, principal: AclPrincipal) -> RowAclPolicy:
    policy = RowAclPolicy(
        name="legacy unconstrained allow",
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        principal=principal,
        predicates=[AclRowPredicate(field="seed", value="seed")],
        effect=PermissionEffect.ALLOW,
    )
    policy.predicates.clear()
    return policy


def test_owner_precedence_beats_role_when_more_specific() -> None:
    subject = AuthorizationSubject(
        user_id="u-1",
        role_ids=frozenset({"r-1"}),
        tenant_ids=frozenset({"t-1"}),
    )
    policies = [
        ResourceAclPolicy(
            name="role deny",
            resource=Resource.GROUP,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.ROLE, "r-1"),
            effect=PermissionEffect.DENY,
        ),
        OwnerAclPolicy(
            name="owner allow",
            resource=Resource.GROUP,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            owner_user_id="u-1",
            effect=PermissionEffect.ALLOW,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.GROUP,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
    )

    assert decision.is_allowed is False
    assert decision.winning_scope is not None and decision.winning_scope.value == "resource"
    assert decision.row_access.mode == RowAccessMode.NONE


def test_superuser_role_short_circuits_tenant_and_policy_checks() -> None:
    subject = AuthorizationSubject(
        user_id="u-1",
        role_ids=frozenset({"superuser"}),
        tenant_ids=frozenset({"t-1"}),
    )

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.DELETE,
        policies=[],
        resource_tenant_id="t-other",
    )

    assert decision.is_allowed is True
    assert decision.row_access.mode == RowAccessMode.ALL


def test_tenant_boundary_denies_before_resource_checks() -> None:
    subject = AuthorizationSubject(
        user_id="u-1",
        role_ids=frozenset({"r-1"}),
        tenant_ids=frozenset({"t-1"}),
    )
    policies = [
        ResourceAclPolicy(
            name="role allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.ROLE, "r-1"),
            effect=PermissionEffect.ALLOW,
        )
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-2",
    )

    assert decision.is_allowed is False
    assert decision.winning_principal is AclPrincipalType.TENANT


def test_conflict_at_same_precedence_prefers_deny() -> None:
    subject = AuthorizationSubject(
        group_ids=frozenset({"g-1"}),
        tenant_ids=frozenset({"t-1"}),
    )
    policies = [
        GroupAclPolicy(
            name="group allow",
            resource=Resource.GROUP,
            action=ResourcePermissionAction.UPDATE,
            principal=AclPrincipal(AclPrincipalType.GROUP, "g-1"),
            effect=PermissionEffect.ALLOW,
        ),
        GroupAclPolicy(
            name="group deny",
            resource=Resource.GROUP,
            action=ResourcePermissionAction.UPDATE,
            principal=AclPrincipal(AclPrincipalType.GROUP, "g-1"),
            effect=PermissionEffect.DENY,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.GROUP,
        action=ResourcePermissionAction.UPDATE,
        policies=policies,
        resource_tenant_id="t-1",
    )

    assert decision.is_allowed is False
    assert decision.row_access.mode == RowAccessMode.NONE


def test_resource_scope_same_rank_conflict_prefers_deny() -> None:
    subject = AuthorizationSubject(user_id="u-1", tenant_ids=frozenset({"t-1"}))
    policies = [
        ResourceAclPolicy(
            name="user allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            effect=PermissionEffect.ALLOW,
        ),
        ResourceAclPolicy(
            name="user deny",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            effect=PermissionEffect.DENY,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
    )

    assert decision.is_allowed is False
    assert decision.winning_scope is not None and decision.winning_scope.value == "resource"
    assert decision.row_access.mode == RowAccessMode.NONE


def test_owner_deny_overrides_resource_allow_when_owner_matches() -> None:
    subject = AuthorizationSubject(user_id="u-1", tenant_ids=frozenset({"t-1"}))
    policies = [
        ResourceAclPolicy(
            name="authenticated allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        OwnerAclPolicy(
            name="owner deny",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            owner_user_id="u-1",
            effect=PermissionEffect.DENY,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
        row_values={"owner_id": "u-1"},
    )

    assert decision.is_allowed is False
    assert decision.winning_scope is not None and decision.winning_scope.value == "owner"
    assert decision.row_access.mode == RowAccessMode.NONE


def test_group_allowed_group_ids_requires_intersection() -> None:
    subject = AuthorizationSubject(
        user_id="u-1",
        group_ids=frozenset({"g-user"}),
        tenant_ids=frozenset({"t-1"}),
    )
    policies = [
        ResourceAclPolicy(
            name="authenticated allow",
            resource=Resource.GROUP,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        GroupAclPolicy(
            name="intersection allow",
            resource=Resource.GROUP,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            allowed_group_ids=["g-user", "g-other"],
            effect=PermissionEffect.ALLOW,
        ),
        GroupAclPolicy(
            name="non-intersection deny",
            resource=Resource.GROUP,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            allowed_group_ids=["g-unrelated"],
            effect=PermissionEffect.DENY,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.GROUP,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
        row_values={"group_id": "g-user"},
    )

    assert decision.is_allowed is True
    assert decision.winning_scope is not None and decision.winning_scope.value == "group"
    assert decision.row_access.mode == RowAccessMode.ALL


def test_row_policy_can_deny_after_coarse_allow() -> None:
    subject = AuthorizationSubject(user_id="u-1", tenant_ids=frozenset({"t-1"}))
    policies = [
        ResourceAclPolicy(
            name="authenticated allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        RowAclPolicy(
            name="owner row deny",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            predicates=[AclRowPredicate(field="owner_id", value="u-2")],
            effect=PermissionEffect.DENY,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
        row_values={"owner_id": "u-2"},
    )

    assert decision.is_allowed is False
    assert decision.row_access.mode == RowAccessMode.NONE


def test_row_allow_returns_filtered_mode_for_collection() -> None:
    subject = AuthorizationSubject(user_id="u-1", tenant_ids=frozenset({"t-1"}))
    policies = [
        ResourceAclPolicy(
            name="authenticated allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        RowAclPolicy(
            name="own rows",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            predicates=[AclRowPredicate(field="owner_id", value="u-1")],
            effect=PermissionEffect.ALLOW,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
    )

    assert decision.is_allowed is True
    assert decision.row_access.mode == RowAccessMode.FILTERED
    assert len(decision.row_access.predicates) == 1


def test_unconstrained_row_allow_returns_all_for_collection() -> None:
    subject = AuthorizationSubject(user_id="u-1", tenant_ids=frozenset({"t-1"}))
    policies = [
        ResourceAclPolicy(
            name="authenticated allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        _legacy_unconstrained_row_allow(
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
    )

    assert decision.is_allowed is True
    assert decision.row_access.mode == RowAccessMode.ALL
    assert decision.row_access.resource_ids == ()
    assert decision.row_access.predicates == ()


def test_constrained_row_allow_returns_filtered_with_constraints() -> None:
    subject = AuthorizationSubject(user_id="u-1", tenant_ids=frozenset({"t-1"}))
    own_rows_predicate = AclRowPredicate(field="owner_id", value="u-1")
    policies = [
        ResourceAclPolicy(
            name="authenticated allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        RowAclPolicy(
            name="resource constrained allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            resource_id="user-42",
            effect=PermissionEffect.ALLOW,
        ),
        RowAclPolicy(
            name="predicate constrained allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            predicates=[own_rows_predicate],
            effect=PermissionEffect.ALLOW,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
    )

    assert decision.is_allowed is True
    assert decision.row_access.mode == RowAccessMode.FILTERED
    assert decision.row_access.resource_ids == ("user-42",)
    assert decision.row_access.predicates == (own_rows_predicate,)


def test_row_deny_after_coarse_allow_returns_none_for_collection() -> None:
    subject = AuthorizationSubject(user_id="u-1", tenant_ids=frozenset({"t-1"}))
    policies = [
        ResourceAclPolicy(
            name="authenticated allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        RowAclPolicy(
            name="row allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            predicates=[AclRowPredicate(field="owner_id", value="u-1")],
            effect=PermissionEffect.ALLOW,
        ),
        RowAclPolicy(
            name="row deny",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            predicates=[AclRowPredicate(field="owner_id", value="u-1")],
            effect=PermissionEffect.DENY,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
    )

    assert decision.is_allowed is False
    assert decision.row_access.mode == RowAccessMode.NONE


def test_row_predicate_matches_scalar_value() -> None:
    subject = AuthorizationSubject(user_id="u-1", tenant_ids=frozenset({"t-1"}))
    policies = [
        ResourceAclPolicy(
            name="authenticated allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        RowAclPolicy(
            name="department scalar allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            predicates=[AclRowPredicate(field="department", value="eng")],
            effect=PermissionEffect.ALLOW,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
        resource_id="user-1",
        row_values={"department": "eng"},
    )

    assert decision.is_allowed is True
    assert decision.row_access.mode == RowAccessMode.FILTERED


def test_row_predicate_matches_list_value() -> None:
    subject = AuthorizationSubject(user_id="u-1", tenant_ids=frozenset({"t-1"}))
    policies = [
        ResourceAclPolicy(
            name="authenticated allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        RowAclPolicy(
            name="department list allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            predicates=[AclRowPredicate(field="department", value=["eng", "ops"])],
            effect=PermissionEffect.ALLOW,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
        resource_id="user-1",
        row_values={"department": "ops"},
    )

    assert decision.is_allowed is True
    assert decision.row_access.mode == RowAccessMode.FILTERED


def test_effective_user_ids_satisfy_owner_authorization() -> None:
    subject = AuthorizationSubject(
        user_id="u-primary",
        effective_user_ids=frozenset({"u-delegate"}),
        tenant_ids=frozenset({"t-1"}),
    )
    policies = [
        ResourceAclPolicy(
            name="tenant user read allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        OwnerAclPolicy(
            name="delegate owner allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-delegate"),
            owner_user_id="u-delegate",
            effect=PermissionEffect.ALLOW,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
        row_values={"owner_id": "u-delegate"},
    )

    assert decision.is_allowed is True


def test_effective_group_ids_satisfy_group_authorization() -> None:
    subject = AuthorizationSubject(
        user_id="u-1",
        group_ids=frozenset({"g-primary"}),
        effective_group_ids=frozenset({"g-extended"}),
        tenant_ids=frozenset({"t-1"}),
    )
    policies = [
        ResourceAclPolicy(
            name="tenant user read allow",
            resource=Resource.GROUP,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        GroupAclPolicy(
            name="extended group allow",
            resource=Resource.GROUP,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.GROUP, "g-extended"),
            allowed_group_ids=["g-extended"],
            effect=PermissionEffect.ALLOW,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.GROUP,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
        row_values={"group_id": "g-extended"},
    )

    assert decision.is_allowed is True


def test_tenant_principal_matches_effective_tenant_membership() -> None:
    subject = AuthorizationSubject(
        user_id="u-1",
        tenant_id="t-primary",
        tenant_ids=frozenset({"t-primary", "t-secondary"}),
    )
    policies = [
        ResourceAclPolicy(
            name="secondary tenant allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.TENANT, "t-secondary"),
            effect=PermissionEffect.ALLOW,
        )
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-secondary",
    )

    assert decision.is_allowed is True
    assert decision.winning_principal is AclPrincipalType.TENANT


def test_tenant_principal_denies_when_not_in_primary_or_effective_memberships() -> None:
    subject = AuthorizationSubject(
        user_id="u-1",
        tenant_id="t-primary",
        tenant_ids=frozenset({"t-primary", "t-other"}),
    )
    policies = [
        ResourceAclPolicy(
            name="unrelated tenant allow",
            resource=Resource.USER,
            action=ResourcePermissionAction.READ,
            principal=AclPrincipal(AclPrincipalType.TENANT, "t-secondary"),
            effect=PermissionEffect.ALLOW,
        )
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourcePermissionAction.READ,
        policies=policies,
        resource_tenant_id="t-primary",
    )

    assert decision.is_allowed is False
    assert decision.winning_principal is None
