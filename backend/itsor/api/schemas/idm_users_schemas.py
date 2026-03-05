from pydantic import BaseModel


class IdmAccountCreate(BaseModel):
    person_id: str
    username: str
    account_status: str = "active"


class IdmAccountUpdate(BaseModel):
    username: str | None = None
    account_status: str | None = None


class IdmAccountResponse(BaseModel):
    id: str
    person_id: str
    username: str
    account_status: str

    model_config = {"from_attributes": True}


IdmUserCreate = IdmAccountCreate
IdmUserUpdate = IdmAccountUpdate
IdmUserResponse = IdmAccountResponse
