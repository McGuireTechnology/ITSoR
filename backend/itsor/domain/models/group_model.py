from dataclasses import dataclass
from dataclasses import field

from itsor.domain.models.base_model import BaseModel


@dataclass
class Group(BaseModel):
    tenant_id: str | None = None
    platform_endpoint_permissions: dict[str, list[str]] = field(default_factory=dict)
