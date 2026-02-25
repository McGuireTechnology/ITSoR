from dataclasses import dataclass

from itsor.domain.models.base_model import BaseModel


@dataclass
class Workspace(BaseModel):
    tenant_id: str | None = None
