from pydantic import BaseModel


class IdmGroupCreate(BaseModel):
    name: str
    description: str = ""


class IdmGroupUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class IdmGroupResponse(BaseModel):
    id: str
    name: str
    description: str

    model_config = {"from_attributes": True}
