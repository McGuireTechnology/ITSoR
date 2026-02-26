from pydantic import BaseModel

from itsor.api.schemas.base_schemas import NamespaceBaseSchema


class NamespaceCreate(NamespaceBaseSchema):
    pass


class NamespaceUpdate(BaseModel):
    name: str | None = None


class NamespaceReplace(NamespaceBaseSchema):
    pass


class NamespaceResponse(NamespaceBaseSchema):
    id: str
    owner_id: str | None = None
    group_id: str | None = None
    permissions: int

    model_config = {"from_attributes": True}
