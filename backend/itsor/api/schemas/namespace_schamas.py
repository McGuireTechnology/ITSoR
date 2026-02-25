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

    model_config = {"from_attributes": True}
