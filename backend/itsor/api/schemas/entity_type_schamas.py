from pydantic import BaseModel


class EntityTypeBaseSchema(BaseModel):
    namespace_id: str
    name: str
    attributes_json: dict[str, object] = {}


class EntityTypeCreate(EntityTypeBaseSchema):
    pass


class EntityTypeUpdate(BaseModel):
    name: str | None = None
    attributes_json: dict[str, object] | None = None


class EntityTypeReplace(EntityTypeBaseSchema):
    pass


class EntityTypeResponse(EntityTypeBaseSchema):
    id: str
    owner_id: str | None = None
    group_id: str | None = None
    permissions: int

    model_config = {"from_attributes": True}
