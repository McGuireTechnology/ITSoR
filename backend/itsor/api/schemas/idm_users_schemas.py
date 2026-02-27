from pydantic import BaseModel


class IdmUserCreate(BaseModel):
    person_id: str
    username: str
    account_status: str = "active"


class IdmUserUpdate(BaseModel):
    username: str | None = None
    account_status: str | None = None


class IdmUserResponse(BaseModel):
    id: str
    person_id: str
    username: str
    account_status: str

    model_config = {"from_attributes": True}
