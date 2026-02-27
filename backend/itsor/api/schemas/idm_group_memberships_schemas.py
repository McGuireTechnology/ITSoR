from pydantic import BaseModel


class IdmGroupMembershipCreate(BaseModel):
    group_id: str
    member_type: str
    member_user_id: str | None = None
    member_group_id: str | None = None


class IdmGroupMembershipUpdate(BaseModel):
    member_type: str | None = None
    member_user_id: str | None = None
    member_group_id: str | None = None


class IdmGroupMembershipResponse(BaseModel):
    id: str
    group_id: str
    member_type: str
    member_user_id: str | None = None
    member_group_id: str | None = None

    model_config = {"from_attributes": True}
