from pydantic import BaseModel


class NamespaceBaseSchema(BaseModel):
    workspace_id: str
    name: str


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
