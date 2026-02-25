from dataclasses import dataclass

from itsor.domain.models.base_model import BaseModel


@dataclass
class Namespace(BaseModel):
    workspace_id: str = ""
