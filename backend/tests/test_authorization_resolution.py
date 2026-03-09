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
from itsor.domain.models.resource_models import Resource, ResourceAction
from itsor.domain.policy import AuthorizationSubject, RowAccessMode, resolve_authorization


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
            action=ResourceAction.READ,
            principal=AclPrincipal(AclPrincipalType.ROLE, "r-1"),
            effect=PermissionEffect.DENY,
        ),
        OwnerAclPolicy(
            name="owner allow",
            resource=Resource.GROUP,
            action=ResourceAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            owner_user_id="u-1",
            effect=PermissionEffect.ALLOW,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.GROUP,
        action=ResourceAction.READ,
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
        action=ResourceAction.DELETE,
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
            action=ResourceAction.READ,
            principal=AclPrincipal(AclPrincipalType.ROLE, "r-1"),
            effect=PermissionEffect.ALLOW,
        )
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourceAction.READ,
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
            action=ResourceAction.UPDATE,
            principal=AclPrincipal(AclPrincipalType.GROUP, "g-1"),
            effect=PermissionEffect.ALLOW,
        ),
        GroupAclPolicy(
            name="group deny",
            resource=Resource.GROUP,
            action=ResourceAction.UPDATE,
            principal=AclPrincipal(AclPrincipalType.GROUP, "g-1"),
            effect=PermissionEffect.DENY,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.GROUP,
        action=ResourceAction.UPDATE,
        policies=policies,
        resource_tenant_id="t-1",
    )

    assert decision.is_allowed is False
    assert decision.row_access.mode == RowAccessMode.NONE


def test_row_policy_can_deny_after_coarse_allow() -> None:
    subject = AuthorizationSubject(user_id="u-1", tenant_ids=frozenset({"t-1"}))
    policies = [
        ResourceAclPolicy(
            name="authenticated allow",
            resource=Resource.USER,
            action=ResourceAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        RowAclPolicy(
            name="owner row deny",
            resource=Resource.USER,
            action=ResourceAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            predicates=[AclRowPredicate(field="owner_id", value="u-2")],
            effect=PermissionEffect.DENY,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourceAction.READ,
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
            action=ResourceAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        RowAclPolicy(
            name="own rows",
            resource=Resource.USER,
            action=ResourceAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-1"),
            predicates=[AclRowPredicate(field="owner_id", value="u-1")],
            effect=PermissionEffect.ALLOW,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourceAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
    )

    assert decision.is_allowed is True
    assert decision.row_access.mode == RowAccessMode.FILTERED
    assert len(decision.row_access.predicates) == 1


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
            action=ResourceAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        OwnerAclPolicy(
            name="delegate owner allow",
            resource=Resource.USER,
            action=ResourceAction.READ,
            principal=AclPrincipal(AclPrincipalType.USER, "u-delegate"),
            owner_user_id="u-delegate",
            effect=PermissionEffect.ALLOW,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.USER,
        action=ResourceAction.READ,
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
            action=ResourceAction.READ,
            principal=AclPrincipal(AclPrincipalType.AUTHENTICATED),
            effect=PermissionEffect.ALLOW,
        ),
        GroupAclPolicy(
            name="extended group allow",
            resource=Resource.GROUP,
            action=ResourceAction.READ,
            principal=AclPrincipal(AclPrincipalType.GROUP, "g-extended"),
            allowed_group_ids=["g-extended"],
            effect=PermissionEffect.ALLOW,
        ),
    ]

    decision = resolve_authorization(
        subject=subject,
        resource=Resource.GROUP,
        action=ResourceAction.READ,
        policies=policies,
        resource_tenant_id="t-1",
        row_values={"group_id": "g-extended"},
    )

    assert decision.is_allowed is True
