from typing import Literal

from pydantic import BaseModel


PermissionEffectLiteral = Literal["allow", "deny"]
ResourceActionLiteral = Literal["create", "read", "update", "delete", "execute"]


class PermissionCreate(BaseModel):
    name: str
    resource: str
    action: ResourceActionLiteral
    effect: PermissionEffectLiteral = "allow"


class PermissionReplace(PermissionCreate):
    pass


class PermissionUpdate(BaseModel):
    name: str | None = None
    resource: str | None = None
    action: ResourceActionLiteral | None = None
    effect: PermissionEffectLiteral | None = None


class PermissionResponse(BaseModel):
    id: str
    name: str
    resource: str
    action: ResourceActionLiteral
    effect: PermissionEffectLiteral = "allow"

    model_config = {"from_attributes": True}
