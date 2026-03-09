from dataclasses import dataclass, field
from typing import Any

from itsor.domain.models.base_model import BaseModel


@dataclass
class CustomNamespace(BaseModel):
    workspace_id: str = ""


@dataclass
class CustomEntityType(BaseModel):
    namespace_id: str = ""
    attributes_json: dict[str, Any] = field(default_factory=dict)


@dataclass
class CustomEntityRecord(BaseModel):
    entity_type_id: str = ""
    values_json: dict[str, Any] = field(default_factory=dict)


@dataclass
class CustomWorkspace(BaseModel):
    tenant_id: str | None = None