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
    owner_id: str | None = None
    group_id: str | None = None
    permissions: int

    model_config = {"from_attributes": True}
