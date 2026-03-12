from typing import Literal

from pydantic import BaseModel


ModuleRoleLiteral = Literal["owner", "editor", "user", "read_only"]


class ModuleUserCreate(BaseModel):
    module_id: str
    user_id: str
    role: ModuleRoleLiteral


class ModuleUserReplace(ModuleUserCreate):
    pass


class ModuleUserUpdate(BaseModel):
    module_id: str | None = None
    user_id: str | None = None
    role: ModuleRoleLiteral | None = None


class ModuleUserResponse(BaseModel):
    id: str
    module_id: str
    user_id: str
    role: ModuleRoleLiteral

    model_config = {"from_attributes": True}
