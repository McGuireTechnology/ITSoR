from pydantic import BaseModel


class IdmPersonCreate(BaseModel):
    display_name: str = ""
    current_identity_id: str | None = None


class IdmPersonUpdate(BaseModel):
    display_name: str | None = None
    current_identity_id: str | None = None


class IdmPersonResponse(BaseModel):
    id: str
    display_name: str
    current_identity_id: str | None = None

    model_config = {"from_attributes": True}
