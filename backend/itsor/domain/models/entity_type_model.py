from dataclasses import dataclass, field
from typing import Any

from itsor.domain.models.base_model import BaseModel


@dataclass
class EntityType(BaseModel):
    namespace_id: str = ""
    attributes_json: dict[str, Any] = field(default_factory=dict)
