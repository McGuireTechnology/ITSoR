from pydantic import BaseModel


class PlatformGroupMembershipCreate(BaseModel):
    group_id: str
    member_type: str
    member_user_id: str | None = None
    member_group_id: str | None = None


class PlatformGroupMembershipUpdate(BaseModel):
    member_type: str | None = None
    member_user_id: str | None = None
    member_group_id: str | None = None


class PlatformGroupMembershipResponse(BaseModel):
    id: str
    group_id: str
    member_type: str
    member_user_id: str | None = None
    member_group_id: str | None = None

    model_config = {"from_attributes": True}
