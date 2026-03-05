from pydantic import BaseModel


class GroupMembershipCreate(BaseModel):
    group_id: str
    member_type: str
    member_user_id: str | None = None
    member_group_id: str | None = None


class GroupMembershipReplace(GroupMembershipCreate):
    pass


class GroupMembershipUpdate(BaseModel):
    member_type: str | None = None
    member_user_id: str | None = None
    member_group_id: str | None = None


class GroupMembershipResponse(BaseModel):
    id: str
    group_id: str
    member_type: str
    member_user_id: str | None = None
    member_group_id: str | None = None

    model_config = {"from_attributes": True}
