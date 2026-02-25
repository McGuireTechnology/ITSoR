from pydantic import BaseModel

from itsor.api.schemas.base_schemas import WorkspaceBaseSchema


class WorkspaceCreate(WorkspaceBaseSchema):
    pass


class WorkspaceUpdate(BaseModel):
    name: str | None = None


class WorkspaceReplace(WorkspaceBaseSchema):
    pass


class WorkspaceResponse(WorkspaceBaseSchema):
    id: str

    model_config = {"from_attributes": True}
