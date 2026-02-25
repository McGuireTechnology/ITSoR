from typing import Any

from pydantic import BaseModel, EmailStr, Field


class NameSchema(BaseModel):
    name: str


class TenantScopedNameSchema(NameSchema):
    tenant_id: str | None = None


class WorkspaceBaseSchema(NameSchema):
    tenant_id: str | None = None


class NamespaceBaseSchema(NameSchema):
    workspace_id: str


class UserIdentitySchema(BaseModel):
    username: str
    email: EmailStr


class EntityTypeBaseSchema(BaseModel):
    namespace_id: str
    name: str
    attributes_json: dict[str, Any] = Field(default_factory=dict)


class EntityRecordBaseSchema(BaseModel):
    entity_type_id: str
    name: str = ""
    values_json: dict[str, Any] = Field(default_factory=dict)
