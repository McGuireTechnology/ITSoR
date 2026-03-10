from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TypeAlias

from itsor.domain._ulid import typed_ulid_factory
from itsor.domain.ids import GroupId, PermissionId, UserId
from itsor.domain.models.resource_models import Resource, ResourcePermissionAction

AclScalar: TypeAlias = str | int | float | bool | None
AclValue: TypeAlias = AclScalar | list[AclScalar]


class PermissionEffect(str, Enum):
	ALLOW = "allow"
	DENY = "deny"


class AclScope(str, Enum):
	RESOURCE = "resource"
	ROW = "row"
	OWNER = "owner"
	GROUP = "group"


class AclPrincipalType(str, Enum):
	USER = "user"
	GROUP = "group"
	ROLE = "role"
	TENANT = "tenant"
	AUTHENTICATED = "authenticated"
	PUBLIC = "public"


@dataclass(frozen=True)
class AclPrincipal:
	principal_type: AclPrincipalType
	principal_id: str | None = None

	def __post_init__(self) -> None:
		is_implicit_principal = self.principal_type in {
			AclPrincipalType.AUTHENTICATED,
			AclPrincipalType.PUBLIC,
		}
		if is_implicit_principal and self.principal_id is not None:
			raise ValueError("Implicit principals cannot include principal_id")
		if not is_implicit_principal and not self.principal_id:
			raise ValueError("Explicit principals require principal_id")


@dataclass(frozen=True)
class AclRowPredicate:
	field: str
	value: AclValue

	def __post_init__(self) -> None:
		if not self.field.strip():
			raise ValueError("Row predicate field cannot be empty")


@dataclass
class Permission:
	id: PermissionId = field(default_factory=typed_ulid_factory(PermissionId), init=False)
	name: str
	resource: Resource
	action: ResourcePermissionAction
	effect: PermissionEffect = PermissionEffect.ALLOW


@dataclass
class BaseAclPolicy:
	id: PermissionId = field(default_factory=typed_ulid_factory(PermissionId), init=False)
	name: str
	resource: Resource
	action: ResourcePermissionAction
	principal: AclPrincipal
	effect: PermissionEffect = PermissionEffect.ALLOW

	def _validate_common(self) -> None:
		if not self.name.strip():
			raise ValueError("ACL policy name cannot be empty")


@dataclass
class ResourceAclPolicy(BaseAclPolicy):
	scope: AclScope = field(default=AclScope.RESOURCE, init=False)

	def __post_init__(self) -> None:
		self._validate_common()


@dataclass
class RowAclPolicy(BaseAclPolicy):
	scope: AclScope = field(default=AclScope.ROW, init=False)
	resource_id: str | None = None
	predicates: list[AclRowPredicate] = field(default_factory=list)

	def __post_init__(self) -> None:
		self._validate_common()
		if self.resource_id is None and not self.predicates:
			raise ValueError("Row ACL requires resource_id or at least one predicate")


@dataclass
class OwnerAclPolicy(BaseAclPolicy):
	scope: AclScope = field(default=AclScope.OWNER, init=False)
	owner_field: str = "owner_id"
	owner_user_id: UserId | None = None

	def __post_init__(self) -> None:
		self._validate_common()
		if not self.owner_field.strip():
			raise ValueError("Owner ACL requires a non-empty owner_field")


@dataclass
class GroupAclPolicy(BaseAclPolicy):
	scope: AclScope = field(default=AclScope.GROUP, init=False)
	group_field: str = "group_id"
	allowed_group_ids: list[GroupId] = field(default_factory=list)

	def __post_init__(self) -> None:
		self._validate_common()
		if not self.group_field.strip():
			raise ValueError("Group ACL requires a non-empty group_field")

		principal_is_group = self.principal.principal_type == AclPrincipalType.GROUP
		if not principal_is_group and not self.allowed_group_ids:
			raise ValueError(
				"Group ACL requires a group principal or allowed_group_ids"
			)


AclPolicy: TypeAlias = ResourceAclPolicy | RowAclPolicy | OwnerAclPolicy | GroupAclPolicy


__all__ = [
	"AclPolicy",
	"AclPrincipal",
	"AclPrincipalType",
	"AclRowPredicate",
	"AclScope",
	"AclValue",
	"BaseAclPolicy",
	"GroupAclPolicy",
	"OwnerAclPolicy",
	"Permission",
	"PermissionEffect",
	"ResourceAclPolicy",
	"RowAclPolicy",
]

