from dataclasses import dataclass, field
from typing import Any

from itsor.domain.models.base_model import BaseModel


@dataclass
class EntityRecord(BaseModel):
    entity_type_id: str = ""
    values_json: dict[str, Any] = field(default_factory=dict)
