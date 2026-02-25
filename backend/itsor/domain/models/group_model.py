from dataclasses import dataclass

from itsor.domain.models.base_model import BaseModel


@dataclass
class Group(BaseModel):
    tenant_id: str | None = None
