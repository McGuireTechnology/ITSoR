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

    model_config = {"from_attributes": True}
