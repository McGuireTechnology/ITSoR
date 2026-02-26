from pydantic import BaseModel

from itsor.api.schemas.base_schemas import EntityRecordBaseSchema


class EntityRecordCreate(EntityRecordBaseSchema):
    pass


class EntityRecordUpdate(BaseModel):
    name: str | None = None
    values_json: dict[str, object] | None = None


class EntityRecordReplace(EntityRecordBaseSchema):
    pass


class EntityRecordResponse(EntityRecordBaseSchema):
    id: str
    owner_id: str | None = None
    group_id: str | None = None
    permissions: int

    model_config = {"from_attributes": True}
