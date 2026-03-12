from typing import Any, Literal

from pydantic import BaseModel, Field

PermissionEffectLiteral = Literal["allow", "deny"]
AclScopeLiteral = Literal["resource", "row", "owner", "group"]
AclPrincipalTypeLiteral = Literal[
    "user",
    "group",
    "role",
    "tenant",
    "authenticated",
    "public",
]
ResourceActionLiteral = Literal["create", "read", "update", "delete", "execute"]


class AclPolicyCreate(BaseModel):
    name: str
    resource: str
    action: ResourceActionLiteral
    scope: AclScopeLiteral
    principal_type: AclPrincipalTypeLiteral
    principal_id: str | None = None
    effect: PermissionEffectLiteral = "allow"
    resource_id: str | None = None
    predicates: list[dict[str, Any]] = Field(default_factory=list)
    owner_field: str = "owner_id"
    owner_user_id: str | None = None
    group_field: str = "group_id"
    allowed_group_ids: list[str] = Field(default_factory=list)


class AclPolicyReplace(AclPolicyCreate):
    pass


class AclPolicyUpdate(BaseModel):
    name: str | None = None
    resource: str | None = None
    action: ResourceActionLiteral | None = None
    scope: AclScopeLiteral | None = None
    principal_type: AclPrincipalTypeLiteral | None = None
    principal_id: str | None = None
    effect: PermissionEffectLiteral | None = None
    resource_id: str | None = None
    predicates: list[dict[str, Any]] | None = None
    owner_field: str | None = None
    owner_user_id: str | None = None
    group_field: str | None = None
    allowed_group_ids: list[str] | None = None


class AclPolicyResponse(BaseModel):
    id: str
    name: str
    resource: str
    action: ResourceActionLiteral
    scope: AclScopeLiteral
    principal_type: AclPrincipalTypeLiteral
    principal_id: str | None = None
    effect: PermissionEffectLiteral = "allow"
    resource_id: str | None = None
    predicates: list[dict[str, Any]] = Field(default_factory=list)
    owner_field: str = "owner_id"
    owner_user_id: str | None = None
    group_field: str = "group_id"
    allowed_group_ids: list[str] = Field(default_factory=list)

    model_config = {"from_attributes": True}
